from django.db import models
from django.contrib.auth.models import User, Group
from django.core import validators
from django.utils.translation import ugettext_lazy as _, string_concat
from web.model_choices import *
from web import raw, utils
import hashlib, urllib, os

class Performer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='performers')

    def __unicode__(self):
        return self.name

class UserPreferences(models.Model):
    user = models.OneToOneField(User, related_name='preferences', on_delete=models.CASCADE)
    description = models.TextField(_('Description'), null=True, help_text=_('Write whatever you want. You can add formatting and links using Markdown.'), blank=True)
    favorite_performer = models.ForeignKey(Performer, related_name='fans', null=True, on_delete=models.SET_NULL)
    location = models.CharField(_('Location'), max_length=200, null=True, blank=True, help_text=string_concat(_('The city you live in.'), ' ', _('It might take up to 24 hours to update your location on the map.')))
    twitter = models.CharField(max_length=32, null=True, blank=True)
    facebook = models.CharField(max_length=32, null=True, blank=True)
    location_changed = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    following = models.ManyToManyField(User, related_name='followers')
    status = models.CharField(choices=STATUS_CHOICES, max_length=12, null=True)
    donation_link = models.CharField(max_length=200, null=True, blank=True)
    donation_link_title = models.CharField(max_length=100, null=True, blank=True)
    private = models.BooleanField(_('Private Profile'), default=False, help_text=_('If your profile is private, only you can see your cards, event participations and cleared songs.'))

    def avatar(self, size):
        default = 'http://fr.gl/static/img/avatar.png'
        if self.twitter:
            default = 'http://schoolido.lu/avatar/twitter/' + self.twitter
        return ("http://www.gravatar.com/avatar/"
                + hashlib.md5(self.user.email.lower()).hexdigest()
                + "?" + urllib.urlencode({'d': default, 's': str(size)}))

class Account(models.Model):
    owner = models.ForeignKey(User, related_name='accounts')
    nickname = models.CharField(_("Nickname"), blank=True, max_length=20)
    os = models.CharField(_("Operating System"), choices=OS_CHOICES, max_length=10, null=True, blank=True)
    device = models.CharField(_('Device'), help_text=_('The modele of your device. Example: Nexus 5, iPhone 4, iPad 2, ...'), max_length=150, null=True, blank=True)
    play_with = models.CharField(_('Play with'), blank=True, null=True, max_length=30, choices=PLAYWITH_CHOICES)
    accept_friend_requests = models.NullBooleanField(_('Accept friend requests on Facebook'), blank=True, null=True)
    rank = models.PositiveIntegerField(_("Rank"), blank=True, null=True)
    stars = models.PositiveIntegerField(_("Stars"), blank=True, null=True)
    account_id = models.PositiveIntegerField(_("ID"), blank=True, null=True, help_text=_('To find your ID, tap the settings icon, then tap "Profile". Your ID is the number you see on top of the window.'))

    def __unicode__(self):
        return unicode(self.owner.username) if self.nickname == '' else unicode(self.nickname)

class UserLink(models.Model):
    alphanumeric = validators.RegexValidator(r'^[0-9a-zA-Z-_\. ]*$', 'Only alphanumeric and - _ characters are allowed.')
    owner = models.ForeignKey(User, related_name='links')
    type = models.CharField(_('Platform'), max_length=20, choices=LINK_CHOICES)
    value = models.CharField(_('Username/ID'), max_length=64, help_text=_('Write your username only, no URL.'), validators=[alphanumeric])
    relevance = models.PositiveIntegerField(_('How often do you tweet/stream/post about Glee?'), choices=LINK_RELEVANCE_CHOICES, null=True, blank=True)

    def url(self):
        return LINK_URLS[self.type].format(self.value)

    def save(self, *args, **kwargs):
        if self.type == 'twitter':
            self.owner.preferences.twitter = self.value
            self.owner.preferences.save()
        if self.type == 'facebook':
            self.owner.preferences.facebook = self.value
            self.owner.preferences.save()
        super(UserLink, self).save(*args, **kwargs)

def card_upload_to(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'cards/' + (str(instance.id) + '_' + utils.randomString(16) if instance and instance.id else utils.randomString(16)) + extension

class Card(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, related_name='added_cards', null=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(User, related_name='modified_cards', null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=12, choices=CARD_TYPES)
    parent = models.ForeignKey('self', related_name='children', null=True)
    rarity = models.CharField(max_length=12, choices=RARITY, default='C')
    image = models.ImageField(upload_to=card_upload_to)
    performer = models.ForeignKey(Performer, related_name='cards', null=True)
    attributes = models.CharField(max_length=100, null=True, blank=True)
    stage_number = models.PositiveIntegerField(null=True, validators=[validators.MaxValueValidator(4), validators.MinValueValidator(1)])
    name = models.CharField(_('Collection'), max_length=200, null=True, blank=True, help_text=_('Cheerio, Glam Girl, Believer, ...'))
    sentence = models.CharField(max_length=200, null=True, blank=True, help_text=_('The sentence you see when you get the story card.'))
    add_value = models.PositiveIntegerField(null=True, blank=True)
    reward_type = models.CharField(max_length=20, choices=REWARDS, null=True, blank=True)
    maximum_performance_ability = models.PositiveIntegerField(null=True, blank=True, help_text=_('The highest performance ability for this card at this stage.'))
    skill = models.CharField(max_length=60, choices=SKILL_TYPES, null=True, blank=True)
    skill_value = models.PositiveIntegerField(null=True, blank=True, help_text=_('The number you see in the sentence that explains what is the effect of the skill at this stage.'))
    trigger_value = models.PositiveIntegerField(null=True, blank=True, help_text=_('The number you see in the sentence that explains when the skill can be activated.'))
    trigger_chance = models.PositiveIntegerField(null=True, blank=True, help_text=_('The % chance of skill activation.'))
    how_to_obtain = models.TextField(_('How to get it?'), null=True, blank=True, help_text=_('For event or special songs cards. Leave empty if it\'s only obtainable in recruitment.'))

    def _rarityData(self, data):
        value = -1
        if self.type == 'unlock':
            value = raw.cards_data[self.rarity][data][1]
        elif self.stage_number:
            value = raw.cards_data[self.rarity][data][self.stage_number + 1]
        return value if value != -1 else '?'

    @property
    def max_level(self):
        return self._rarityData('levels')

    @property
    def max_level_at_max_stage(self):
        return raw.cards_data[self.rarity]['levels'][raw.cards_data[self.rarity]['stages'] + 1]

    @property
    def maximum_performance(self):
        if self.maximum_performance_ability:
            return self.maximum_performance_ability
        return self._rarityData('performances')

    @property
    def experience(self):
        return self._rarityData('experiences')

    @property
    def max_level_reward(self):
        return raw.cards_data[self.rarity]['max_level_reward']

    @property
    def minimum_performance(self):
        return raw.cards_data[self.rarity]['performances'][0]

    def __unicode__(self):
        return u'{} [{}]: {} {}'.format(cardTypeToString(self.type),
                                        self.rarity,
                                        (self.name if self.name else (self.parent.name if self.parent else '')),
                                        (self.performer if self.performer else (self.parent.performer.name if self.parent else '')))

    class Meta:
        unique_together = (('parent', 'stage_number'),)

class OwnedCard(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, verbose_name=_('Account'), related_name='ownedcards')
    card = models.ForeignKey(Card, related_name='ownedcards')

    def __unicode__(self):
        return unicode(self.account) + u' owns ' + unicode(self.card)

# Add card to deck/album/wish list
# Level up
class Activity(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name='activities', null=True, blank=True)
    message = models.CharField(max_length=300, choices=ACTIVITY_MESSAGE_CHOICES)
    rank = models.PositiveIntegerField(null=True, blank=True)
    ownedcard = models.ForeignKey(OwnedCard, null=True, blank=True)
#    eventparticipation = models.ForeignKey(EventParticipation, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_activities")

    def __unicode__(self):
        return u'%s %s' % (self.account, self.message)
