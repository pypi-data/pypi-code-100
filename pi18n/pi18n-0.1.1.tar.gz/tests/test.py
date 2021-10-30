from tests import translation_service

translation = translation_service.get("HELLO_WORLD")
print(f"Message in Spanish: {translation}")

translation = translation_service.get("WITH_PARAMS", fruit1="apple", fruit2="orange", fruit3="banana")
print(f"Message with params: {translation}")

translation_service.change_locale("en")
translation = translation_service.get("HELLO_WORLD")
print(f"Message in English: {translation}")

params = {"fruit1": "apple", "fruit2": "orange", "fruit3": "banana"}
translation = translation_service.get("WITH_PARAMS", params)
print(f"Message with params: {translation}")
