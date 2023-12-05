from django import template
register = template.Library()

@register.filter()
def color_filter_impulse(type):
    if type == "L":
        return 'bg-success'
    elif type == "S":
        return 'bg-danger'
    else:
        return ''

@register.filter()
def color_filter_impulse_text(type):
    if type == "L" or type == "S":
        return 'color:white;'
    else:
        return ''
    
@register.filter()
def color_filter_count_level(value):
    if value['count_level'] != '':
        if value['count_level'] > 0:
            if value['type'] == 'L':
                return 'bg-success'
            else:
                return 'bg-danger'
        else:
            return ''
    else:
        return ''
        
@register.filter()
def color_filter_count_level_text(value):
    if value['count_level'] != '':
        if value['count_level'] > 0:
            return 'color:white;'
        else:
            return ''
    else:
        return ''

@register.filter()
def filter_count_dict(dict : dict):
    return len(dict) + 1

@register.filter()
def filter_type(dict : dict):
    if dict['type'] == 1:
        return "table-success"
    elif dict['type'] == 2:
        return "table-danger"
    
@register.filter()
def filter_links(symbol):
    return "window.open('https://www.binance.com/ru/trade/" + symbol + "_USDT'); window.open('https://www.binance.com/ru/futures/" + symbol + "USDT');"

@register.filter()
def filter_links2(symbol):
    return "https://www.binance.com/ru/trade/" + symbol + "_USDT"
