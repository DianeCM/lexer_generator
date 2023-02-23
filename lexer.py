from .cmp.utils import Token
from .cmp.automata import State
from .nfa_dfa_class import DFA
from .regex import *
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
            automata = regex_clase.automaton
            print(automata.transitions)

            automat, states = State.from_nfa(automata, True)
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

        start_state, states = start.to_deterministic(True)

        self.automata_mini(states)

        return start_state

    def automata_mini(self, states):

        # states = []
        # states.append(states_[0])

        # states.append((1,2))
        # states.append((2,))
        # states.append((3,4))
        # states.append((4,))
        # states = [(0, start), (1,2), (2,), (3,4), (4,)]
        transitions={}

        print("DFA UNION")
        print("-----------------------------------------------------------------")

        # print("states")
        # print(states)

        # print("estado inicial")
        # print(states[0].state[0].state)
        # print(type(states[0].state[0].state))

        for i in range(0,len(states)):

            # print("STATE")
            # print(state.state)

            # state = states[i].state
            # print("Stateeeeeee")
            # print(state)
            # print(type(state))
            if i == 0:
                state = states[0]

                # state_sin_tupla = state[0].state

                state_sin_tupla = state.state[0].state
                # print("ESTADO INICIAL")
            else:
                state = states[i]

                if len(state.state) == 1:
                    # state_sin_tupla = state[0].state
                    state_sin_tupla = state.state[0].state
                else:
                    # estados = [temp.state for temp in state]
                    estados = [temp.state for temp in state.state]
                    # print("ESTADOS DE LA KEY")
                    # print(estados)
                    state_sin_tupla = tuple(estados)

            # if len(state.state) == 1:
            #     state_sin_tupla = state.state[0]
            # else:
            #     state_sin_tupla = state.state

            # print("state_sin_tupla")
            # print(state_sin_tupla)

            # print("state.transitions")
            # print(state.transitions)

            for key in state.transitions:

                # print("key")
                # print(key)

                if len(state.transitions[key][0].state) == 1:
                    transitions[state_sin_tupla, key] = state.transitions[key][0].state[0].state

                    # print("transitions[state.id, key]")
                    # print(transitions[state_sin_tupla, key])
                    # print(type(transitions[state_sin_tupla, key]))

                else:
                    estados = [temp.state for temp in state.transitions[key][0].state]
                    
                    # print("ESTADOS DEL DESTINO")
                    # print(estados)

                    transitions[state_sin_tupla, key] = tuple(estados)

                    # print("transitions[state.id, key]")
                    # print(transitions[state_sin_tupla, key])
                    # print(type(state_sin_tupla))

        # print("TRANSICIONES EN EL METODO")
        # for trans in transitions.items():
        #     print(trans[0])
        #     for item in trans[0]:
        #         if isinstance(item, tuple):
        #             for items in item:
        #                 print(type(items))
                
        #         print("=========================")
        #     print(trans[1])
        #     print("************************")

        print(transitions)

            # print("FOR VALUES")
            # for value in transitions.values():
            #     print(value.state)
            #     print(type(value.state))

        # assert all(isinstance(value, int) for value in transitions.values())

        print("-----------------------------------------------------------------------------------")

        # transitions[state.id, symbol]

        
                    # finals.append(state.state)

        # finals = [ state.state for state in states if state.final ]

        dicc = { state: {} for state in range(len(states)) }
        # print("DICC")
        # print(dicc)
        # count=0
        # for key in transitions.keys():
        #     dicc[key[0]] = count
        #     count+=1

        for item in transitions.keys():
            if item[0] in dicc:
                dicc[item[0]] = item[0]

        # print("DICC")
        # print(dicc)

        for item in transitions.values():
            if item in dicc:
                dicc[item] = item

        # print("DICC")
        # print(dicc)

        for trans in transitions.keys():
            if not trans[0] == 0 and not trans[0] in dicc:
                for item in dicc.keys():
                    if not item == 0 and not dicc[item] and not trans[0] in dicc.values():
                        dicc[item] = trans[0]
                        break

        # print("DICC")
        # print(dicc)

                

        for trans in transitions.values():
            if not trans in dicc:
                for item in dicc.keys():
                    if not item == 0 and not dicc[item] and not trans in dicc.values():
                        dicc[item] = trans
                        break

        # print("DICC")
        # print(dicc)

        

        dicc_act = {value:key for (key,value) in dicc.items()}
        # print("dicc_act")
        # print(dicc_act)

        transitions_act={}
        # for item in dicc.keys():
        #     if item == 0:
        #         transitions_act[item]=transitions[dicc[item]]

        for item in transitions.keys():
            transitions_act[dicc_act[item[0]], item[1]]=transitions[item]

        # finals_temp=[]
        # for item in finals:
        #     finals_temp.append(dicc_act[item])

        

        finals = []
        for i in range(0, len(states)):
            state = states[i]
            if state.final:
                if i == 0:
                    # print("state.state[0].state")
                    # print(state.state[0].state)
                    finals.append(state.state[0].state)
                else:
                    if len(state.state) == 1:
                        finals.append(dicc_act[state.state[0].state])
                    else:
                        estados = [temp.state for temp in state.state]
                        finals.append(dicc_act[tuple(estados)])
                        # print("ESTADOSSS")
                        # print(estados)

        # print("finals_temp")
        # print(finals)


        # # for item in transitions.items():
        # #     transitions_act[dicc[item[1]]] = item[1]

        # print("Transiciones")
        # print(transitions)
        # print("Transiciones actualizadas")
        # print(transitions_act)

        dfa = DFA(len(states), finals, transitions_act)
        self.automata_dfa_mini = automata_minimization(dfa)
        print("DFA")
        print(dfa.transitions)

        print("MINI")
        print(self.automata_dfa_mini.transitions)
    
        
    def _walk(self, string):
        state = self.automaton 
        final = state if state.final else None
        final_lex = lex = ''

        transitions = []
        # transitions.append(state)
        
        for symbol in string:
            # Your code here!!!
            lex = lex + symbol
            if state.has_transition(symbol):
                # print("state.transitions")
                # print(state.transitions[symbol])
                state_ant= state
                state = state.transitions[symbol][0]
                print(type(state))
                
                transitions.append((state_ant, symbol, state))
                print("tupla")
                print((state_ant, symbol, state))
                if state.final:
                    final = state
                    final_lex = lex
            else:
                return final, final_lex, transitions

        # final_lex = lex  
        #---------------end----------------------
        return final, final_lex, transitions
    
    def _tokenize(self, text):
        transitions = []
        # Your code here!!!
        while len(text) > 0:
            if text == 0: break
            final, final_lex, transitions = self._walk(text)
            min_tag = sys.maxsize
            for state in final.state:
                if state.final:
                    n, token_type = state.tag
                    if n < min_tag:
                        min_tag = n
                        final_type = token_type
            text = text[len(final_lex):]
            yield final_lex, final_type, transitions
                        
        #---------------end------------------------
        
        yield '$', self.eof, transitions
    
    def __call__(self, text):
        return [ (Token(lex, ttype), transitions) for lex, ttype, transitions in self._tokenize(text) ]

nonzero_digits = '|'.join(str(n) for n in range(1,10))
letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

print('Non-zero digits:', nonzero_digits)
print('Letters:', letters)

# lexer = Lexer([
#     ('exp_diane', 'ab*bb|a'),
# ], 'eof')

# lexer = Lexer([
#     ('exp1', 'ab*b|a')
# ], 'eof')

# lexer = Lexer([
#     ('exp1', 'ab*b|a')
#     # ('exp2', 'b|a')
# ], 'eof')

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
    ('for' , 'a*(a|b)*cd | ε'),
    # ('exp_diane', '(ab*)b(b|a)'),
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
list_tokens_transitions = lexer(text)

for tokens, transitions in list_tokens_transitions:
    print(tokens)
    print(transitions)