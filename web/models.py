from django.db import models
from django.contrib.auth.models import User, Group
from django.core import validators
from django.utils.translation import ugettext_lazy as _, string_concat

class Performer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='performers')

    def __unicode__(self):
        return self.name

ATTRIBUTES = (
    ('crazy', _('Crazy')),
    ('cool', _('Cool')),
    ('hot', _('Hot')),
    ('deep', _('Deep')),
    ('fun', _('Fun')),
    ('classic', _('Classic')),
)
def attributeToString(attribute): return dict(ATTRIBUTES)[attribute]

CARD_TYPES = (
    ('reward', _('Reward')),
    ('boost', _('Boost')),
    ('unlock', _('Unlock')),
    ('stageup', _('Stage Up')),
)
def cardTypeToString(card_type): return dict(CARD_TYPES)[card_type]

SKILL_TYPES = (
    ('overthebar', _('Over the bar')),
    ('pitchperfect', _('Pitch Perfect')),
    ('greattiming', _('Great Timing')),
    ('vocalrun', _('Vocal Run')),
    ('extraeffort', _('Extra Effort')),
)
def skillTypeToString(skill_type): return dict(SKILL_TYPES)[skill_type]

SKILL_SENTENCES = (
    ('overthebar', _('Add {} points to the score')),
    ('pitchperfect', _('Add {} points to the score')),
    ('greattiming', _('Add {} points to the score')),
    ('vocalrun', _('Add {} points to the score')),
    ('extraeffort', _('Change all OK notes to Great, and Great notes to perfect for {} seconds')),
)
def skillToSentence(skill_type, value): return _(dict(SKILL_SENTENCES)[skill_type]).format(value)

TRIGGER_TYPES = (
    ('greattiming', _('Every {} seconds')),
    ('pitchperfect', _('Every {} perfect notes')),
    ('overthebar', _('Every {} OK (or better) notes')),
    ('extraeffort', _('Every {} OK (or better) notes')),
    ('vocalrun', _('Every {} unbroken combo notes')),
)
def triggerTypeToString(trigger_type, value): return _(dict(TRIGGER_TYPES)[trigger_type]).format(value)

RARITY = (
    ('C', _('Common')),
    ('R', _('Rare')),
    ('SR', _('Super Rare')),
    ('UR', _('Ultra Rare')),
)
def rarityToString(rarity): return dict(RARITY)[rarity]

REWARDS = (
    ('glee', _('Glee Coin')),
    ('token', _('Story Token')),
    ('card', _('Story Card')),
    ('pass', _('Hall Pass')),
    ('coupon', _('Premium Chance Coupon')),
    ('eventtoken', _('Event Token')),
    ('ticket', _('Tickets')),
)
def rewardToString(reward): return dict(REWARDS)[reward]

class Card(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=12, choices=CARD_TYPES)
    parent = models.ForeignKey('self', related_name='children', null=True)
    rarity = models.CharField(max_length=12, choices=RARITY, null=True, blank=True)
    image = models.ImageField(upload_to='cards')
    performer = models.ForeignKey(Performer, related_name='cards', null=True)
    attributes = models.CharField(max_length=100, null=True, blank=True)
    stage_number = models.PositiveIntegerField(null=True, validators=[validators.MaxValueValidator(4), validators.MinValueValidator(1)])
    name = models.CharField(max_length=200, null=True, blank=True)
    sentence = models.CharField(max_length=200, null=True, blank=True)
    add_value = models.PositiveIntegerField(null=True, blank=True)
    reward_type = models.CharField(max_length=20, choices=REWARDS, null=True, blank=True)
    max_level = models.PositiveIntegerField(null=True, blank=True)
    minimum_performance = models.PositiveIntegerField(null=True, blank=True)
    maximum_performance = models.PositiveIntegerField(null=True, blank=True)
    max_level_reward = models.PositiveIntegerField(null=True, blank=True)
    skill = models.CharField(max_length=60, choices=SKILL_TYPES, null=True, blank=True)
    skill_value = models.PositiveIntegerField(null=True, blank=True)
    trigger_value = models.PositiveIntegerField(null=True, blank=True)
    trigger_chance = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        if self.name:
            return u'{}: {}'.format(self.type, self.name)
        return u'{} Card'.format(self.type)

    class Meta:
        unique_together = (('parent', 'stage_number'),)
