from .utils import ContainerSet, pprint, inspect
from .pycompiler import Grammar
from itertools import islice
from collections import defaultdict

def compute_local_first(firsts, alpha):
    first_alpha = ContainerSet()
    
    for xi in alpha:
        firsts_Xi = firsts[xi]
        first_alpha.update(firsts_Xi)
        if not firsts_Xi.contains_epsilon: break
    else: first_alpha.set_epsilon()

    # First(alpha)
    return first_alpha

def compute_firsts(G):
    firsts = {}
    change = True
    
    # init First(Vt)
    for terminal in G.terminals:
        firsts[terminal] = ContainerSet(terminal)
        
    # init First(Vn)
    for nonterminal in G.nonTerminals:
        firsts[nonterminal] = ContainerSet()
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            # get current First(X)
            first_X = firsts[X]
                
            # init First(alpha)
            try:
                first_alpha = firsts[alpha]
            except KeyError:
                first_alpha = firsts[alpha] = ContainerSet()
            
            # CurrentFirst(alpha)???
            local_first = compute_local_first(firsts, alpha)
            
            # update First(X) and First(alpha) from CurrentFirst(alpha)
            change |= first_alpha.hard_update(local_first)
            change |= first_X.hard_update(local_first)
                    
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

def compute_follows(G, firsts):
    follows = defaultdict(ContainerSet)
    change = True
    
    # init Follow(Vn)
    for nonterminal in G.nonTerminals:
        follows[nonterminal] = ContainerSet()
    follows[G.startSymbol] = ContainerSet(G.EOF)
    
    while change:
        change = False
        
        # P: X -> alpha
        for production in G.Productions:
            X = production.Left
            alpha = production.Right
            
            follow_X = follows[X]
                
            for i,Y in enumerate(alpha,1):
                if Y.IsNonTerminal:
                    beta = alpha[i:]
                    firsts_beta = compute_local_first(firsts,beta) if beta not in firsts else firsts[beta]
                    change |= follows[Y].update(firsts_beta)
                    if firsts_beta.contains_epsilon: change |= follows[Y].update(follow_X)
            
    return follows

def build_parsing_table(G, firsts, follows):
    # init parsing table
    M = defaultdict(list)

    # P: X -> alpha
    for production in G.Productions:
        X = production.Left
        alpha = production.Right
        
        for terminal in firsts[alpha]:
            # working with symbols on First(alpha) ...
            M[X,terminal].append(production)

        # working with epsilon...
        if firsts[alpha].contains_epsilon:
            for terminal in follows[X]:
                M[X,terminal].append(production)
    
    # parsing table is ready!!!
    return M   



def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    
    # checking table...
    if M is None:
        if firsts is None:
            firsts = compute_firsts(G)
        if follows is None:
            follows = compute_follows(G, firsts)
        M = build_parsing_table(G, firsts, follows)
    
    # parser construction...
    def parser(w):
        # w ends with $ (G.EOF)
        print("table")
        pprint(M)
        print(M.keys())
        print("w")
        print(w)
        # for key in M.keys():
        #     print(type(key[0]))
        #     print(type(key[1]))
    
        # init:
        stack = [G.EOF, G.startSymbol]
        cursor = 0
        output = []
        
        # parsing w...
        while True:
            top = stack.pop()
            a = w[cursor]
            if top == G.EOF: break
            if top.IsTerminal:
                print("top como terminal")
                print(top)
                print(a)
                if top == a:
                    print("top es igual a 'a'")
                assert top == a
                cursor+=1
            elif top.IsNonTerminal:
                print("M[top, a]")
                print(M[top, a])
                print("top")
                print(top)
                print("a")
                print(a)
                print(type(a))

                production = M[top, a][0]
                output.append(production)
                if production.IsEpsilon:continue
                symbols = production.Right[::-1]
                for item in symbols: stack.append(item)
            else: raise Exception("Malformed Expression!!")
        # left parse is ready!!!
        return output
    
    # parser is ready!!!
    return parser

deprecated_metodo_predictivo_no_recursivo = metodo_predictivo_no_recursivo
def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M, firsts, follows)
    def updated(tokens):
        print("tokens")
        print(tokens)
        return parser([t.token_type for t in tokens])
    return updated