from utils import Token
from state_class import *
import sys

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

        final_lex = lex  
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