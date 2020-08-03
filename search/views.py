import json

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from word.models import Word

class SearchView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            search_word = data['search_word']

            if search_word == ' ' or search_word == "":
                return JsonResponse({'message' : 'NO_RESULT'}, status = 200)

            search = Q(name__startswith = search_word)

            words = Word.objects.filter(search)

            search_list = [{
                'word_id'          : word.id,
                'word_name'        : word.name,
                'word_description' : word.description
            } for word in words]
            return JsonResponse({'search_list' : search_list}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
