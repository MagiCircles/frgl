from django import template
from web.model_choices import LINK_URLS

register = template.Library()

def avatar(user, size):
    return user.preferences.avatar(size)
register.filter('avatar', avatar)

def linkValueUrl(type, value):
    return LINK_URLS[type].format(value)
register.filter('linkValueUrl', linkValueUrl)

def linkUrl(link):
    return linkValueUrl(link['type'], link['value'].id if hasattr(link['value'], 'id') else link['value'])
register.filter('linkUrl', linkUrl)
