"""
Parser test cases for TyC compiler
Implement 100 test cases for parser
"""

import pytest
from tests.utils import Parser


def assert_error_prefix(source: str):
    res = Parser(source).parse()
    assert res.startswith("Error on line ")


def assert_error_endswith_token(source: str, token_text: str):
    res = Parser(source).parse()
    assert res.startswith("Error on line ")
    assert res.endswith(f": {token_text}")


# ========== Simple Test Cases (10 types) ==========
def test_empty_program():
    """1. Empty program"""
    assert Parser("").parse() == "success"


def test_program_with_only_main():
    """2. Program with only main function"""
    assert Parser("void main() {}").parse() == "success"


def test_struct_simple():
    """3. Struct declaration"""
    source = "struct Point { int x; int y; };"
    assert Parser(source).parse() == "success"


def test_function_no_params():
    """4. Function with no parameters"""
    source = 'void greet() { printString("Hello"); }'
    assert Parser(source).parse() == "success"


def test_var_decl_auto_with_init():
    """5. Variable declaration"""
    source = "void main() { auto x = 5; }"
    assert Parser(source).parse() == "success"


def test_if_simple():
    """6. If statement"""
    source = "void main() { if (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_while_simple():
    """7. While statement"""
    source = "void main() { while (1) printInt(1); }"
    assert Parser(source).parse() == "success"


def test_for_simple():
    """8. For statement"""
    source = "void main() { for (auto i = 0; i < 10; ++i) printInt(i); }"
    assert Parser(source).parse() == "success"


def test_switch_simple():
    """9. Switch statement"""
    source = "void main() { switch (1) { case 1: printInt(1); break; } }"
    assert Parser(source).parse() == "success"


def test_assignment_simple():
    """10. Assignment statement"""
    source = "void main() { int x; x = 5; }"
    assert Parser(source).parse() == "success"


# ========== Valid Programs / Decls ==========
def test_program_many_decls():
    """11. Many declarations"""
    src = """
    struct A { int x; };
    int f(int a) { return a; }
    void main() { auto y = f(1); }
    """
    assert Parser(src).parse() == "success"


def test_program_only_structs():
    """12. Only structs"""
    src = """
    struct Empty {};
    struct Point { int x; int y; };
    """
    assert Parser(src).parse() == "success"


def test_program_only_funcs():
    """13. Only functions"""
    src = """
    void main() { }
    int id(int x) { return x; }
    """
    assert Parser(src).parse() == "success"


def test_struct_empty_members():
    """14. Empty struct body allowed"""
    src = "struct Empty { };"
    assert Parser(src).parse() == "success"


def test_struct_many_members():
    """15. Struct many members"""
    src = "struct Person { string name; int age; float height; };"
    assert Parser(src).parse() == "success"


def test_struct_member_struct_type():
    """16. Struct member is another struct type"""
    src = """
    struct Point { int x; int y; };
    struct Line { Point a; Point b; };
    """
    assert Parser(src).parse() == "success"


def test_func_with_params():
    """17. Function with params"""
    src = "int add(int x, int y) { return x + y; }"
    assert Parser(src).parse() == "success"


def test_func_inferred_return_type():
    """18. Function inferred return type omitted"""
    src = "add(int x, int y) { return x + y; }"
    assert Parser(src).parse() == "success"


def test_func_inferred_void_return_type():
    """19. Inferred return type void (return;)"""
    src = 'greet(string name) { printString(name); return; }'
    assert Parser(src).parse() == "success"


def test_func_many_params():
    """20. Many params"""
    src = "float f(float a, float b, int c, string s) { return a + b; }"
    assert Parser(src).parse() == "success"


# ========== Valid statements ==========
def test_var_decl_auto_no_init():
    """21. auto without init"""
    src = "void main() { auto x; }"
    assert Parser(src).parse() == "success"


def test_var_decl_explicit_no_init():
    """22. explicit without init"""
    src = "void main() { int x; float y; string s; }"
    assert Parser(src).parse() == "success"


def test_var_decl_struct_type():
    """23. struct type variable"""
    src = """
    struct Point { int x; int y; };
    void main() { Point p; }
    """
    assert Parser(src).parse() == "success"


def test_var_decl_struct_init():
    """24. struct init literal"""
    src = """
    struct Point { int x; int y; };
    void main() { Point p = {1, 2}; }
    """
    assert Parser(src).parse() == "success"


def test_nested_blocks():
    """25. Nested blocks"""
    src = "void main() { { int x; { auto y = 1; } } }"
    assert Parser(src).parse() == "success"


def test_if_else_block():
    """26. if-else with blocks"""
    src = "void main() { if (1) { printInt(1); } else { printInt(0); } }"
    assert Parser(src).parse() == "success"


def test_nested_if_dangling_else():
    """27. Dangling else binds to nearest if"""
    src = "void main() { if (1) if (0) printInt(1); else printInt(2); }"
    assert Parser(src).parse() == "success"


def test_while_with_block():
    """28. while with block"""
    src = "void main() { while (1) { printInt(1); } }"
    assert Parser(src).parse() == "success"


def test_for_all_omitted_parts():
    """29. for(;;)"""
    src = "void main() { for(;;) { break; } }"
    assert Parser(src).parse() == "success"


def test_for_init_assignment():
    """30. for init as assignment expr"""
    src = "void main() { int i; for(i=0; i<10; i=i+1) printInt(i); }"
    assert Parser(src).parse() == "success"


def test_for_update_postfix():
    """31. for update i++"""
    src = "void main() { int i; for(i=0; i<10; i++) { } }"
    assert Parser(src).parse() == "success"


def test_for_cond_omitted():
    """32. for cond omitted"""
    src = "void main() { for(auto i=0;;++i) { break; } }"
    assert Parser(src).parse() == "success"


def test_switch_empty_body():
    """33. Empty switch body"""
    src = "void main() { switch(1) { } }"
    assert Parser(src).parse() == "success"


def test_switch_multiple_cases_default_end():
    """34. switch multiple cases + default at end"""
    src = """
    void main() {
        switch(2) {
            case 1: printInt(1); break;
            case 2: printInt(2); break;
            default: printInt(0); break;
        }
    }
    """
    assert Parser(src).parse() == "success"


def test_switch_default_in_middle():
    """35. default in middle"""
    src = """
    void main() {
        switch(1) {
            case 1: printInt(1); break;
            default: printInt(0); break;
            case 2: printInt(2); break;
        }
    }
    """
    assert Parser(src).parse() == "success"


def test_switch_case_empty_stmt_list():
    """36. case with empty statement list"""
    src = "void main() { switch(1){ case 1: default: } }"
    assert Parser(src).parse() == "success"


def test_break_stmt():
    """37. break statement"""
    src = "void main() { while(1) break; }"
    assert Parser(src).parse() == "success"


def test_continue_stmt():
    """38. continue statement"""
    src = "void main() { while(1) continue; }"
    assert Parser(src).parse() == "success"


def test_return_void():
    """39. return; in void"""
    src = "void main() { return; }"
    assert Parser(src).parse() == "success"


def test_return_with_expr():
    """40. return expr"""
    src = "int f() { return 1+2*3; }"
    assert Parser(src).parse() == "success"


def test_expr_stmt_call():
    """41. call as expr stmt"""
    src = 'void main() { printString("Hi"); }'
    assert Parser(src).parse() == "success"


def test_expr_stmt_assignment_chain():
    """42. assignment chain as expr stmt"""
    src = "void main() { int x; int y; int z; x = y = z = 10; }"
    assert Parser(src).parse() == "success"


def test_expr_stmt_useless_expr():
    """43. expression statement 'x+y;' allowed"""
    src = "void main() { int x; int y; x + y; }"
    assert Parser(src).parse() == "success"


# ========== Expression precedence / postfix / member / calls ==========
def test_precedence_mul_over_add():
    """44. 1 + 2*3"""
    src = "void main() { auto x = 1 + 2 * 3; }"
    assert Parser(src).parse() == "success"


def test_precedence_parens_override():
    """45. (1+2)*3"""
    src = "void main() { auto x = (1 + 2) * 3; }"
    assert Parser(src).parse() == "success"


def test_precedence_rel_eq():
    """46. 1 < 2 == 3 < 4 (syntactically allowed)"""
    src = "void main() { auto x = 1 < 2 == 3 < 4; }"
    assert Parser(src).parse() == "success"


def test_precedence_and_or():
    """47. 1 && 0 || 1"""
    src = "void main() { auto x = 1 && 0 || 1; }"
    assert Parser(src).parse() == "success"


def test_assignment_right_assoc():
    """48. x = (y = 1)"""
    src = "void main() { int x; int y; x = y = 1; }"
    assert Parser(src).parse() == "success"


def test_unary_not():
    """49. !x"""
    src = "void main() { int x; auto y = !x; }"
    assert Parser(src).parse() == "success"


def test_unary_prefix_inc_dec():
    """50. ++x; --x;"""
    src = "void main() { int x; ++x; --x; }"
    assert Parser(src).parse() == "success"


def test_postfix_inc_dec():
    """51. x++; x--;"""
    src = "void main() { int x; x++; x--; }"
    assert Parser(src).parse() == "success"


def test_mix_prefix_postfix():
    """52. ++x + y--"""
    src = "void main() { int x; int y; auto z = ++x + y--; }"
    assert Parser(src).parse() == "success"


def test_call_no_args():
    """53. readInt()"""
    src = "void main() { auto x = readInt(); }"
    assert Parser(src).parse() == "success"


def test_call_many_args():
    """54. call with many args"""
    src = "void main() { auto x = add(1,2,3,4); }"
    assert Parser(src).parse() == "success"


def test_call_nested():
    """55. nested calls"""
    src = "void main() { auto x = add(readInt(), add(1,2)); }"
    assert Parser(src).parse() == "success"


def test_member_access_in_expr():
    """56. p.x in expression"""
    src = """
    struct Point { int x; int y; };
    void main() { Point p = {1,2}; auto a = p.x + p.y; }
    """
    assert Parser(src).parse() == "success"


def test_member_access_chain():
    """57. a.b.c chain"""
    src = """
    struct C { int x; };
    struct B { C c; };
    struct A { B b; };
    void main() { A a; a.b.c.x = 1; }
    """
    assert Parser(src).parse() == "success"


def test_struct_literal_empty():
    """58. empty struct literal {}"""
    src = """
    struct Empty { };
    void main() { Empty e = {}; }
    """
    assert Parser(src).parse() == "success"


def test_struct_literal_nested():
    """59. nested struct literal {{1,2},3}"""
    src = """
    struct P2 { int x; int y; };
    struct P3 { P2 p; int z; };
    void main() { P3 p = {{1,2}, 3}; }
    """
    assert Parser(src).parse() == "success"


def test_struct_literal_in_call():
    """60. struct literal as call arg"""
    src = """
    struct P { int x; int y; };
    void foo(P p) { return; }
    void main() { foo({1,2}); }
    """
    assert Parser(src).parse() == "success"


def test_switch_case_unary_plus_minus():
    """61. case +1 and case -2"""
    src = """
    void main() {
        switch(1) {
            case +1: break;
            case -2: break;
        }
    }
    """
    assert Parser(src).parse() == "success"


def test_switch_case_paren_expr():
    """62. case (1+2)"""
    src = """
    void main() {
        switch(3) {
            case (1+2): break;
        }
    }
    """
    assert Parser(src).parse() == "success"


# ========== Parser ERROR cases (assert exact suffix token when stable) ==========
def test_struct_member_missing_semi_error():
    """63. Missing semicolon in struct member -> offending 'int' or 'y' depending on recovery, check prefix only"""
    src = "struct A { int x int y; };"
    assert_error_prefix(src)


def test_struct_missing_trailing_semi_error():
    """64. Missing trailing ';' after struct decl -> offending <EOF> or next token, prefix only"""
    src = "struct A { int x; }"
    assert_error_prefix(src)


def test_struct_missing_rbrace_error():
    """65. Missing '}' -> offending <EOF> typically"""
    src = "struct A { int x; "
    assert_error_prefix(src)


def test_func_param_missing_type_error():
    """66. Param missing type: int f(x) ... -> offending ')'"""
    src = "int f(x) { return 1; }"
    assert_error_endswith_token(src, ")")


def test_func_missing_rparen_error():
    """67. Missing ')' in function header -> offending '{'"""
    src = "void main( { }"
    assert_error_endswith_token(src, "{")


def test_func_missing_block_error():
    """68. Missing block -> offending ';'"""
    src = "void main();"
    assert_error_endswith_token(src, ";")


def test_var_decl_missing_semi_error():
    """69. Missing ';' after var decl -> offending '}'"""
    src = "void main() { int x }"
    assert_error_endswith_token(src, "}")


def test_var_decl_missing_id_error():
    """70. Missing identifier: int ; -> offending ';'"""
    src = "void main() { int ; }"
    assert_error_endswith_token(src, ";")


def test_block_missing_rbrace_error():
    """71. Missing '}' -> offending <EOF>"""
    src = "void main() { int x; "
    assert_error_prefix(src)


def test_if_missing_rparen_error():
    """72. if (1 printInt... -> offending 'printInt'"""
    src = "void main() { if (1 printInt(1); }"
    assert_error_endswith_token(src, "printInt")


def test_while_missing_lparen_error():
    """73. while 1) ... -> offending '1'"""
    src = "void main() { while 1) printInt(1); }"
    assert_error_endswith_token(src, "1")


def test_for_missing_first_semi_error():
    """74. for(auto i=0 i<10;...) -> offending 'i' (from i<10)"""
    src = "void main() { for(auto i=0 i<10; ++i) {} }"
    assert_error_prefix(src)


def test_for_missing_rparen_error():
    """75. for(... ++i { -> offending '{'"""
    src = "void main() { for(auto i=0; i<10; ++i { } }"
    assert_error_endswith_token(src, "{")


def test_switch_missing_colon_error():
    """76. case 1 printInt -> offending 'printInt'"""
    src = "void main() { switch(1){ case 1 printInt(1); } }"
    assert_error_endswith_token(src, "printInt")


def test_switch_missing_rbrace_error():
    """77. switch missing '}' -> offending <EOF>"""
    src = "void main() { switch(1){ case 1: break; }"
    assert_error_prefix(src)


def test_return_missing_semi_error():
    """78. return } -> offending '}'"""
    src = "void main() { return }"
    assert_error_endswith_token(src, "}")


def test_expr_stmt_missing_semi_error():
    """79. printInt(1) } -> offending '}'"""
    src = "void main() { printInt(1) }"
    assert_error_endswith_token(src, "}")


def test_call_missing_rparen_error():
    """80. printInt(1; -> offending ';'"""
    src = "void main() { printInt(1; }"
    assert_error_endswith_token(src, ";")


def test_member_access_missing_id_error():
    """81. p.; -> offending ';'"""
    src = """
    struct P { int x; };
    void main(){ P p; p.; }
    """
    assert_error_endswith_token(src, ";")


def test_missing_function_name_error():
    """82. void (){} -> offending '(' or ')' depending, prefix only"""
    src = "void () { }"
    assert_error_prefix(src)


def test_param_missing_identifier_error():
    """83. int f(int){...} -> offending ')'"""
    src = "int f(int) { return 1; }"
    assert_error_endswith_token(src, ")")


def test_extra_comma_in_params_error():
    """84. int f(int x, ) -> offending ')'"""
    src = "int f(int x, ) { return x; }"
    assert_error_endswith_token(src, ")")


def test_extra_comma_in_args_error():
    """85. printInt(1,) -> offending ')'"""
    src = "void main(){ printInt(1,); }"
    assert_error_endswith_token(src, ")")


def test_break_missing_semi_error():
    """86. break } -> offending '}'"""
    src = "void main(){ while(1) break }"
    assert_error_endswith_token(src, "}")


def test_continue_missing_semi_error():
    """87. continue } -> offending '}'"""
    src = "void main(){ while(1) continue }"
    assert_error_endswith_token(src, "}")


def test_invalid_top_level_statement_error():
    """88. top-level statement not allowed -> offending 'break' (at top-level)"""
    src = "break;"
    assert_error_prefix(src)


def test_extra_tokens_after_program_error():
    """89. extra tokens after program -> offending '='"""
    src = "void main(){} x = 1;"
    assert_error_endswith_token(src, "=")



def test_lonely_semi_in_block_error():
    """90. ';' alone is not a statement (per spec) -> offending ';'"""
    src = "void main(){ ; }"
    assert_error_endswith_token(src, ";")


def test_invalid_var_decl_two_ids_error():
    """91. int x y; -> offending 'y'"""
    src = "void main(){ int x y; }"
    assert_error_endswith_token(src, "y")


def test_invalid_struct_member_init_error():
    """92. struct member cannot have init -> offending '='"""
    src = "struct A { int x = 1; };"
    assert_error_endswith_token(src, "=")


def test_invalid_switch_section_random_decl_error():
    """93. int x; inside switch section not allowed by grammar -> offending 'int'"""
    src = "void main(){ switch(1){ int x; } }"
    assert_error_endswith_token(src, "int")


def test_invalid_struct_contains_block_error():
    """94. struct A { { int x; } }; -> offending '{' (inner)"""
    src = "struct A { { int x; } };"
    assert_error_prefix(src)


def test_invalid_func_missing_rbrace_error():
    """95. function missing '}' -> offending <EOF>"""
    src = "void main(){ int x; "
    assert_error_prefix(src)


def test_invalid_switch_missing_rparen_error():
    """96. switch(1 { -> offending '{'"""
    src = "void main(){ switch(1 { } }"
    assert_error_endswith_token(src, "{")


def test_invalid_for_missing_second_semi_error():
    """97. for(i=0; i<10 ++i) -> offending '++' or ')', prefix only"""
    src = "void main(){ int i; for(i=0; i<10 ++i) {} }"
    assert_error_prefix(src)


def test_invalid_if_missing_condition_error():
    """98. if () -> offending ')'"""
    src = "void main(){ if () printInt(1); }"
    assert_error_endswith_token(src, ")")


def test_invalid_return_at_top_level_error():
    """99. return; at top-level -> offending 'return'"""
    src = "return;"
    assert_error_prefix(src)


def test_big_valid_program():
    """100. Larger valid program"""
    src = """
    struct Point { int x; int y; };
    int add(int a, int b) { return a + b; }
    void main() {
        Point p = {1,2};
        auto s = add(p.x, p.y);
        if (s > 0) { printInt(s); }
        for (auto i = 0; i < 3; ++i) {
            switch(i) {
                case 0: printInt(0); break;
                case 1: printInt(1); break;
                default: printInt(9); break;
            }
        }
        return;
    }
    """
    assert Parser(src).parse() == "success"
