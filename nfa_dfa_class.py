import pydot

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        print("self.transitions")
        print(self.transitions)

        # dicc = {}
        # count=0
        # for key in transitions.keys():
        #     dicc[key[0]] = count
        #     count+=1
        
        # print("TRANSICIONES EN NFA")
        # print(self.transitions)
        # print("TRANSICIONES PROPIA EN LA CLASE NFA")
        # for trans in self.transitions.items():
        #     print(trans[0])
        #     if isinstance(trans[0], tuple):
        #         for item in trans[0]:
        #             if isinstance(item, tuple):
        #                 for items in item:
        #                     print(type(items))
        #             # print(type(item))
        #             print("=========================")
        #         # print(type(trans[0]))
        #     print("************************")
        # print(transitions)

        # print("TRANSICIONES EN LA CLASE NFA")
        # for trans in transitions.items():
        #     print(trans[0])
        #     for item in trans[0]:
        #         if isinstance(item, tuple):
        #             for items in item:
        #                 print(type(items))
        #         # print(type(item))
        #         print("=========================")
        #     # print(type(trans[0]))
        #     print("************************")

        print("transitions")
        print(transitions)

        for (origin, symbol), destinations in transitions.items():

            # print("ORIGINAL SYMBOL")
            # print(origin, symbol)
            # print("TIPO DE ORIGIN")
            # print(type(origin))
            # print(destinations)
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = set(destinations)
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                edge_id=str(start)+ " " + tran + " " + str(end)
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2,id=edge_id))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass


class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        # print("DFA TRANSICIONES STATE")
        # print(transitions)
        # print(finals)
        # assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        # print("TRANSICIONES DFA")
        # print("ANTES")
        # print(transitions)
        transitions = { key: [value] for key, value in transitions.items() }
        # print("DESPUES")
        # print(transitions)
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        try:
            temp=self.transitions[self.current]
            self.current=list(temp[symbol])[0]
        except:
            return False 
        return True 
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        for symbol in string:
            if not self._move(symbol): return False 
        final=self.current in self.finals
        self._reset()
        return final