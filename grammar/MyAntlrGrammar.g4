grammar MyAntlrGrammar;

program: header my_rules;

header: grammar_name my_options? my_tokens? code_header? code_members?;

grammar_name: GRAMMAR ID SCOL #grammarDecl;

my_options
    : OPTIONS WHATEVER_IN_BRACE #optionDecl
    ;

my_tokens
    : TOKENS WHATEVER_IN_BRACE #tokensDecl   
    ;

code_header
    : AT_CODE_HEADER WHATEVER_IN_BRACE #codeHeaderDecl
    ;

code_members
    : AT_CODE_MEMBERS WHATEVER_IN_BRACE #codeMembersDecl
    ;

my_rules: (my_rule)* #myRuleList;

my_rule
    : ID COL branch_l SCOL #ruleDecl
    | FRAGMENT ID COL branch_l SCOL #fragmentDecl
    ;

branch_l
    : branch #branchListBase
    | branch PIPE branch_l #branchList
    ;

branch
    : expr tagName? #myParserRule
    | expr code? #myLexerRule
    | tagName? #onlyTagName // a éviter -> warning à faire, on préfère que l’utilisateur mette des "?" ça m’a déjà posé problème
    ;

code
    : ARROW WHATEVER_IN_BRACE #realCode
    | ARROW SKIP_WORD #skipCode
    ;
    

// value
//     : OPAR value CPAR #parValue
//     | ID #idValue
//     | WHATEVER_IN_SG_QUOTE #stringValue
//     | value PIPE value #orValue
//     | value STAR #repeatValue
//     | value QUESTION_MARK #optionValue
//     ;
// ok il aime pas les récursions gauche ?

// value
//     : OPAR value CPAR #parValue
//     | ID #idValue
//     | WHATEVER_IN_SG_QUOTE #stringValue
//     | 

expr
    : value_modif  #exprBase
    | value_modif PIPE expr #pipeExpr
    | value_modif expr #concatExpr
    ;

value_modif: value modif? #valueModif;

modif
    : QUESTION_MARK
    | STAR
    ;

//un jour il faudra séparer les règles pour lexer et parser je pense ?
value
    : OPAR expr CPAR #parValue //both
    | ID EQUAL value #idWithNameValue //parseur
    | ID #idValue //parseur
    | my_regexp #regExpValue //pour les lexers 
    | WHATEVER_IN_SG_QUOTE #stringValue//pour les lexers
    // | value STAR #repeatValue
    // | value QUESTION_MARK #optionValue
    ;

my_regexp
    // : OBRACKET (caracter_set)* CBRACKET #bracketRegExp
    : CHARSET #bracketRegExp
    | TILDE my_regexp #notRegExp
    | my_regexp STAR #starRegExp
    | my_regexp PLUS #plusRegExp
    | DOT #dotRegExp
    ;

// caracter_set
//     : CHARSET
//     | CHAR MINUS CHAR
//     ;

tagName
    : HASHTAG ID #withTagName // cannot be name tagName because it’s rule name... 
    ;



GRAMMAR: 'grammar';
SCOL: ';';
COL: ':';
OBRACE: '{';
CBRACE: '}';
OBRACKET: '[';
CBRACKET: ']';
OPAR: '(';
CPAR: ')';
HASHTAG: '#';
OPTIONS: 'options';
TOKENS: 'tokens';
AT_CODE_HEADER: '@header';
AT_CODE_MEMBERS: '@members';
PIPE: '|';
STAR: '*';
SG_QUOTE: '\'';
QUESTION_MARK: '?';
PLUS: '+';
ARROW: '->';
SKIP_WORD: 'skip';
TILDE: '~';
MINUS: '-';
DOT: '.';
EQUAL: '=';
FRAGMENT: 'fragment';

// this was wrong
// CHARSET
//     : '[' [ "a-zA-Z0-9_'\-\\.]* ']'
//     ;
//tout sauf [ ] et \\ sauf si [ ou ] est précédé par \
CHARSET
        : '[' ('\\' . | ~[\]\\])* ']'
    ;

ID
    : [a-zA-Z_][a-zA-Z0-9_]*
    ;
    
COMMENT
    : '//' ~[\r\n]* -> skip
    ;



SPACE
 : [ \t\r\n] -> skip
 ;

WHATEVER_IN_BRACE
    : '{' NESTED_BRACED_CONTENT* '}'
    ;

fragment NESTED_BRACED_CONTENT
    : '{' NESTED_BRACED_CONTENT* '}'
    | ~[{}]
    ;
    

// WHATEVER_IN_SG_QUOTE
//     : '\'' .*? '\''
//     ;
// cette définition pose problème avec '\''
//
// donc on fait pareil mais on lui dit: a l’intérieur tu peux lire tout sauf \ et ', mais tu as aussi le droit de lire \'
// ceci est un bordel mais ça marche...
// ça fait cabler par contre
//
// on veut que le texte commence et finisse par ' donc '\'' ok
// on veut tout sauf ' ou \\, je doit lui donner \\ mais [] comprend ' tout seul.
// ou \ suivi de n’importe quoi on peut lire, donc texte \ c’est '\\' et n’importe quoi c’est .
WHATEVER_IN_SG_QUOTE
    : '\'' (~['\\] | '\\'. )*  '\''
    ;



