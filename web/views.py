from __future__ import division
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from utils import *
from frgl.middleware.httpredirect import HttpRedirectException
from web import models, forms
import math

def index(request):
    context = globalContext(request)
    context['current'] = 'index'
    return render(request, 'index.html', context)


def cards(request, card=None, ajax=False):
    page = 0
    context = globalContext(request)

    cards = models.Card.objects.filter()
    if 'search' in request.GET:
        if request.GET['search']:
            terms = request.GET['search'].split(' ')
            for term in terms:
                cards = cards.filter(Q(name__contains=term)
                                     | Q(performer__name__contains=term)
                                     | Q(sentence__name__contains=term)
                                     | Q(skill__contains=term)
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
    context['ajax'] = ajax
    context['colsize'] = 3
    context['perline'] = 4
    context['show_search_results'] = bool(request.GET)

    if ajax:
        return render(request, 'cardsPage.html', context)
    return render(request, 'cards.html', context)

def card(request, card=None, ajax=False):
    context = globalContext(request)
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
    return render(request, 'addcard.html', context)

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

def wiki(request):
    return redirect('https://github.com/SchoolIdolTomodachi/frgl/wiki')

def about(request):
    context = globalContext(request)
    return render(request, 'about.html', context)
