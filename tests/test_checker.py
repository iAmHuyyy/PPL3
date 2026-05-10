from tests.utils import Checker
from src.utils.nodes import (
    Program,
    FuncDecl,
    BlockStmt,
    VarDecl,
    AssignExpr,
    ExprStmt,
    IntType,
    FloatType,
    StringType,
    VoidType,
    StructType,
    IntLiteral,
    FloatLiteral,
    StringLiteral,
    Identifier,
    BinaryOp,
    MemberAccess,
    FuncCall,
    StructDecl,
    MemberDecl,
    Param,
    ReturnStmt,
)


def assert_success(source: str):
    assert Checker(source).check_from_source() == "Static checking passed"

def assert_kind(source: str, prefix: str):
    result = Checker(source).check_from_source()
    assert result.startswith(prefix), f"Expected {prefix} but got {result}"

# ============================================================================
# 001 - 015: Valid Programs
# ============================================================================
def test_001_valid_basic():
    source = "void main() { int x = 5; int y = x + 1; }"
    assert_success(source)

def test_002_valid_auto():
    source = "void main() { auto x = 10; auto y = 3.14; auto z = x + y; }"
    assert_success(source)

def test_003_valid_func_call():
    source = "int add(int x, int y) { return x + y; } void main() { int sum = add(5, 3); }"
    assert_success(source)

def test_004_valid_struct():
    source = "struct Point { int x; int y; }; void main() { Point p; p.x = 10; }"
    assert_success(source)

def test_005_valid_global_var():
    source = "void main() { int g; g = 10; }"
    assert_success(source)

def test_006_valid_float_strict():
    source = "void main() { float f = 1.5; f = f * 2.0; }"
    assert_success(source)

def test_007_valid_recursion():
    source = "int f(int n) { if(n<1) return 1; return n * f(n-1); } void main(){}"
    assert_success(source)

def test_008_valid_while_loop():
    source = "void main() { int i = 0; while(i < 10) { i = i + 1; } }"
    assert_success(source)

def test_009_valid_for_loop():
    source = "void main() { int i; for(i=0; i<10; i++) { printInt(i); } }"
    assert_success(source)

def test_010_valid_switch_default():
    source = "void main() { int x = 1; switch(x) { case 1: break; default: break; } }"
    assert_success(source)

def test_011_valid_struct_literal():
    source = "struct S { int x; float y; }; void main() { S s = {10, 2.5}; }"
    assert_success(source)

def test_012_valid_string():
    source = "void main() { string s = \"TyC\"; printString(s); }"
    assert_success(source)

def test_013_valid_inc_dec():
    source = "void main() { int x = 0; x++; --x; }"
    assert_success(source)

def test_014_valid_scope_shadowing():
    source = "void main() { int x; { float x = 1.1; } }"
    assert_success(source)

def test_015_valid_complex_expression():
    source = "void main() { float res = (1.0 + 2.0) * 3.5 / 0.5; }"
    assert_success(source)

# ============================================================================
# 016 - 030: Redeclared Errors
# ============================================================================
def test_016_redeclared_var():
    source = "void main() { int x; float x; }"
    assert_kind(source, "Redeclared(Variable, x)")

def test_017_redeclared_func():
    source = "void f(){} void f(int x){} void main(){}"
    assert_kind(source, "Redeclared(Function, f)")

def test_018_redeclared_struct():
    source = "struct S{int a;}; struct S{int b;}; void main(){}"
    assert_kind(source, "Redeclared(Struct, S)")

def test_019_redeclared_param():
    source = "void f(int a, float a){} void main(){}"
    assert_kind(source, "Redeclared(Parameter, a)")

def test_020_redeclared_member():
    source = "struct S{int x; int x;}; void main(){}"
    assert_kind(source, "Redeclared(Member, x)")

def test_021_redeclared_global_vs_func():
    source = "void f(){} int f(){ return 1; } void main(){}"
    assert_kind(source, "Redeclared(Function, f)")

def test_022_redeclared_local_vs_param():
    source = "void f(int a){ int a; } void main(){}"
    assert_kind(source, "Redeclared(Variable, a)")

def test_023_redeclared_in_block():
    source = "void main() { { int x; int x; } }"
    assert_kind(source, "Redeclared(Variable, x)")

def test_024_redeclared_struct_name_as_var():
    source = "struct S {int x;}; void main(){ int S; float S; }"
    assert_kind(source, "Redeclared(Variable, S)")

def test_025_redeclared_built_in():
    source = "void printInt(int x){} void main(){}"
    assert_kind(source, "Redeclared(Function, printInt)")

def test_026_redeclared_auto_var():
    source = "void main() { auto x = 1; int x = 2; }"
    assert_kind(source, "Redeclared(Variable, x)")

def test_027_redeclared_switch_case_var():
    source = "void main() { switch(1){ case 1: int a; int a; } }"
    assert_kind(source, "Redeclared(Variable, a)")

def test_028_redeclared_global():
    source = "void main(){ int g; float g; }"
    assert_kind(source, "Redeclared(Variable, g)")

def test_029_redeclared_nested_block():
    source = "void main() { int x; { int y; int y; } }"
    assert_kind(source, "Redeclared(Variable, y)")

def test_030_redeclared_member_complex():
    source = "struct A { int x; }; struct B { int x; A x; }; void main(){}"
    assert_kind(source, "Redeclared(Member, x)")

# ============================================================================
# 031 - 050: Undeclared Errors
# ============================================================================
def test_031_undeclared_var():
    source = "void main() { x = 10; }"
    assert_kind(source, "UndeclaredIdentifier(x)")

def test_032_undeclared_func():
    source = "void main() { unknown_func(); }"
    assert_kind(source, "UndeclaredFunction(unknown_func)")

def test_033_undeclared_struct():
    source = "void main() { MyStruct s; }"
    assert_kind(source, "UndeclaredStruct(MyStruct)")

def test_034_undeclared_member():
    source = "struct S{int a;}; void main(){ S s; s.b = 1; }"
    assert_kind(source, "TypeMismatchInExpression(MemberAccess(")

def test_035_undeclared_in_expr():
    source = "void main(){ int y = 1 + z; }"
    assert_kind(source, "UndeclaredIdentifier(z)")

def test_036_undeclared_global_type():
    source = "void main(){ Unknown g; }"
    assert_kind(source, "UndeclaredStruct(Unknown)")

def test_037_undeclared_func_in_call():
    source = "void main() { int x = 1 + getVal(); }"
    assert_kind(source, "UndeclaredFunction(getVal)")

def test_038_undeclared_struct_in_param():
    source = "void f(Data d){} void main(){}"
    assert_kind(source, "UndeclaredStruct(Data)")

def test_039_undeclared_in_for_init():
    source = "void main() { for(i=0; i<10; i++){} }"
    assert_kind(source, "UndeclaredIdentifier(i)")

def test_040_undeclared_in_switch():
    source = "void main() { switch(val){} }"
    assert_kind(source, "UndeclaredIdentifier(val)")

def test_041_undeclared_postfix():
    source = "void main() { count++; }"
    assert_kind(source, "UndeclaredIdentifier(count)")

def test_042_undeclared_unary():
    source = "void main() { int x = -y; }"
    assert_kind(source, "UndeclaredIdentifier(y)")

def test_043_undeclared_in_struct_literal():
    source = "struct S{int x;}; void main(){ S s = {y}; }"
    assert_kind(source, "UndeclaredIdentifier(y)")

def test_044_undeclared_out_of_scope():
    source = "void main() { { int x = 1; } int y = x; }"
    assert_kind(source, "UndeclaredIdentifier(x)")

def test_045_undeclared_in_while():
    source = "void main() { while(active){} }"
    assert_kind(source, "UndeclaredIdentifier(active)")

def test_046_undeclared_recursive_member():
    source = "struct S{int a;}; void main(){ S s; s.a = s.b; }"
    assert_kind(source, "TypeMismatchInExpression(MemberAccess(")

def test_047_undeclared_func_arg():
    source = "void f(int x){} void main(){ f(y); }"
    assert_kind(source, "UndeclaredIdentifier(y)")

def test_048_undeclared_return_var():
    source = "int f(){ return val; } void main(){}"
    assert_kind(source, "UndeclaredIdentifier(val)")

def test_049_undeclared_member_chain():
    source = "struct A{int x;}; struct B{A a;}; void main(){ B b; b.a.z = 1; }"
    assert_kind(source, "TypeMismatchInExpression(MemberAccess(")

def test_050_undeclared_in_if_cond():
    source = "void main(){ if(cond){} }"
    assert_kind(source, "UndeclaredIdentifier(cond)")

# ============================================================================
# 051 - 065: Type Mismatch
# ============================================================================
def test_051_mismatch_assign():
    source = "void main() { int x = \"str\"; }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_052_mismatch_if_cond():
    source = "void main() { if(1.5) {} }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_053_mismatch_while_cond():
    source = "void main() { while(\"true\") {} }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_054_mismatch_return_type():
    source = "int f() { return 1.5; } void main(){}"
    assert_kind(source, "TypeMismatchInStatement(")

def test_055_mismatch_binary_op():
    source = "void main() { int x = 5 + \"hi\"; }"
    assert_kind(source, "TypeMismatchInExpression(")

def test_056_mismatch_unary_not():
    source = "void main() { if(!1.5) {} }"
    assert_kind(source, "TypeMismatchInExpression(")

def test_057_mismatch_func_args_count():
    source = "void f(int x){} void main(){ f(1, 2); }"
    assert_kind(source, "TypeMismatchInExpression(")

def test_058_mismatch_func_args_type():
    source = "void f(int x){} void main(){ f(1.5); }"
    assert_kind(source, "TypeMismatchInExpression(")

def test_059_mismatch_member_access_non_struct():
    source = "void main(){ int x; x.y = 10; }"
    assert_kind(source, "TypeMismatchInExpression(")

def test_060_mismatch_struct_literal_size():
    source = "struct S{int a; int b;}; void main(){ S s = {1}; }"
    assert_kind(source, "TypeMismatchInExpression(")

def test_061_mismatch_struct_literal_type():
    source = "struct S{int a;}; void main(){ S s = {1.5}; }"
    assert_kind(source, "TypeMismatchInExpression(")

def test_062_mismatch_for_cond():
    source = "void main() { for(; \"err\"; ){} }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_063_mismatch_switch_expr():
    source = "void main() { switch(1.1) { case 1: break; } }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_064_mismatch_case_constant():
    source = "void main() { switch(1) { case \"1\": break; } }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_065_mismatch_void_assignment():
    source = "void f(){} void main(){ int x = f(); }"
    assert_kind(source, "TypeMismatchInStatement(")

# ============================================================================
# 066 - 080: Type Inference (auto)
# ============================================================================
def test_066_auto_no_init():
    source = "void main() { auto x; }"
    assert_kind(source, "TypeCannotBeInferred(")

def test_067_auto_from_literal():
    source = "void main() { auto x = 10; x = \"err\"; }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_068_auto_circular_dependency():
    source = "void main() { auto x = x; }"
    assert_kind(source, "UndeclaredIdentifier(x)")

def test_069_auto_from_call():
    source = "float f(){ return 1.0; } void main(){ auto x = f(); x = 1; }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_070_auto_complex_chain():
    source = "void main(){ auto a = 1.0; auto b = a; int c = b; }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_071_auto_struct_member():
    source = "struct S{int x;}; void main(){ S s; auto m = s.x; m = 1.1; }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_072_auto_switch_expr():
    source = "void main(){ auto x = 1; switch(x){ case 1: break; } }"
    assert_success(source)

def test_073_auto_assignment_infer():
    source = "void main(){ auto x; x = 5; }"
    assert_success(source)

def test_074_auto_multi_inference():
    source = "void main(){ auto x = 1; auto y = 2; auto z = x + y; }"
    assert_success(source)

def test_075_auto_in_for_loop():
    source = "void main(){ for(auto i=0; i<10; i++){} }"
    assert_success(source)

def test_076_auto_mismatch_in_block():
    source = "void main(){ auto x = 1; { x = 1.1; } }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_077_auto_return_inference():
    source = "void main(){ auto x = 1 + 2.5; float y = x; }"
    assert_success(source)

def test_078_auto_param_fail():
    source = "void main() { auto x; }"
    assert_kind(source, "TypeCannotBeInferred(")

def test_079_auto_struct_member_fail():
    source = "void main() { auto x = 1; x = \"string\"; }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_080_auto_assign_void_call():
    source = "void f(){} void main(){ auto x = f(); }"
    assert_success(source)

# ============================================================================
# 081 - 090: Loop Constraints (MustInLoop)
# ============================================================================
def test_081_break_outside():
    source = "void main() { break; }"
    assert_kind(source, "MustInLoop(")

def test_082_continue_outside():
    source = "void main() { continue; }"
    assert_kind(source, "MustInLoop(")

def test_083_continue_in_switch():
    source = "void main() { switch(1){ case 1: continue; } }"
    assert_kind(source, "MustInLoop(")

def test_084_break_in_if_outside_loop():
    source = "void main() { if(1){ break; } }"
    assert_kind(source, "MustInLoop(")

def test_085_valid_break_nested():
    source = "void main(){ while(1){ if(1){ break; } } }"
    assert_success(source)

def test_086_break_in_for_loop():
    source = "void main(){ for(int i=0; i<5; i++){ break; } }"
    assert_success(source)

def test_087_continue_in_while():
    source = "void main(){ while(1){ continue; } }"
    assert_success(source)

def test_088_break_deeply_nested():
    source = "void main(){ while(1){ switch(1){ case 1: { if(1){ break; } } } } }"
    assert_success(source)

def test_089_continue_outside_but_in_func():
    source = "void f(){ continue; } void main(){ while(1){ f(); } }"
    assert_kind(source, "MustInLoop(")

def test_090_break_in_main_after_loop():
    source = "void main(){ while(1){} break; }"
    assert_kind(source, "MustInLoop(")

# ============================================================================
# 091 - 100: Edge Cases
# ============================================================================
def test_091_main_signature_mismatch():
    source = "void main() { int main; main = 1; }" 
    assert_success(source)

def test_092_struct_circular_dependency():
    source = "struct A { B b; }; struct B { int x; }; void main(){}"
    assert_kind(source, "UndeclaredStruct(B)")

def test_093_strict_float_math():
    source = "void main() { float f = 1.0 + 2; }"
    assert_success(source)

def test_094_empty_program():
    source = ""
    assert_success(source)

def test_095_void_parameter():
    source = "void main() { int x; x = printInt(1); }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_096_assign_expr_type():
    source = "void main(){ int x; float y; x = y = 1.0; }"
    assert_kind(source, "TypeMismatchInStatement(")

def test_097_logical_op_strict():
    source = "void main(){ if(1 && 0){} }"
    assert_success(source)

def test_098_struct_member_as_arg():
    source = "struct S{int x;}; void f(int a){} void main(){ S s; f(s.x); }"
    assert_success(source)

def test_099_multiple_errors_first_one():
    source = "void main(){ break; unknown(); }"
    assert_kind(source, "MustInLoop(")

def test_100_valid_final():
    source = """
    struct Config { int id; float ratio; };
    void main() {
        int g_count;
        Config c = {1, 0.5};
        auto x = c.ratio;
        g_count = 0;
        while(g_count < 10) {
            g_count = g_count + 1;
            if(g_count == 5) break;
        }
    }
    """
    assert_success(source)