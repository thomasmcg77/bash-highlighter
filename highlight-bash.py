from lark import Lark, Transformer, v_args

my_grammar = """
start: script*


script: pipeline ("\\n")* | whileloop ("\\n")* | forloop ("\\n")* | comment ("\\n")* | ("\\n")*

pipeline: command (" | " command)*
command: WORD ((" " operator) | (" " argument))* | assignment | whileloop | forloop
argument: filename | WORD | STRING | path | NUMBER


loop: whileloop | forloop
whileloop: "while " comparison (" " | "\\n")+ "do" (" " | "\\n")+ (pipeline)* (" " | "\\n")+ "done"
forloop: "for " WORD (" ")+ "in" (" ")+ (value (" " value))* (" " | "\\n")+ "do" (" ")+ (pipeline)* (" " | "\\n")+ "done"


operator: "-" WORD
filename: (path)* WORD "." WORD ("." WORD)*
path: (("." | "..")? "/" (WORD | "..")+ ("/")?)+ | ((WORD | "..") "/")+ | ("./" filename) | ".." | "."
comment: "#"

assignment: WORD "=" (NUMBER | operation)
comparison: "[" (" ")? variable " " operator " " NUMBER (" ")? "]"
operation: "$((" (" ")? variable " " operand " " NUMBER (" ")? "))"
operand: "-" | "+" | "*" | "/"
value: WORD | NUMBER | STRING
variable: "$" WORD


%import common.WORD
%import common.ESCAPED_STRING -> STRING
%import common.SIGNED_NUMBER -> NUMBER
"""

parser = Lark(my_grammar)

# Class that determines which colors to assign to each type
class BashHighlighter(Transformer):
    @v_args(inline=True)
    def script(self, *args):
        return ''.join(args)

    @v_args(inline=True)
    def pipeline(self, *args):
        highlighted = ' | '.join('\033[94m{}\033[0m'.format(arg) for arg in args)
        return highlighted

    @v_args(inline=True)
    def command(self, *args):
        highlighted = '\033[94m{}\033[0m'.format(args[0])
        if len(args) > 1:
            highlighted += ''.join(' \033[94m{}\033[0m'.format(arg) for arg in args[1:])
        return highlighted
    
    @v_args(inline=True)
    def operator(self, arg):
        return '\033[0m{}\033[0m'.format('-') + '\033[033m{}\033[0m'.format(str(arg))

    @v_args(inline=True)
    def argument(self, arg):
        if arg.type == 'STRING':
            return '\033[92m{}\033[0m'.format(str(arg))
        elif arg.type == 'NUMBER':
            return '\033[91m{}\033[0m'.format(str(arg))
        else:
            return '\033[0m{}\033[0m'.format(str(arg))


highlighter = BashHighlighter()

script = input("Enter a bash script: ")
parse_tree = parser.parse(script)

highlighted = highlighter.transform(parse_tree)
print(highlighted.pretty())
