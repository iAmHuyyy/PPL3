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

class StaticChecker(ASTVisitor):
    def __init__(self):
        self.symbols: Dict[str, Union[VarDecl, FuncDecl, StructDecl]] = {}
        self.errors: List[StaticError] = []
        self.current_function: Optional[FuncDecl] = None
        self.current_scope: Optional[Set[str]] = None

    def check_program(self, ast: Program):
        """Entry point to perform static checking on the entire program."""
        self.visit(ast)  # Start visiting the AST
        if self.errors:
            return f"Static checking failed with {len(self.errors)} errors."
        return "Static checking passed"

    def visit_program(self, node: "Program", o: Any = None):
        for decl in node.decls:
            self.visit(decl, o)

    def visit_member_access(self, node: "MemberAccess", o: Any = None):
        self.visit(node.obj, o)  # Đảm bảo đối tượng cơ sở (obj) được truy cập trước

        # Kiểm tra nếu đối tượng truy cập là một Identifier (tên biến)
        if isinstance(node.obj, Identifier):
            if isinstance(node.obj.type, StructType):
                # Truy cập thành viên của struct
                struct_type = node.obj.type
                member = struct_type.get_member(node.member_name)  # Lấy thành viên từ struct
                if not member:
                    self.errors.append(UndeclaredIdentifier(node.member_name))  # Thành viên không tồn tại
                else:
                    node.type = member.type  # Gán kiểu dữ liệu của thành viên cho MemberAccess
            else:
                # Nếu không phải là kiểu struct, báo lỗi kiểu mismatch
                self.errors.append(TypeMismatchInExpression(node))
        else:
            # Nếu đối tượng không phải là Identifier, báo lỗi kiểu mismatch
            self.errors.append(TypeMismatchInExpression(node))

    def visit_identifier(self, node: "Identifier", o: Any = None):
        if node.name not in self.symbols:
            self.errors.append(UndeclaredIdentifier(node.name))
        elif not node.type:
            self.errors.append(TypeCannotBeInferred(node))
        else:
            # Kiểm tra loại biến/identifier này
            pass

    # Other visit methods follow here...
    def visit_struct_decl(self, node: "StructDecl", o: Any = None):
        if node.name in self.symbols:
            self.errors.append(Redeclared("Struct", node.name))
        else:
            self.symbols[node.name] = node
        self.current_scope = set()
        for member in node.members:
            self.visit(member)

    def visit_member_decl(self, node: "MemberDecl", o: Any = None):
        if node.name in self.current_scope:
            self.errors.append(Redeclared("Member", node.name))
        else:
            self.current_scope.add(node.name)

    def visit_func_decl(self, node: "FuncDecl", o: Any = None):
        if node.name in self.symbols:
            self.errors.append(Redeclared("Function", node.name))
        else:
            self.symbols[node.name] = node
        self.current_function = node
        self.current_scope = {param.name for param in node.params}
        for param in node.params:
            self.visit(param, o)
        self.visit(node.body, o)

    def visit_param(self, node: "Param", o: Any = None):
        if node.name in self.current_scope:
            self.errors.append(Redeclared("Parameter", node.name))
        else:
            self.current_scope.add(node.name)

    def visit_var_decl(self, node: "VarDecl", o: Any = None):
        if node.name in self.current_scope:
            self.errors.append(Redeclared("Variable", node.name))
        else:
            self.current_scope.add(node.name)
        if isinstance(node.var_type, VoidType):
            self.errors.append(TypeMismatchInStatement(node))  # Void type not allowed for variables

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        prev_scope = self.current_scope
        self.current_scope = set()
        for stmt in node.statements:
            self.visit(stmt, o)
        self.current_scope = prev_scope

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        self.visit(node.condition, o)
        self.visit(node.then_stmt, o)
        if node.else_stmt:
            self.visit(node.else_stmt, o)

    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        self.visit(node.condition, o)
        self.visit(node.body, o)

    def visit_for_stmt(self, node: "ForStmt", o: Any = None):
        self.visit(node.init, o)
        self.visit(node.condition, o)
        self.visit(node.update, o)
        self.visit(node.body, o)

    def visit_switch_stmt(self, node: "SwitchStmt", o: Any = None):
        self.visit(node.expr, o)
        for case in node.cases:
            self.visit(case, o)
        if node.default_case:
            self.visit(node.default_case, o)

    def visit_case_stmt(self, node: "CaseStmt", o: Any = None):
        self.visit(node.expr, o)
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_default_stmt(self, node: "DefaultStmt", o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        if not self.current_function:
            self.errors.append(MustInLoop(node))

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        if not self.current_function:
            self.errors.append(MustInLoop(node))

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        if self.current_function and isinstance(self.current_function.return_type, VoidType):
            if node.expr:
                self.errors.append(TypeMismatchInStatement(node))
        if node.expr:
            self.visit(node.expr, o)

    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        self.visit(node.expr, o)

    # Kiểm tra các kiểu dữ liệu
    def visit_int_type(self, node: "IntType", o: Any = None):
        pass

    def visit_float_type(self, node: "FloatType", o: Any = None):
        pass

    def visit_string_type(self, node: "StringType", o: Any = None):
        pass

    def visit_void_type(self, node: "VoidType", o: Any = None):
        pass

    def visit_struct_type(self, node: "StructType", o: Any = None):
        if node.name not in self.symbols:
            self.errors.append(UndeclaredStruct(node.name))

    # Kiểm tra các biểu thức
    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        self.visit(node.left, o)
        self.visit(node.right, o)
        
        # Kiểm tra kiểu của các toán hạng
        if node.left.type != node.right.type:
            self.errors.append(TypeMismatchInExpression(node))

    def visit_prefix_op(self, node: "PrefixOp", o: Any = None):
        self.visit(node.operand, o)
        if isinstance(node.operand, Identifier) and node.operand.type != IntType:
            self.errors.append(TypeMismatchInExpression(node))

    def visit_postfix_op(self, node: "PostfixOp", o: Any = None):
        self.visit(node.operand, o)
        if isinstance(node.operand, Identifier) and node.operand.type != IntType:
            self.errors.append(TypeMismatchInExpression(node))

    def visit_assign_expr(self, node: "AssignExpr", o: Any = None):
        self.visit(node.lhs, o)
        self.visit(node.rhs, o)
        if node.lhs.type != node.rhs.type:
            self.errors.append(TypeMismatchInExpression(node))


    def visit_func_call(self, node: "FuncCall", o: Any = None):
        for arg in node.args:
            self.visit(arg, o)
        if node.name not in self.symbols:
            self.errors.append(UndeclaredFunction(node.name))

    

    def visit_struct_literal(self, node: "StructLiteral", o: Any = None):
        for value in node.values:
            self.visit(value, o)

    def visit_int_literal(self, node: "IntLiteral", o: Any = None):
        pass

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        pass

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        pass