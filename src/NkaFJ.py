class State:
    counter = 0
    
    def __init__(self, is_accepting=False):
        self.transitions = {}  
        self.is_accepting = is_accepting
        self.number = State.counter
        State.counter += 1

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)
        symbol_str = 'ε' if symbol is None else repr(symbol)
        print(f"Transition from (S{self.number}) to (S{state.number}) on symbol {symbol_str}")


    def __repr__(self):
        return f"<S{self.number} accepting={self.is_accepting}>"

class NKA:
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states

    def is_accepted(self, string):
        def epsilon_closure(states):
            closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                print(f"Processing state: {state}")
                if None in state.transitions:
                    for next_state in state.transitions[None]:
                        if next_state not in closure:
                            print(f"Adding state: {next_state}")
                            closure.add(next_state)
                            stack.append(next_state)
            return closure

        def dfs(current_states, pos):
            current_states = epsilon_closure(current_states)
            print(f"At position {pos}, current states: {current_states}")


            if pos == len(string):
                result = any(state.is_accepting for state in current_states)
                print(f"Final states: {current_states}, Is accepting? {result}")
                return result


            next_states = []
            for state in current_states:
                if string[pos] in state.transitions:
                    next_states.update(state.transitions[string[pos]])
                    print(f"Transition on '{string[pos]}': {state} -> {state.transitions[string[pos]]}")
               
            if not next_states:
                print("No states to process for next character!")
                return False  # Dead end, not accepted


            return dfs(next_states, pos + 1)

        return dfs([self.start_state], 0)

def build_nka(node):
    if isinstance(node, tuple):
        if node[0] == "element":
            symbol = node[1]
            if isinstance(symbol, tuple) and symbol[0] == "SYMBOL":
                start_state = State(is_accepting=False)
                accept_state = State(is_accepting=False)
                start_state.add_transition(symbol[1], accept_state)
                print(f"Created transition {symbol[1]}: {start_state} -> {accept_state}")
                return start_state, accept_state
            elif isinstance(symbol, tuple) and symbol[0] in {"regular", "LCBRA", "RCBRA"}:
                return build_nka(symbol[1])
            else:
                raise TypeError(f"Неожиданный тип в элементе: {symbol[0]}")
        
        elif node[0] == "regular":
            return build_nka(node[1])
        
        elif isinstance(node, tuple) and node[0] == "LCBRA":
            inner = node[1]  
            if inner[0] in {"alternative", "sequence"}:
                inner_start, inner_accept = build_nka(inner)

                start_state = State()
                accept_state = State(is_accepting=True)

                start_state.add_transition(None, inner_start)
                inner_accept.add_transition(None, inner_start) 
                inner_accept.add_transition(None, accept_state)

                return start_state, accept_state
            else:
                raise ValueError("Ожидался узел типа 'regular' после '{'")
        
        elif node[0] == "alternative":
            left_start, left_accept = build_nka(node[1])
            right_start, right_accept = build_nka(node[2])
            start_state = State()
            accept_state = State(is_accepting=True)
            start_state.add_transition(None, left_start)
            start_state.add_transition(None, right_start)
            left_accept.add_transition(None, accept_state)
            right_accept.add_transition(None, accept_state)
            print(f"Created alternative: {start_state} -> ({left_start}, {right_start})")
            return start_state, accept_state
       
        elif node[0] == "sequence":
            start_state = None
            last_accept = None
            for child in node[1]:
                child_start, child_accept = build_nka(child)
                if start_state is None:
                    start_state = child_start
                else:
                    last_accept.add_transition(None, child_start)
                last_accept = child_accept
                
            last_accept.is_accepting = True
            print(f"Created sequence starting at {start_state}")
            return start_state, last_accept
        
        else:
            raise TypeError(f"Неожиданный тип узла: {node[0]}")
    else:
        raise TypeError(f"Ожидался кортеж, но найден: {type(node)}")

def regex_to_nka(parsed_tree):
    start_state, accept_state = build_nka(parsed_tree)
    return NKA(start_state, [accept_state])
