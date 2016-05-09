import pdb

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from django.views.generic import FormView, TemplateView, View
from .forms import LoginForm, RegisterForm, MessageForm

from .models import Message

from django.contrib.auth import models as auth_models, authenticate, login, logout
from django.contrib.auth.decorators import login_required

from app.models import Snippet, Comment


class HomeView(View):
    def get(self, request):
        #pdb.set_trace()
        if request.user.is_authenticated():
            return redirect(reverse('userssnippets'))
        return render(request, 'index.html', {})


class SuccessView(TemplateView):
    template_name = 'success.html'


class SnippetView(View):
    def get(self, request, identifier):
        snippet = Snippet.objects.get(pk=identifier)
        comments = Comment.objects.filter(snippet=snippet)
        return render(
            request, 'snippet.html', {
                'name': snippet.name,
                'id': identifier,
                'comments': comments,
                'editable': snippet.user == request.user,
            })


def comment_view(request, identifier):
    if request.method == 'POST':
        snippet = Snippet.objects.get(pk=(int(identifier)))
        c = Comment(
            snippet=snippet, user=request.user, text=request.POST['text'])
        c.save()
        return redirect('/snippet/' + identifier)


class NewSnippetView(View):
    def get(self, request):
        s = Snippet(text='', user=request.user)
        s.save()
        return redirect('/snippet/' + str(s.pk))


def render_snippets(request, snippets, context=None):
    def pairwise(it):
        odds = it[::2]
        evens = it[1::2]
        if len(odds) > len(evens):
            evens.append(None)
        return zip(odds, evens)
    context.update({
        'snippets': pairwise(snippets)})
    return render(request, 'users-snippets.html', context)


@login_required(login_url='/login/')
def users_snippets_view(request):
    snippets = Snippet.objects.filter(user=request.user)
    return render_snippets(request, snippets, {'title': 'Your snippets'})


@login_required(login_url='/login/')
def all_snippets_view(request):
    return render_snippets(request, Snippet.objects.all(), {'title': 'Explore'})


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/success'

    def form_valid(self, form):
        data = form.cleaned_data
        user = auth_models.User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.save()
        return super(RegisterView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/success'

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(
            username=data['username'], password=data['password'])
        if user is not None:
            login(self.request, user)
            return redirect('/snippets')
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login/')
def compose_message(request):
    if request.method == 'GET':
        form = MessageForm()
        return render(request, 'message.html', {'form': form})
    elif request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            message = Message(user=request.user, text=data['text'])
            message.save()
    return redirect('/')
