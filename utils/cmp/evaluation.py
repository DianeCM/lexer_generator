from cmp.pycompiler import EOF
# from cmp.tools.parsing import ShiftReduceParser

def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token.lex)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(rule is None for rule in attributes[1:]), 'There must be only synteticed attributes.'
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stack[-len(body):]
                value = rule(None, synteticed)
                stack[-len(body):] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception('Invalid action!!!')

    assert len(stack) == 1
    assert isinstance(next(tokens).token_type, EOF)
    return stack[0]

def evaluate_parse(left_parse, tokens):
    if not left_parse or not tokens:
        return
    
    left_parse = iter(left_parse)
    tokens = iter(tokens)
    result = evaluate(next(left_parse), left_parse, tokens)
    
    assert isinstance(next(tokens).token_type, EOF)
    return result

def evaluate(production, left_parse, tokens, inherited_value=None):
    head, body = production
    attributes = production.attributes
    
    synteticed = [None] * len(attributes)
    inherited = [None] * len(attributes)
    inherited[0] = inherited_value

    for i, symbol in enumerate(body, 1):
        if symbol.IsTerminal:
            assert inherited[i] is None
            next_token = next(tokens)
            assert next_token.token_type == symbol 
            synteticed[i] = next_token.lex
        else:
            next_production = next(left_parse)
            assert symbol == next_production.Left
            inherited_value = attributes[i](inherited,synteticed) if attributes[i] != None else None
            inherited_value = evaluate(next_production, left_parse, tokens, inherited_value)
            synteticed[i] = inherited_value
    return attributes[0](inherited,synteticed)

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, tokens, ope=False,tokens_list = []):
        stack = [0]
        cursor = 0
        output = []
        operations = []
        errors = []

        while True:
            state = stack[-1]
            lookahead = tokens[cursor]
            try:
                action, tag = self.action[state, lookahead]
                # Shift case
                if action == self.SHIFT:
                    operations.append(self.SHIFT)
                    stack.append(tag)
                    cursor += 1

                # Reduce case
                elif action == self.REDUCE:
                    operations.append(self.REDUCE)
                    output.append(tag)
                    for _ in tag.Right:
                        stack.pop()
                    a = self.goto[stack[-1], tag.Left.name]
                    stack.append(a)

                # OK case
                elif action == self.OK:
                    return errors, output, operations if ope else output
                # Invalid case
                else:
                    raise NameError
            except KeyError:
                errors.append(tokens[cursor]+" "+"Ln"+ ": "+str(tokens_list[cursor].Ln)+", Col: "+str(tokens_list[cursor].Col) )
                return errors, output, operations if ope else output


    # def __call__(self, w):
    #     stack = [ 0 ]
    #     cursor = 0
    #     output = []
        
    #     while True:
    #         state = stack[-1]
    #         lookahead = w[cursor]
    #         if self.verbose: print(stack, '<---||--->', w[cursor:])
                
    #         # Your code here!!! (Detect error)
            
    #         action, tag = self.action[state, lookahead]
    #         # Your code here!!! (Shift case)
    #         # Your code here!!! (Reduce case)
    #         # Your code here!!! (OK case)
    #         # Your code here!!! (Invalid case)

