grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit()
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit()
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        result = super().emit()
        raise ErrorToken(result.text)
    else:
        return super().emit()
}

options{
    language=Python3;
}


program
    : declList EOF
    ;

declList
    : decl declList
    | /* empty */
    ;

decl
    : structDecl
    | funcDecl
    ;

/* struct <id> { <type> <id>; ... } ; */
structDecl
    : STRUCT ID LBRACE structMemberList RBRACE SEMI
    ;

structMemberList
    : structMember structMemberList
    | /* empty */
    ;

structMember
    : type ID SEMI
    ;

funcDecl
    : funcHead LPAREN paramListOpt RPAREN blockStmt
    ;

funcHead
    : typeOrVoid ID
    | ID
    ;

typeOrVoid
    : VOID
    | type
    ;

paramListOpt
    : paramList
    | /* empty */
    ;

paramList
    : param paramListTail
    ;

paramListTail
    : COMMA param paramListTail
    | /* empty */
    ;

param
    : type ID
    ;

type
    : INT
    | FLOAT
    | STRING
    | ID      /* struct type name */
    ;

/* ===== Statements ===== */

statement
    : varDeclStmt
    | blockStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    ;

statementList
    : statement statementList
    | /* empty */
    ;

varDeclStmt
    : varDecl SEMI
    ;

varDecl
    : varDeclHead ID varInitOpt
    ;

varDeclHead
    : AUTO
    | type
    ;

varInitOpt
    : ASSIGN expr
    | /* empty */
    ;

blockStmt
    : LBRACE statementList RBRACE
    ;

ifStmt
    : IF LPAREN expr RPAREN statement elseOpt
    ;

elseOpt
    : ELSE statement
    | /* empty */
    ;

whileStmt
    : WHILE LPAREN expr RPAREN statement
    ;

forStmt
    : FOR LPAREN forInitOpt SEMI exprOpt SEMI forUpdateOpt RPAREN statement
    ;

forInitOpt
    : forInit
    | /* empty */
    ;

forInit
    : forVarDecl
    | forAssign
    ;

forAssign
    : lvalue ASSIGN expr
    ;

forVarDecl
    : varDeclHead ID varInitOpt
    ;

exprOpt
    : expr
    | /* empty */
    ;

forUpdateOpt
    : forUpdate
    | /* empty */
    ;

// for-update: phải có ít nhất một ++/-- (prefix hoặc postfix)
// để:
// - ++(a+b) OK
// - {a,b}-- OK
// - --f().a++ OK
// - còn "1" sẽ ăn được postfixExpr rồi thiếu ++/-- -> vấp tại ')'
forUpdate
    : lvalue ASSIGN expr
    | prefixIncDec+ postfixExpr postfixIncDec*   // ++i, --(a+b), --f().a++, ...
    | postfixExpr postfixIncDec+                 // i++, {a,b}--, 1?? -> fail tại ')'
    ;


switchStmt
    : SWITCH LPAREN expr RPAREN LBRACE switchSections RBRACE
    ;
switchSections
    : caseSection* defaultSection? caseSection*
    ;
caseSection
    : CASE expr COLON statementList
    ;

defaultSection
    : DEFAULT COLON statementList
    ;


breakStmt
    : BREAK SEMI
    ;

continueStmt
    : CONTINUE SEMI
    ;

returnStmt
    : RETURN returnExprOpt SEMI
    ;

returnExprOpt
    : expr
    | /* empty */
    ;

exprStmt
    : expr SEMI
    ;

/* ===== Expressions ===== */

expr
    : assignExpr
    ;

/* '=' right associative */

// LHS hợp lệ:
// 1) ID(.ID)*
// 2) <expr_postfix> . ID (.ID)*   (bắt buộc có ít nhất 1 field access)
lvalue
    : ID (DOT ID)*                              // x, x.a, x.a.b
    | lvalueBase lvalueField+                   // t().a, (f()).a, {...}.a, 5..a
    ;

// Base của dạng 2: cho phép mọi postfixExpr (call, paren, literal, structLiteral, ...)
// nhưng KHÔNG kèm DOT ở đây để đảm bảo field bắt buộc nằm trong lvalueField+
lvalueBase
    : primaryExpr lvalueBaseTail*
    ;

lvalueBaseTail
    : LPAREN argListOpt RPAREN                   // call
    ;

lvalueField
    : DOT ID
    ;

assignExpr
    : lvalue ASSIGN assignExpr     // right associative
    | orExpr
    ;


orExpr
    : andExpr orTail
    ;

orTail
    : OR andExpr orTail
    | /* empty */
    ;

andExpr
    : eqExpr andTail
    ;

andTail
    : AND eqExpr andTail
    | /* empty */
    ;

eqExpr
    : relExpr eqTail
    ;

eqTail
    : EQ relExpr eqTail
    | NEQ relExpr eqTail
    | /* empty */
    ;

relExpr
    : addExpr relTail
    ;

relTail
    : LT addExpr relTail
    | LE addExpr relTail
    | GT addExpr relTail
    | GE addExpr relTail
    | /* empty */
    ;

addExpr
    : mulExpr addTail
    ;

addTail
    : ADD mulExpr addTail
    | SUB mulExpr addTail
    | /* empty */
    ;

mulExpr
    : unaryExpr mulTail
    ;

mulTail
    : MUL unaryExpr mulTail
    | DIV unaryExpr mulTail
    | MOD unaryExpr mulTail
    | /* empty */
    ;

unaryExpr
    : incDecExpr
    | unarySignExpr
    ;

unarySignExpr
    : NOT unaryExpr
    | ADD unaryExpr
    | SUB unaryExpr
    ;

incDecExpr
    : prefixIncDec* postfixExpr postfixIncDec*
    ;

prefixIncDec
    : INC
    | DEC
    ;

postfixIncDec
    : INC
    | DEC
    ;



postfixExpr
    : callOrPrimary fieldTail* incDecTail?
    ;

callOrPrimary
    : primaryExpr callTail?
    ;

callTail
    : LPAREN argListOpt RPAREN
    ;

fieldTail
    : DOT ID
    ;

incDecTail
    : INC
    | DEC
    ;


argListOpt
    : argList
    | /* empty */
    ;

argList
    : expr argListTail
    ;

argListTail
    : COMMA expr argListTail
    | /* empty */
    ;

primaryExpr
    : literal
    | ID
    | LPAREN expr RPAREN
    | structLiteral
    ;

structLiteral
    : LBRACE structInitOpt RBRACE
    ;

structInitOpt
    : expr structInitTail
    | /* empty */
    ;

structInitTail
    : COMMA expr structInitTail
    | /* empty */
    ;

literal
    : INT_LIT
    | FLOAT_LIT
    | STRING_LIT
    ;

/* =========================
 * Lexer rules
 * ========================= */

/* ----- Keywords ----- */
AUTO      : 'auto';
BREAK     : 'break';
CASE      : 'case';
CONTINUE  : 'continue';
DEFAULT   : 'default';
ELSE      : 'else';
FLOAT     : 'float';
FOR       : 'for';
IF        : 'if';
INT       : 'int';
RETURN    : 'return';
STRING    : 'string';
STRUCT    : 'struct';
SWITCH    : 'switch';
VOID      : 'void';
WHILE     : 'while';

/* ----- Operators ----- */
OR        : '||';
AND       : '&&';
EQ        : '==';
NEQ       : '!=';
LE        : '<=';
GE        : '>=';
LT        : '<';
GT        : '>';

INC       : '++';
DEC       : '--';
NOT       : '!';
ASSIGN    : '=';

ADD       : '+';
SUB       : '-';
MUL       : '*';
DIV       : '/';
MOD       : '%';

DOT       : '.';

/* ----- Separators ----- */
LBRACE    : '{';
RBRACE    : '}';
LPAREN    : '(';
RPAREN    : ')';
SEMI      : ';';
COMMA     : ',';
COLON     : ':';

/* ----- Identifiers ----- */
ID
    : [A-Za-z_] [A-Za-z_0-9]*
    ;

/* ----- Literals ----- */
INT_LIT
    : DIGITS
    ;

FLOAT_LIT
    : DIGITS DOT DIGITS? EXP?
    | DOT DIGITS EXP?
    | DIGITS EXP
    ;

fragment DIGITS : [0-9]+;
fragment EXP    : [eE] [+-]? DIGITS;


fragment STR_CHAR
    : ~["\\\r\n]
    ;

fragment ESC_SEQ
    : '\\' [bfrnt"\\]
    ;

/* Illegal escape: include backslash + illegal char */
ILLEGAL_ESCAPE
    : '"' (STR_CHAR | ESC_SEQ)* '\\' ~[bfrnt"\\\r\n]
      {
        self.text = self.text[1:]
      }
    ;

/* Unclosed string: ends before closing quote due to newline/CR/EOF */
UNCLOSE_STRING: '"' (STR_CHAR | ESC_SEQ)*  '\\'? ('\n' | '\r\n' | EOF) {
    if self.text[-1] == '\n' and self.text[-2] == '\r':
        raise UncloseString(self.text[1:-2])
    elif self.text[-1] == '\n':
        raise UncloseString(self.text[1:-1])
    else:
        raise UncloseString(self.text[1:])
};

/* Valid string: strip quotes */
STRING_LIT
    : '"' (STR_CHAR | ESC_SEQ)* '"'
      {
        self.text = self.text[1:-1]
      }
    ;

/* ----- Comments & whitespace ----- */
LINE_COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

WS
    : [ \t\f\r\n]+ -> skip
    ;

/* ----- Error char ----- */
ERROR_CHAR
    : .
    ;
