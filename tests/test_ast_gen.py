"""
AST Generation test cases for TyC compiler.
Implemented 100 test cases for AST generation.
"""

from tests.utils import ASTGenerator


def test_001():
    source = ""
    expected = "Program([])"
    assert str(ASTGenerator(source).generate()) == expected


def test_002():
    source = "void main() {}"
    expected = "Program([FuncDecl(VoidType(), main, [], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003():
    source = "main() {}"
    expected = "Program([FuncDecl(auto, main, [], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004():
    source = "struct Point { int x; };"
    expected = "Program([StructDecl(Point, [MemberDecl(IntType(), x)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005():
    source = "struct Point { int x; float y; };"
    expected = "Program([StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(FloatType(), y)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006():
    source = "int sum() {}"
    expected = "Program([FuncDecl(IntType(), sum, [], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007():
    source = "string name() {}"
    expected = "Program([FuncDecl(StringType(), name, [], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_008():
    source = "Point clone(Point p) {}"
    expected = "Program([FuncDecl(StructType(Point), clone, [Param(StructType(Point), p)], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009():
    source = "void f() {} void g() {}"
    expected = "Program([FuncDecl(VoidType(), f, [], []), FuncDecl(VoidType(), g, [], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_010():
    source = "struct S { string a; int b; }; void main() {}"
    expected = "Program([StructDecl(S, [MemberDecl(StringType(), a), MemberDecl(IntType(), b)]), FuncDecl(VoidType(), main, [], [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_011():
    source = "void main(){ int x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(IntType(), x)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_012():
    source = "void main(){ float x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(FloatType(), x)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_013():
    source = "void main(){ string s; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(StringType(), s)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_014():
    source = "void main(){ auto x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(auto, x)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_015():
    source = "void main(){ int x = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(IntType(), x = IntLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_016():
    source = "void main(){ auto x = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(auto, x = IntLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_017():
    source = 'void main(){ string s = "abc"; }'
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(StringType(), s = StringLiteral('abc'))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_018():
    source = "void main(){ return; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ReturnStmt(return)])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_019():
    source = "void main(){ break; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [BreakStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_020():
    source = "void main(){ continue; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ContinueStmt()])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_021():
    source = "void main(){ 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(IntLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_022():
    source = "void main(){ 1.5; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(FloatLiteral(1.5))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_023():
    source = 'void main(){ "x"; }'
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(StringLiteral('x'))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_024():
    source = "void main(){ x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_025():
    source = "void main(){ {}; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(StructLiteral({}))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_026():
    source = "void main(){ {1}; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(StructLiteral({IntLiteral(1)}))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_027():
    source = "void main(){ {1,2}; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(StructLiteral({IntLiteral(1), IntLiteral(2)}))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_028():
    source = "void main(){ (1); }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(IntLiteral(1))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_029():
    source = "void main(){ ((x)); }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(Identifier(x))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_030():
    source = "void main(){ {} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [BlockStmt([])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_031():
    source = "void main(){ 1 + 2; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(IntLiteral(1), +, IntLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_032():
    source = "void main(){ 1 - 2 - 3; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), -, IntLiteral(2)), -, IntLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_033():
    source = "void main(){ 1 * 2 + 3; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), *, IntLiteral(2)), +, IntLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_034():
    source = "void main(){ 1 + 2 * 3; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_035():
    source = "void main(){ 1 % 2 / 3; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), %, IntLiteral(2)), /, IntLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_036():
    source = "void main(){ 1 < 2; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(IntLiteral(1), <, IntLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_037():
    source = "void main(){ 1 <= 2 == 3; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), <=, IntLiteral(2)), ==, IntLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_038():
    source = "void main(){ 1 < 2 && 3 < 4; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), <, IntLiteral(2)), &&, BinaryOp(IntLiteral(3), <, IntLiteral(4))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_039():
    source = "void main(){ 1 < 2 || 3 < 4 && 5 < 6; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), <, IntLiteral(2)), ||, BinaryOp(BinaryOp(IntLiteral(3), <, IntLiteral(4)), &&, BinaryOp(IntLiteral(5), <, IntLiteral(6)))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_040():
    source = "void main(){ (1 + 2) * 3; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, IntLiteral(3)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_041():
    source = "void main(){ -1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(-IntLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_042():
    source = "void main(){ +1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(+IntLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_043():
    source = "void main(){ !x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(!Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_044():
    source = "void main(){ ++x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(++Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_045():
    source = "void main(){ --x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(--Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_046():
    source = "void main(){ x++; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PostfixOp(Identifier(x)++))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_047():
    source = "void main(){ x--; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PostfixOp(Identifier(x)--))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_048():
    source = "void main(){ ++x++; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(++PostfixOp(Identifier(x)++)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_049():
    source = "void main(){ !-+x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(!PrefixOp(-PrefixOp(+Identifier(x)))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_050():
    source = "void main(){ ++(x); }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(PrefixOp(++Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_051():
    source = "void main(){ x = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(AssignExpr(Identifier(x) = IntLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_052():
    source = "void main(){ x = y = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(AssignExpr(Identifier(x) = AssignExpr(Identifier(y) = IntLiteral(1))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_053():
    source = "void main(){ x.a = 1; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(AssignExpr(MemberAccess(Identifier(x).a) = IntLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_054():
    source = "void main(){ x.a.b = y; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier(x).a).b) = Identifier(y)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_055():
    source = "void main(){ f(); }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(FuncCall(f, []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_056():
    source = "void main(){ f(1, 2); }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(FuncCall(f, [IntLiteral(1), IntLiteral(2)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_057():
    source = "void main(){ f(1 + 2, x); }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(FuncCall(f, [BinaryOp(IntLiteral(1), +, IntLiteral(2)), Identifier(x)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_058():
    source = "void main(){ x.a; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(MemberAccess(Identifier(x).a))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_059():
    source = "void main(){ x.a.b; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(MemberAccess(MemberAccess(Identifier(x).a).b))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_060():
    source = "void main(){ f().a; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(MemberAccess(FuncCall(f, []).a))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_061():
    source = "void main(){ if (x) y; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [IfStmt(if Identifier(x) then ExprStmt(Identifier(y)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_062():
    source = "void main(){ if (x) y; else z; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [IfStmt(if Identifier(x) then ExprStmt(Identifier(y)), else ExprStmt(Identifier(z)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_063():
    source = "void main(){ if (x) { y; } else { z; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [IfStmt(if Identifier(x) then BlockStmt([ExprStmt(Identifier(y))]), else BlockStmt([ExprStmt(Identifier(z))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_064():
    source = "void main(){ while (x) y; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [WhileStmt(while Identifier(x) do ExprStmt(Identifier(y)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_065():
    source = "void main(){ while (x < 10) { x++; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [WhileStmt(while BinaryOp(Identifier(x), <, IntLiteral(10)) do BlockStmt([ExprStmt(PostfixOp(Identifier(x)++))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_066():
    source = "void main(){ if (x) while (y) z; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [IfStmt(if Identifier(x) then WhileStmt(while Identifier(y) do ExprStmt(Identifier(z))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_067():
    source = "void main(){ if (x) if (y) z; else t; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [IfStmt(if Identifier(x) then IfStmt(if Identifier(y) then ExprStmt(Identifier(z)), else ExprStmt(Identifier(t))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_068():
    source = "void main(){ while (x) if (y) z; else t; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [WhileStmt(while Identifier(x) do IfStmt(if Identifier(y) then ExprStmt(Identifier(z)), else ExprStmt(Identifier(t))))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_069():
    source = "void main(){ if (x) return; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [IfStmt(if Identifier(x) then ReturnStmt(return))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_070():
    source = "void main(){ while (x) break; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [WhileStmt(while Identifier(x) do BreakStmt())])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_071():
    source = "void main(){ for (;;) x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; None; None do ExprStmt(Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_072():
    source = "void main(){ for (int i = 0; i < 10; i++) x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do ExprStmt(Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_073():
    source = "void main(){ for (auto i = 0; ; ) x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for VarDecl(auto, i = IntLiteral(0)); None; None do ExprStmt(Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_074():
    source = "void main(){ for (i = 0; i < 10; i = i + 1) x; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for ExprStmt(AssignExpr(Identifier(i) = IntLiteral(0))); BinaryOp(Identifier(i), <, IntLiteral(10)); AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, IntLiteral(1))) do ExprStmt(Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_075():
    source = "void main(){ for (; x; ++i) {} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; Identifier(x); PrefixOp(++Identifier(i)) do BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_076():
    source = "void main(){ for (; x; --i++) {} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; Identifier(x); PrefixOp(--PostfixOp(Identifier(i)++)) do BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_077():
    source = "void main(){ for (; ; a.b = 1) {} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; None; AssignExpr(MemberAccess(Identifier(a).b) = IntLiteral(1)) do BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_078():
    source = "void main(){ for (int i; ; ) {} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for VarDecl(IntType(), i); None; None do BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_079():
    source = "void main(){ for (; i < 10; i--) {} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)--) do BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_080():
    source = "void main(){ for (; ; ++a.b) {} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for None; None; PrefixOp(++MemberAccess(Identifier(a).b)) do BlockStmt([]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_081():
    source = "void main(){ switch(x){} }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_082():
    source = "void main(){ switch(x){ case 1: } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [])])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_083():
    source = "void main(){ switch(x){ default: } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [], default DefaultStmt(default: []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_084():
    source = "void main(){ switch(x){ case 1: y; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(Identifier(y))])])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_085():
    source = "void main(){ switch(x){ case 1: y; break; default: z; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(Identifier(y)), BreakStmt()])], default DefaultStmt(default: [ExprStmt(Identifier(z))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_086():
    source = "void main(){ switch(x){ case 1: y; case 2: z; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(Identifier(y))]), CaseStmt(case IntLiteral(2): [ExprStmt(Identifier(z))])])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_087():
    source = "void main(){ switch(x){ case 1: case 2: } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): []), CaseStmt(case IntLiteral(2): [])])])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_088():
    source = "void main(){ switch(x){ case 1: default: } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [])], default DefaultStmt(default: []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_089():
    source = "void main(){ switch(x){ default: case 2: } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(2): [])], default DefaultStmt(default: []))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_090():
    source = "void main(){ switch(x){ case 1: return; default: break; } }"
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ReturnStmt(return)])], default DefaultStmt(default: [BreakStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_091():
    source = "void main(){ Point p = {}; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(StructType(Point), p = StructLiteral({}))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_092():
    source = "void main(){ Point p = {1, 2}; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(StructType(Point), p = StructLiteral({IntLiteral(1), IntLiteral(2)}))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_093():
    source = "void main(){ auto p = {{1}, 2}; }"
    expected = "Program([FuncDecl(VoidType(), main, [], [VarDecl(auto, p = StructLiteral({StructLiteral({IntLiteral(1)}), IntLiteral(2)}))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_094():
    source = "void main(){ f({1,2}); }"
    expected = "Program([FuncDecl(VoidType(), main, [], [ExprStmt(FuncCall(f, [StructLiteral({IntLiteral(1), IntLiteral(2)})]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_095():
    source = """
struct Point { int x; int y; };
void main() {
    Point p = {1,2};
    p.x = p.y;
}
"""
    expected = "Program([StructDecl(Point, [MemberDecl(IntType(), x), MemberDecl(IntType(), y)]), FuncDecl(VoidType(), main, [], [VarDecl(StructType(Point), p = StructLiteral({IntLiteral(1), IntLiteral(2)})), ExprStmt(AssignExpr(MemberAccess(Identifier(p).x) = MemberAccess(Identifier(p).y)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_096():
    source = """
int sum(int a, int b) {
    return a + b;
}
"""
    expected = "Program([FuncDecl(IntType(), sum, [Param(IntType(), a), Param(IntType(), b)], [ReturnStmt(return BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_097():
    source = """
void main() {
    if (x) {
        while (y) z++;
    } else {
        return;
    }
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [IfStmt(if Identifier(x) then BlockStmt([WhileStmt(while Identifier(y) do ExprStmt(PostfixOp(Identifier(z)++)))]), else BlockStmt([ReturnStmt(return)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_098():
    source = """
void main() {
    for (int i = 0; i < 10; i++) {
        if (i == 5) break;
    }
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [ForStmt(for VarDecl(IntType(), i = IntLiteral(0)); BinaryOp(Identifier(i), <, IntLiteral(10)); PostfixOp(Identifier(i)++) do BlockStmt([IfStmt(if BinaryOp(Identifier(i), ==, IntLiteral(5)) then BreakStmt())]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_099():
    source = """
void main() {
    switch (x) {
        case 1:
            y = 2;
        default:
            return;
    }
}
"""
    expected = "Program([FuncDecl(VoidType(), main, [], [SwitchStmt(switch Identifier(x) cases [CaseStmt(case IntLiteral(1): [ExprStmt(AssignExpr(Identifier(y) = IntLiteral(2)))])], default DefaultStmt(default: [ReturnStmt(return)]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_100():
    source = """
struct S { int a; };
S make(int x) {
    return {x};
}
"""
    expected = "Program([StructDecl(S, [MemberDecl(IntType(), a)]), FuncDecl(StructType(S), make, [Param(IntType(), x)], [ReturnStmt(return StructLiteral({Identifier(x)}))])])"
    assert str(ASTGenerator(source).generate()) == expected