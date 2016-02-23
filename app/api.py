from django.views.generic import View
from app.models import Snippet
from django.core.serializers import serialize


from django.http import HttpResponse


class SnippetView(View):
    def get(self, request, identifier):
        snippet = Snippet.objects.filter(id=int(identifier))
        snippet_json = serialize('json', list(snippet))
        return HttpResponse(snippet_json, content_type='application/json')

    def put(self, request, identifier):
        snippet = Snippet.objects.get(pk=int(identifier))
        snippet.text = request.body.decode()
        snippet.save()
        return HttpResponse('ok')


# TODO: make view equivalent
class UsersSnippetsView(View):
    def get(self, request):
        user = request.user
        snippets = serialize('json', list(Snippet.objects.filter(user=user)))
        return HttpResponse(snippets, content_type='application/json')
