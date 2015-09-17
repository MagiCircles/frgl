from django import template
from web import models

register = template.Library()
register.filter('attributeToString', models.attributeToString)
register.filter('cardTypeToString', models.cardTypeToString)
register.filter('skillTypeToString', models.skillTypeToString)
register.filter('skillToSentence', models.skillToSentence)
register.filter('triggerTypeToString', models.triggerTypeToString)
register.filter('rarityToString', models.rarityToString)
register.filter('rewardToString', models.rewardToString)
