from django.conf.urls import include, patterns, url
from django.conf import settings
from web import views
from web.utils import rawContext

loginContext = rawContext.copy()
loginContext['current'] = 'login'

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('web',),
}

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'^cards[/]+$', views.cards, name='cards'),
    url(r'^card[s]?/(?P<card>\d+)[/]+$', views.card, name='card'),
    url(r'^login[/]+$', 'django.contrib.auth.views.login', {'template_name': 'login.html', 'extra_context': loginContext}),
    url(r'^signup[/]+$', views.signup, name='signup'),
    url(r'^users[/]+$', views.users, name='users'),
    url(r'^u[s]?[e]?[r]?[s]?/(?P<username>[\w.@+-]+)[/]+$', views.profile, name='profile'),
    url(r'^logout[/]+$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^addcard/(?P<type>[\w_]+)[/]+$', views.addcard, name='addcard'),
    url(r'^editcard/(?P<card>\d+)[/]+$', views.editcard, name='editcard'),
    url(r'^addaccount[/]+$', views.addaccount, name='addaccount'),
    url(r'^editaccount/(?P<account>\d+)[/]+$', views.editaccount, name='editaccount'),
    url(r'^settings[/]+$', views.settings, name='settings'),
    url(r'^activities/(?P<activity>\d+)[/]+$', views.activity, name='activity'),

    url(r'^wiki[/]+$', views.wiki, name='wiki'),
    url(r'^wiki/(?P<wiki_url>[^/]+)[/]+$', views.wiki, name='wiki'),
    url(r'^about[/]+$', views.about, name='about'),
    url(r'^donate[/]+$', views.donate, name='donate'),

    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^ajax/card[s]?/(?P<card>\d+)[/]+$', views.card, {'ajax': True}, name='ajaxcard'),
    url(r'^ajax/cards[/]+$', views.cards, {'ajax': True}, name='ajaxcards'),
    url(r'^ajax/users[/]+$', views.users, {'ajax': True}, name='ajaxusers'),
    url(r'^ajax/addcard/(?P<card>\d+)[/]+$', views.ajaxaddcard, name='ajaxaddcard'),
    url(r'^ajax/deleteownedcard/(?P<card>\d+)[/]+$', views.ajaxdeleteownedcard, name='ajaxdeleteownedcard'),
    url(r'^ajax/deletelink/(?P<link>\d+)[/]+$', views.ajaxdeletelink, name='ajaxdeletelink'),
    url(r'^ajax/follow/(?P<username>[\w.@+-]+)[/]+$', views.ajaxfollow, name='ajaxfollow'),
    url(r'^ajax/followers/(?P<username>[\w.@+-]+)[/]+$', views.ajaxfollowers, name='ajaxfollowers'),
    url(r'^ajax/following/(?P<username>[\w.@+-]+)[/]+$', views.ajaxfollowing, name='ajaxfollowing'),
    url(r'^ajax/activities[/]+$', views.ajaxactivities, name='ajaxactivities'),
    url(r'^ajax/likeactivity/(?P<activity>\d+)[/]+$', views.ajaxlikeactivity, name='ajaxlikeactivity'),
)
