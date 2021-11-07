def get_description(age: int) -> str:
    print(__name__)
    if age <= 0:
        return f"Podany wiek jest błędny: {age}"
    if age < 18:
        return "Nastolatek"
    if age < 30:
        return "Mlody"
    if age < 50:
        return "Dojrzaly"
    if age < 65:
        return "Wiekowy"
    return "Emeryt"
