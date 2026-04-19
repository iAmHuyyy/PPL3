"""
Lexer test cases for TyC compiler
Implement 100 test cases for lexer
"""

import pytest
from tests.utils import Tokenizer


# ========== Simple Test Cases (10 types) ==========
def test_keyword_auto():
    """1. Keyword"""
    tokenizer = Tokenizer("auto")
    assert tokenizer.get_tokens_as_string() == "auto,<EOF>"


def test_operator_assign():
    """2. Operator"""
    tokenizer = Tokenizer("=")
    assert tokenizer.get_tokens_as_string() == "=,<EOF>"


def test_separator_semi():
    """3. Separator"""
    tokenizer = Tokenizer(";")
    assert tokenizer.get_tokens_as_string() == ";,<EOF>"


def test_integer_single_digit():
    """4. Integer literal"""
    tokenizer = Tokenizer("5")
    assert tokenizer.get_tokens_as_string() == "5,<EOF>"


def test_float_decimal():
    """5. Float literal"""
    tokenizer = Tokenizer("3.14")
    assert tokenizer.get_tokens_as_string() == "3.14,<EOF>"


def test_string_simple():
    """6. String literal"""
    tokenizer = Tokenizer('"hello"')
    assert tokenizer.get_tokens_as_string() == "hello,<EOF>"


def test_identifier_simple():
    """7. Identifier"""
    tokenizer = Tokenizer("x")
    assert tokenizer.get_tokens_as_string() == "x,<EOF>"


def test_line_comment():
    """8. Line comment"""
    tokenizer = Tokenizer("// This is a comment")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_integer_in_expression():
    """9. Mixed: integers and operator"""
    tokenizer = Tokenizer("5+10")
    assert tokenizer.get_tokens_as_string() == "5,+,10,<EOF>"


def test_complex_expression():
    """10. Complex: variable declaration"""
    tokenizer = Tokenizer("auto x = 5 + 3 * 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,+,3,*,2,;,<EOF>"


# ========== Keywords (more) ==========
def test_keyword_break():
    """11. Keyword break"""
    tokenizer = Tokenizer("break")
    assert tokenizer.get_tokens_as_string() == "break,<EOF>"


def test_keyword_case():
    """12. Keyword case"""
    tokenizer = Tokenizer("case")
    assert tokenizer.get_tokens_as_string() == "case,<EOF>"


def test_keyword_continue():
    """13. Keyword continue"""
    tokenizer = Tokenizer("continue")
    assert tokenizer.get_tokens_as_string() == "continue,<EOF>"


def test_keyword_default():
    """14. Keyword default"""
    tokenizer = Tokenizer("default")
    assert tokenizer.get_tokens_as_string() == "default,<EOF>"


def test_keyword_else():
    """15. Keyword else"""
    tokenizer = Tokenizer("else")
    assert tokenizer.get_tokens_as_string() == "else,<EOF>"


def test_keyword_float():
    """16. Keyword float"""
    tokenizer = Tokenizer("float")
    assert tokenizer.get_tokens_as_string() == "float,<EOF>"


def test_keyword_for():
    """17. Keyword for"""
    tokenizer = Tokenizer("for")
    assert tokenizer.get_tokens_as_string() == "for,<EOF>"


def test_keyword_if():
    """18. Keyword if"""
    tokenizer = Tokenizer("if")
    assert tokenizer.get_tokens_as_string() == "if,<EOF>"


def test_keyword_int():
    """19. Keyword int"""
    tokenizer = Tokenizer("int")
    assert tokenizer.get_tokens_as_string() == "int,<EOF>"


def test_keyword_return():
    """20. Keyword return"""
    tokenizer = Tokenizer("return")
    assert tokenizer.get_tokens_as_string() == "return,<EOF>"


def test_keyword_string():
    """21. Keyword string"""
    tokenizer = Tokenizer("string")
    assert tokenizer.get_tokens_as_string() == "string,<EOF>"


def test_keyword_struct():
    """22. Keyword struct"""
    tokenizer = Tokenizer("struct")
    assert tokenizer.get_tokens_as_string() == "struct,<EOF>"


def test_keyword_switch():
    """23. Keyword switch"""
    tokenizer = Tokenizer("switch")
    assert tokenizer.get_tokens_as_string() == "switch,<EOF>"


def test_keyword_void():
    """24. Keyword void"""
    tokenizer = Tokenizer("void")
    assert tokenizer.get_tokens_as_string() == "void,<EOF>"


def test_keyword_while():
    """25. Keyword while"""
    tokenizer = Tokenizer("while")
    assert tokenizer.get_tokens_as_string() == "while,<EOF>"


# ========== Operators ==========
def test_operator_plus_minus_mul_div_mod():
    """26. Operators + - * / %"""
    tokenizer = Tokenizer("+ - * / %")
    assert tokenizer.get_tokens_as_string() == "+,-,*,/,%,<EOF>"


def test_operator_relational_all():
    """27. Operators == != < <= > >="""
    tokenizer = Tokenizer("== != < <= > >=")
    assert tokenizer.get_tokens_as_string() == "==,!=,<,<=,>,>=,<EOF>"


def test_operator_logical_all():
    """28. Operators && || !"""
    tokenizer = Tokenizer("&& || !")
    assert tokenizer.get_tokens_as_string() == "&&,||,!,<EOF>"


def test_operator_inc_dec_prefix():
    """29. Prefix ++ and --"""
    tokenizer = Tokenizer("++a --b")
    assert tokenizer.get_tokens_as_string() == "++,a,--,b,<EOF>"


def test_operator_inc_dec_postfix():
    """30. Postfix ++ and --"""
    tokenizer = Tokenizer("a++ b--")
    assert tokenizer.get_tokens_as_string() == "a,++,b,--,<EOF>"


def test_operator_member_access_dot():
    """31. Dot operator"""
    tokenizer = Tokenizer("p.x")
    assert tokenizer.get_tokens_as_string() == "p,.,x,<EOF>"


def test_operator_chained_assign():
    """32. Chained assignment tokens"""
    tokenizer = Tokenizer("x=y=z=10")
    assert tokenizer.get_tokens_as_string() == "x,=,y,=,z,=,10,<EOF>"


# ========== Separators ==========
def test_separators_all():
    """33. Separators {} () ; , :"""
    tokenizer = Tokenizer("{ } ( ) ; , :")
    # Note: token text for ',' is ',', so join will produce triple commas before ':'
    assert tokenizer.get_tokens_as_string() == "{,},(,),;,,,:,<EOF>"


def test_separators_in_switch_case():
    """34. Separators with switch/case form"""
    tokenizer = Tokenizer("switch(x){case 1: break;}")
    assert tokenizer.get_tokens_as_string() == "switch,(,x,),{,case,1,:,break,;,},<EOF>"


# ========== Identifiers ==========
def test_identifier_with_underscore():
    """35. Identifier starts with _"""
    tokenizer = Tokenizer("_x")
    assert tokenizer.get_tokens_as_string() == "_x,<EOF>"


def test_identifier_mixed_letters_digits():
    """36. Identifier contains digits"""
    tokenizer = Tokenizer("abc123")
    assert tokenizer.get_tokens_as_string() == "abc123,<EOF>"


def test_identifier_case_sensitive():
    """37. Case sensitivity"""
    tokenizer = Tokenizer("MyVar myvar MYVAR")
    assert tokenizer.get_tokens_as_string() == "MyVar,myvar,MYVAR,<EOF>"


def test_identifier_keyword_like_prefix():
    """38. Identifier that starts with keyword text"""
    tokenizer = Tokenizer("intValue autoX while1")
    assert tokenizer.get_tokens_as_string() == "intValue,autoX,while1,<EOF>"


def test_identifier_single_letter_upper():
    """39. Single letter identifier uppercase"""
    tokenizer = Tokenizer("X")
    assert tokenizer.get_tokens_as_string() == "X,<EOF>"


# ========== Integer literals ==========
def test_integer_zero():
    """40. Integer 0"""
    tokenizer = Tokenizer("0")
    assert tokenizer.get_tokens_as_string() == "0,<EOF>"


def test_integer_multi_digits():
    """41. Integer multi digits"""
    tokenizer = Tokenizer("2500")
    assert tokenizer.get_tokens_as_string() == "2500,<EOF>"


def test_integer_negative_as_tokens():
    """42. Negative integer appears as '-' then INT_LIT (lexer tokens)"""
    tokenizer = Tokenizer("-45")
    assert tokenizer.get_tokens_as_string() == "-,45,<EOF>"


def test_integer_in_struct_init():
    """43. Integers inside struct literal"""
    tokenizer = Tokenizer("{10,20}")
    assert tokenizer.get_tokens_as_string() == "{,10,,,20,},<EOF>"


# ========== Float literals ==========
def test_float_trailing_dot():
    """44. Float 1."""
    tokenizer = Tokenizer("1.")
    assert tokenizer.get_tokens_as_string() == "1.,<EOF>"


def test_float_leading_dot():
    """45. Float .5"""
    tokenizer = Tokenizer(".5")
    assert tokenizer.get_tokens_as_string() == ".5,<EOF>"


def test_float_exponent_no_dot():
    """46. Float 1e4"""
    tokenizer = Tokenizer("1e4")
    assert tokenizer.get_tokens_as_string() == "1e4,<EOF>"


def test_float_exponent_with_sign():
    """47. Float 2E-3"""
    tokenizer = Tokenizer("2E-3")
    assert tokenizer.get_tokens_as_string() == "2E-3,<EOF>"


def test_float_with_dot_and_exp():
    """48. Float 1.23e4"""
    tokenizer = Tokenizer("1.23e4")
    assert tokenizer.get_tokens_as_string() == "1.23e4,<EOF>"


def test_float_negative_as_tokens():
    """49. Negative float tokens: '-' then FLOAT_LIT"""
    tokenizer = Tokenizer("-3.14")
    assert tokenizer.get_tokens_as_string() == "-,3.14,<EOF>"


# ========== String literals valid (strip quotes, no unescape) ==========
def test_string_empty():
    """50. Empty string"""
    tokenizer = Tokenizer('""')
    assert tokenizer.get_tokens_as_string() == ",<EOF>"


def test_string_with_spaces():
    """51. String with spaces"""
    tokenizer = Tokenizer('"hello world"')
    assert tokenizer.get_tokens_as_string() == "hello world,<EOF>"


def test_string_with_tab_escape():
    """52. String with \\t (kept as two chars)"""
    tokenizer = Tokenizer('"a\\tb"')
    assert tokenizer.get_tokens_as_string() == "a\\tb,<EOF>"


def test_string_with_newline_escape():
    """53. String with \\n"""
    tokenizer = Tokenizer('"a\\nb"')
    assert tokenizer.get_tokens_as_string() == "a\\nb,<EOF>"


def test_string_with_carriage_escape():
    """54. String with \\r"""
    tokenizer = Tokenizer('"a\\rb"')
    assert tokenizer.get_tokens_as_string() == "a\\rb,<EOF>"


def test_string_with_backspace_escape():
    """55. String with \\b"""
    tokenizer = Tokenizer('"a\\bb"')
    assert tokenizer.get_tokens_as_string() == "a\\bb,<EOF>"


def test_string_with_formfeed_escape():
    """56. String with \\f"""
    tokenizer = Tokenizer('"a\\fb"')
    assert tokenizer.get_tokens_as_string() == "a\\fb,<EOF>"


def test_string_with_quote_escape():
    """57. String with \\" (kept as backslash+quote)"""
    tokenizer = Tokenizer('"He said: \\"Hi\\""')
    assert tokenizer.get_tokens_as_string() == 'He said: \\"Hi\\",<EOF>'


def test_string_with_backslash_escape():
    """58. String with \\\\ """
    tokenizer = Tokenizer('"C:\\\\path\\\\file"')
    assert tokenizer.get_tokens_as_string() == "C:\\\\path\\\\file,<EOF>"


def test_string_with_mixed_escapes():
    """59. String with mixed escapes"""
    tokenizer = Tokenizer('"a\\\\b\\tc\\n"')
    assert tokenizer.get_tokens_as_string() == "a\\\\b\\tc\\n,<EOF>"


# ========== Comments ==========
def test_block_comment_simple():
    """60. Block comment removed"""
    tokenizer = Tokenizer("/* comment */")
    assert tokenizer.get_tokens_as_string() == "<EOF>"


def test_block_comment_multiline_then_code():
    """61. Block comment multiline then tokens"""
    tokenizer = Tokenizer("/* a\nb\nc */ auto x;")
    assert tokenizer.get_tokens_as_string() == "auto,x,;,<EOF>"


def test_line_comment_then_newline_code():
    """62. Line comment then code on next line"""
    tokenizer = Tokenizer("//cmt\nauto x;")
    assert tokenizer.get_tokens_as_string() == "auto,x,;,<EOF>"


def test_comment_markers_inside_other_comment():
    """63. // inside block comment, /* inside line comment"""
    tokenizer = Tokenizer("/* This is a block // not line */\n// line /* not block\nauto x;")
    assert tokenizer.get_tokens_as_string() == "auto,x,;,<EOF>"


def test_comment_between_tokens():
    """64. Comment between tokens"""
    tokenizer = Tokenizer("auto/*x*/y;")
    assert tokenizer.get_tokens_as_string() == "auto,y,;,<EOF>"


# ========== Whitespace / newlines ==========
def test_whitespace_skipped():
    """65. Whitespace skipped"""
    tokenizer = Tokenizer(" \t\f\r\n auto \n x \t= \r 5 ; ")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,5,;,<EOF>"


def test_multiple_newlines():
    """66. Multiple newlines"""
    tokenizer = Tokenizer("\n\n\nint\nx\n;\n")
    assert tokenizer.get_tokens_as_string() == "int,x,;,<EOF>"


# ========== Mixed realistic snippets ==========
def test_function_decl_tokens():
    """67. Function declaration tokens"""
    tokenizer = Tokenizer('int add(int x, int y){return x+y;}')
    assert tokenizer.get_tokens_as_string() == "int,add,(,int,x,,,int,y,),{,return,x,+,y,;,},<EOF>"


def test_inferred_return_func_tokens():
    """68. Inferred return type function (no leading type)"""
    tokenizer = Tokenizer("add(int x,int y){return x+y;}")
    assert tokenizer.get_tokens_as_string() == "add,(,int,x,,,int,y,),{,return,x,+,y,;,},<EOF>"


def test_struct_decl_tokens():
    """69. Struct declaration tokens"""
    tokenizer = Tokenizer("struct Point{int x; int y;};")
    assert tokenizer.get_tokens_as_string() == "struct,Point,{,int,x,;,int,y,;,},;,<EOF>"


def test_struct_var_decl_init_tokens():
    """70. Struct var init tokens"""
    tokenizer = Tokenizer("Point p={10,20};")
    assert tokenizer.get_tokens_as_string() == "Point,p,=,{,10,,,20,},;,<EOF>"


def test_switch_tokens_with_fallthrough():
    """71. Switch with two cases"""
    tokenizer = Tokenizer("switch(day){case 1:break;case 2:case 3:break;default:break;}")
    assert tokenizer.get_tokens_as_string() == "switch,(,day,),{,case,1,:,break,;,case,2,:,case,3,:,break,;,default,:,break,;,},<EOF>"


def test_for_tokens_full():
    """72. For loop tokens full"""
    tokenizer = Tokenizer("for(auto i=0;i<10;++i){printInt(i);}")
    assert tokenizer.get_tokens_as_string() == "for,(,auto,i,=,0,;,i,<,10,;,++,i,),{,printInt,(,i,),;,},<EOF>"


def test_for_tokens_missing_parts():
    """73. For loop tokens with omitted init/cond/update"""
    tokenizer = Tokenizer("for(;;)break;")
    assert tokenizer.get_tokens_as_string() == "for,(,;,;,),break,;,<EOF>"


def test_if_else_tokens():
    """74. If else tokens"""
    tokenizer = Tokenizer("if(x){y=1;}else y=2;")
    assert tokenizer.get_tokens_as_string() == "if,(,x,),{,y,=,1,;,},else,y,=,2,;,<EOF>"


def test_while_tokens():
    """75. While tokens"""
    tokenizer = Tokenizer("while(i<10){i++;}")
    assert tokenizer.get_tokens_as_string() == "while,(,i,<,10,),{,i,++,;,},<EOF>"


# ========== Member access + call + postfix/prefix ==========
def test_member_access_chain_tokens():
    """76. Member access chain"""
    tokenizer = Tokenizer("a.b.c")
    assert tokenizer.get_tokens_as_string() == "a,.,b,.,c,<EOF>"


def test_call_tokens_empty_args():
    """77. Function call empty args"""
    tokenizer = Tokenizer("readInt()")
    assert tokenizer.get_tokens_as_string() == "readInt,(,),<EOF>"


def test_call_tokens_args():
    """78. Function call args"""
    tokenizer = Tokenizer("add(1,2+3)")
    assert tokenizer.get_tokens_as_string() == "add,(,1,,,2,+,3,),<EOF>"


def test_postfix_on_member_access():
    """79. Postfix ++ on member access"""
    tokenizer = Tokenizer("p.x++")
    assert tokenizer.get_tokens_as_string() == "p,.,x,++,<EOF>"


def test_prefix_on_member_access():
    """80. Prefix ++ on member access"""
    tokenizer = Tokenizer("++p.x")
    assert tokenizer.get_tokens_as_string() == "++,p,.,x,<EOF>"


# ========== ERROR_TOKEN tests ==========
def test_error_token_at():
    """81. Unrecognized char @"""
    tokenizer = Tokenizer("@")
    assert tokenizer.get_tokens_as_string() == "Error Token @"


def test_error_token_hash_in_code():
    """82. Unrecognized char # inside code (tokens then error appended)"""
    tokenizer = Tokenizer("auto x = 1 # 2;")
    assert tokenizer.get_tokens_as_string() == "auto,x,=,1,Error Token #"


def test_error_token_dollar():
    """83. Unrecognized char $"""
    tokenizer = Tokenizer("$")
    assert tokenizer.get_tokens_as_string() == "Error Token $"


# ========== UNCLOSE_STRING tests ==========
def test_unclose_string_eof():
    """84. Unclosed string reaches EOF"""
    tokenizer = Tokenizer('"abc')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: abc"


def test_unclose_string_newline():
    """85. Unclosed string reaches newline"""
    tokenizer = Tokenizer('"abc\n')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: abc"


def test_unclose_string_carriage_return():
    """86. Unclosed string reaches \\r (current grammar doesn't handle lone \\r)"""
    tokenizer = Tokenizer('"abc\r')
    assert tokenizer.get_tokens_as_string() == 'Error Token "'


def test_unclose_string_escapes_then_eof():
    """87. Unclosed string with valid escapes then EOF"""
    tokenizer = Tokenizer('"a\\nb')
    assert tokenizer.get_tokens_as_string() == "Unclosed String: a\\nb"


# ========== ILLEGAL_ESCAPE tests ==========
def test_illegal_escape_x():
    """88. Illegal escape \\x"""
    tokenizer = Tokenizer('"ab\\x"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: ab\\x"


def test_illegal_escape_0():
    """89. Illegal escape \\0"""
    tokenizer = Tokenizer('"a\\0b"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: a\\0"


def test_illegal_escape_hex_like():
    """90. Illegal escape \\x80 style (first illegal at \\x)"""
    tokenizer = Tokenizer('"\\x80"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: \\x"


def test_illegal_escape_uppercase():
    """91. Illegal escape \\N (not supported)"""
    tokenizer = Tokenizer('"a\\Nb"')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: a\\N"


def test_illegal_escape_before_newline():
    """92. Illegal escape should be detected before unclosed (order)"""
    tokenizer = Tokenizer('"a\\q\n')
    assert tokenizer.get_tokens_as_string() == "Illegal Escape In String: a\\q"


# ========== More mixed edge cases ==========
def test_keyword_not_identifier_split():
    """93. Keyword followed by identifier chars => identifier"""
    tokenizer = Tokenizer("auto_")
    assert tokenizer.get_tokens_as_string() == "auto_,<EOF>"


def test_float_then_dot_member():
    """94. Float followed by dot member access"""
    tokenizer = Tokenizer("1.0.toString")
    assert tokenizer.get_tokens_as_string() == "1.0,.,toString,<EOF>"


def test_dot_then_identifier():
    """95. Dot alone then id"""
    tokenizer = Tokenizer(".x")
    assert tokenizer.get_tokens_as_string() == ".,x,<EOF>"


def test_nested_braces_tokens():
    """96. Nested braces tokens"""
    tokenizer = Tokenizer("{{1,2},{3,4}}")
    assert tokenizer.get_tokens_as_string() == "{,{,1,,,2,},,,{,3,,,4,},},<EOF>"


def test_string_followed_by_identifier():
    """97. String then identifier"""
    tokenizer = Tokenizer('"hi"x')
    assert tokenizer.get_tokens_as_string() == "hi,x,<EOF>"


def test_comment_like_in_string():
    """98. Comment markers inside string should stay as string content"""
    tokenizer = Tokenizer('"/* not a comment */"')
    assert tokenizer.get_tokens_as_string() == "/* not a comment */,<EOF>"


def test_slashes_not_comment_when_single():
    """99. Single / is DIV operator"""
    tokenizer = Tokenizer("a/b")
    assert tokenizer.get_tokens_as_string() == "a,/,b,<EOF>"


def test_full_program_like_tokens():
    """100. A larger snippet tokens"""
    code = """
    struct Point { int x; int y; };
    void main() {
        Point p = {1,2};
        if (p.x >= 1) printInt(p.x);
        return;
    }
    """
    tokenizer = Tokenizer(code)
    assert tokenizer.get_tokens_as_string() == (
        "struct,Point,{,int,x,;,int,y,;,},;,void,main,(,),{,"
        "Point,p,=,{,1,,,2,},;,if,(,p,.,x,>=,1,),printInt,(,p,.,x,),;,return,;,},<EOF>"
    )
