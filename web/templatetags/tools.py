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
