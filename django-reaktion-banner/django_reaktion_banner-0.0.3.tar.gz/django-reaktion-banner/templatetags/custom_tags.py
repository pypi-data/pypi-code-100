from django import template

register = template.Library()

def calculate_kpi(value, arg):    
    if arg == "view":
        if value.impressions == 0:
            return 0
        return round((value.views/value.impressions) * 100)
    if arg == "click":
        if value.views == 0:
            return 0
        return round((value.clicks/value.views) * 100)

    return value
    
register.filter('calculate_kpi', calculate_kpi)