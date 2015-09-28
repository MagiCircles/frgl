from __future__ import division
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.http import Http404
from django.db.models import Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from utils import *
from frgl.middleware.httpredirect import HttpRedirectException
from django.contrib.auth.models import User, Group
from web import models, forms, donations
import math
import operator
import re
from collections import OrderedDict

def index(request):
    context = globalContext(request)
    return render(request, 'index.html', context)

def cards(request, card=None, ajax=False):
    page = 0
    context = contextWithAccounts(request)

    cards = models.Card.objects.filter()
    if 'search' in request.GET:
        if request.GET['search']:
            terms = request.GET['search'].split(' ')
            for term in terms:
                cards = cards.filter(Q(name__icontains=term)
                                     | Q(performer__name__icontains=term)
                                     | Q(sentence__name__icontains=term)
                                     | Q(skill__icontains=term)
                                 )
    if 'performer' in request.GET and request.GET['performer']:
        cards = cards.filter(performer=request.GET['performer'])
    if 'type' in request.GET and request.GET['type']:
        cards = cards.filter(type=request.GET['type'])
    if 'attributes' in request.GET and request.GET['attributes']:
        for attribute in request.GET.getlist('attributes'):
            cards = cards.filter(attributes__contains=attribute)
    if 'rarity' in request.GET and request.GET['rarity']:
        cards = cards.filter(rarity__exact=request.GET['rarity'])
    if 'skill' in request.GET and request.GET['skill']:
        cards = cards.filter(skill__exact=request.GET['skill'])
    if 'trigger' in request.GET and request.GET['trigger']:
        cards = cards.filter(trigger__exact=request.GET['trigger'])

    reverse = 'reverse_order' in request.GET and request.GET['reverse_order']
    ordering = request.GET['ordering'] if 'ordering' in request.GET and request.GET['ordering'] else 'creation'
    prefix = '-' if reverse else ''
    cards = cards.order_by(prefix + ordering)

    context['total_results'] = cards.count()

    page_size = 12
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    cards = cards.select_related('performer', 'parent')[(page * page_size):((page * page_size) + page_size)]

    context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
    context['cards'] = cards
    context['page'] = page + 1
    context['page_size'] = page_size
    context['filter_form'] = forms.FilterCardForm(request.GET)
    context['show_no_result'] = not ajax
    context['colsize'] = 3
    context['perline'] = 4
    context['show_search_results'] = bool(request.GET)

    if ajax:
        return render(request, 'cardsPage.html', context)
    return render(request, 'cards.html', context)

def card(request, card=None, ajax=False):
    context = contextWithAccounts(request)
    context['card'] = get_object_or_404(models.Card, id=int(card))
    context['ajax'] = ajax
    if context['card'].type == 'stageup':
        context['stageup'] = context['card']
        context['card'] = context['card'].parent
        context['card'].stages = models.Card.objects.filter(Q(parent=context['stageup'].parent) | Q(pk=context['card'].pk)).exclude(pk=context['stageup'].pk).order_by('stage_number')
    elif context['card'].type == 'unlock':
        context['card'].stages = context['card'].children.all().order_by('stage_number')

    if ajax:
        return render(request, 'ajaxcard.html', context)
    return render(request, 'card.html', context)

def addcard(request, type):
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect('/about/#contribute')
    context = globalContext(request)
    try:
        formClass = forms.cardTypeForms[type]
    except KeyError:
        raise Http404
    if request.method == 'GET':
        form = formClass()
    elif request.method == 'POST':
        form = formClass(request.POST, request.FILES)
        if form.is_valid():
            card = form.save()
            raise HttpRedirectException('/cards/' + str(card.id) + '/')
    context['form'] = form
    context['multipart'] = True
    context['type'] = type
    return render(request, 'addCard.html', context)

def editcard(request, card):
    if not request.user.is_authenticated() or not request.user.is_staff:
        return redirect('/about/#contribute')
    context = globalContext(request)
    try:
        card = models.Card.objects.get(pk=card)
    except ObjectDoesNotExist:
        raise Http404
    formClass = forms.cardTypeForms[card.type]
    if request.method == 'GET':
        form = formClass(instance=card)
    elif request.method == 'POST':
        form = formClass(request.POST, request.FILES, instance=card)
        if form.is_valid():
            card = form.save()
            raise HttpRedirectException('/cards/' + str(card.id) + '/')
    context['card'] = card
    context['form'] = form
    context['multipart'] = True
    context['type'] = type
    return render(request, 'editcard.html', context)

def wiki(request, wiki_url='Home'):
    context = globalContext(request)
    context['wiki_url'] = wiki_url
    return render(request, 'wiki.html', context)

def about(request):
    context = globalContext(request)
    return render(request, 'about.html', context)

def donate(request):
    context = globalContext(request)
    context['donators_low'] = models.User.objects.filter(Q(preferences__status='THANKS') | Q(preferences__status='SUPPORTER') | Q(preferences__status='LOVER') | Q(preferences__status='AMBASSADOR')).order_by('preferences__status', '-preferences__donation_link', '-preferences__donation_link_title')
    context['donators_high'] = models.User.objects.filter(Q(preferences__status='PRODUCER') | Q(preferences__status='DEVOTEE')).order_by('preferences__status')
    context['total_donators'] = models.UserPreferences.objects.filter(status__isnull=False).count()
    context['donations'] = donations.donations
    return render(request, 'donate.html', context)

def signup(request):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        return redirect('/')
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            preferences = models.UserPreferences.objects.create(user=user)
            login(request, user)
            disqusProfileSubscribe(user)
            return redirect('/addaccount')
    else:
        form = forms.CreateUserForm()
    context = globalContext(request)
    context['form'] = form
    return render(request, 'signup.html', context)

def profile(request, username):
    context = globalContext(request)
    user = get_object_or_404(User, username=username)
    context['profile_user'] = user
    context['is_me'] = user == request.user
    context['user_accounts'] = user.accounts.all()
    if not user.preferences.private or context['is_me']:
        for account in context['user_accounts']:
            account.cards = account.ownedcards.select_related('card', 'card__parent').order_by('-card__performer', '-card__id')
            account.performers = OrderedDict()
            if account.cards:
                for card in account.cards:
                    if card.card.parent:
                        card.card.performer = card.card.parent.performer
                    performer = card.card.performer
                    if performer not in account.performers:
                        account.performers[performer] = 1
                    else:
                        account.performers[performer] += 1
                performer_with_max_cards, max_cards_per_performer = max(account.performers.iteritems(), key=operator.itemgetter(1))
                max_lines = math.ceil(max_cards_per_performer / 6)
                account.item_height = 139 + (max_lines * 110)
                account.cards_total_sr = sum(card.card.rarity == 'SR' for card in account.cards)
                account.cards_total_ur = sum(card.card.rarity == 'UR' for card in account.cards)
                account.selected_performer = user.preferences.favorite_performer.name if user.preferences.favorite_performer else performer_with_max_cards
    context['links'] = list(context['profile_user'].links.all().values())
    context['show_facebook_requests'] = any(link['type'] == 'facebook' for link in context['links'])
    if user.preferences.favorite_performer:
        context['links'].insert(0, {
            'type': 'Favorite Performer',
            'value': user.preferences.favorite_performer,
            'translate_type': True,
        })
        if user.preferences.location:
            context['links'].insert(1, {
                'type': 'Location',
                'value': user.preferences.location,
                'translate_type': True,
                'flaticon': 'world',
            })
    num_links = len(context['links'])
    best_links_on_last_line = 0
    for i in range(4, 7):
        links_on_last_line = num_links % i
        if links_on_last_line == 0:
            context['per_line'] = i
            break
        if links_on_last_line > best_links_on_last_line:
            best_links_on_last_line = links_on_last_line
            context['per_line'] = i
    context['following'] = isFollowing(user, request)
    context['total_following'] = user.preferences.following.count()
    context['total_followers'] = user.followers.count()
    return render(request, 'profile.html', context)

def addaccount(request):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    formClass = forms.SimpleAccountForm
    if 'advanced' in request.GET:
        formClass = forms.AccountForm
        context['advanced'] = True
    if request.method == "POST":
        form = formClass(request.POST, request=request)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return redirect('cards')
    else:
        form = formClass(initial={
            'nickname': request.user.username
        }, request=request)
        context['form'] = form
        return render(request, 'addaccount.html', context)

def editaccount(request, account):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    account = get_object_or_404(models.Account, pk=account, owner=request.user)

    form = forms.AccountForm(instance=account, request=request)
    form_delete = forms.ConfirmDelete(initial={
        'thing_to_delete': account.id,
    })
    if request.method == 'POST':
        if 'delete' in request.POST:
            form_delete = forms.ConfirmDelete(request.POST)
            if form_delete.is_valid():
                account.delete()
                redirectToProfile(request)
        else:
            form = forms.AccountForm(request.POST, instance=account, request=request)
            if form.is_valid():
                account = form.save()
                redirectToProfile(request, account)
    context['form'] = form
    context['form_delete'] = form_delete
    return render(request, 'editaccount.html', context)

def settings(request):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    context = globalContext(request)
    context['preferences'] = request.user.preferences
    context['accounts'] = request.user.accounts.all()
    form = forms.UserForm(instance=request.user)
    form_preferences = forms.UserPreferencesForm(instance=context['preferences'])
    form_addlink = forms.AddLinkForm()
    form_changepassword = forms.ChangePasswordForm()
    if request.method == "POST":
        if 'editPreferences' in request.POST:
            form_preferences = forms.UserPreferencesForm(request.POST, instance=context['preferences'])
            old_location = context['preferences'].location
            if form_preferences.is_valid():
                prefs = form_preferences.save(commit=False)
                if old_location != prefs.location:
                    prefs.location_changed = True
                prefs.save()
                return redirect('/user/' + request.user.username + '/')
        elif 'changePassword' in request.POST:
            form_changepassword = forms.ChangePasswordForm(request.POST)
            if form_changepassword.is_valid():
                new_password = form_changepassword.cleaned_data['new_password']
                username = request.user.username
                old_password = form_changepassword.cleaned_data['old_password']
                user = authenticate(username=username, password=old_password)
                if user is not None:
                    for account in context['accounts']:
                        if account.transfer_code and transfer_code.is_encrypted(account.transfer_code):
                            clear_transfer_code = transfer_code.decrypt(account.transfer_code, old_password)
                            encrypted_transfer_code = transfer_code.encrypt(clear_transfer_code, new_password)
                            account.transfer_code = encrypted_transfer_code
                            account.save()
                    user.set_password(new_password)
                    user.save()
                    authenticate(username=username, password=new_password)
                    login(request, user)
                    return redirect('/user/' + request.user.username + '/')
                errors = form_changepassword._errors.setdefault("old_password", ErrorList())
                errors.append(_('Wrong password.'))
        elif 'addLink' in request.POST:
            form_addlink = forms.AddLinkForm(request.POST)
            if form_addlink.is_valid():
                link = form_addlink.save(commit=False)
                link.owner = request.user
                link.save()
                return redirect('/settings/#link' + str(link.id))
        else:
            form = forms.UserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/user/' + request.user.username)
    context['form'] = form
    context['form_addlink'] = form_addlink
    context['form_changepassword'] = form_changepassword
    context['form_preferences'] = form_preferences
    context['links'] = list(request.user.links.all().values())
    return render(request, 'settings.html', context)

def ajaxdeletelink(request, link):
    if not request.user.is_authenticated() or request.user.is_anonymous():
        raise PermissionDenied()
    try:
        link = models.UserLink.objects.get(owner=request.user, pk=int(link))
    except ObjectDoesNotExist:
        raise PermissionDenied()
    link.delete()
    return HttpResponse('deleted')

def ajaxaddcard(request, card):
    if not request.user.is_authenticated() or request.user.is_anonymous() or request.method != 'POST':
        raise PermissionDenied()
    account = get_object_or_404(models.Account, pk=request.POST['account'], owner=request.user)
    card = get_object_or_404(models.Card, pk=card)
    ownedcard = None
    activity = None
    # only 1 card of the same "family" can be owned by account
    try:
        ownedcard = models.OwnedCard.objects.filter(account=account).get(Q(card=card)
                                                                          | Q(card=card.parent)
                                                                          | Q(card__in=(card.parent.children.all() if card.parent else [])))
        activity = models.Activity.objects.get(ownedcard=ownedcard)
        activity.ownedcard = None
        activity.save()
    except ObjectDoesNotExist: pass
    if ownedcard:
        ownedcard.delete()
    ownedcard = models.OwnedCard.objects.create(account=account, card=card)
    if activity:
        activity.ownedcard = ownedcard
        activity.creation = timezone.now()
        activity.save()
    else:
        pushActivity(account=ownedcard.account,
                     message="Added a card",
                     ownedcard=ownedcard)
    return HttpResponse('added ' + str(ownedcard.pk))

def ajaxdeleteownedcard(request, card):
    if not request.user.is_authenticated() or request.user.is_anonymous() or request.method != 'POST':
        raise PermissionDenied()
    get_object_or_404(models.OwnedCard, pk=card).delete()
    return HttpResponse('deleted')

def ajaxfollowers(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'followlist.html', { 'follow': [u.user for u in user.followers.all()] })

def ajaxfollowing(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'followlist.html', { 'follow': user.preferences.following.all() })

@csrf_exempt
def ajaxfollow(request, username):
    context = globalContext(request)
    if (not request.user.is_authenticated() or request.user.is_anonymous()
        or request.method != 'POST' or request.user.username == username):
        raise PermissionDenied()
    user = get_object_or_404(User, username=username)
    if 'follow' in request.POST and not isFollowing(user, request):
        request.user.preferences.following.add(user)
        request.user.preferences.save()
        return HttpResponse('followed')
    if 'unfollow' in request.POST and isFollowing(user, request):
        request.user.preferences.following.remove(user)
        request.user.preferences.save()
        return HttpResponse('unfollowed')
    raise PermissionDenied()


def _activities(request, account=None, follower=None, avatar_size=3):
    context = ajaxContext(request)
    page = 0
    page_size = 10
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    activities = models.Activity.objects.all().order_by('-creation')
    if account is not None:
        activities = activities.filter(account=account)
        context['account'] = account
    if follower is not None:
        follower = get_object_or_404(User, username=follower)
        accounts = models.Account.objects.filter(owner__in=follower.preferences.following.all())
        activities = activities.filter(account__in=accounts)
    total = activities.count()
    activities = activities[(page * page_size):((page * page_size) + page_size)]
    for activity in activities:
        activity.likers = activity.likes.all()
        activity.likers_count = activity.likers.count()
    context['activities'] = activities
    context['page'] = page + 1
    context['page_size'] = page_size
    context['avatar_size'] = avatar_size
    context['content_size'] = 12 - avatar_size
    context['total_results'] = total
    context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
    return context

def ajaxactivities(request):
    account = int(request.GET['account']) if 'account' in request.GET and request.GET['account'] and request.GET['account'].isdigit() else None
    follower = request.GET['follower'] if 'follower' in request.GET and request.GET['follower'] else None
    if 'feed' in request.GET:
        follower = request.user
    avatar_size = int(request.GET['avatar_size']) if 'avatar_size' in request.GET and request.GET['avatar_size'] and request.GET['avatar_size'].isdigit() else 3
    return render(request, 'activities.html', _activities(request, account=account, follower=follower, avatar_size=avatar_size))

@csrf_exempt
def ajaxlikeactivity(request, activity):
    context = ajaxContext(request)
    if not request.user.is_authenticated() or request.method != 'POST':
        raise PermissionDenied()
    activity = get_object_or_404(models.Activity, id=activity)
    if activity.account.owner.id != request.user.id:
        print isLiking(request, activity)
        if 'like' in request.POST and not isLiking(request, activity):
            activity.likes.add(request.user)
            activity.save()
            return HttpResponse('liked')
        if 'unlike' in request.POST and isLiking(request, activity):
            activity.likes.remove(request.user)
            activity.save()
            return HttpResponse('unliked')
        print 'test5'
    raise PermissionDenied()

def activity(request, activity):
    context = ajaxContext(request)
    context['activity'] = get_object_or_404(models.Activity, pk=activity)
    context['activity'].likers = context['activity'].likes.all()
    context['activity'].likers_count = context['activity'].likers.count()
    context['avatar_size'] = 2
    context['content_size'] = 10
    return render(request, 'activity.html', context)

def users(request, ajax=False):
    page = 0
    context = globalContext(request)

    accounts = models.Account.objects.filter(owner__preferences__private=False)
    if 'search' in request.GET:
        if request.GET['search']:
            terms = request.GET['search'].split(' ')
            for term in terms:
                accounts = accounts.filter(Q(owner__username__icontains=term)
                                           | Q(owner__preferences__description__icontains=term)
                                           | Q(owner__preferences__location__icontains=term)
                                           | Q(owner__links__value__icontains=term)
                                           | Q(owner__email__iexact=term)
                                           | Q(nickname__icontains=term)
                                           | Q(account_id__iexact=term)
                                       )
    if 'play_with' in request.GET and request.GET['play_with']:
        accounts = accounts.filter(play_with=request.GET['play_with'])

    reverse = ('reverse_order' in request.GET and request.GET['reverse_order']) or not request.GET or len(request.GET) == 1
    ordering = request.GET['ordering'] if 'ordering' in request.GET and request.GET['ordering'] else 'rank'
    prefix = '-' if reverse else ''
    accounts = accounts.order_by(prefix + ordering)

    context['total_results'] = accounts.count()

    page_size = 12
    if 'page' in request.GET and request.GET['page']:
        page = int(request.GET['page']) - 1
        if page < 0:
            page = 0
    accounts = accounts.select_related('owner')[(page * page_size):((page * page_size) + page_size)]

    if ordering == 'rank':
        for (i, account) in enumerate(accounts):
            account.position = (page * page_size) + i + 1
    context['total_pages'] = int(math.ceil(context['total_results'] / page_size))
    context['accounts'] = accounts
    context['page'] = page + 1
    context['page_size'] = page_size
    context['filter_form'] = forms.FilterUserForm(request.GET)
    context['show_no_result'] = not ajax
    context['colsize'] = 3
    context['perline'] = 4
    context['show_search_results'] = bool(request.GET)

    if ajax:
        return render(request, 'usersPage.html', context)
    return render(request, 'users.html', context)
