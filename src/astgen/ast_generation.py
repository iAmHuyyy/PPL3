"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.TyCVisitor import TyCVisitor
from build.TyCParser import TyCParser
from src.utils.nodes import *

class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _build_member_chain(self, base, field_names):
        result = base
        for name in field_names:
            result = MemberAccess(result, name)
        return result

    def _apply_prefix_ops(self, ops, expr):
        result = expr
        for op in reversed(ops):
            result = PrefixOp(op, result)
        return result

    def _apply_postfix_ops(self, expr, ops):
        result = expr
        for op in ops:
            result = PostfixOp(op, result)
        return result

    def _fold_binary_tail(self, left, tail):
        result = left
        for op, right in tail:
            result = BinaryOp(result, op, right)
        return result

    # ------------------------------------------------------------------
    # Program / declarations
    # ------------------------------------------------------------------
    def visitProgram(self, ctx: TyCParser.ProgramContext):
        return Program(self.visit(ctx.declList()))

    def visitDeclList(self, ctx: TyCParser.DeclListContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.decl())] + self.visit(ctx.declList())

    def visitDecl(self, ctx: TyCParser.DeclContext):
        if ctx.structDecl():
            return self.visit(ctx.structDecl())
        return self.visit(ctx.funcDecl())

    def visitStructDecl(self, ctx: TyCParser.StructDeclContext):
        return StructDecl(ctx.ID().getText(), self.visit(ctx.structMemberList()))

    def visitStructMemberList(self, ctx: TyCParser.StructMemberListContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.structMember())] + self.visit(ctx.structMemberList())

    def visitStructMember(self, ctx: TyCParser.StructMemberContext):
        return MemberDecl(self.visit(ctx.type_()), ctx.ID().getText())

    def visitFuncDecl(self, ctx: TyCParser.FuncDeclContext):
        return_type, name = self.visit(ctx.funcHead())
        params = self.visit(ctx.paramListOpt())
        body = self.visit(ctx.blockStmt())
        return FuncDecl(return_type, name, params, body)

    def visitFuncHead(self, ctx: TyCParser.FuncHeadContext):
        if ctx.typeOrVoid():
            return self.visit(ctx.typeOrVoid()), ctx.ID().getText()
        return None, ctx.ID().getText()

    def visitTypeOrVoid(self, ctx: TyCParser.TypeOrVoidContext):
        if ctx.VOID():
            return VoidType()
        return self.visit(ctx.type_())

    def visitParamListOpt(self, ctx: TyCParser.ParamListOptContext):
        if ctx.paramList():
            return self.visit(ctx.paramList())
        return []

    def visitParamList(self, ctx: TyCParser.ParamListContext):
        return [self.visit(ctx.param())] + self.visit(ctx.paramListTail())

    def visitParamListTail(self, ctx: TyCParser.ParamListTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.param())] + self.visit(ctx.paramListTail())

    def visitParam(self, ctx: TyCParser.ParamContext):
        return Param(self.visit(ctx.type_()), ctx.ID().getText())

    def visitType(self, ctx: TyCParser.TypeContext):
        if ctx.INT():
            return IntType()
        if ctx.FLOAT():
            return FloatType()
        if ctx.STRING():
            return StringType()
        return StructType(ctx.ID().getText())

    # ------------------------------------------------------------------
    # Statements
    # ------------------------------------------------------------------
    def visitStatement(self, ctx: TyCParser.StatementContext):
        return self.visit(ctx.getChild(0))

    def visitStatementList(self, ctx: TyCParser.StatementListContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.statement())] + self.visit(ctx.statementList())

    def visitVarDeclStmt(self, ctx: TyCParser.VarDeclStmtContext):
        return self.visit(ctx.varDecl())

    def visitVarDecl(self, ctx: TyCParser.VarDeclContext):
        var_type = self.visit(ctx.varDeclHead())
        name = ctx.ID().getText()
        init_value = self.visit(ctx.varInitOpt())
        return VarDecl(var_type, name, init_value)

    def visitVarDeclHead(self, ctx: TyCParser.VarDeclHeadContext):
        if ctx.AUTO():
            return None
        return self.visit(ctx.type_())

    def visitVarInitOpt(self, ctx: TyCParser.VarInitOptContext):
        if ctx.expr():
            return self.visit(ctx.expr())
        return None

    def visitBlockStmt(self, ctx: TyCParser.BlockStmtContext):
        return BlockStmt(self.visit(ctx.statementList()))

    def visitIfStmt(self, ctx: TyCParser.IfStmtContext):
        return IfStmt(
            self.visit(ctx.expr()),
            self.visit(ctx.statement()),
            self.visit(ctx.elseOpt()),
        )

    def visitElseOpt(self, ctx: TyCParser.ElseOptContext):
        if ctx.statement():
            return self.visit(ctx.statement())
        return None

    def visitWhileStmt(self, ctx: TyCParser.WhileStmtContext):
        return WhileStmt(self.visit(ctx.expr()), self.visit(ctx.statement()))

    def visitForStmt(self, ctx: TyCParser.ForStmtContext):
        init = self.visit(ctx.forInitOpt())
        if init is not None and isinstance(init, Expr):
            init = ExprStmt(init)
        return ForStmt(
            init,
            self.visit(ctx.exprOpt()),
            self.visit(ctx.forUpdateOpt()),
            self.visit(ctx.statement()),
        )

    def visitForInitOpt(self, ctx: TyCParser.ForInitOptContext):
        if ctx.forInit():
            return self.visit(ctx.forInit())
        return None

    def visitForInit(self, ctx: TyCParser.ForInitContext):
        if ctx.forVarDecl():
            return self.visit(ctx.forVarDecl())
        return self.visit(ctx.forAssign())

    def visitForAssign(self, ctx: TyCParser.ForAssignContext):
        return AssignExpr(self.visit(ctx.lvalue()), self.visit(ctx.expr()))

    def visitForVarDecl(self, ctx: TyCParser.ForVarDeclContext):
        return VarDecl(
            self.visit(ctx.varDeclHead()),
            ctx.ID().getText(),
            self.visit(ctx.varInitOpt()),
        )

    def visitExprOpt(self, ctx: TyCParser.ExprOptContext):
        if ctx.expr():
            return self.visit(ctx.expr())
        return None

    def visitForUpdateOpt(self, ctx: TyCParser.ForUpdateOptContext):
        if ctx.forUpdate():
            return self.visit(ctx.forUpdate())
        return None

    def visitForUpdate(self, ctx: TyCParser.ForUpdateContext):
        if ctx.lvalue() and ctx.ASSIGN():
            return AssignExpr(self.visit(ctx.lvalue()), self.visit(ctx.expr()))

        if ctx.postfixExpr():
            base = self.visit(ctx.postfixExpr())
            prefix_ops = [node.getText() for node in ctx.prefixIncDec()]
            postfix_ops = [node.getText() for node in ctx.postfixIncDec()]
            return self._apply_postfix_ops(self._apply_prefix_ops(prefix_ops, base), postfix_ops)

        return None

    def visitSwitchStmt(self, ctx: TyCParser.SwitchStmtContext):
        cases, default_case = self.visit(ctx.switchSections())
        return SwitchStmt(self.visit(ctx.expr()), cases, default_case)

    def visitSwitchSections(self, ctx: TyCParser.SwitchSectionsContext):
        cases = [self.visit(case_ctx) for case_ctx in ctx.caseSection()]
        default_case = self.visit(ctx.defaultSection()) if ctx.defaultSection() else None
        return cases, default_case

    def visitCaseSection(self, ctx: TyCParser.CaseSectionContext):
        return CaseStmt(self.visit(ctx.expr()), self.visit(ctx.statementList()))

    def visitDefaultSection(self, ctx: TyCParser.DefaultSectionContext):
        return DefaultStmt(self.visit(ctx.statementList()))

    def visitBreakStmt(self, ctx: TyCParser.BreakStmtContext):
        return BreakStmt()

    def visitContinueStmt(self, ctx: TyCParser.ContinueStmtContext):
        return ContinueStmt()

    def visitReturnStmt(self, ctx: TyCParser.ReturnStmtContext):
        return ReturnStmt(self.visit(ctx.returnExprOpt()))

    def visitReturnExprOpt(self, ctx: TyCParser.ReturnExprOptContext):
        if ctx.expr():
            return self.visit(ctx.expr())
        return None

    def visitExprStmt(self, ctx: TyCParser.ExprStmtContext):
        return ExprStmt(self.visit(ctx.expr()))

    # ------------------------------------------------------------------
    # Expressions
    # ------------------------------------------------------------------
    def visitExpr(self, ctx: TyCParser.ExprContext):
        return self.visit(ctx.assignExpr())

    def visitLvalue(self, ctx: TyCParser.LvalueContext):
        ids = ctx.ID()
        if ids:
            base = Identifier(ids[0].getText())
            return self._build_member_chain(base, [tok.getText() for tok in ids[1:]])

        base = self.visit(ctx.lvalueBase())
        fields = [self.visit(field_ctx) for field_ctx in ctx.lvalueField()]
        return self._build_member_chain(base, fields)

    def visitLvalueBase(self, ctx: TyCParser.LvalueBaseContext):
        result = self.visit(ctx.primaryExpr())
        for tail_ctx in ctx.lvalueBaseTail():
            args = self.visit(tail_ctx)
            if isinstance(result, Identifier):
                result = FuncCall(result.name, args)
            else:
                result = FuncCall(str(result), args)
        return result

    def visitLvalueBaseTail(self, ctx: TyCParser.LvalueBaseTailContext):
        return self.visit(ctx.argListOpt())

    def visitLvalueField(self, ctx: TyCParser.LvalueFieldContext):
        return ctx.ID().getText()

    def visitAssignExpr(self, ctx: TyCParser.AssignExprContext):
        if ctx.lvalue():
            return AssignExpr(self.visit(ctx.lvalue()), self.visit(ctx.assignExpr()))
        return self.visit(ctx.orExpr())

    def visitOrExpr(self, ctx: TyCParser.OrExprContext):
        return self._fold_binary_tail(self.visit(ctx.andExpr()), self.visit(ctx.orTail()))

    def visitOrTail(self, ctx: TyCParser.OrTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [(ctx.OR().getText(), self.visit(ctx.andExpr()))] + self.visit(ctx.orTail())

    def visitAndExpr(self, ctx: TyCParser.AndExprContext):
        return self._fold_binary_tail(self.visit(ctx.eqExpr()), self.visit(ctx.andTail()))

    def visitAndTail(self, ctx: TyCParser.AndTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [(ctx.AND().getText(), self.visit(ctx.eqExpr()))] + self.visit(ctx.andTail())

    def visitEqExpr(self, ctx: TyCParser.EqExprContext):
        return self._fold_binary_tail(self.visit(ctx.relExpr()), self.visit(ctx.eqTail()))

    def visitEqTail(self, ctx: TyCParser.EqTailContext):
        if ctx.getChildCount() == 0:
            return []
        op = ctx.getChild(0).getText()
        return [(op, self.visit(ctx.relExpr()))] + self.visit(ctx.eqTail())

    def visitRelExpr(self, ctx: TyCParser.RelExprContext):
        return self._fold_binary_tail(self.visit(ctx.addExpr()), self.visit(ctx.relTail()))

    def visitRelTail(self, ctx: TyCParser.RelTailContext):
        if ctx.getChildCount() == 0:
            return []
        op = ctx.getChild(0).getText()
        return [(op, self.visit(ctx.addExpr()))] + self.visit(ctx.relTail())

    def visitAddExpr(self, ctx: TyCParser.AddExprContext):
        return self._fold_binary_tail(self.visit(ctx.mulExpr()), self.visit(ctx.addTail()))

    def visitAddTail(self, ctx: TyCParser.AddTailContext):
        if ctx.getChildCount() == 0:
            return []
        op = ctx.getChild(0).getText()
        return [(op, self.visit(ctx.mulExpr()))] + self.visit(ctx.addTail())

    def visitMulExpr(self, ctx: TyCParser.MulExprContext):
        return self._fold_binary_tail(self.visit(ctx.unaryExpr()), self.visit(ctx.mulTail()))

    def visitMulTail(self, ctx: TyCParser.MulTailContext):
        if ctx.getChildCount() == 0:
            return []
        op = ctx.getChild(0).getText()
        return [(op, self.visit(ctx.unaryExpr()))] + self.visit(ctx.mulTail())

    def visitUnaryExpr(self, ctx: TyCParser.UnaryExprContext):
        if ctx.incDecExpr():
            return self.visit(ctx.incDecExpr())
        return self.visit(ctx.unarySignExpr())

    def visitUnarySignExpr(self, ctx: TyCParser.UnarySignExprContext):
        return PrefixOp(ctx.getChild(0).getText(), self.visit(ctx.unaryExpr()))

    def visitIncDecExpr(self, ctx: TyCParser.IncDecExprContext):
        prefix_ops = [node.getText() for node in ctx.prefixIncDec()]
        postfix_ops = [node.getText() for node in ctx.postfixIncDec()]
        base = self.visit(ctx.postfixExpr())
        return self._apply_postfix_ops(self._apply_prefix_ops(prefix_ops, base), postfix_ops)

    def visitPrefixIncDec(self, ctx: TyCParser.PrefixIncDecContext):
        return ctx.getText()

    def visitPostfixIncDec(self, ctx: TyCParser.PostfixIncDecContext):
        return ctx.getText()

    def visitPostfixExpr(self, ctx: TyCParser.PostfixExprContext):
        result = self.visit(ctx.callOrPrimary())
        for field_ctx in ctx.fieldTail():
            result = MemberAccess(result, self.visit(field_ctx))
        if ctx.incDecTail():
            result = PostfixOp(self.visit(ctx.incDecTail()), result)
        return result

    def visitCallOrPrimary(self, ctx: TyCParser.CallOrPrimaryContext):
        base = self.visit(ctx.primaryExpr())
        if ctx.callTail():
            args = self.visit(ctx.callTail())
            if isinstance(base, Identifier):
                return FuncCall(base.name, args)
            return FuncCall(str(base), args)
        return base

    def visitCallTail(self, ctx: TyCParser.CallTailContext):
        return self.visit(ctx.argListOpt())

    def visitFieldTail(self, ctx: TyCParser.FieldTailContext):
        return ctx.ID().getText()

    def visitIncDecTail(self, ctx: TyCParser.IncDecTailContext):
        return ctx.getText()

    def visitArgListOpt(self, ctx: TyCParser.ArgListOptContext):
        if ctx.argList():
            return self.visit(ctx.argList())
        return []

    def visitArgList(self, ctx: TyCParser.ArgListContext):
        return [self.visit(ctx.expr())] + self.visit(ctx.argListTail())

    def visitArgListTail(self, ctx: TyCParser.ArgListTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.argListTail())

    def visitPrimaryExpr(self, ctx: TyCParser.PrimaryExprContext):
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        if ctx.expr():
            return self.visit(ctx.expr())
        return self.visit(ctx.structLiteral())

    def visitStructLiteral(self, ctx: TyCParser.StructLiteralContext):
        return StructLiteral(self.visit(ctx.structInitOpt()))

    def visitStructInitOpt(self, ctx: TyCParser.StructInitOptContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.structInitTail())

    def visitStructInitTail(self, ctx: TyCParser.StructInitTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.structInitTail())

    def visitLiteral(self, ctx: TyCParser.LiteralContext):
        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        if ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        return StringLiteral(ctx.STRING_LIT().getText())
