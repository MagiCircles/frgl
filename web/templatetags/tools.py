from django import template
register = template.Library()

def mod(value, arg):
    return value % arg == 0
register.filter('mod', mod)

def split(string, splitter=","):
    if string:
        return string.split(splitter)
    return []
register.filter('split', split)

def addint(string, int):
    return string + unicode(int)
register.filter('addint', addint)

def times(value):
        return range(value)
register.filter('times', times)

def padzeros(value, length):
    if value is None:
        return None
    return ("%0" + str(length) + "d") % value
register.filter('padzeros', padzeros)

def isnone(value):
    return value is None
register.filter('isnone', isnone)

def torfc2822(date):
    return date.strftime("%B %d, %Y %H:%M:%S %z")
register.filter('torfc2822', torfc2822)
