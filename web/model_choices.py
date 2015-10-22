from django.utils.translation import ugettext_lazy as _, string_concat

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
    ('profile', _('Profile Icon')),
)
def rewardToString(reward): return dict(REWARDS)[reward]

PLAYWITH_CHOICES = (
    ('Thumbs', _('Thumbs')),
    ('Fingers', _('All fingers')),
    ('Index', _('Index fingers')),
    ('Hand', _('One hand')),
    ('Other', _('Other')),
)
def playwithToString(playwith): return dict(PLAYWITH_CHOICES)[playwith]

STATUS_CHOICES = (
    ('THANKS', 'Thanks'),
    ('SUPPORTER', _('Gleek')),
    ('LOVER', _('Super Gleek')),
    ('AMBASSADOR', _('Extreme Gleek')),
    ('PRODUCER', _('Gleek Master')),
    ('DEVOTEE', _('Ultimate Glee Lover')),
)
def statusToString(status): return dict(STATUS_CHOICES)[status]

def statusToColor(status):
    if status == 'SUPPORTER': return '#4a86e8'
    elif status == 'LOVER': return '#ff53a6'
    elif status == 'AMBASSADOR': return '#a8a8a8'
    elif status == 'PRODUCER': return '#c98910'
    elif status == 'DEVOTEE': return '#c98910'
    return ''

def statusToColorString(status):
    if status == 'SUPPORTER': return _('blue')
    elif status == 'LOVER': return _('pink')
    elif status == 'AMBASSADOR': return _('shiny Silver')
    elif status == 'PRODUCER': return _('shiny Gold')
    elif status == 'DEVOTEE': return _('shiny Gold')
    return ''

LINK_CHOICES = (
    ('facebook', 'Facebook'),
    ('twitter', 'Twitter'),
    ('reddit', 'Reddit'),
    ('schoolidolu', 'School Idol Tomodachi'),
    ('line', 'LINE Messenger'),
    ('tumblr', 'Tumblr'),
    ('twitch', 'Twitch'),
    ('steam', 'Steam'),
    ('instagram', 'Instagram'),
    ('youtube', 'YouTube'),
    ('github', 'GitHub'),
)
def linkToString(link): return dict(LINK_CHOICES)[link]

LINK_URLS = {
    'Favorite Performer': '/cards/?performer={}',
    'Location': 'http://maps.google.com/?q={}',
    'twitter': 'http://twitter.com/{}',
    'facebook': 'https://www.facebook.com/{}',
    'reddit': 'http://www.reddit.com/user/{}',
    'schoolidolu': 'http://schoolido.lu/user/{}/',
    'line': 'http://line.me/#{}',
    'tumblr': 'http://{}.tumblr.com/',
    'twitch': 'http://twitch.tv/{}',
    'steam': 'http://steamcommunity.com/id/{}',
    'instagram': 'https://instagram.com/{}/',
    'youtube': 'https://www.youtube.com/user/{}',
    'github': 'https://github.com/{}',
}

LINK_RELEVANCE_CHOICES = (
    (0, _('Never')),
    (1, _('Sometimes')),
    (2, _('Often')),
    (3, _('Every single day')),
)
def linkRelevanceToString(rel): return dict(LINK_RELEVANCE_CHOICES)[rel]

OS_CHOICES = (
    ('Android', 'Android'),
    ('iOs', 'iOs'),
)
def osToString(os): return dict(OS_CHOICES)[os]

ACTIVITY_MESSAGE_CHOICES = (
    ('Added a card', _('Added a card')),
    ('Rank Up', _('Rank Up')),
    ('Ranked in event', _('Ranked in event')),
    ('Followed', _('Followed')),
)
def activityMessageToString(activity): return dict(ACTIVITY_MESSAGE_CHOICES)[activity]
