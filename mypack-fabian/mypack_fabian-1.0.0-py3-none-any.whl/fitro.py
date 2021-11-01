import intput

def fitro(
    action, choices
):  # ¤ takes the action input as a string and the choices as a list
    choice_text = "["  # ¤ starts the text conversion of the list
    # ¤ converts the text into the [n = choiceN, n2 = choiceN2] format
    for i in range(len(choices)):
        n = i + 1
        if n < len(choices):
            choice_text += f"{n} = {choices[i]}, "
        else:
            choice_text += f"{n} = {choices[i]}]"
    # ¤ takes user input and returns item chosen from list
    return choices[(intput(f"{action} {choice_text}: ") - 1)]