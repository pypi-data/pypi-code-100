from person_descriptor.descriptor import get_description


def start_app():
    while True:
        print("Aby zakończyć aplikację wpisz x")
        given_age = input("Podaj swój wiek: ")

        if given_age == "x":
            print("Do widzenia")
            exit()

        age_description = get_description(int(given_age))
        print(f"Twoja grupa wiekowa to: {age_description}")
