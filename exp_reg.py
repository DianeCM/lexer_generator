
from nfa_dfa import *
from cmp.ast import *
from cmp.pycompiler import Grammar
from cmp.parsing import metodo_predictivo_no_recursivo
from cmp.utils import Token
from cmp.evaluation import evaluate_parse


#-------------------------------CP8----------------------------


printer = get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode)

EPSILON = 'ε'

class EpsilonNode(AtomicNode):
    def evaluate(self):
        # return NFA(2,[1],{(0,''):[1]})
        return NFA(states = 1, finals =[0], transitions = {})

EpsilonNode(EPSILON).evaluate()

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return NFA(states = 2,finals = [1],transitions = {(0,s):  [1]})

print(type(SymbolNode('a').evaluate()))

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        # Your code here!!!
        return automata_closure(value)
    
print(type(ClosureNode(SymbolNode('a')).evaluate()))

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automata_union(lvalue,rvalue)

print(type(UnionNode(SymbolNode('a'), SymbolNode('b')).evaluate()))

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return automata_concatenation(lvalue,rvalue)

print(type(ConcatNode(SymbolNode('a'), SymbolNode('b')).evaluate()))



G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

# > PRODUCTIONS???
# Your code here!!!
#  E --> T X 
E %= T + X, lambda h,s: s[2], None, lambda h,s: s[1]                      

#  X --> |T X 
# X --> epsilon 
X %= pipe + T + X, lambda h,s: s[3], None, None, lambda h,s: UnionNode(h[0],s[2])    
X %= G.Epsilon, lambda h,s: h[0]                                                    

# T --> F Y 
T %= F + Y, lambda h,s: s[2], None, lambda h,s: s[1]                      

#  Y --> F Y 
# Y --> epsilon 
Y %= F + Y, lambda h,s: s[2], None, lambda h,s: ConcatNode(h[0] , s[1])        
Y %= G.Epsilon, lambda h,s: h[0]                                                    

# F --> A Z 
F %= A + Z, lambda h,s: s[2],None,lambda h,s: s[1]

# Z --> * Z 
# Z --> epsilon 
Z %= star + Z, lambda h,s: s[2], None,lambda h,s:ClosureNode(h[0])
Z %= G.Epsilon, lambda h,s: h[0] 

#  A --> symbol 
#  A --> ( E ) 
#  A --> epsilon 
A %= symbol, lambda h,s: SymbolNode(s[1]) , None
A %= opar + E + cpar, lambda h,s: s[2], None, None, None
A %= epsilon, lambda h,s: EpsilonNode(h[0])

print(G)



# def regex_tokenizer(text, G, skip_whitespaces=False):
#     tokens = []
#     # > fixed_tokens = ???
#     fixed_tokens = { lex: Token(lex, G[lex]) for lex in '| * ( ) ε'.split() }
#     for char in text:
#         if skip_whitespaces and char.isspace():
#             continue
#         # Your code here!!!
#         try:
#                 token = fixed_tokens[char]
#         except:
#                 token = Token( char, G['symbol'] )

#         tokens.append(token)

#     tokens.append(Token('$', G.EOF))
#     return tokens

# tokens = regex_tokenizer('a*(a|b)*cd | ε',G)
# print(tokens)

# parser = metodo_predictivo_no_recursivo(G)

# print("==============Left-Parse==============")
# left_parse = parser(tokens)
# print(left_parse)

# print('=================AST==================')
# ast = evaluate_parse(left_parse, tokens)
# print(printer(ast))

# print(type(ast))

# print('================Result================')
# nfa = ast.evaluate()
# print(nfa.transitions)
# print(type(nfa))

# dfa = nfa_to_dfa(nfa)
# print(dfa.transitions)
# print(dfa.finals)
# assert dfa.recognize('')
# assert dfa.recognize('cd')
# assert dfa.recognize('aaaaacd')
# assert dfa.recognize('bbbbbcd')
# assert dfa.recognize('bbabababcd')
# assert dfa.recognize('aaabbabababcd')

# assert not dfa.recognize('cda')
# assert not dfa.recognize('aaaaa')
# assert not dfa.recognize('bbbbb')
# assert not dfa.recognize('ababba')
# assert not dfa.recognize('cdbaba')
# assert not dfa.recognize('cababad')
# assert not dfa.recognize('bababacc')

# mini = automata_minimization(dfa)
# display(mini)