"""
Static Semantic Checker for TyC Programming Language

This module implements a comprehensive static semantic checker using visitor pattern
for the TyC procedural programming language. It performs type checking,
scope management, type inference, and detects all semantic errors as
specified in the TyC language specification.
"""

from functools import reduce
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Any,
    Tuple,
    NamedTuple,
    Union,
    TYPE_CHECKING,
)
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode,
    Program,
    StructDecl,
    MemberDecl,
    FuncDecl,
    Param,
    VarDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    ReturnStmt,
    BlockStmt,
    SwitchStmt,
    CaseStmt,
    DefaultStmt,
    Type,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    BinaryOp,
    PrefixOp,
    PostfixOp,
    AssignExpr,
    MemberAccess,
    FuncCall,
    Identifier,
    StructLiteral,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    ExprStmt,
    Expr,
    Stmt,
    Decl,
)

# Type aliases for better type hints
TyCType = Union[IntType, FloatType, StringType, VoidType, StructType]
from .static_error import (
    StaticError,
    Redeclared,
    UndeclaredIdentifier,
    UndeclaredFunction,
    UndeclaredStruct,
    TypeCannotBeInferred,
    TypeMismatchInStatement,
    TypeMismatchInExpression,
    MustInLoop,
)

class VarInfo:
    def __init__(self, name, var_type, is_auto):
        self.name = name
        self.var_type = var_type
        self.is_auto = is_auto

class StructInfo:
    def __init__(self, name, members, member_order):
        self.name = name
        self.members = members
        self.member_order = member_order

class FuncInfo:
    def __init__(self, name, param_types, return_type, inferred_return):
        self.name = name
        self.param_types = param_types
        self.return_type = return_type
        self.inferred_return = inferred_return
        self.saw_bare_return = False

class StaticChecker(ASTVisitor):
    """Type checker with first-failure error reporting for TyC."""

    def __init__(self):
        self.struct_table = {}
        self.func_table = {}
        self.scope_stack = []
        self.current_params = {}
        self.current_function = None
        self.loop_depth = 0
        self.switch_depth = 0

        self.int_type = IntType()
        self.float_type = FloatType()
        self.string_type = StringType()
        self.void_type = VoidType()

        self._install_builtins()

    def check_program(self, ast):
        self.visit(ast)

    def _install_builtins(self):
        self.func_table["readInt"] = FuncInfo("readInt", [], self.int_type, False)
        self.func_table["readFloat"] = FuncInfo("readFloat", [], self.float_type, False)
        self.func_table["readString"] = FuncInfo("readString", [], self.string_type, False)
        self.func_table["printInt"] = FuncInfo("printInt", [self.int_type], self.void_type, False)
        self.func_table["printFloat"] = FuncInfo("printFloat", [self.float_type], self.void_type, False)
        self.func_table["printString"] = FuncInfo("printString", [self.string_type], self.void_type, False)

    def _ctx_expected(self, o):
        if isinstance(o, dict):
            return o.get("expected")
        return None

    def _ctx_assign_stmt(self, o):
        if isinstance(o, dict):
            return bool(o.get("assign_stmt", False))
        return False

    def _expr_ctx(self, expected=None, assign_stmt=False):
        return {"expected": expected, "assign_stmt": assign_stmt}

    def _same_type(self, left, right):
        if left is None or right is None:
            return False
        if type(left) is not type(right):
            return False
        if isinstance(left, StructType):
            return left.struct_name == right.struct_name
        return True

    def _is_int(self, ty):
        return isinstance(ty, IntType)

    def _is_float(self, ty):
        return isinstance(ty, FloatType)

    def _is_numeric(self, ty):
        return self._is_int(ty) or self._is_float(ty)

    def _is_void(self, ty):
        return isinstance(ty, VoidType)

    def _resolve_declared_type(self, ty, owner_node, allow_void):
        if ty is None: return None
        if isinstance(ty, VoidType):
            if allow_void: return ty
            raise TypeMismatchInStatement(owner_node)
        if isinstance(ty, StructType) and ty.struct_name not in self.struct_table:
            raise UndeclaredStruct(ty.struct_name)
        return ty

    def _push_scope(self):
        self.scope_stack.append({})

    def _pop_scope_with_inference_check(self, owner_node):
        scope = self.scope_stack.pop()
        for info in scope.values():
            if info.is_auto and info.var_type is None:
                raise TypeCannotBeInferred(owner_node)

    def _pop_scope_silent(self):
        self.scope_stack.pop()

    def _lookup_var(self, name):
        for scope in reversed(self.scope_stack):
            if name in scope: return scope[name]
        if name in self.current_params: return self.current_params[name]
        raise UndeclaredIdentifier(name)

    def _eval_expr(self, expr, expected=None, assign_stmt=False):
        return self.visit(expr, self._expr_ctx(expected, assign_stmt))

    def _check_int_condition(self, cond, stmt):
        cond_type = self._eval_expr(cond, expected=self.int_type)
        if cond_type is None: raise TypeCannotBeInferred(cond)
        if not self._is_int(cond_type): raise TypeMismatchInStatement(stmt)

    def _visit_stmt_in_inner_scope(self, stmt):
        self._push_scope()
        try:
            self.visit(stmt)
        except Exception:
            self._pop_scope_silent()
            raise
        self._pop_scope_with_inference_check(stmt)

    def _is_constant_expr(self, expr):
        if isinstance(expr, (IntLiteral, FloatLiteral, StringLiteral)): return True
        if isinstance(expr, PrefixOp):
            if expr.operator in ("++", "--"): return False
            return self._is_constant_expr(expr.operand)
        if isinstance(expr, BinaryOp):
            return self._is_constant_expr(expr.left) and self._is_constant_expr(expr.right)
        return False

    def visit_program(self, node, o=None):
        for decl in node.decls: self.visit(decl)

    def visit_struct_decl(self, node, o=None):
        if node.name in self.struct_table: raise Redeclared("Struct", node.name)
        members, member_order = {}, []
        for member in node.members:
            if member.name in members: raise Redeclared("Member", member.name)
            m_type = self._resolve_declared_type(member.member_type, member, False)
            members[member.name] = m_type
            member_order.append(member.name)
        self.struct_table[node.name] = StructInfo(node.name, members, member_order)

    def visit_member_decl(self, node, o=None):
        self._resolve_declared_type(node.member_type, node, False)

    def visit_func_decl(self, node, o=None):
        if node.name in self.func_table: raise Redeclared("Function", node.name)
        ret_type = self._resolve_declared_type(node.return_type, node, True)
        func_info = FuncInfo(node.name, [], ret_type, node.return_type is None)
        self.func_table[node.name] = func_info
        old_func, old_params = self.current_function, self.current_params
        self.current_function, self.current_params = func_info, {}
        try:
            for p in node.params: self.visit(p)
            self.visit(node.body)
            if func_info.inferred_return and func_info.return_type is None:
                func_info.return_type = self.void_type
        finally:
            self.current_function, self.current_params = old_func, old_params

    def visit_param(self, node, o=None):
        if node.name in self.current_params: raise Redeclared("Parameter", node.name)
        p_type = self._resolve_declared_type(node.param_type, node, False)
        self.current_params[node.name] = VarInfo(node.name, p_type, False)
        if self.current_function: self.current_function.param_types.append(p_type)

    def visit_block_stmt(self, node, o=None):
        self._push_scope()
        try:
            for stmt in node.statements: self.visit(stmt)
        except Exception:
            self._pop_scope_silent()
            raise
        self._pop_scope_with_inference_check(node)

    def visit_var_decl(self, node, o=None):
        if not self.scope_stack: self._push_scope()
        scope = self.scope_stack[-1]
        if node.name in scope or node.name in self.current_params:
            raise Redeclared("Variable", node.name)
        is_auto = node.var_type is None
        var_type = self._resolve_declared_type(node.var_type, node, False)
        if node.init_value:
            if is_auto:
                inf_type = self._eval_expr(node.init_value)
                if inf_type is None: raise TypeCannotBeInferred(node.init_value)
                var_type = inf_type
            else:
                init_t = self._eval_expr(node.init_value, expected=var_type)
                if init_t is None: raise TypeCannotBeInferred(node.init_value)
                if not self._same_type(init_t, var_type): raise TypeMismatchInStatement(node)
        scope[node.name] = VarInfo(node.name, var_type, is_auto)

    def visit_if_stmt(self, node, o=None):
        self._check_int_condition(node.condition, node)
        self._visit_stmt_in_inner_scope(node.then_stmt)
        if node.else_stmt: self._visit_stmt_in_inner_scope(node.else_stmt)

    def visit_while_stmt(self, node, o=None):
        self._check_int_condition(node.condition, node)
        self.loop_depth += 1
        try: self._visit_stmt_in_inner_scope(node.body)
        finally: self.loop_depth -= 1

    def visit_for_stmt(self, node, o=None):
        if node.init: self.visit(node.init)
        if node.condition: self._check_int_condition(node.condition, node)
        if node.update:
            up_type = self._eval_expr(node.update, assign_stmt=isinstance(node.update, AssignExpr))
            if up_type is None: raise TypeCannotBeInferred(node.update)
        self.loop_depth += 1
        self._push_scope()
        try: self.visit(node.body)
        except Exception:
            self._pop_scope_silent()
            self.loop_depth -= 1
            raise
        self.loop_depth -= 1
        self._pop_scope_with_inference_check(node)

    def visit_switch_stmt(self, node, o=None):
        self._check_int_condition(node.expr, node)
        self.switch_depth += 1
        self._push_scope()
        try:
            for case in node.cases: self.visit(case, node)
            if node.default_case: self.visit(node.default_case, node)
        except Exception:
            self._pop_scope_silent()
            self.switch_depth -= 1
            raise
        self._pop_scope_with_inference_check(node)
        self.switch_depth -= 1

    def visit_case_stmt(self, node, o=None):
        owner = o if isinstance(o, SwitchStmt) else node
        self._check_int_condition(node.expr, owner)
        if not self._is_constant_expr(node.expr): raise TypeMismatchInStatement(owner)
        for stmt in node.statements: self.visit(stmt)

    def visit_default_stmt(self, node, o=None):
        for stmt in node.statements: self.visit(stmt)

    def visit_break_stmt(self, node, o=None):
        if self.loop_depth == 0 and self.switch_depth == 0: raise MustInLoop(node)

    def visit_continue_stmt(self, node, o=None):
        if self.loop_depth == 0: raise MustInLoop(node)

    def visit_return_stmt(self, node, o=None):
        if not self.current_function: return
        func = self.current_function
        if node.expr is None:
            if func.inferred_return:
                if func.return_type and not self._is_void(func.return_type): raise TypeMismatchInStatement(node)
                func.saw_bare_return = True
            elif not self._is_void(func.return_type): raise TypeMismatchInStatement(node)
            return
        val_type = self._eval_expr(node.expr, expected=func.return_type)
        if val_type is None: raise TypeCannotBeInferred(node)
        if func.inferred_return:
            if func.return_type is None:
                if func.saw_bare_return: raise TypeMismatchInStatement(node)
                func.return_type = val_type
            elif not self._same_type(func.return_type, val_type): raise TypeMismatchInStatement(node)
        elif not self._same_type(func.return_type, val_type): raise TypeMismatchInStatement(node)

    def visit_expr_stmt(self, node, o=None):
        is_assign = isinstance(node.expr, AssignExpr)
        try:
            res_type = self._eval_expr(node.expr, assign_stmt=is_assign)
        except TypeMismatchInStatement as err:
            if isinstance(err.stmt, AssignExpr): raise TypeMismatchInStatement(node)
            raise
        if res_type is None: raise TypeCannotBeInferred(node.expr)

    def visit_binary_op(self, node, o=None):
        op = node.operator
        if op in ("&&", "||", "%"):
            l, r = self._eval_expr(node.left, self.int_type), self._eval_expr(node.right, self.int_type)
            if l is None or r is None: raise TypeCannotBeInferred(node)
            if not self._is_int(l) or not self._is_int(r): raise TypeMismatchInExpression(node)
            return self.int_type
        if op in ("==", "!=", "<", "<=", ">", ">="):
            l, r = self._eval_expr(node.left), self._eval_expr(node.right)
            if (l and not self._is_numeric(l)) or (r and not self._is_numeric(r)): raise TypeMismatchInExpression(node)
            if l is None or r is None: raise TypeCannotBeInferred(node)
            return self.int_type
        if op in ("+", "-", "*", "/"):
            l, r = self._eval_expr(node.left), self._eval_expr(node.right)
            if (l and not self._is_numeric(l)) or (r and not self._is_numeric(r)): raise TypeMismatchInExpression(node)
            if l is None and r is None: raise TypeCannotBeInferred(node)
            if l is None:
                if not isinstance(node.right, IntLiteral): raise TypeCannotBeInferred(node)
                l = self._eval_expr(node.left, self.int_type)
            elif r is None:
                if not isinstance(node.left, IntLiteral): raise TypeCannotBeInferred(node)
                r = self._eval_expr(node.right, self.int_type)
            if l is None or r is None: raise TypeCannotBeInferred(node)
            return self.int_type if (self._is_int(l) and self._is_int(r)) else self.float_type
        raise TypeMismatchInExpression(node)

    def visit_prefix_op(self, node, o=None):
        op = node.operator
        if op in ("++", "--"):
            if not isinstance(node.operand, (Identifier, MemberAccess)): raise TypeMismatchInExpression(node)
            t = self._eval_expr(node.operand, self.int_type)
            if t is None: raise TypeCannotBeInferred(node)
            if not self._is_int(t): raise TypeMismatchInExpression(node)
            return self.int_type
        if op == "!":
            t = self._eval_expr(node.operand, self.int_type)
            if t is None: raise TypeCannotBeInferred(node)
            if not self._is_int(t): raise TypeMismatchInExpression(node)
            return self.int_type
        if op in ("+", "-"):
            t = self._eval_expr(node.operand)
            if t is None: raise TypeCannotBeInferred(node)
            if not self._is_numeric(t): raise TypeMismatchInExpression(node)
            return t
        raise TypeMismatchInExpression(node)

    def visit_postfix_op(self, node, o=None):
        if not isinstance(node.operand, (Identifier, MemberAccess)): raise TypeMismatchInExpression(node)
        t = self._eval_expr(node.operand, self.int_type)
        if t is None: raise TypeCannotBeInferred(node)
        if not self._is_int(t): raise TypeMismatchInExpression(node)
        return self.int_type

    def visit_assign_expr(self, node, o=None):
        if not isinstance(node.lhs, (Identifier, MemberAccess)): raise TypeMismatchInExpression(node)
        lt = self._eval_expr(node.lhs)
        rt = self._eval_expr(node.rhs, expected=lt)
        if lt is None and rt and isinstance(node.lhs, Identifier): lt = self._eval_expr(node.lhs, expected=rt)
        if rt is None and lt: rt = self._eval_expr(node.rhs, expected=lt)
        if lt is None or rt is None: raise TypeCannotBeInferred(node)
        if not self._same_type(lt, rt):
            if self._ctx_assign_stmt(o): raise TypeMismatchInStatement(node)
            raise TypeMismatchInExpression(node)
        return lt

    def visit_member_access(self, node, o=None):
        obj_t = self._eval_expr(node.obj)
        if obj_t is None: raise TypeCannotBeInferred(node)
        if not isinstance(obj_t, StructType): raise TypeMismatchInExpression(node)
        info = self.struct_table.get(obj_t.struct_name)
        if info is None: raise UndeclaredStruct(obj_t.struct_name)
        if node.member not in info.members: raise TypeMismatchInExpression(node)
        return info.members[node.member]

    def visit_func_call(self, node, o=None):
        if node.name not in self.func_table: raise UndeclaredFunction(node.name)
        info = self.func_table[node.name]
        if len(node.args) != len(info.param_types): raise TypeMismatchInExpression(node)
        for arg, p_type in zip(node.args, info.param_types):
            a_type = self._eval_expr(arg, expected=p_type)
            if a_type is None: raise TypeCannotBeInferred(arg)
            if not self._same_type(a_type, p_type): raise TypeMismatchInExpression(node)
        return info.return_type

    def visit_identifier(self, node, o=None):
        info = self._lookup_var(node.name)
        exp = self._ctx_expected(o)
        if info.var_type is None and exp: info.var_type = exp
        return info.var_type

    def visit_struct_literal(self, node, o=None):
        exp = self._ctx_expected(o)
        if exp is None:
            for v in node.values: self._eval_expr(v)
            return None
        if not isinstance(exp, StructType): raise TypeMismatchInExpression(node)
        info = self.struct_table.get(exp.struct_name)
        if info is None: raise UndeclaredStruct(exp.struct_name)
        if len(node.values) != len(info.member_order): raise TypeMismatchInExpression(node)
        for val, m_name in zip(node.values, info.member_order):
            m_type = info.members[m_name]
            v_type = self._eval_expr(val, expected=m_type)
            if v_type is None: raise TypeCannotBeInferred(val)
            if not self._same_type(v_type, m_type): raise TypeMismatchInExpression(node)
        return exp

    def visit_int_type(self, node, o=None): return node
    def visit_float_type(self, node, o=None): return node
    def visit_string_type(self, node, o=None): return node
    def visit_void_type(self, node, o=None): return node
    def visit_struct_type(self, node, o=None):
        if node.struct_name not in self.struct_table: raise UndeclaredStruct(node.struct_name)
        return node

    def visit_int_literal(self, node, o=None): return self.int_type
    def visit_float_literal(self, node, o=None): return self.float_type
    def visit_string_literal(self, node, o=None): return self.string_type
