import pdb

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from django.views.generic import FormView, TemplateView, View
from .forms import LoginForm, RegisterForm, MessageForm

from .models import Message

from django.contrib.auth import models as auth_models, authenticate, login
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
        comments = Comment.objects.filter(
            snippet=Snippet.objects.get(pk=(int(identifier))))
        return render(
            request, 'snippet.html', {'id': identifier, 'comments': comments})


def comment_view(request, identifier):
    if request.method == 'POST':
        snippet = Snippet.objects.get(pk=(int(identifier)))
        c = Comment(
            snippet=snippet, user=request.user, text=request.POST['text'])
        c.save()
        return redirect('/snippet/' + identifier)


class NewSnippetView(View):
    def get(self, request):
        s = Snippet(text='', languages='PY', user=request.user)
        s.save()
        return redirect('/snippet/' + str(s.pk))


@login_required(login_url='/login/')
def users_snippets_view(request):
    snippets = Snippet.objects.filter(user=request.user)
    return render(request, 'users-snippets.html', {'snippets': snippets})


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
            print('User has logged in:', user.username, user.email)
            return redirect('/snippets')


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
