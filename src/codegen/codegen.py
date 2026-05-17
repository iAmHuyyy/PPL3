"""
Code generator for TyC.
"""

from typing import Any

from ..utils.nodes import *
from ..utils.visitor import BaseVisitor
from .emitter import *
from .frame import *
from .io import IO_SYMBOL_LIST
from .utils import *


class StringArrayType:
    """Marker type for JVM main(String[] args)."""
    pass


class StructInfo:
    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.index = {}
        self.types = {}
        for i, member in enumerate(members):
            self.index[member.name] = i
            self.types[member.name] = member.member_type


class TypeBox:
    def __init__(self, typ=None, decl_id=None):
        self.type = typ
        self.decl_id = decl_id


class CodeGenerator(BaseVisitor):
    """AST -> Jasmin code generator for TyC."""

    def __init__(self):
        self.emit = None
        self.functions = {}
        self.structs = {}
        self.current_return_type = VoidType()
        self.class_name = "TyC"
        self.var_decl_types = {}
        self.break_labels = []
        self.continue_labels = []

    # ------------------------------------------------------------------
    # Type helpers
    # ------------------------------------------------------------------
    def _copy_type(self, typ):
        if typ is None:
            return None
        if is_int_type(typ):
            return IntType()
        if is_float_type(typ):
            return FloatType()
        if is_string_type(typ):
            return StringType()
        if is_void_type(typ):
            return VoidType()
        if is_struct_type(typ):
            return typ
        return typ

    def _same_type(self, left, right):
        if left is None or right is None:
            return False
        if type(left) is not type(right):
            return False
        if is_struct_type(left):
            return getattr(left, "struct_name", None) == getattr(right, "struct_name", None)
        return True

    def _lookup_symbol(self, name: str, sym_list: list[Symbol]) -> Symbol:
        for sym in reversed(sym_list):
            if sym.name == name:
                return sym
        raise RuntimeError(f"Undeclared symbol: {name}")

    def _make_access(self, frame, sym, expected=None):
        access = Access(frame, sym)
        access.expected_type = expected
        return access

    def _access_expected(self, access):
        if access is None:
            return None
        return getattr(access, "expected_type", None)

    def _default_type_for_unknown(self):
        return IntType()

    # ------------------------------------------------------------------
    # Prepass: enough type inference for direct AST codegen tests
    # ------------------------------------------------------------------
    def _prepass_lookup_box(self, name, scopes):
        for scope in reversed(scopes):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Undeclared symbol during codegen prepass: {name}")

    def _prepass_set_box_type(self, box, typ):
        if box is not None and box.type is None and typ is not None:
            box.type = self._copy_type(typ)
            if box.decl_id is not None:
                self.var_decl_types[box.decl_id] = box.type

    def _prepass_set_expr_type(self, expr, scopes, typ):
        if typ is None:
            return
        if isinstance(expr, Identifier):
            box = self._prepass_lookup_box(expr.name, scopes)
            self._prepass_set_box_type(box, typ)

    def _prepass_expr(self, node, scopes, expected=None):
        if node is None:
            return None
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            box = self._prepass_lookup_box(node.name, scopes)
            if box.type is None and expected is not None:
                self._prepass_set_box_type(box, expected)
            return box.type
        if isinstance(node, StructLiteral):
            if expected is not None and is_struct_type(expected):
                info = self.structs[expected.struct_name]
                for value, member in zip(node.values, info.members):
                    self._prepass_expr(value, scopes, member.member_type)
                return expected
            for value in node.values:
                self._prepass_expr(value, scopes)
            return expected
        if isinstance(node, FuncCall):
            fn_type = self.functions[node.name].type
            for arg, param_type in zip(node.args, fn_type.param_types):
                self._prepass_expr(arg, scopes, param_type)
            return fn_type.return_type
        if isinstance(node, MemberAccess):
            obj_type = self._prepass_expr(node.obj, scopes)
            if obj_type is None:
                return None
            info = self.structs[obj_type.struct_name]
            return info.types[node.member]
        if isinstance(node, AssignExpr):
            lhs_type = self._prepass_expr(node.lhs, scopes)
            rhs_type = self._prepass_expr(node.rhs, scopes, lhs_type)
            if lhs_type is None and rhs_type is not None:
                self._prepass_set_expr_type(node.lhs, scopes, rhs_type)
                lhs_type = rhs_type
            if rhs_type is None and lhs_type is not None:
                rhs_type = self._prepass_expr(node.rhs, scopes, lhs_type)
            return lhs_type if lhs_type is not None else rhs_type
        if isinstance(node, BinaryOp):
            op = node.operator
            if op in ("&&", "||", "%"):
                self._prepass_expr(node.left, scopes, IntType())
                self._prepass_expr(node.right, scopes, IntType())
                return IntType()
            if op in ("+", "-", "*", "/"):
                lt = self._prepass_expr(node.left, scopes)
                rt = self._prepass_expr(node.right, scopes)
                if lt is None and isinstance(node.right, IntLiteral):
                    lt = self._prepass_expr(node.left, scopes, IntType())
                if rt is None and isinstance(node.left, IntLiteral):
                    rt = self._prepass_expr(node.right, scopes, IntType())
                if lt is None and rt is not None and is_float_type(rt):
                    lt = self._prepass_expr(node.left, scopes, FloatType())
                if rt is None and lt is not None and is_float_type(lt):
                    rt = self._prepass_expr(node.right, scopes, FloatType())
                if is_float_type(lt) or is_float_type(rt):
                    return FloatType()
                if lt is not None and rt is not None:
                    return IntType()
                return expected
            if op in ("<", "<=", ">", ">=", "==", "!="):
                self._prepass_expr(node.left, scopes)
                self._prepass_expr(node.right, scopes)
                return IntType()
        if isinstance(node, PrefixOp):
            if node.operator in ("++", "--", "!"):
                self._prepass_expr(node.operand, scopes, IntType())
                return IntType()
            return self._prepass_expr(node.operand, scopes, expected)
        if isinstance(node, PostfixOp):
            self._prepass_expr(node.operand, scopes, IntType())
            return IntType()
        return expected

    def _prepass_stmt(self, node, scopes, returns):
        if isinstance(node, BlockStmt):
            scopes.append({})
            for stmt in node.statements:
                self._prepass_stmt(stmt, scopes, returns)
            scopes.pop()
            return
        if isinstance(node, VarDecl):
            typ = self._copy_type(node.var_type)
            if node.init_value is not None:
                init_type = self._prepass_expr(node.init_value, scopes, typ)
                if typ is None:
                    typ = self._copy_type(init_type)
            box = TypeBox(typ, id(node))
            scopes[-1][node.name] = box
            self.var_decl_types[id(node)] = typ
            return
        if isinstance(node, ExprStmt):
            self._prepass_expr(node.expr, scopes)
            return
        if isinstance(node, IfStmt):
            self._prepass_expr(node.condition, scopes, IntType())
            self._prepass_stmt(node.then_stmt, [dict(scope) for scope in scopes], returns)
            if node.else_stmt is not None:
                self._prepass_stmt(node.else_stmt, [dict(scope) for scope in scopes], returns)
            return
        if isinstance(node, WhileStmt):
            self._prepass_expr(node.condition, scopes, IntType())
            self._prepass_stmt(node.body, [dict(scope) for scope in scopes], returns)
            return
        if isinstance(node, ForStmt):
            if node.init is not None:
                self._prepass_stmt(node.init, scopes, returns)
            if node.condition is not None:
                self._prepass_expr(node.condition, scopes, IntType())
            if node.update is not None:
                self._prepass_expr(node.update, scopes)
            self._prepass_stmt(node.body, [dict(scope) for scope in scopes], returns)
            return
        if isinstance(node, SwitchStmt):
            self._prepass_expr(node.expr, scopes, IntType())
            for case in node.cases:
                self._prepass_expr(case.expr, scopes, IntType())
                for stmt in case.statements:
                    self._prepass_stmt(stmt, scopes, returns)
            if node.default_case is not None:
                for stmt in node.default_case.statements:
                    self._prepass_stmt(stmt, scopes, returns)
            return
        if isinstance(node, ReturnStmt):
            if node.expr is not None:
                ret_type = self._prepass_expr(node.expr, scopes)
                if ret_type is not None:
                    returns.append(ret_type)
            return

    def _prepass_function(self, node):
        scopes = [{}]
        for param in node.params:
            scopes[0][param.name] = TypeBox(param.param_type, None)
        returns = []
        for stmt in node.body.statements:
            self._prepass_stmt(stmt, scopes, returns)
        if node.return_type is not None:
            return node.return_type
        return returns[0] if returns else VoidType()

    # ------------------------------------------------------------------
    # Type inference during emission
    # ------------------------------------------------------------------
    def _infer_type(self, node, o):
        expected = self._access_expected(o)
        if isinstance(node, IntLiteral):
            return IntType()
        if isinstance(node, FloatLiteral):
            return FloatType()
        if isinstance(node, StringLiteral):
            return StringType()
        if isinstance(node, Identifier):
            sym = self._lookup_symbol(node.name, o.sym)
            if sym.type is None and expected is not None:
                sym.type = expected
            return sym.type
        if isinstance(node, StructLiteral):
            return expected
        if isinstance(node, FuncCall):
            return self.functions[node.name].type.return_type
        if isinstance(node, AssignExpr):
            return self._infer_type(node.lhs, o)
        if isinstance(node, MemberAccess):
            obj_type = self._infer_type(node.obj, o)
            info = self.structs[obj_type.struct_name]
            return info.types[node.member]
        if isinstance(node, BinaryOp):
            if node.operator in ("+", "-", "*", "/"):
                lt = self._infer_type(node.left, o)
                rt = self._infer_type(node.right, o)
                return FloatType() if is_float_type(lt) or is_float_type(rt) else IntType()
            return IntType()
        if isinstance(node, PrefixOp):
            if node.operator in ("++", "--", "!"):
                return IntType()
            return self._infer_type(node.operand, o)
        if isinstance(node, PostfixOp):
            return IntType()
        return expected or IntType()

    # ------------------------------------------------------------------
    # Raw JVM helpers not wrapped by emitter.py
    # ------------------------------------------------------------------
    def _raw(self, text):
        return "\t" + text + "\n"

    def _emit_anew_object_array(self, size, frame):
        code = self.emit.emit_push_iconst(size, frame)
        code += self.emit.jvm.emitANEWARRAY("java/lang/Object")
        return code

    def _emit_aaload(self, frame):
        frame.pop()
        return self.emit.jvm.emitAALOAD()

    def _emit_aastore(self, frame):
        frame.pop()
        frame.pop()
        frame.pop()
        return self.emit.jvm.emitAASTORE()

    def _emit_checkcast(self, target):
        return self._raw("checkcast " + target)

    def _emit_box(self, typ, frame):
        if is_int_type(typ):
            return self._raw("invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;")
        if is_float_type(typ):
            return self._raw("invokestatic java/lang/Float/valueOf(F)Ljava/lang/Float;")
        return ""

    def _emit_unbox_or_cast(self, typ, frame):
        if is_int_type(typ):
            return self._emit_checkcast("java/lang/Integer") + self._raw("invokevirtual java/lang/Integer/intValue()I")
        if is_float_type(typ):
            return self._emit_checkcast("java/lang/Float") + self._raw("invokevirtual java/lang/Float/floatValue()F")
        if is_string_type(typ):
            return self._emit_checkcast("java/lang/String")
        if is_struct_type(typ):
            return self._emit_checkcast("[Ljava/lang/Object;")
        return ""

    def _emit_i2f_if_needed(self, actual, expected, frame):
        if actual is not None and expected is not None and is_int_type(actual) and is_float_type(expected):
            return self.emit.emit_i2f(frame)
        return ""

    def _emit_load_temp(self, index, typ, frame):
        return self.emit.emit_read_var("$tmp", typ, index, frame)

    def _emit_store_temp(self, index, typ, frame):
        return self.emit.emit_write_var("$tmp", typ, index, frame)

    # ------------------------------------------------------------------
    # Program / declarations
    # ------------------------------------------------------------------
    def visit_program(self, node: Program, o: Any = None):
        self.emit = Emitter(f"{self.class_name}.j")
        self.emit.print_out(self.emit.emit_prolog(self.class_name))

        for decl in node.decls:
            if isinstance(decl, StructDecl):
                self.structs[decl.name] = StructInfo(decl.name, decl.members)

        for io_sym in IO_SYMBOL_LIST:
            self.functions[io_sym.name] = io_sym

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = decl.return_type if decl.return_type else VoidType()
                param_types = [p.param_type for p in decl.params]
                self.functions[decl.name] = Symbol(
                    decl.name, FunctionType(param_types, return_type), CName(self.class_name)
                )

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                return_type = self._prepass_function(decl)
                self.functions[decl.name].type.return_type = return_type

        for decl in node.decls:
            if isinstance(decl, FuncDecl):
                self.visit(decl, None)

        self.emit.emit_epilog()

    def visit_func_decl(self, node: FuncDecl, o: Any = None):
        self.current_return_type = self.functions[node.name].type.return_type
        frame = Frame(node.name, self.current_return_type)
        frame.enter_scope(True)

        if node.name == "main":
            mtype = FunctionType([StringArrayType()], VoidType())
        else:
            mtype = FunctionType([p.param_type for p in node.params], self.current_return_type)

        self.emit.print_out(self.emit.emit_method(node.name, mtype, True))

        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))

        local_syms = []
        if node.name == "main":
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(args_idx, "args", StringArrayType(), start_label, end_label)
            )

        for param in node.params:
            idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx, param.name, param.param_type, start_label, end_label)
            )
            local_syms.append(Symbol(param.name, param.param_type, Index(idx)))

        sub_body = SubBody(frame, local_syms)
        sub_body.is_func_body = True
        self.visit(node.body, sub_body)

        self.emit.print_out(self._emit_default_value(self.current_return_type, frame))
        self.emit.print_out(self.emit.emit_return(self.current_return_type, frame))

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        self.emit.print_out(self.emit.emit_end_method(frame))

    def visit_struct_decl(self, node: StructDecl, o: Any = None):
        return None

    def visit_member_decl(self, node: MemberDecl, o: Any = None):
        return None

    def visit_param(self, node: Param, o: Any = None):
        return None

    # ------------------------------------------------------------------
    # Statements
    # ------------------------------------------------------------------
    def visit_block_stmt(self, node: BlockStmt, o: SubBody = None):
        frame = o.frame
        if getattr(o, "is_func_body", False):
            o.is_func_body = False
            for stmt in node.statements:
                self.visit(stmt, o)
            return o

        frame.enter_scope(False)
        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        inner = SubBody(frame, list(o.sym))
        for stmt in node.statements:
            self.visit(stmt, inner)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        return o


    def _visit_child_statement(self, stmt, o):
        if isinstance(stmt, BlockStmt):
            return self.visit(stmt, o)
        frame = o.frame
        frame.enter_scope(False)
        start_label = frame.get_start_label()
        end_label = frame.get_end_label()
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        inner = SubBody(frame, list(o.sym))
        self.visit(stmt, inner)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        frame.exit_scope()
        return o

    def _emit_default_value(self, typ, frame):
        if is_void_type(typ):
            return ""
        if is_int_type(typ):
            return self.emit.emit_push_iconst(0, frame)
        if is_float_type(typ):
            return self.emit.emit_push_fconst("0.0", frame)
        if is_string_type(typ):
            return self.emit.emit_push_const("", StringType(), frame)
        if is_struct_type(typ):
            return self._emit_default_struct(typ, frame)
        return ""

    def _emit_default_struct(self, typ, frame):
        info = self.structs[typ.struct_name]
        code = self._emit_anew_object_array(len(info.members), frame)
        for idx, member in enumerate(info.members):
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_push_iconst(idx, frame)
            code += self._emit_default_value(member.member_type, frame)
            code += self._emit_box(member.member_type, frame)
            code += self._emit_aastore(frame)
        return code

    def _emit_copy_struct(self, typ, frame):
        info = self.structs[typ.struct_name]
        src_idx = frame.get_new_index()
        code = self._emit_store_temp(src_idx, typ, frame)
        code += self._emit_anew_object_array(len(info.members), frame)
        for idx, member in enumerate(info.members):
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_push_iconst(idx, frame)
            code += self._emit_load_temp(src_idx, typ, frame)
            code += self.emit.emit_push_iconst(idx, frame)
            code += self._emit_aaload(frame)
            if is_struct_type(member.member_type):
                code += self._emit_unbox_or_cast(member.member_type, frame)
                code += self._emit_copy_struct(member.member_type, frame)
            code += self._emit_aastore(frame)
        return code

    def visit_var_decl(self, node: VarDecl, o: SubBody = None):
        frame = o.frame
        idx = frame.get_new_index()
        var_type = self.var_decl_types.get(id(node)) or node.var_type
        if var_type is None:
            if node.init_value is not None:
                var_type = self._infer_type(node.init_value, self._make_access(frame, o.sym))
            else:
                var_type = self._default_type_for_unknown()

        self.emit.print_out(
            self.emit.emit_var(idx, node.name, var_type, frame.get_start_label(), frame.get_end_label())
        )

        if node.init_value is not None:
            rhs_code, rhs_type = self.visit(node.init_value, self._make_access(frame, o.sym, var_type))
            self.emit.print_out(rhs_code)
            self.emit.print_out(self._emit_i2f_if_needed(rhs_type, var_type, frame))
            if is_struct_type(var_type):
                self.emit.print_out(self._emit_copy_struct(var_type, frame))
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))
        else:
            self.emit.print_out(self._emit_default_value(var_type, frame))
            self.emit.print_out(self.emit.emit_write_var(node.name, var_type, idx, frame))

        o.sym.append(Symbol(node.name, var_type, Index(idx)))
        return o

    def visit_expr_stmt(self, node: ExprStmt, o: SubBody = None):
        code, expr_type = self.visit(node.expr, self._make_access(o.frame, o.sym))
        self.emit.print_out(code)
        if not is_void_type(expr_type):
            self.emit.print_out(self.emit.emit_pop(o.frame))
        return o

    def visit_if_stmt(self, node: IfStmt, o: SubBody = None):
        frame = o.frame
        else_label = frame.get_new_label()
        end_label = frame.get_new_label()
        cond_code, _ = self.visit(node.condition, self._make_access(frame, o.sym, IntType()))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        self._visit_child_statement(node.then_stmt, o)
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        if node.else_stmt is not None:
            self._visit_child_statement(node.else_stmt, o)
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_while_stmt(self, node: WhileStmt, o: SubBody = None):
        frame = o.frame
        start_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.continue_labels.append(start_label)
        self.break_labels.append(end_label)
        self.emit.print_out(self.emit.emit_label(start_label, frame))
        cond_code, _ = self.visit(node.condition, self._make_access(frame, o.sym, IntType()))
        self.emit.print_out(cond_code)
        self.emit.print_out(self.emit.emit_if_false(end_label, frame))
        self._visit_child_statement(node.body, o)
        self.emit.print_out(self.emit.emit_goto(start_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))
        self.break_labels.pop()
        self.continue_labels.pop()
        return o

    def visit_for_stmt(self, node: ForStmt, o: SubBody = None):
        frame = o.frame
        if node.init is not None:
            self.visit(node.init, o)

        cond_label = frame.get_new_label()
        update_label = frame.get_new_label()
        end_label = frame.get_new_label()
        self.continue_labels.append(update_label)
        self.break_labels.append(end_label)

        self.emit.print_out(self.emit.emit_label(cond_label, frame))
        if node.condition is not None:
            cond_code, _ = self.visit(node.condition, self._make_access(frame, o.sym, IntType()))
            self.emit.print_out(cond_code)
            self.emit.print_out(self.emit.emit_if_false(end_label, frame))

        self._visit_child_statement(node.body, o)
        self.emit.print_out(self.emit.emit_label(update_label, frame))
        if node.update is not None:
            update_code, update_type = self.visit(node.update, self._make_access(frame, o.sym))
            self.emit.print_out(update_code)
            if not is_void_type(update_type):
                self.emit.print_out(self.emit.emit_pop(frame))
        self.emit.print_out(self.emit.emit_goto(cond_label, frame))
        self.emit.print_out(self.emit.emit_label(end_label, frame))

        self.break_labels.pop()
        self.continue_labels.pop()
        return o

    def visit_switch_stmt(self, node: SwitchStmt, o: SubBody = None):
        frame = o.frame
        end_label = frame.get_new_label()
        default_label = frame.get_new_label() if node.default_case is not None else end_label
        case_labels = [frame.get_new_label() for _ in node.cases]

        switch_code, _ = self.visit(node.expr, self._make_access(frame, o.sym, IntType()))
        temp_idx = frame.get_new_index()
        self.emit.print_out(switch_code)
        self.emit.print_out(self._emit_store_temp(temp_idx, IntType(), frame))

        for case, label in zip(node.cases, case_labels):
            self.emit.print_out(self._emit_load_temp(temp_idx, IntType(), frame))
            case_code, _ = self.visit(case.expr, self._make_access(frame, o.sym, IntType()))
            self.emit.print_out(case_code)
            frame.pop()
            frame.pop()
            self.emit.print_out(self.emit.jvm.emitIFICMPEQ(label))
        self.emit.print_out(self.emit.emit_goto(default_label, frame))

        self.break_labels.append(end_label)
        for case, label in zip(node.cases, case_labels):
            self.emit.print_out(self.emit.emit_label(label, frame))
            self.visit(case, o)
        if node.default_case is not None:
            self.emit.print_out(self.emit.emit_label(default_label, frame))
            self.visit(node.default_case, o)
        self.break_labels.pop()

        self.emit.print_out(self.emit.emit_label(end_label, frame))
        return o

    def visit_case_stmt(self, node: CaseStmt, o: SubBody = None):
        inner = SubBody(o.frame, list(o.sym))
        for stmt in node.statements:
            self.visit(stmt, inner)
        return o

    def visit_default_stmt(self, node: DefaultStmt, o: SubBody = None):
        inner = SubBody(o.frame, list(o.sym))
        for stmt in node.statements:
            self.visit(stmt, inner)
        return o

    def visit_break_stmt(self, node: BreakStmt, o: SubBody = None):
        if not self.break_labels:
            raise RuntimeError("break outside loop/switch during codegen")
        self.emit.print_out(self.emit.emit_goto(self.break_labels[-1], o.frame))
        return o

    def visit_continue_stmt(self, node: ContinueStmt, o: SubBody = None):
        if not self.continue_labels:
            raise RuntimeError("continue outside loop during codegen")
        self.emit.print_out(self.emit.emit_goto(self.continue_labels[-1], o.frame))
        return o

    def visit_return_stmt(self, node: ReturnStmt, o: SubBody = None):
        if node.expr is None:
            self.emit.print_out(self.emit.emit_return(VoidType(), o.frame))
            return o
        code, ret_type = self.visit(node.expr, self._make_access(o.frame, o.sym, self.current_return_type))
        self.emit.print_out(code)
        self.emit.print_out(self._emit_i2f_if_needed(ret_type, self.current_return_type, o.frame))
        if is_struct_type(self.current_return_type):
            self.emit.print_out(self._emit_copy_struct(self.current_return_type, o.frame))
        self.emit.print_out(self.emit.emit_return(self.current_return_type, o.frame))
        return o

    # ------------------------------------------------------------------
    # Expressions
    # ------------------------------------------------------------------
    def visit_binary_op(self, node: BinaryOp, o: Access = None):
        frame = o.frame
        op = node.operator

        if op in ("&&", "||"):
            return self._emit_logical_op(node, o), IntType()

        left_code, left_type = self.visit(node.left, o)
        right_code, right_type = self.visit(node.right, o)

        if op in ("+", "-", "*", "/"):
            result_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            code = left_code + self._emit_i2f_if_needed(left_type, result_type, frame)
            code += right_code + self._emit_i2f_if_needed(right_type, result_type, frame)
            if op in ("+", "-"):
                code += self.emit.emit_add_op(op, result_type, frame)
            else:
                code += self.emit.emit_mul_op(op, result_type, frame)
            return code, result_type

        if op == "%":
            return left_code + right_code + self.emit.emit_mod(frame), IntType()

    
        if op in ("<", "<=", ">", ">=", "==", "!="):
            op_type = FloatType() if is_float_type(left_type) or is_float_type(right_type) else IntType()
            code = left_code + self._emit_i2f_if_needed(left_type, op_type, frame)
            code += right_code + self._emit_i2f_if_needed(right_type, op_type, frame)
            code += self.emit.emit_re_op(op, op_type, frame)
            return code, IntType()

        raise RuntimeError(f"Unsupported operator: {op}")

    def _emit_logical_op(self, node: BinaryOp, o: Access):
        frame = o.frame
        true_label = frame.get_new_label()
        false_label = frame.get_new_label()
        end_label = frame.get_new_label()
        code = ""
        if node.operator == "&&":
            left_code, _ = self.visit(node.left, self._make_access(frame, o.sym, IntType()))
            right_code, _ = self.visit(node.right, self._make_access(frame, o.sym, IntType()))
            code += left_code
            code += self.emit.emit_if_false(false_label, frame)
            code += right_code
            code += self.emit.emit_if_false(false_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(false_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(end_label, frame)
        else:
            left_code, _ = self.visit(node.left, self._make_access(frame, o.sym, IntType()))
            right_code, _ = self.visit(node.right, self._make_access(frame, o.sym, IntType()))
            code += left_code
            code += self.emit.emit_if_true(true_label, frame)
            code += right_code
            code += self.emit.emit_if_true(true_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(true_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(end_label, frame)
        return code

    def visit_assign_expr(self, node: AssignExpr, o: Access = None):
        frame = o.frame
        if isinstance(node.lhs, Identifier):
            lhs_sym = self._lookup_symbol(node.lhs.name, o.sym)
            lhs_type = lhs_sym.type
            if lhs_type is None:
                lhs_type = self._infer_type(node.rhs, self._make_access(frame, o.sym))
                lhs_sym.type = lhs_type
            rhs_code, rhs_type = self.visit(node.rhs, self._make_access(frame, o.sym, lhs_type))
            code = rhs_code + self._emit_i2f_if_needed(rhs_type, lhs_type, frame)
            if is_struct_type(lhs_type):
                code += self._emit_copy_struct(lhs_type, frame)
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_write_var(node.lhs.name, lhs_type, lhs_sym.value.value, frame)
            return code, lhs_type

        if isinstance(node.lhs, MemberAccess):
            lhs_type = self._infer_type(node.lhs, o)
            rhs_code, rhs_type = self.visit(node.rhs, self._make_access(frame, o.sym, lhs_type))
            temp_idx = frame.get_new_index()
            code = rhs_code + self._emit_i2f_if_needed(rhs_type, lhs_type, frame)
            if is_struct_type(lhs_type):
                code += self._emit_copy_struct(lhs_type, frame)
            code += self._emit_store_temp(temp_idx, lhs_type, frame)
            addr_code, member_type = self._emit_member_address(node.lhs, o)
            code += addr_code
            code += self._emit_load_temp(temp_idx, lhs_type, frame)
            code += self._emit_box(lhs_type, frame)
            code += self._emit_aastore(frame)
            code += self._emit_load_temp(temp_idx, lhs_type, frame)
            return code, member_type

        raise RuntimeError("Invalid assignment lhs during codegen")

    def visit_func_call(self, node: FuncCall, o: Access = None):
        frame = o.frame
        fn_sym = self.functions[node.name]
        fn_type = fn_sym.type
        code = ""
        for arg, param_type in zip(node.args, fn_type.param_types):
            arg_code, arg_type = self.visit(arg, self._make_access(frame, o.sym, param_type))
            code += arg_code + self._emit_i2f_if_needed(arg_type, param_type, frame)
            if is_struct_type(param_type):
                code += self._emit_copy_struct(param_type, frame)
        code += self.emit.emit_invoke_static(f"{fn_sym.value.value}/{node.name}", fn_type, frame)
        return code, fn_type.return_type

    def visit_identifier(self, node: Identifier, o: Access = None):
        sym = self._lookup_symbol(node.name, o.sym)
        expected = self._access_expected(o)
        if sym.type is None and expected is not None:
            sym.type = expected
        if sym.type is None:
            sym.type = self._default_type_for_unknown()
        return self.emit.emit_read_var(node.name, sym.type, sym.value.value, o.frame), sym.type

    def visit_int_literal(self, node: IntLiteral, o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: FloatLiteral, o: Access = None):
        return self.emit.emit_push_fconst(str(node.value), o.frame), FloatType()

    def visit_string_literal(self, node: StringLiteral, o: Access = None):
        return self.emit.emit_push_const(node.value, StringType(), o.frame), StringType()

    def visit_struct_literal(self, node: StructLiteral, o: Access = None):
        expected = self._access_expected(o)
        if expected is None or not is_struct_type(expected):
            raise RuntimeError("Struct literal needs an expected struct type during codegen")
        info = self.structs[expected.struct_name]
        frame = o.frame
        code = self._emit_anew_object_array(len(info.members), frame)
        for idx, (value, member) in enumerate(zip(node.values, info.members)):
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_push_iconst(idx, frame)
            value_code, value_type = self.visit(value, self._make_access(frame, o.sym, member.member_type))
            code += value_code + self._emit_i2f_if_needed(value_type, member.member_type, frame)
            code += self._emit_box(member.member_type, frame)
            code += self._emit_aastore(frame)
        return code, expected

    def visit_member_access(self, node: MemberAccess, o: Access = None):
        frame = o.frame
        addr_code, member_type = self._emit_member_address(node, o)
        code = addr_code + self._emit_aaload(frame) + self._emit_unbox_or_cast(member_type, frame)
        return code, member_type

    def _flatten_member_access(self, node):
        fields = []
        cur = node
        while isinstance(cur, MemberAccess):
            fields.append(cur.member)
            cur = cur.obj
        fields.reverse()
        return cur, fields

    def _emit_member_address(self, node, o):
        frame = o.frame
        base, fields = self._flatten_member_access(node)
        base_code, base_type = self.visit(base, self._make_access(frame, o.sym))
        code = base_code
        current_type = base_type
        for field in fields[:-1]:
            info = self.structs[current_type.struct_name]
            field_type = info.types[field]
            code += self.emit.emit_push_iconst(info.index[field], frame)
            code += self._emit_aaload(frame)
            code += self._emit_unbox_or_cast(field_type, frame)
            current_type = field_type
        info = self.structs[current_type.struct_name]
        final_field = fields[-1]
        code += self.emit.emit_push_iconst(info.index[final_field], frame)
        return code, info.types[final_field]

    def visit_prefix_op(self, node: PrefixOp, o: Access = None):
        frame = o.frame
        op = node.operator
        if op in ("+", "-"):
            code, typ = self.visit(node.operand, o)
            if op == "-":
                code += self.emit.emit_neg_op(typ, frame)
            return code, typ
        if op == "!":
            code, _ = self.visit(node.operand, self._make_access(frame, o.sym, IntType()))
            true_label = frame.get_new_label()
            end_label = frame.get_new_label()
            code += self.emit.emit_if_false(true_label, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_goto(end_label, frame)
            code += self.emit.emit_label(true_label, frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_label(end_label, frame)
            return code, IntType()
        if op in ("++", "--"):
            return self._emit_inc_dec(node.operand, op, True, o), IntType()
        raise RuntimeError(f"Unsupported prefix operator: {op}")

    def visit_postfix_op(self, node: PostfixOp, o: Access = None):
        return self._emit_inc_dec(node.operand, node.operator, False, o), IntType()

    def _emit_inc_dec(self, operand, operator, prefix, o):
        frame = o.frame
        op = "+" if operator == "++" else "-"

        if isinstance(operand, Identifier):
            sym = self._lookup_symbol(operand.name, o.sym)
            code = self.emit.emit_read_var(operand.name, IntType(), sym.value.value, frame)
            if prefix:
                code += self.emit.emit_push_iconst(1, frame)
                code += self.emit.emit_add_op(op, IntType(), frame)
                code += self.emit.emit_dup(frame)
                code += self.emit.emit_write_var(operand.name, IntType(), sym.value.value, frame)
                return code
            code += self.emit.emit_dup(frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_add_op(op, IntType(), frame)
            code += self.emit.emit_write_var(operand.name, IntType(), sym.value.value, frame)
            return code

        if isinstance(operand, MemberAccess):
            old_idx = frame.get_new_index()
            new_idx = frame.get_new_index()
            code, _ = self.visit(operand, self._make_access(frame, o.sym, IntType()))
            code += self._emit_store_temp(old_idx, IntType(), frame)
            code += self._emit_load_temp(old_idx, IntType(), frame)
            code += self.emit.emit_push_iconst(1, frame)
            code += self.emit.emit_add_op(op, IntType(), frame)
            code += self._emit_store_temp(new_idx, IntType(), frame)
            addr_code, _ = self._emit_member_address(operand, o)
            code += addr_code
            code += self._emit_load_temp(new_idx, IntType(), frame)
            code += self._emit_box(IntType(), frame)
            code += self._emit_aastore(frame)
            code += self._emit_load_temp(new_idx if prefix else old_idx, IntType(), frame)
            return code

        raise RuntimeError("++/-- operand must be identifier or member access")

    # ------------------------------------------------------------------
    # Types
    # ------------------------------------------------------------------
    def visit_int_type(self, node: IntType, o: Any = None):
        return node

    def visit_float_type(self, node: FloatType, o: Any = None):
        return node

    def visit_string_type(self, node: StringType, o: Any = None):
        return node

    def visit_void_type(self, node: VoidType, o: Any = None):
        return node

    def visit_struct_type(self, node: StructType, o: Any = None):
        return node
