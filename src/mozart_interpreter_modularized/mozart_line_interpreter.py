import mozart_lex
import mozart_parser

fp = open("../../data/mozart_code_examples/example_1.mozart", "r", encoding="utf-8")
code_lines = fp.readlines()

stack = ["OPEN_SCOPE"]
# Interpretador
program_counter = 0
debug = False
while True:
    if code_lines[program_counter].strip() != "":
        out = mozart_parser.parse(code_lines[program_counter])
        print("pc", program_counter + 1, "parser out:", out, "start_stack:", stack)
        if type(out) == tuple:
            if out[0] == "if" and out[1] == True:
                # if é verdadeiro -> segue normalmente o fluxo, pulando o bloco else
                stack.append("if_true")
            elif out[0] == "if" and out[1] == False:
                stack.append("if_false")
                # if é falso, pule ao bloco else e execute normalmente seguindo em frente
                # run lexer until find a END_SCOPE
                close_line = -1
                control_stack = ["OPEN_SCOPE"]
                for i in range(program_counter + 1, len(code_lines)):
                    mozart_lex.lexer.input(code_lines[i])

                    for token in mozart_lex.lexer:
                        if "OPEN_SCOPE" in str(token):
                            control_stack.append("OPEN_SCOPE")
                        if "END_SCOPE" in str(token):
                            control_stack.pop()

                        if len(control_stack) == 0:
                            close_line = i - 1
                            break
                    if close_line != -1:
                        break
                program_counter = close_line
            elif out[0] == "else":
                if len(stack) == 0:
                    print("[ERROR] Is this else necessary? The scope stack is empty!")
                if stack[-1] == "if_true":
                    # Então esse bloco de código deve ser pulado, pois o bloco a executar era do if
                    stack.pop()
                    close_line = -1
                    control_stack = ["OPEN_SCOPE"]
                    for i in range(program_counter + 1, len(code_lines)):
                        mozart_lex.lexer.input(code_lines[i])
                        for token in mozart_lex.lexer:
                            if "OPEN_SCOPE" in str(token):
                                control_stack.append("OPEN_SCOPE")
                            if "END_SCOPE" in str(token):
                                control_stack.pop()

                            if len(control_stack) == 0:
                                close_line = i
                                break
                        if close_line != -1:
                            break
                    program_counter = close_line
                elif stack[-1] == "if_false":
                    # o bloco deve ser executado normalmente, pois caiu no else
                    stack.pop()
            elif out[0] == "while":
                if out[1]:
                    # The condition is true, so run the loop normally
                    stack.append(("loop", program_counter - 1))
                else:
                    # The condition is false, so go to the end of the loop
                    close_line = -1
                    control_stack = ["OPEN_SCOPE"]
                    for i in range(program_counter + 1, len(code_lines)):
                        mozart_lex.lexer.input(code_lines[i])

                        for token in mozart_lex.lexer:
                            if "OPEN_SCOPE" in str(token):
                                control_stack.append("OPEN_SCOPE")
                            if "END_SCOPE" in str(token):
                                control_stack.pop()

                            if len(control_stack) == 0:
                                close_line = i
                                break
                        if close_line != -1:
                            break
                    program_counter = close_line
            else:
                print("Ih rapaz!")
        elif type(out) == str:
            if out == "END_SCOPE":
                if type(stack[-1]) == tuple:
                    if stack[-1][0] == "loop":
                        program_counter = stack[-1][1]
                        stack.pop()
                else:
                    stack.pop()
    program_counter += 1
    if program_counter == len(code_lines):
        break

    # Debug
    if debug:
        mozart_lex.lexer.input(code_lines[program_counter])
        for token in mozart_lex.lexer:
            print(token)

print("final state", mozart_parser.program_state)
print("final stack", stack)
