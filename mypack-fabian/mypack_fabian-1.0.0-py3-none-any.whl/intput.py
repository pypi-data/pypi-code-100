import clear

# = integer input checker

# ¤ Makes an int from input by trying the input until it doesnt crash


def intput(printable, value_error_text = "You didnt write a number."):

    while True:
        try:
            choice = int(input(printable))
            return choice

        except ValueError:
            clear()
            print(value_error_text)

