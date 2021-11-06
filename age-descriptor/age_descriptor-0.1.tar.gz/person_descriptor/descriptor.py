def get_description(age: int) -> str:
    if age < 0:
        return f"Podany wiek jest błędny: {age}"
    if age < 18:
        return f"Nastolatek"
    if age < 30:
        return f"Mlody"
    if age < 50:
        return f"dojrzaly"
    if age < 65:
        return f"wiekowy"
    return "Emeryt"