from django.conf.urls import include, patterns, url
from django.conf import settings
from web import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^cards[/]+$', views.cards, name='cards'),
    url(r'^card[s]?/(?P<card>\d+)[/]+$', views.card, name='card'),
    url(r'^addcard/(?P<type>[\w_]+)[/]+$', views.addcard, name='addcard'),
    url(r'^editcard/(?P<card>\d+)[/]+$', views.editcard, name='editcard'),

    url(r'^wiki[/]+$', views.wiki, name='wiki'),
    url(r'^about[/]+$', views.about, name='about'),

    url(r'^ajax/card[s]?/(?P<card>\d+)[/]+$', views.card, {'ajax': True}, name='ajaxcard'),
    url(r'^ajax/cards[/]+$', views.cards, {'ajax': True}, name='ajaxcards'),
)
