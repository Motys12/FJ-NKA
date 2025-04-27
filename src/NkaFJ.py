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
                    next_states.extend(state.transitions[string[pos]])
                    print(f"Transition on '{string[pos]}': {state} -> {state.transitions[string[pos]]}")
                else:
                    print(f"No valid transition for '{string[pos]}' at state: {state}")

            if not next_states:
                print("No states to process for next character!")
                return False  

            return dfs(next_states, pos + 1)

        return dfs([self.start_state], 0)

def build_nka(node, has_LCBRA=False):
    if isinstance(node, tuple):
        # print(f"Processing node: {node[0]}")
        if node[0] == "element":
            symbol = node[1]
            if isinstance(symbol, tuple) and symbol[0] == "SYMBOL":
                # print(f"Processing SYMBOL: {symbol[1]}")
                start_state = State(is_accepting=False)
                accept_state = State(is_accepting=False)
                start_state.add_transition(symbol[1], accept_state)
                print(f"Created transition {symbol[1]}: {start_state} -> {accept_state}")
                
                return start_state, accept_state
            
            elif isinstance(symbol, tuple) and symbol[0] == "LCBRA": 
                print("Processing LCBRA")
                has_LCBRA=True
                inner_start, inner_accept = build_nka(symbol[1], has_LCBRA) 
                if inner_start is None or inner_accept is None:
                    raise ValueError("Error: start or accept state is None inside parentheses.") 

                print(f"Created group with existing states: {inner_start} -> {inner_accept}")
                return inner_start, inner_accept
    
            elif isinstance(symbol, tuple) and symbol[0] == "RCBRA":  
                print("Processing RCBRA (close bracket)")
                has_LCBRA=False;
                return None, None
            
            elif isinstance(symbol, tuple) and symbol[0] == "LBRCKT":  
                print("Processing LBRCKT ( [] )")
                inner_start, inner_accept = build_nka(symbol[1])

                start_state = State(is_accepting=True)
                accept_state = State(is_accepting=True)

                start_state.add_transition(None, inner_start)   
                start_state.add_transition(None, accept_state)  
                inner_accept.add_transition(None, accept_state)

                print(f"Created LBRCKT group with ε-skipping: {start_state} -> {accept_state}")
                return start_state, accept_state
            
            elif isinstance(symbol, tuple) and symbol[0] == "RBRCKT":  
                print("Processing RCBRKT (close square bracket)")
                return None, None
            
            elif isinstance(symbol, tuple) and symbol[0] in {"regular", "LCBRA", "RCBRA"}:
                return build_nka(symbol[1], has_LCBRA)
            else:
                raise TypeError(f"Неожиданный тип в элементе: {symbol[0]}")

        
        elif node[0] == "regular":
            # print(f"Processing regular expression: {node[1]}")
            return build_nka(node[1], has_LCBRA)
        
        
        elif node[0] == "alternative":
            # print(f"Processing alternative: {node[1]} | {node[2]}") 
            
            left_start, left_accept = build_nka(node[1])
            right_start, right_accept = build_nka(node[2])
            
            if has_LCBRA:
                start_state = State()
            else:
                start_state = State(is_accepting=True)
            accept_state = State(is_accepting=True)

            start_state.add_transition(None, left_start)
            start_state.add_transition(None, right_start)
            left_accept.add_transition(None, accept_state)
            right_accept.add_transition(None, accept_state)
            print(f"Created alternative start state: {start_state}")
            print(f"Created alternative accept state: {accept_state}")
            if has_LCBRA:
                accept_state.add_transition(None, start_state)
                print(f"Added ε-transition due to bracket: {accept_state} -> {start_state}")
                
            print(f"Created alternative: {start_state} -> ({left_start}, {right_start})")
            return start_state, accept_state
       
        elif node[0] == "sequence":
            # print(f"Processing sequence: {node[1]}")  
            
            start_state = None
            last_accept = None
            for child in node[1]:
                # print(f"Processing child in sequence: {child}")
                
                child_start, child_accept = build_nka(child, has_LCBRA)
                if start_state is None:
                    start_state = child_start
                else:
                    last_accept.add_transition(None, child_start)
                last_accept = child_accept
                

            start_state.is_accepting = True    
            last_accept.is_accepting = True

            if has_LCBRA:
                print(f"Adding ε-transition from {last_accept} to {start_state}")
                last_accept.add_transition(None, start_state)

            print(f"Created sequence starting at {start_state}")
            return start_state, last_accept    

def regex_to_nka(parsed_tree):
    start_state, accept_state = build_nka(parsed_tree)
    return NKA(start_state, [accept_state])
