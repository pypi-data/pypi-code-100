import re

def clean_no(no):
    no = re.sub(r'[^0-9]', '', no)
    return no

def validate_no(no, field, msg):
    if len(no) < 8 or len(no) > 11:
        val_msg = f'{msg}{field} is less than 8 or greater than 11 digits. '
    elif (no.startswith('61') and len(no) < 11):
        val_msg = f'{msg}{field} has missing digit(s). '
    else:
        val_msg = msg
    return val_msg

def format_no(no, state_code):
    #Ex: 61410206170 -> 0410206170
    if no.startswith('61'):
        local_no = no[3:]
        area_code = no[2]
        no = '0' + area_code + local_no
    #Ex: 0410206170, 13XX XXX XXX, 18XX XXX XXX
    elif no.startswith('0') or no.startswith('13') or no.startswith('18'):
        pass
    #Ex: 410206170 -> 0410206170
    elif not(no.startswith('0')) and len(no) == 9:
        no = '0' + no
    #Ex: not a fixed line: 10206170 -> 0410206170
    elif no[0] not in ['9','8','7','4','5','6','3','2'] and len(no) == 8:
        no = '04' + no
    elif state_code in ['NSW', 'ACT'] and len(no) == 8:
        no = '02' + no
    elif state_code in ['VIC', 'TAS'] and len(no) == 8:
        no = '03' + no
    elif state_code == 'QLD' and len(no) == 8:
        no = '07' + no
    elif state_code in ['WA', 'SA', 'NT'] and len(no) == 8:
        no = '08' + no    
    return no

def validator(no, state_code, field_name, msg):
    no_cleaned = clean_no(no)
    val_msg = validate_no(no_cleaned, field_name, msg)
    no_formatted = format_no(no_cleaned, state_code)
    return no_formatted, val_msg