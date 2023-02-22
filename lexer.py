from .cmp.utils import Token
from .cmp.automata import State
from .nfa_dfa_class import DFA
from .regex import Regex
import sys

a = State(0)
b = State(1, True)
a.add_transition('a', a)
a.add_transition('b', b)
b.add_transition('a', a)
b.add_transition('b', b)

# display(a)

print('----------- Estado 0 -------------')
print('Identificador:', a.state)
print('Es final:', a.final)
print('Transiciones:', a.transitions)
print('Epsilon transiciones:', a.epsilon_transitions)

# display(b)

print('----------- Estado 1 -------------')
print('Identificador:', b.state)
print('Es final:', b.final)
print('Transiciones:', b.transitions)
print('Epsilon transiciones:', b.epsilon_transitions)

c = State(2)
c.add_epsilon_transition(a)
c.add_epsilon_transition(b)

# display(c)

c.to_deterministic()



automaton = DFA(states=3, finals=[2], transitions={
    (0, 'a'): 0,
    (0, 'b'): 1,
    (1, 'a'): 2,
    (1, 'b'): 1,
    (2, 'a'): 0,
    (2, 'b'): 1,
})
print('Original (DFA):')
# display(automaton)

automaton = State.from_nfa(automaton)
print('Copia (State):')
# display(automaton)

assert automaton.recognize('ba')
assert automaton.recognize('aababbaba')

assert not automaton.recognize('')
assert not automaton.recognize('aabaa')
assert not automaton.recognize('aababb')

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            # Your code here!!!
            regex_clase = Regex(regex)
            print("regex_clase.automton")
            print(regex_clase.regex)
            print(token_type)
            automat, states = State.from_nfa(regex_clase.automaton, True)
            finals = [state for state in states if state.final]
            for final in finals:
                final.tag = (n, token_type)
            regexs.append(automat)
            # - Remember to tag the final states with the token_type and priority.
            # - <State>.tag might be useful for that purpose ;-)
            # pass
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        # Your code here!!!
        for regex in self.regexs:
            start.add_epsilon_transition(regex)
        #---------------end-------------------
        return start.to_deterministic()
    
        
    def _walk(self, string):
        state = self.automaton 
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            # Your code here!!!
            lex = lex + symbol
            if state.has_transition(symbol):
                state = state.transitions[symbol][0]
                if state.final:
                    final = state
                    final_lex = lex
            else:
                return final, final_lex

        # final_lex = lex  
        #---------------end----------------------
        return final, final_lex
    
    def _tokenize(self, text):
        # Your code here!!!
        while len(text) > 0:
            if text == 0: break
            final,final_lex = self._walk(text)
            min_tag = sys.maxsize
            for state in final.state:
                if state.final:
                    n, token_type = state.tag
                    if n < min_tag:
                        min_tag = n
                        final_type = token_type
            text = text[len(final_lex):]
            yield final_lex,final_type
                        
        #---------------end------------------------
        
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]

nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

print('Non-zero digits:', nonzero_digits)
print('Letters:', letters)

# lexer = Lexer([
#     ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
#     ('for' , 'for'),
#     ('let', 'let'),
#     ('in', 'in'),
#     ('foreach' , 'foreach'),
#     ('sum', '+'),
#     ('equal', '='),
#     ('space', '  *'),
#     ('id', f'({letters})({letters}|0|{nonzero_digits})*')
# ], 'eof')

lexer = Lexer([
    ('type_a_clausura' , 'a*'),
    ('type_ba_a_clausura_clausura', '(baa*)*'),
    ('type_b_or_epsilon', 'b|c')
], 'eof')

# lexer = Lexer([
#     ('space', '  *'),
# ], 'eof')

# text = '5465 for 45foreach fore'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
# assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']

# text = '4forense forforeach for4foreach foreach 4for'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['num', 'id', 'space', 'id', 'space', 'id', 'space', 'foreach', 'space', 'num', 'for', 'eof']
# assert [t.lex for t in tokens] == ['4', 'forense', ' ', 'forforeach', ' ', 'for4foreach', ' ', 'foreach', ' ', '4', 'for', '$']

# text = 'let x = read in 2 + x + 5'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['let', 'space', 'id', 'space', 'equal', 'space', 'id', 'space', 'in', 'space', 'num', 'space', 'sum', 'space', 'id', 'space', 'sum', 'space', 'num', 'eof']
# assert [t.lex for t in tokens] == ['let', ' ', 'x', ' ', '=', ' ', 'read', ' ', 'in', ' ', '2', ' ', '+', ' ', 'x', ' ', '+', ' ', '5', '$']

# text = 'b'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['type_b_or_epsilon', 'eof']
# assert [t.lex for t in tokens] == ['b', '$']

# assert not [t.token_type for t in tokens] == ['type_ba_a_clausura_clausura', 'eof']

# text = 'aaaa'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['type_a_clausura', 'eof']
# assert [t.lex for t in tokens] == ['aaaa', '$']

# # # assert [t.token_type for t in tokens] == ['type_a_clausura', 'type_a_clausura', 'type_a_clausura', 'type_a_clausura', 'eof']
# # # assert [t.lex for t in tokens] == ['a', 'a', 'a', 'a', '$']

# text = 'baaaa'
# print(f'\n>>> Tokenizando: "{text}"')
# tokens = lexer(text)
# print(tokens)
# assert [t.token_type for t in tokens] == ['type_ba_a_clausura_clausura', 'eof']
# assert [t.lex for t in tokens] == ['baaaa' '$']

text = 'baaaab'
print(f'\n>>> Tokenizando: "{text}"')
tokens = lexer(text)
print(tokens)