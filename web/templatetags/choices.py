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
register.filter('playwithToString', models.playwithToString)
register.filter('statusToString', models.statusToString)
register.filter('statusToColor', models.statusToColor)
register.filter('statusToColorString', models.statusToColorString)
register.filter('linkToString', models.linkToString)
register.filter('linkRelevanceToString', models.linkRelevanceToString)
register.filter('osToString', models.osToString)
register.filter('activityMessageToString', models.activityMessageToString)
