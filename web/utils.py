from django.conf import settings
from django.core.urlresolvers import resolve
from frgl.middleware.httpredirect import HttpRedirectException
from disqusapi import DisqusAPI
try: from web import models
except: pass
import string, random

rawContext ={
    'debug': settings.DEBUG,
    'images_hosting_path': settings.IMAGES_HOSTING_PATH,
}

def globalContext(request):
    context = rawContext.copy()
    context['current'] = resolve(request.path_info).url_name
    context['current_url'] = request.get_full_path() + ('?' if request.get_full_path()[-1] == '/' else '&')
    context['hidenavbar'] = 'hidenavbar' in request.GET
    if request.user.is_authenticated() and not request.user.is_anonymous():
        pass
    return context

def ajaxContext(request):
    context = rawContext.copy()
    return context

def randomString(length, choice=(string.ascii_letters + string.digits)):
    return ''.join(random.SystemRandom().choice(choice) for _ in range(length))

def isFollowing(user, request):
    if request.user.is_authenticated():
        try:
            request.user.preferences.following.get(username=user.username)
            return True
        except: pass
    return False

def isLiking(request, activity):
    if request.user.is_authenticated():
        try:
            activity.likes.get(username=request.user.username)
            return True
        except: pass
    return False

def redirectToProfile(request, account=None):
    raise HttpRedirectException('/user/' + request.user.username + '/'+ ('#' + str(account.id) if account else ''))

def contextWithAccounts(request):
    context = globalContext(request)
    if request.user.is_authenticated():
        context['accounts'] = request.user.accounts.all()
    return context

def pushActivity(account, message, rank=None, ownedcard=None, eventparticipation=None):
    if ownedcard is not None:
        card = ownedcard.card.parent if ownedcard.card.parent else ownedcard.card
        if card.rarity == 'C' or card.rarity == 'R':
            return
    activity = models.Activity.objects.create(account=account, message=message, rank=rank, ownedcard=ownedcard) #, eventparticipation=eventparticipation)
    disqusActivitySubscribe(activity)
    return activity

def disqus():
    return DisqusAPI(settings.DISQUS_SECRET_KEY, settings.DISQUS_PUBLIC_KEY)

def disqusCreateThread(title, identifier, url, d=None):
    if d is None:
        d = disqus()
    return d.post('threads.create', method='POST', forum='frgl', title=title, identifier=identifier, url=url, access_token=settings.DISQUS_ACCESS_TOKEN)

def disqusThreadSubscribe(thread_id, email, d=None):
    if d is None:
        d = disqus()
    d.post('threads.subscribe', method='POST', thread=thread_id, email=email)

def disqusProfileSubscribe(user):
    d = disqus()
    thread = disqusCreateThread(title=u'{} fr.gl Profile'.format(user.username), identifier='user-' + str(user.id), url='http://fr.gl/user/' + user.username + '/')
    disqusThreadSubscribe(thread['id'], user.email)

def disqusActivitySubscribe(activity):
    d = disqus()
    thread = disqusCreateThread(title=u'fr.gl Activity: {}'.format(unicode(activity)), identifier='activity-' + str(activity.id), url='http://fr.gl/activity/' + str(activity.id) + '/')
    disqusThreadSubscribe(thread['id'], activity.account.owner.email)
