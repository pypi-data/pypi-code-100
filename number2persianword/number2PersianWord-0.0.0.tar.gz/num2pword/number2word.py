words = ['', 'یک', 'دو', 'سه', 'چهار', 'پنج','شش' ,'هفت' ,'هشت' ,'نه' , 'ده','یازده', 'دوازده', 'سیزده', 'چهارده', 'پانزده', 'شانزده', 'هفده', 'هیجده', 'نوزده', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود']

def number2words(n: int) -> str:
    if n < 20:
        return words[n]
    elif n < (10**2):
        return words[18 + n // 10] + ('' if n % 10 == 0 else ' و ' + words[n % 10])
    elif n < (10**3):
        return number2words(n // (10**2)) + " صد" + (' و ' + number2words(n % (10**2)) if n % (10**2) > 0 else ' و ')
    elif n < (10**6):
        return number2words(n // (10**3)) + " هزار" + ('و ' + number2words(n % (10**3)) if n % (10**3) > 0 else ' و ')
    elif n < (10**9):
        return number2words(n // (10**6)) + " میلیون" + (' و ' + number2words(n % (10**6)) if n % (10**6) > 0 else ' و ')
    elif n < (10**12):
        return number2words(n // (10**9)) + " میلیارد" + (' و ' + number2words(n % (10**9)) if n % (10**9) > 0 else ' و ')
