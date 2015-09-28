from django import template
from web.model_choices import LINK_URLS

register = template.Library()

def avatar(user, size):
    return user.preferences.avatar(size)
register.filter('avatar', avatar)

def linkUrl(link):
    if hasattr(link['value'], 'id'):
        return LINK_URLS[link['type']].format(link['value'].id)
    return LINK_URLS[link['type']].format(link['value'])
register.filter('linkUrl', linkUrl)
