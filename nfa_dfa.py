from cmp.utils import ContainerSet, DisjointSet

from nfa_dfa_class import *


#-----------------------CP6--------------------------------------

# automaton = NFA(states=6, finals=[3, 5], transitions={
#     (0, ''): [ 1, 2 ],
#     (1, ''): [ 3 ],
#     (1,'b'): [ 4 ],
#     (2,'a'): [ 4 ],
#     (3,'c'): [ 3 ],
#     (4, ''): [ 5 ],
#     (5,'d'): [ 5 ]
# })
# automaton

def move(automaton, states, symbol):
    moves = set()
    for state in states:
       try:
            moves.update(automaton.transitions[state][symbol])
       except:
           continue
    return moves

# # assert move(automaton, [1], 'a') == set()
# # assert move(automaton, [2], 'a') == {4}
# # assert move(automaton, [1, 5], 'd') == {5}

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        try: 
            next=automaton.transitions[state]['']
            add_pending=[s for s in next if s not in closure and s not in pending]
            #if len(): pending=list(set(pending).union(next))
            pending = pending + add_pending
            closure.update(next)
        except KeyError:
            continue         
    return ContainerSet(*closure)

# # assert epsilon_closure(automaton, [0]) == {0,1,2,3}
# # assert epsilon_closure(automaton, [0, 4]) == {0,1,2,3,4,5}
# # assert epsilon_closure(automaton, [1, 2, 4]) == {1,2,3,4,5}


def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]

    pending = [ start ]
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            next=epsilon_closure(automaton,move(automaton, state.set, symbol))
            if len(next.set)==0: continue
            next.id=len(states)
            for s in states:
                if s.set==next.set: 
                    next.id=s.id
                    break
            else:
                    states.append(next)
                    pending.append(next)
                    next.is_final = any(s in automaton.finals for s in next.set)
            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol]=next.id

    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa


# dfa = nfa_to_dfa(automaton)
# # display(dfa)

# assert dfa.states == 4
# assert len(dfa.finals) == 4

# assert dfa.recognize('')
# assert dfa.recognize('a')
# assert dfa.recognize('b')
# assert dfa.recognize('cccccc')
# assert dfa.recognize('adddd')
# assert dfa.recognize('bdddd')

# assert not dfa.recognize('dddddd')
# assert not dfa.recognize('cdddd')
# assert not dfa.recognize('aa')
# assert not dfa.recognize('ab')
# assert not dfa.recognize('ddddc')

#-------------------CP7---------------------------------------

# automaton = DFA(states=2, finals=[1], transitions={
#     (0,'a'):  0,
#     (0,'b'):  1,
#     (1,'a'):  0,
#     (1,'b'):  1,
# })
# automaton

def automata_union(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        destinations=list(map(lambda x : x +d1, destinations))
        transitions[origin+d1,symbol]=destinations

    for (origin, symbol), destinations in a2.map.items():
        ## Relocate a2 transitions ...
        destinations=list(map(lambda x : x +d2,destinations))
        transitions[origin+d2,symbol]=destinations
    
    ## Add transitions from start state ...
    transitions[0,''] = [d1,d2]
    
    ## Add transitions to final state ...
    for state in a1.finals:
        try:
            transitions[state+d1,''].append(final)
        except KeyError:
            transitions[state+d1,'']=[final]
    for state in a2.finals:
        try:
            transitions[state+d2,''].append(final)
        except KeyError:
             transitions[state+d2,'']=[final]
            
    states = a1.states + a2.states + 2
    finals = { final }
    return NFA(states, finals, transitions, start)

# union = automata_union(automaton, automaton)
# # display(union)
# recognize = nfa_to_dfa(union).recognize

# assert union.states == 2 * automaton.states + 2

# assert recognize('b')
# assert recognize('abbb')
# assert recognize('abaaababab')

# assert not recognize('')
# assert not recognize('a')
# assert not recognize('abbbbaa')


def automata_concatenation(a1, a2):
    transitions = {}
    
    start = 0
    d1 = 0
    d2 = a1.states + d1
    final = a2.states + d2
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate a1 transitions ...
        transitions[origin+d1,symbol]=destinations
        

    for (origin, symbol), destinations in a2.map.items():
        destinations=list(map(lambda x : x +d2,destinations))
        transitions[origin+d2,symbol]=destinations
    
    ## Add transitions to final state ...
    try:
        transitions[a1.states-1,''].append(a1.states)
    except KeyError:
       transitions[a1.states-1,''] = [a1.states]

    for state in a2.finals:
        try:
            transitions[state+d2,''].append(final)
        except KeyError:
            transitions[state+d2,'']=[final]
            
            
    states = a1.states + a2.states + 1
    finals = { final}
    return NFA(states, finals, transitions, start)

# concat = automata_concatenation(automaton, automaton)
# # display(concat)
# recognize = nfa_to_dfa(concat).recognize

# assert concat.states == 2 * automaton.states + 1

# assert recognize('bb')
# assert recognize('abbb')
# assert recognize('abaaababab')

# assert not recognize('')
# assert not recognize('a')
# assert not recognize('b')
# assert not recognize('ab')
# assert not recognize('aaaab')
# assert not recognize('abbbbaa')


def automata_closure(a1):
    transitions = {}
    
    start = 0
    d1 = 1
    final = a1.states + d1
    
    for (origin, symbol), destinations in a1.map.items():
        ## Relocate automaton transitions ...
        destinations=list(map(lambda x : x +d1, destinations))
        transitions[origin+d1,symbol]=destinations
    
    ## Add transitions from start state ...
        transitions[start,''] = [a1.start+1,final]
    
    ## Add transitions to final state and to start state ...
    for state in a1.finals:
        try:
            transitions[state+d1,''].append(final)
        except KeyError:
            transitions[state+d1,'']=[final]
    transitions[final,'']=[start]
            
    states = a1.states +  2
    finals = { final }
    return NFA(states, finals, transitions, start)

# closure = automata_closure(automaton)
# # display(closure)
# recognize = nfa_to_dfa(closure).recognize

# assert closure.states == automaton.states + 2

# assert recognize('')
# assert recognize('b')
# assert recognize('ab')
# assert recognize('bb')
# assert recognize('abbb')
# assert recognize('abaaababab')

# assert not recognize('a')
# assert not recognize('abbbbaa')



# dset = DisjointSet(*range(10))
# print('> Inicializando conjuntos disjuntos:\n', dset)

# dset.merge([5,9])
# print('> Mezclando conjuntos 5 y 9:\n', dset)

# dset.merge([8,0,2])
# print('> Mezclando conjuntos 8, 0 y 2:\n', dset)

# dset.merge([2,9])
# print('> Mezclando conjuntos 2 y 9:\n', dset)

# print('> Representantes:\n', dset.representatives)
# print('> Grupos:\n', dset.groups)
# print('> Nodos:\n', dset.nodes)
# print('> Conjunto 0:\n', dset[0], '--->', type(dset[0]))
# print('> Conjunto 0 [valor]:\n', dset[0].value, '--->' , type(dset[0].value))
# print('> Conjunto 0 [representante]:\n', dset[0].representative, '--->' , type(dset[0].representative))

# automaton = DFA(states=5, finals=[4], transitions={
#     (0,'a'): 1,
#     (0,'b'): 2,
#     (1,'a'): 1,
#     (1,'b'): 3,
#     (2,'a'): 1,
#     (2,'b'): 2,
#     (3,'a'): 1,
#     (3,'b'): 4,
#     (4,'a'): 1,
#     (4,'b'): 2,
# })
# automaton

def distinguish_states(group, automaton, partition):
    split = {}
    vocabulary = tuple(automaton.vocabulary)
    transitions = automaton.transitions

    for member in group:
        current_transitions=[automaton.states for _ in range(len(vocabulary))]
        for i,symbol in enumerate(vocabulary):
            try:
                # print(transitions[member][symbol])
                destination=list(transitions[member][symbol])[0]
                destination_group=partition[destination].representative
                current_transitions[i]=destination_group
            except KeyError:
                continue 
        current_transitions=tuple(current_transitions)
        try:
            split[current_transitions].append(member)
        except KeyError:
             split[current_transitions]=[member]     

    return [ group for group in split.values()]
            
def state_minimization(automaton):
    partition = DisjointSet(*range(automaton.states))
    
    ## partition = { NON-FINALS | FINALS }
    partition.merge(list(automaton.finals))
    non_finals=[i for i in range(automaton.states) if not i in list(automaton.finals)]
    partition.merge(non_finals)
    
    while True:
        new_partition = DisjointSet(*range(automaton.states))
        
        ## Split each group if needed (use distinguish_states(group, automaton, partition))
        for group in partition.groups:
            group=[node.value for node in group]
            subgroups=distinguish_states(group, automaton, partition)
            for g in subgroups:
                new_partition.merge(g)

        if len(new_partition) == len(partition):
            break

        partition = new_partition
        
    return partition

def automata_minimization(automaton):
    partition = state_minimization(automaton)
    states = [s for s in partition.representatives]
    
    transitions = {}
    for i, state in enumerate(states):
        origin = state.value
        # Your code here
        for symbol, destinations in automaton.transitions[origin].items():
            print("destinations")
            print(destinations)
            next=0
            for j in range(len(states)):
                if list(destinations)[0] in [node.value for node in partition.groups[j]]:
                    next=j
                    break
            try:
                transitions[i,symbol]
                assert False
            except KeyError:
                # Your code here
                transitions[i,symbol]=next
    
    ## finals = ???
    ## start  = ???
    # Your code here
    finals=[i for i in range(len(states)) if any( state.value in automaton.finals for state in partition.groups[i])]
    start=0
    for i in range(len(states)):
        if any (state == automaton.start for state in partition.groups[i] ):
            start=i
            break
    return DFA(len(states), finals, transitions, start)

# states = state_minimization(automaton)
# print(states)

# for members in states.groups:
#     all_in_finals = all(m.value in automaton.finals for m in members)
#     none_in_finals = all(m.value not in automaton.finals for m in members)
#     assert all_in_finals or none_in_finals
    
# assert len(states) == 4
# assert states[0].representative == states[2].representative
# assert states[1].representative == states[1]
# assert states[3].representative == states[3]
# assert states[4].representative == states[4]


# mini = automata_minimization(automaton)
# # display(mini)

# assert mini.states == 4

# assert mini.recognize('abb')
# assert mini.recognize('ababbaabb')

# assert not mini.recognize('')
# assert not mini.recognize('ab')
# assert not mini.recognize('aaaaa')
# assert not mini.recognize('bbbbb')
# assert not mini.recognize('abbabababa')