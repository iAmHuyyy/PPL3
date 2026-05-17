"""
100 explicit test cases for TyC code generation.
"""
from src.utils.nodes import *
from tests.utils import CodeGenerator

def assert_codegen(ast, expected):
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected, f"Expected {expected!r}, got {result!r}"


def test_001():
    """001_hello"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printString', [StringLiteral('Hello World')]))]))])
    expected = 'Hello World'
    assert_codegen(ast, expected)


def test_002():
    """002_int"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [IntLiteral(42)]))]))])
    expected = '42'
    assert_codegen(ast, expected)


def test_003():
    """003_float"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [FloatLiteral(3.14)]))]))])
    expected = '3.14'
    assert_codegen(ast, expected)


def test_004():
    """004_var"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'x', IntLiteral(10)), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '10'
    assert_codegen(ast, expected)


def test_005():
    """005_add"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(5), '+', IntLiteral(3))]))]))])
    expected = '8'
    assert_codegen(ast, expected)


def test_006():
    """006_mul"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(6), '*', IntLiteral(7))]))]))])
    expected = '42'
    assert_codegen(ast, expected)


def test_007():
    """007_if"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([IfStmt(BinaryOp(IntLiteral(1), '<', IntLiteral(2)), ExprStmt(FuncCall('printString', [StringLiteral('yes')])), ExprStmt(FuncCall('printString', [StringLiteral('no')])))]))])
    expected = 'yes'
    assert_codegen(ast, expected)


def test_008():
    """008_while"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'i', IntLiteral(0)), WhileStmt(BinaryOp(Identifier('i'), '<', IntLiteral(3)), BlockStmt([ExprStmt(FuncCall('printInt', [Identifier('i')])), ExprStmt(AssignExpr(Identifier('i'), BinaryOp(Identifier('i'), '+', IntLiteral(1))))]))]))])
    expected = '012'
    assert_codegen(ast, expected)


def test_009():
    """009_func_call"""
    ast = Program([FuncDecl(IntType(), 'add', [Param(IntType(), 'a'), Param(IntType(), 'b')], BlockStmt([ReturnStmt(BinaryOp(Identifier('a'), '+', Identifier('b')))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [FuncCall('add', [IntLiteral(20), IntLiteral(22)])]))]))])
    expected = '42'
    assert_codegen(ast, expected)


def test_010():
    """010_two_vars"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'x', IntLiteral(10)), VarDecl(IntType(), 'y', IntLiteral(20)), ExprStmt(FuncCall('printInt', [BinaryOp(Identifier('x'), '+', Identifier('y'))]))]))])
    expected = '30'
    assert_codegen(ast, expected)


def test_011():
    """011_sub"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(9), '-', IntLiteral(4))]))]))])
    expected = '5'
    assert_codegen(ast, expected)


def test_012():
    """012_div"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(20), '/', IntLiteral(5))]))]))])
    expected = '4'
    assert_codegen(ast, expected)


def test_013():
    """013_mod"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(20), '%', IntLiteral(6))]))]))])
    expected = '2'
    assert_codegen(ast, expected)


def test_014():
    """014_nested1"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(BinaryOp(IntLiteral(1), '+', IntLiteral(2)), '*', IntLiteral(3))]))]))])
    expected = '9'
    assert_codegen(ast, expected)


def test_015():
    """015_nested2"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(1), '+', BinaryOp(IntLiteral(2), '*', IntLiteral(3)))]))]))])
    expected = '7'
    assert_codegen(ast, expected)


def test_016():
    """016_neg"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [PrefixOp('-', IntLiteral(7))]))]))])
    expected = '-7'
    assert_codegen(ast, expected)


def test_017():
    """017_plus"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [PrefixOp('+', IntLiteral(7))]))]))])
    expected = '7'
    assert_codegen(ast, expected)


def test_018():
    """018_lt_true"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(1), '<', IntLiteral(2))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_019():
    """019_lt_false"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(2), '<', IntLiteral(1))]))]))])
    expected = '0'
    assert_codegen(ast, expected)


def test_020():
    """020_le_true"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(2), '<=', IntLiteral(2))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_021():
    """021_gt_true"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(3), '>', IntLiteral(2))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_022():
    """022_ge_false"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(1), '>=', IntLiteral(2))]))]))])
    expected = '0'
    assert_codegen(ast, expected)


def test_023():
    """023_eq_true"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(5), '==', IntLiteral(5))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_024():
    """024_eq_false"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(5), '==', IntLiteral(6))]))]))])
    expected = '0'
    assert_codegen(ast, expected)


def test_025():
    """025_neq_true"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(5), '!=', IntLiteral(6))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_026():
    """026_neq_false"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(5), '!=', IntLiteral(5))]))]))])
    expected = '0'
    assert_codegen(ast, expected)


def test_027():
    """027_combo1"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(BinaryOp(IntLiteral(8), '/', IntLiteral(2)), '+', BinaryOp(IntLiteral(3), '*', IntLiteral(4)))]))]))])
    expected = '16'
    assert_codegen(ast, expected)


def test_028():
    """028_combo2"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(BinaryOp(IntLiteral(10), '%', IntLiteral(4)), '+', BinaryOp(IntLiteral(9), '-', IntLiteral(3)))]))]))])
    expected = '8'
    assert_codegen(ast, expected)


def test_029():
    """029_combo3"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(BinaryOp(IntLiteral(1), '<', IntLiteral(2)), '+', BinaryOp(IntLiteral(3), '>', IntLiteral(4)))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_030():
    """030_combo4"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(BinaryOp(IntLiteral(7), '!=', IntLiteral(8)), '*', IntLiteral(9))]))]))])
    expected = '9'
    assert_codegen(ast, expected)


def test_031():
    """031_float_lit"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [FloatLiteral(1.5)]))]))])
    expected = '1.5'
    assert_codegen(ast, expected)


def test_032():
    """032_float_add"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [BinaryOp(FloatLiteral(1.5), '+', FloatLiteral(2.5))]))]))])
    expected = '4.0'
    assert_codegen(ast, expected)


def test_033():
    """033_float_sub"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [BinaryOp(FloatLiteral(5.5), '-', FloatLiteral(2.5))]))]))])
    expected = '3.0'
    assert_codegen(ast, expected)


def test_034():
    """034_float_mul"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [BinaryOp(FloatLiteral(2.0), '*', FloatLiteral(3.5))]))]))])
    expected = '7.0'
    assert_codegen(ast, expected)


def test_035():
    """035_float_div"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [BinaryOp(FloatLiteral(7.0), '/', FloatLiteral(2.0))]))]))])
    expected = '3.5'
    assert_codegen(ast, expected)


def test_036():
    """036_int_float_add"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [BinaryOp(IntLiteral(2), '+', FloatLiteral(3.0))]))]))])
    expected = '5.0'
    assert_codegen(ast, expected)


def test_037():
    """037_float_int_mul"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [BinaryOp(FloatLiteral(3.0), '*', IntLiteral(4))]))]))])
    expected = '12.0'
    assert_codegen(ast, expected)


def test_038():
    """038_float_neg"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [PrefixOp('-', FloatLiteral(2.5))]))]))])
    expected = '-2.5'
    assert_codegen(ast, expected)


def test_039():
    """039_float_rel"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(FloatLiteral(1.5), '<', FloatLiteral(2.0))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_040():
    """040_mixed_rel"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(2), '<=', FloatLiteral(2.0))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_041():
    """041_and_true"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(2), '&&', IntLiteral(3))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_042():
    """042_and_false"""
    ast = Program([FuncDecl(IntType(), 'side', [], BlockStmt([ExprStmt(FuncCall('printInt', [IntLiteral(9)])), ReturnStmt(IntLiteral(1))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(0), '&&', FuncCall('side', []))]))]))])
    expected = '0'
    assert_codegen(ast, expected)


def test_043():
    """043_or_true"""
    ast = Program([FuncDecl(IntType(), 'side', [], BlockStmt([ExprStmt(FuncCall('printInt', [IntLiteral(9)])), ReturnStmt(IntLiteral(1))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(5), '||', FuncCall('side', []))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_044():
    """044_or_false"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(IntLiteral(0), '||', IntLiteral(0))]))]))])
    expected = '0'
    assert_codegen(ast, expected)


def test_045():
    """045_not_zero"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [PrefixOp('!', IntLiteral(0))]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_046():
    """046_not_nonzero"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [PrefixOp('!', PrefixOp('-', IntLiteral(1)))]))]))])
    expected = '0'
    assert_codegen(ast, expected)


def test_047():
    """047_assign_expr"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'x'), ExprStmt(FuncCall('printInt', [AssignExpr(Identifier('x'), IntLiteral(12))])), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '1212'
    assert_codegen(ast, expected)


def test_048():
    """048_post_inc"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'x', IntLiteral(1)), ExprStmt(FuncCall('printInt', [PostfixOp('++', Identifier('x'))])), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '12'
    assert_codegen(ast, expected)


def test_049():
    """049_pre_inc"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'x', IntLiteral(1)), ExprStmt(FuncCall('printInt', [PrefixOp('++', Identifier('x'))])), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '22'
    assert_codegen(ast, expected)


def test_050():
    """050_pre_dec"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'x', IntLiteral(3)), ExprStmt(FuncCall('printInt', [PrefixOp('--', Identifier('x'))])), ExprStmt(FuncCall('printInt', [PostfixOp('--', Identifier('x'))])), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '221'
    assert_codegen(ast, expected)


def test_051():
    """051_if_no_else_true"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([IfStmt(IntLiteral(1), ExprStmt(FuncCall('printString', [StringLiteral('T')]))), ExprStmt(FuncCall('printString', [StringLiteral('E')]))]))])
    expected = 'TE'
    assert_codegen(ast, expected)


def test_052():
    """052_if_no_else_false"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([IfStmt(IntLiteral(0), ExprStmt(FuncCall('printString', [StringLiteral('T')]))), ExprStmt(FuncCall('printString', [StringLiteral('E')]))]))])
    expected = 'E'
    assert_codegen(ast, expected)


def test_053():
    """053_nested_if"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([IfStmt(IntLiteral(1), IfStmt(IntLiteral(0), ExprStmt(FuncCall('printString', [StringLiteral('A')])), ExprStmt(FuncCall('printString', [StringLiteral('B')]))), ExprStmt(FuncCall('printString', [StringLiteral('C')])))]))])
    expected = 'B'
    assert_codegen(ast, expected)


def test_054():
    """054_while_break"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'i', IntLiteral(0)), WhileStmt(IntLiteral(1), BlockStmt([IfStmt(BinaryOp(Identifier('i'), '==', IntLiteral(3)), BreakStmt()), ExprStmt(FuncCall('printInt', [Identifier('i')])), ExprStmt(PrefixOp('++', Identifier('i')))]))]))])
    expected = '012'
    assert_codegen(ast, expected)


def test_055():
    """055_while_continue"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'i', IntLiteral(0)), WhileStmt(BinaryOp(Identifier('i'), '<', IntLiteral(5)), BlockStmt([ExprStmt(PrefixOp('++', Identifier('i'))), IfStmt(BinaryOp(BinaryOp(Identifier('i'), '%', IntLiteral(2)), '==', IntLiteral(0)), ContinueStmt()), ExprStmt(FuncCall('printInt', [Identifier('i')]))]))]))])
    expected = '135'
    assert_codegen(ast, expected)


def test_056():
    """056_for_vardecl"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(4)), PostfixOp('++', Identifier('i')), ExprStmt(FuncCall('printInt', [Identifier('i')])))]))])
    expected = '0123'
    assert_codegen(ast, expected)


def test_057():
    """057_for_assign_init"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'i'), ForStmt(ExprStmt(AssignExpr(Identifier('i'), IntLiteral(1))), BinaryOp(Identifier('i'), '<=', IntLiteral(3)), AssignExpr(Identifier('i'), BinaryOp(Identifier('i'), '+', IntLiteral(1))), ExprStmt(FuncCall('printInt', [Identifier('i')])))]))])
    expected = '123'
    assert_codegen(ast, expected)


def test_058():
    """058_for_break"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), IntLiteral(1), PostfixOp('++', Identifier('i')), BlockStmt([IfStmt(BinaryOp(Identifier('i'), '==', IntLiteral(3)), BreakStmt()), ExprStmt(FuncCall('printInt', [Identifier('i')]))]))]))])
    expected = '012'
    assert_codegen(ast, expected)


def test_059():
    """059_block_shadow"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'x', IntLiteral(1)), BlockStmt([VarDecl(IntType(), 'x', IntLiteral(2)), ExprStmt(FuncCall('printInt', [Identifier('x')]))]), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '21'
    assert_codegen(ast, expected)


def test_060():
    """060_empty_block"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([BlockStmt([]), ExprStmt(FuncCall('printString', [StringLiteral('ok')]))]))])
    expected = 'ok'
    assert_codegen(ast, expected)


def test_061():
    """061_switch_case1"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([SwitchStmt(IntLiteral(1), [CaseStmt(IntLiteral(1), [ExprStmt(FuncCall('printString', [StringLiteral('A')])), BreakStmt()]), CaseStmt(IntLiteral(2), [ExprStmt(FuncCall('printString', [StringLiteral('B')])), BreakStmt()])])]))])
    expected = 'A'
    assert_codegen(ast, expected)


def test_062():
    """062_switch_default"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([SwitchStmt(IntLiteral(3), [CaseStmt(IntLiteral(1), [ExprStmt(FuncCall('printString', [StringLiteral('A')])), BreakStmt()])], DefaultStmt([ExprStmt(FuncCall('printString', [StringLiteral('D')]))]))]))])
    expected = 'D'
    assert_codegen(ast, expected)


def test_063():
    """063_switch_fallthrough"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([SwitchStmt(IntLiteral(1), [CaseStmt(IntLiteral(1), [ExprStmt(FuncCall('printString', [StringLiteral('A')]))]), CaseStmt(IntLiteral(2), [ExprStmt(FuncCall('printString', [StringLiteral('B')])), BreakStmt()])], DefaultStmt([ExprStmt(FuncCall('printString', [StringLiteral('D')]))]))]))])
    expected = 'AB'
    assert_codegen(ast, expected)


def test_064():
    """064_switch_expr_case"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([SwitchStmt(IntLiteral(3), [CaseStmt(BinaryOp(IntLiteral(1), '+', IntLiteral(2)), [ExprStmt(FuncCall('printString', [StringLiteral('C')])), BreakStmt()])], DefaultStmt([ExprStmt(FuncCall('printString', [StringLiteral('D')]))]))]))])
    expected = 'C'
    assert_codegen(ast, expected)


def test_065():
    """065_nested_loop_switch_break"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([ForStmt(VarDecl(IntType(), 'i', IntLiteral(0)), BinaryOp(Identifier('i'), '<', IntLiteral(2)), PostfixOp('++', Identifier('i')), BlockStmt([SwitchStmt(IntLiteral(1), [CaseStmt(IntLiteral(1), [BreakStmt()])]), ExprStmt(FuncCall('printInt', [Identifier('i')]))]))]))])
    expected = '01'
    assert_codegen(ast, expected)


def test_066():
    """066_void_func"""
    ast = Program([FuncDecl(VoidType(), 'hello', [], BlockStmt([ExprStmt(FuncCall('printString', [StringLiteral('H')]))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('hello', [])), ExprStmt(FuncCall('printString', [StringLiteral('!')]))]))])
    expected = 'H!'
    assert_codegen(ast, expected)


def test_067():
    """067_float_func"""
    ast = Program([FuncDecl(FloatType(), 'avg', [Param(FloatType(), 'a'), Param(FloatType(), 'b')], BlockStmt([ReturnStmt(BinaryOp(BinaryOp(Identifier('a'), '+', Identifier('b')), '/', FloatLiteral(2.0)))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printFloat', [FuncCall('avg', [FloatLiteral(2.0), FloatLiteral(4.0)])]))]))])
    expected = '3.0'
    assert_codegen(ast, expected)


def test_068():
    """068_string_func"""
    ast = Program([FuncDecl(StringType(), 'id', [Param(StringType(), 's')], BlockStmt([ReturnStmt(Identifier('s'))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printString', [FuncCall('id', [StringLiteral('abc')])]))]))])
    expected = 'abc'
    assert_codegen(ast, expected)


def test_069():
    """069_recursive_fact"""
    ast = Program([FuncDecl(IntType(), 'fact', [Param(IntType(), 'n')], BlockStmt([IfStmt(BinaryOp(Identifier('n'), '<=', IntLiteral(1)), ReturnStmt(IntLiteral(1))), ReturnStmt(BinaryOp(Identifier('n'), '*', FuncCall('fact', [BinaryOp(Identifier('n'), '-', IntLiteral(1))])))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [FuncCall('fact', [IntLiteral(5)])]))]))])
    expected = '120'
    assert_codegen(ast, expected)


def test_070():
    """070_many_params"""
    ast = Program([FuncDecl(IntType(), 'sum4', [Param(IntType(), 'a'), Param(IntType(), 'b'), Param(IntType(), 'c'), Param(IntType(), 'd')], BlockStmt([ReturnStmt(BinaryOp(BinaryOp(Identifier('a'), '+', Identifier('b')), '+', BinaryOp(Identifier('c'), '+', Identifier('d'))))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [FuncCall('sum4', [IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4)])]))]))])
    expected = '10'
    assert_codegen(ast, expected)


def test_071():
    """071_auto_init_int"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(None, 'x', IntLiteral(7)), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '7'
    assert_codegen(ast, expected)


def test_072():
    """072_auto_init_float"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(None, 'x', FloatLiteral(2.5)), ExprStmt(FuncCall('printFloat', [Identifier('x')]))]))])
    expected = '2.5'
    assert_codegen(ast, expected)


def test_073():
    """073_auto_init_string"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(None, 's', StringLiteral('auto')), ExprStmt(FuncCall('printString', [Identifier('s')]))]))])
    expected = 'auto'
    assert_codegen(ast, expected)


def test_074():
    """074_auto_no_init_assign"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(None, 'x'), ExprStmt(AssignExpr(Identifier('x'), IntLiteral(9))), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '9'
    assert_codegen(ast, expected)


def test_075():
    """075_auto_no_init_arg"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(None, 'x'), ExprStmt(AssignExpr(Identifier('x'), IntLiteral(4))), ExprStmt(FuncCall('printInt', [Identifier('x')]))]))])
    expected = '4'
    assert_codegen(ast, expected)


def test_076():
    """076_chain_assign"""
    ast = Program([FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(IntType(), 'a'), VarDecl(IntType(), 'b'), ExprStmt(AssignExpr(Identifier('a'), AssignExpr(Identifier('b'), IntLiteral(6)))), ExprStmt(FuncCall('printInt', [Identifier('a')])), ExprStmt(FuncCall('printInt', [Identifier('b')]))]))])
    expected = '66'
    assert_codegen(ast, expected)


def test_077():
    """077_func_side_effect_order"""
    ast = Program([FuncDecl(IntType(), 'p', [Param(IntType(), 'x')], BlockStmt([ExprStmt(FuncCall('printInt', [Identifier('x')])), ReturnStmt(Identifier('x'))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [BinaryOp(FuncCall('p', [IntLiteral(1)]), '+', FuncCall('p', [IntLiteral(2)]))]))]))])
    expected = '123'
    assert_codegen(ast, expected)


def test_078():
    """078_return_assign_expr"""
    ast = Program([FuncDecl(IntType(), 'f', [], BlockStmt([VarDecl(IntType(), 'x'), ReturnStmt(AssignExpr(Identifier('x'), IntLiteral(8)))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [FuncCall('f', [])]))]))])
    expected = '8'
    assert_codegen(ast, expected)


def test_079():
    """079_inferred_return_int"""
    ast = Program([FuncDecl(None, 'f', [], BlockStmt([ReturnStmt(IntLiteral(11))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [FuncCall('f', [])]))]))])
    expected = '11'
    assert_codegen(ast, expected)


def test_080():
    """080_inferred_return_void"""
    ast = Program([FuncDecl(None, 'f', [], BlockStmt([ExprStmt(FuncCall('printString', [StringLiteral('v')])), ReturnStmt()])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('f', []))]))])
    expected = 'v'
    assert_codegen(ast, expected)


def test_081():
    """081_struct_literal_member"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(3), IntLiteral(4)])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'y')]))]))])
    expected = '34'
    assert_codegen(ast, expected)


def test_082():
    """082_struct_member_assign"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p'), ExprStmt(AssignExpr(MemberAccess(Identifier('p'), 'x'), IntLiteral(7))), ExprStmt(AssignExpr(MemberAccess(Identifier('p'), 'y'), IntLiteral(8))), ExprStmt(FuncCall('printInt', [BinaryOp(MemberAccess(Identifier('p'), 'x'), '+', MemberAccess(Identifier('p'), 'y'))]))]))])
    expected = '15'
    assert_codegen(ast, expected)


def test_083():
    """083_struct_float_string"""
    ast = Program([StructDecl('Pair', [MemberDecl(FloatType(), 'a'), MemberDecl(StringType(), 'b')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Pair'), 'p', StructLiteral([FloatLiteral(1.5), StringLiteral('s')])), ExprStmt(FuncCall('printFloat', [MemberAccess(Identifier('p'), 'a')])), ExprStmt(FuncCall('printString', [MemberAccess(Identifier('p'), 'b')]))]))])
    expected = '1.5s'
    assert_codegen(ast, expected)


def test_084():
    """084_struct_assign_copy"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(1), IntLiteral(2)])), VarDecl(StructType('Point'), 'q'), ExprStmt(AssignExpr(Identifier('q'), Identifier('p'))), ExprStmt(AssignExpr(MemberAccess(Identifier('q'), 'x'), IntLiteral(9))), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('q'), 'x')]))]))])
    expected = '19'
    assert_codegen(ast, expected)


def test_085():
    """085_struct_auto_copy"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(5), IntLiteral(6)])), VarDecl(None, 'q', Identifier('p')), ExprStmt(AssignExpr(MemberAccess(Identifier('q'), 'y'), IntLiteral(1))), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'y')])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('q'), 'y')]))]))])
    expected = '61'
    assert_codegen(ast, expected)


def test_086():
    """086_nested_struct"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), StructDecl('Wrap', [MemberDecl(StructType('Point'), 'p'), MemberDecl(IntType(), 'tag')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Wrap'), 'w', StructLiteral([StructLiteral([IntLiteral(2), IntLiteral(3)]), IntLiteral(4)])), ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('w'), 'p'), 'x')])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('w'), 'tag')]))]))])
    expected = '24'
    assert_codegen(ast, expected)


def test_087():
    """087_nested_struct_assign"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), StructDecl('Wrap', [MemberDecl(StructType('Point'), 'p'), MemberDecl(IntType(), 'tag')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Wrap'), 'w'), ExprStmt(AssignExpr(MemberAccess(Identifier('w'), 'p'), StructLiteral([IntLiteral(8), IntLiteral(9)]))), ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('w'), 'p'), 'y')]))]))])
    expected = '9'
    assert_codegen(ast, expected)


def test_088():
    """088_func_return_struct"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(StructType('Point'), 'mk', [Param(IntType(), 'x'), Param(IntType(), 'y')], BlockStmt([ReturnStmt(StructLiteral([Identifier('x'), Identifier('y')]))])), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', FuncCall('mk', [IntLiteral(4), IntLiteral(5)])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'y')]))]))])
    expected = '45'
    assert_codegen(ast, expected)


def test_089():
    """089_func_arg_struct"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(IntType(), 'sum', [Param(StructType('Point'), 'p')], BlockStmt([ReturnStmt(BinaryOp(MemberAccess(Identifier('p'), 'x'), '+', MemberAccess(Identifier('p'), 'y')))])), FuncDecl(VoidType(), 'main', [], BlockStmt([ExprStmt(FuncCall('printInt', [FuncCall('sum', [StructLiteral([IntLiteral(6), IntLiteral(7)])])]))]))])
    expected = '13'
    assert_codegen(ast, expected)


def test_090():
    """090_member_postfix"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(1), IntLiteral(0)])), ExprStmt(FuncCall('printInt', [PostfixOp('++', MemberAccess(Identifier('p'), 'x'))])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')]))]))])
    expected = '12'
    assert_codegen(ast, expected)


def test_091():
    """091_member_prefix"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(1), IntLiteral(0)])), ExprStmt(FuncCall('printInt', [PrefixOp('++', MemberAccess(Identifier('p'), 'x'))])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')]))]))])
    expected = '22'
    assert_codegen(ast, expected)


def test_092():
    """092_member_assign_expr"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p'), ExprStmt(FuncCall('printInt', [AssignExpr(MemberAccess(Identifier('p'), 'x'), IntLiteral(3))])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')]))]))])
    expected = '33'
    assert_codegen(ast, expected)


def test_093():
    """093_struct_param_copy"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'mut', [Param(StructType('Point'), 'p')], BlockStmt([ExprStmt(AssignExpr(MemberAccess(Identifier('p'), 'x'), IntLiteral(9)))])), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(1), IntLiteral(2)])), ExprStmt(FuncCall('mut', [Identifier('p')])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')]))]))])
    expected = '1'
    assert_codegen(ast, expected)


def test_094():
    """094_struct_nested_copy"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), StructDecl('Wrap', [MemberDecl(StructType('Point'), 'p'), MemberDecl(IntType(), 'tag')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Wrap'), 'a', StructLiteral([StructLiteral([IntLiteral(1), IntLiteral(2)]), IntLiteral(3)])), VarDecl(StructType('Wrap'), 'b', Identifier('a')), ExprStmt(AssignExpr(MemberAccess(MemberAccess(Identifier('b'), 'p'), 'x'), IntLiteral(9))), ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('a'), 'p'), 'x')])), ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('b'), 'p'), 'x')]))]))])
    expected = '19'
    assert_codegen(ast, expected)


def test_095():
    """095_struct_in_block"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(4), IntLiteral(4)])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')]))]), ExprStmt(FuncCall('printString', [StringLiteral('x')]))]))])
    expected = '4x'
    assert_codegen(ast, expected)


def test_096():
    """096_struct_member_float_math"""
    ast = Program([StructDecl('Pair', [MemberDecl(FloatType(), 'a'), MemberDecl(StringType(), 'b')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Pair'), 'p', StructLiteral([FloatLiteral(2.5), StringLiteral('!')])), ExprStmt(FuncCall('printFloat', [BinaryOp(MemberAccess(Identifier('p'), 'a'), '+', FloatLiteral(0.5))])), ExprStmt(FuncCall('printString', [MemberAccess(Identifier('p'), 'b')]))]))])
    expected = '3.0!'
    assert_codegen(ast, expected)


def test_097():
    """097_struct_switch_member"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(2), IntLiteral(0)])), SwitchStmt(MemberAccess(Identifier('p'), 'x'), [CaseStmt(IntLiteral(1), [ExprStmt(FuncCall('printString', [StringLiteral('A')])), BreakStmt()]), CaseStmt(IntLiteral(2), [ExprStmt(FuncCall('printString', [StringLiteral('B')])), BreakStmt()])], DefaultStmt([ExprStmt(FuncCall('printString', [StringLiteral('D')]))]))]))])
    expected = 'B'
    assert_codegen(ast, expected)


def test_098():
    """098_struct_loop_member"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(0), IntLiteral(3)])), WhileStmt(BinaryOp(MemberAccess(Identifier('p'), 'x'), '<', MemberAccess(Identifier('p'), 'y')), BlockStmt([ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('p'), 'x')])), ExprStmt(PrefixOp('++', MemberAccess(Identifier('p'), 'x')))]))]))])
    expected = '012'
    assert_codegen(ast, expected)


def test_099():
    """099_func_return_nested_struct"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), StructDecl('Wrap', [MemberDecl(StructType('Point'), 'p'), MemberDecl(IntType(), 'tag')]), FuncDecl(StructType('Wrap'), 'makeW', [], BlockStmt([ReturnStmt(StructLiteral([StructLiteral([IntLiteral(7), IntLiteral(8)]), IntLiteral(9)]))])), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Wrap'), 'w', FuncCall('makeW', [])), ExprStmt(FuncCall('printInt', [MemberAccess(MemberAccess(Identifier('w'), 'p'), 'y')])), ExprStmt(FuncCall('printInt', [MemberAccess(Identifier('w'), 'tag')]))]))])
    expected = '89'
    assert_codegen(ast, expected)


def test_100():
    """100_final_mix"""
    ast = Program([StructDecl('Point', [MemberDecl(IntType(), 'x'), MemberDecl(IntType(), 'y')]), FuncDecl(IntType(), 'sum', [Param(StructType('Point'), 'p')], BlockStmt([ReturnStmt(BinaryOp(MemberAccess(Identifier('p'), 'x'), '+', MemberAccess(Identifier('p'), 'y')))])), FuncDecl(VoidType(), 'main', [], BlockStmt([VarDecl(StructType('Point'), 'p', StructLiteral([IntLiteral(10), IntLiteral(20)])), ExprStmt(AssignExpr(MemberAccess(Identifier('p'), 'x'), BinaryOp(MemberAccess(Identifier('p'), 'x'), '+', IntLiteral(1)))), ExprStmt(FuncCall('printInt', [FuncCall('sum', [Identifier('p')])]))]))])
    expected = '31'
    assert_codegen(ast, expected)


