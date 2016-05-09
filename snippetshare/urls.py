from django.conf.urls import patterns, include, url
from django.contrib import admin

from app.views import (
    HomeView, SuccessView, RegisterView, LoginView, SnippetView,
    NewSnippetView)
from app.views import (
    users_snippets_view, all_snippets_view, compose_message, comment_view,
    logout_view)
import app.api as api

api_patterns = [
    url(r'^', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^snippet/(?P<id>[0-9]+)/$', api.SnippetView.as_view()),
    url(r'^users-snippets/', api.UsersSnippetsView.as_view()),
    url(r'^all-snippets', api.AllSnippetsView.as_view()),
]

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^success/$', SuccessView.as_view(), name='home'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^message/$', compose_message, name='message'),
    url(r'^comment/([0-9])', comment_view, name='comment'),
    url(r'^snippet/([0-9])$', SnippetView.as_view(), name='test'),
    url(r'^snippets/$', users_snippets_view, name='userssnippets'),
    url(r'^all-snippets/$', all_snippets_view, name='allsnippets'),
    url(r'^new-snippet/$', NewSnippetView.as_view(), name='newsnippet'),

    url(r'^api/', include(api_patterns)),
)
