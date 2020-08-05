import json
import random

from django.views import View
from django.http import (
    HttpResponse,
    JsonResponse
)
from django.db.models import Count

from .models import (
    Menu,
    Category,
    Word,
    WordAccount
)
from account.models import Account
from account.utils import login_required

class MenuView(View):
    def get(self, request):
        try:
            menu_id = request.GET.get('menu_id')

            menus = Menu.objects.all()
            categories = Category.objects.select_related('menu').filter(menu = menu_id)

            menu_list = [{
                'menu_id'   : menu.id,
                'menu_name' : menu.name
            } for menu in menus]

            category_list = [{
                'category_id'   : category.id,
                'category_name' : category.name
            } for category in categories]

            return JsonResponse({
                'menu_list'     : menu_list,
                'category_list' : category_list
            }, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class SubWordListView(View):
    def get(self, request):
        try:
            words = Word.objects.prefetch_related('wordcategory_set__category', 'wordaccount_set').order_by('-created_at')[:30]

            sub_word_list = [{
                'word_id'          : word.id,
                'word_name'        : word.name,
                'word_description' : word.description,
                'word_example'     : word.example,
                'word_like'        : word.wordaccount_set.filter(word_id = word.id, like = 1).count(),
                'word_dislike'     : word.wordaccount_set.filter(word_id = word.id, dislike = 1).count(),
                'word_category'    : [word_category.category.name for word_category in word.wordcategory_set.exclude(category__menu_id = 3)]
            } for word in words]

            random.shuffle(sub_word_list)

            return JsonResponse({'sub_word_list' : sub_word_list}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class MainWordListView(View):
    def get(self, request):
        try:
            words = Word.objects.prefetch_related('wordcategory_set__category', 'wordaccount_set__account').order_by('-created_at')

            sort = request.GET.get('sort', None)

            if sort == 'new':
                words
            elif sort == 'like':
                words = words.annotate(count = Count('wordaccount__word_id')).filter(wordaccount__dislike=1).order_by('-count');

            main_word_list = [{
                'word_id'          : word.id,
                'word_name'        : word.name,
                'word_description' : word.description,
                'word_example'     : word.example,
                'word_like'        : word.wordaccount_set.filter(word_id = word.id, like = 1).count(),
                'word_dislike'     : word.wordaccount_set.filter(word_id = word.id, dislike = 1).count(),
                'word_category'    : [word_category.category.name for word_category in word.wordcategory_set.exclude(category__menu_id = 3)]
            } for word in words]

            return JsonResponse({'main_word_list' : main_word_list}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class WordDetailView(View):
    def get(self, request, word_id):
        try:
            word = Word.objects.prefetch_related('wordcategory_set__category', 'wordaccount_set').get(id = word_id)

            word_info = {
                'word_id'          : word.id,
                'word_name'        : word.name,
                'word_description' : word.description,
                'word_example'     : word.example,
                'word_like'        : word.wordaccount_set.filter(word_id = word.id, like = 1).count(),
                'word_dislike'     : word.wordaccount_set.filter(word_id = word.id, dislike = 1).count(),
                'word_category'    : [word_category.category.name for word_category in word.wordcategory_set.exclude(category__menu_id = 3)]
            }
            return JsonResponse({'word_info' : word_info}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class LikeView(View):
    @login_required
    def post(self, request, word_id):

        try:
            if WordAccount.objects.filter(
                word_id = word_id,
                account = Account.objects.get(id = request.user.id)
            ).exists():

                word = WordAccount.objects.get(
                    word_id = word_id,
                    account = Account.objects.get(id = request.user.id)
                )

                if word.like == 0 and word.dislike == 0:
                    word.like = True
                    word.save()

                    return HttpResponse(status = 200)

                return JsonResponse({'message' : 'NOT_ALLOWED'}, status = 406)

            word = Word.objects.get(id = word_id)
            WordAccount.objects.create(
                word_id    = word.id,
                account_id = Account.objects.get(id = request.user.id).id,
                like       = True
            )
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class DislikeView(View):
    @login_required
    def post(self, request, word_id):

        try:
            if WordAccount.objects.filter(
                word_id = word_id,
                account = Account.objects.get(id = request.user.id)
            ).exists():

                word = WordAccount.objects.get(
                    word_id = word_id,
                    account = Account.objects.get(id = request.user.id)
                )

                if word.like == 0 and word.dislike == 0:
                    word.dislike = True
                    word.save()

                    return HttpResponse(status = 200)

                return JsonResponse({'message' : 'NOT_ALLOWED'}, status = 406)

            word = Word.objects.get(id = word_id)
            WordAccount.objects.create(
                word_id    = word.id,
                account_id = Account.objects.get(id = request.user.id).id,
                dislike    = True
            )
            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
