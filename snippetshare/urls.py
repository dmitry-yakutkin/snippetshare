from django.conf.urls import patterns, include, url
from django.contrib import admin

from app.views import HomeView, SuccessView, RegisterView, LoginView, SnippetView, compose_message
from app.views import users_snippets_view, NewSnippetView, comment_view
import app.api as api

api_patterns = [
    url(r'^snippet/([0-9])', api.SnippetView.as_view()),
    url(r'^users-snippets/', api.UsersSnippetsView.as_view())
]

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^success/$', SuccessView.as_view(), name='home'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^message/$', compose_message, name='message'),
    url(r'^comment/([0-9])', comment_view, name='comment'),
    url(r'^snippet/([0-9])$', SnippetView.as_view(), name='test'),
    url(r'^snippets/$', users_snippets_view, name='userssnippets'),
    url(r'^new-snippet/$', NewSnippetView.as_view(), name='newsnippet'),

    url(r'^api/', include(api_patterns)),
)

