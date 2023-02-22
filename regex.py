from .cmp.pycompiler import Grammar
from .cmp.utils import Token
from .cmp.parsing import build_parsing_table, metodo_predictivo_no_recursivo
from .cmp.evaluation import evaluate_parse
from .nfa_dfa import *
from .cmp.ast import *
from .exp_reg import *


def regex_tokenizer(text, G, skip_whitespaces=False):
    tokens = []
    fixed_tokens = { lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split() }
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        try:
            token = fixed_tokens[char]
        except:
            token = Token(char,G['symbol'])
        tokens.append(token)
        
    tokens.append(Token('$', G.EOF))
    return tokens


class Regex:

    def __init__(self, regex):
        self.regex = regex
        print("regex")
        print(self.regex)
        self.automaton = self._dfa()

    def _dfa(self):
        tokens = regex_tokenizer(self.regex, G)

        print("tokens dfa")
        print(tokens)

        parser = metodo_predictivo_no_recursivo(G)

        print("parser")
        print(parser)

        left_parse = parser(tokens)

        print("left_parser")
        print(left_parse)

        ast = evaluate_parse(left_parse, tokens)

        print("ast")
        print(ast.__repr__())
        print(ast)

        nfa = ast.evaluate()

        print("nfa")
        print(nfa)

        dfa = nfa_to_dfa(nfa)

        print("dfa")
        print(dfa)
        print(dfa.transitions)
        return dfa