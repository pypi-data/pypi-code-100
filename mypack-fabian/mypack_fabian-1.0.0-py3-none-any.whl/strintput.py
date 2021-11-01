import clear

# = string integer input checker

# ¤ Makes a string from an integer taken from input by trying input until it doesnt crash


def strintput(printable, value_error_text = "You didnt write a number."):
    while True:
        try:
            stringput = input(printable)
            if stringput.startswith("0"):
                choice = "0" + str(int(stringput))
            else:
                choice = str(int(stringput))

            return choice

        except ValueError:
            clear()
            print(value_error_text)