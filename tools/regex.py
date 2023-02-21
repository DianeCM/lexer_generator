from .cmp.pycompiler import Grammar
from .cmp.utils import Token
from .cmp.parsing import build_parsing_table, metodo_predictivo_no_recursivo
from .cmp.evaluation import evaluate_parse
from .nfa_dfa import *
from .cmp.ast import *
from .exp_reg import *

# G = Grammar()

# E = G.NonTerminal('E', True)
# T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
# pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

# # > PRODUCTIONS???
# # Your code here!!!
# #  E --> T X 
# E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]                      

# #  X --> |T X 
# # X --> epsilon 
# X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0],s[2])    
# X %= G.Epsilon, lambda h,s: h[0]                                                    

# # T --> F Y 
# T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]                      

# #  Y --> F Y 
# # Y --> epsilon 
# Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0] , s[1])        
# Y %= G.Epsilon, lambda h,s: h[0]                                                    

# # F --> A Z 
# F %= A + Z, lambda h,s: s[2],None,lambda h,s: s[1]

# # Z --> * Z 
# # Z --> epsilon 
# Z %= star + Z, lambda h,s: s[2], None,lambda h,s:ClosureNode(h[0])
# Z %= G.Epsilon, lambda h,s: h[0] 

# #  A --> symbol 
# #  A --> ( E ) 
# #  A --> epsilon 
# A %= symbol, lambda h,s: SymbolNode(s[1]) , None
# A %= opar + E + cpar, lambda h,s: s[2], None, None, None
# A %= epsilon, lambda h,s: EpsilonNode(h[0])



def regex_tokenizer(text, G, skip_whitespaces=False):
    print("TEXT METODO REGEX_TOKENIZER")
    print(text)
    tokens = []
    # > fixed_tokens = ???
    # Your code here!!!
    fixed_tokens = { lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split() }
    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        # Your code here!!!
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