from django.views.generic import View
from django.core.serializers import serialize
from django.http import HttpResponse

from rest_framework.views import APIView, Response
from rest_framework import generics

from app.models import Snippet
from .serializers import SnippetSerializer


class SnippetView(View):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, id):
        snippet = Snippet.objects.filter(id=int(id))
        snippet_json = serialize('json', list(snippet))
        return HttpResponse(snippet_json, content_type='application/json')

    def put(self, request, id):
        snippet = Snippet.objects.get(pk=int(id))
        snippet.text = request.body.decode()
        snippet.save()
        return HttpResponse('ok')


# TODO: make view equivalent
class UsersSnippetsView(View):
    def get(self, request):
        user = request.user
        snippets = serialize('json', list(Snippet.objects.filter(user=user)))
        return HttpResponse(snippets, content_type='application/json')


class AllSnippetsView(generics.ListAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
