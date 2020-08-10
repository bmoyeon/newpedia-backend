import json
import random

from django.views import View
from django.http import (
    HttpResponse,
    JsonResponse
)
from django.db.models import Q, Sum
from django.core.paginator import Paginator

from .models import (
    Menu,
    Category,
    Word,
    WordAccount,
    WordCategory
)
from .utils import find_category
from account.models import Account
from account.utils import login_required

class MenuView(View):
    def get(self, request):
        try:
            menu_id = request.GET.get('menu_id', None)

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
            words = Word.objects.prefetch_related(
                'wordcategory_set__category',
                'wordaccount_set'
            ).order_by('-created_at')[:30]

            sub_word_list = [{
                'word_id'          : word.id,
                'word_name'        : word.name,
                'word_description' : word.description,
                'word_example'     : word.example,
                'word_like'        : word.wordaccount_set.filter(Q(word_id = word.id) & Q(like = 1)).count(),
                'word_dislike'     : word.wordaccount_set.filter(Q(word_id = word.id) & Q(dislike = 1)).count(),
                'word_category'    : [
                    word_category.category.name
                    for word_category in word.wordcategory_set.exclude(category__menu_id = 3)
                ]
            } for word in words]

            random.shuffle(sub_word_list)

            return JsonResponse({'sub_word_list' : sub_word_list}, status = 200)

        except Word.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status = 404)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class MainWordListView(View):
    def get(self, request):
        try:
            words = Word.objects.prefetch_related(
                'wordcategory_set__category',
                'wordaccount_set__account'
            ).order_by('-created_at')

            sort = request.GET.get('sort', None)
            if sort == 'new':
                words
            elif sort == 'like':
                words = words.annotate(
                    sum = Sum('wordaccount__like')
                ).order_by('-sum')

            page = request.GET.get('page', 1)
            paginator = Paginator(words, 7)
            total_count = paginator.count
            words = paginator.get_page(page)

            main_word_list = [{
                'word_id'          : word.id,
                'word_name'        : word.name,
                'word_description' : word.description,
                'word_example'     : word.example,
                'word_like'        : word.wordaccount_set.filter(Q(word_id = word.id) & Q(like = 1)).count(),
                'word_dislike'     : word.wordaccount_set.filter(Q(word_id = word.id) & Q(dislike = 1)).count(),
                'word_category'    : [
                    word_category.category.name
                    for word_category in word.wordcategory_set.exclude(category__menu_id = 3)
                ],
                'word_created_user' : word.wordaccount_set.get(is_created = 1).account.nickname,
                'word_updated_user' : (
                    word.wordaccount_set.filter(is_updated = 1).last().account.nickname
                    if word.wordaccount_set.filter(is_updated = 1).last() else ''
                )
            } for word in words]
            return JsonResponse({'main_word_list' : main_word_list}, status = 200)

        except Word.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status = 404)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class WordView(View):
    def get(self, request, word_id):
        try:
            word = Word.objects.prefetch_related(
                'wordcategory_set__category',
                'wordaccount_set__account'
            ).get(id = word_id)

            word_updated = word.wordaccount_set.filter(is_updated=1).last()

            word_info = {
                'word_id'          : word.id,
                'word_name'        : word.name,
                'word_description' : word.description,
                'word_example'     : word.example,
                'word_like'        : word.wordaccount_set.filter(Q(word_id = word.id) & Q(like = 1)).count(),
                'word_dislike'     : word.wordaccount_set.filter(Q(word_id = word.id) & Q(dislike = 1)).count(),
                'word_category'    : [
                    word_category.category.name
                    for word_category in word.wordcategory_set.exclude(category__menu_id = 3)
                ],
                'word_created_user' : word.wordaccount_set.get(is_created = 1).account.nickname,
                'word_updated_user' : (word_updated.account.nickname if word_updated else '')
            }
            return JsonResponse({'word_info' : word_info}, status = 200)

        except Word.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status = 404)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

    @login_required
    def put(self, request, word_id):
        data = json.loads(request.body)

        try:
            word = Word.objects.get(id = word_id)

            word.name        = data['name']
            word.description = data['description']
            word.example     = data['example']
            word.save()

            word_category = WordCategory.objects.filter(word_id = word_id)
            word_category.delete()

            category_list = data['category'] + [find_category(data['name'])]
            for category in category_list:
                WordCategory.objects.create(
                    word_id     = word_id,
                    category_id = Category.objects.get(name = category).id
                )

            if WordAccount.objects.filter(
                word_id = word_id,
                account = Account.objects.get(id = request.user.id)
            ).exists():
                word_account = WordAccount.objects.get(
                    word_id = word_id,
                    account = Account.objects.get(id = request.user.id)
                )
                if WordAccount.objects.filter(is_updated = False):
                    word_account.is_updated = True
                    word_account.save()

                    return HttpResponse(status = 200)

            WordAccount.objects.create(
                word_id    = word_id,
                account    = Account.objects.get(id = request.user.id),
                is_updated = True
            )

            return HttpResponse(status = 200)

        except Category.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status = 404)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

class WordCreateView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Word.objects.filter(name = data['name']).exists():
                return JsonResponse({'message' : 'ALREADY_WORD'}, status = 200)

            word_id = Word.objects.create(
                name        = data['name'],
                description = data['description'],
                example     = data['example']
            ).id

            category_list = data['category'] + [find_category(data['name'])]
            for category in category_list:
                WordCategory.objects.create(
                    word_id     = word_id,
                    category_id = Category.objects.get(name = category).id
                )

            WordAccount.objects.create(
                word_id    = word_id,
                account    = Account.objects.get(id = request.user.id),
                is_created = True
            )

            return HttpResponse(status = 200)

        except Category.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status = 404)

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

                elif word.dislike == 1:
                    word.like = True
                    word.dislike = False
                    word.save()

                    return HttpResponse(status = 200)

                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 200)

            word = Word.objects.get(id = word_id)
            WordAccount.objects.create(
                word_id = word.id,
                account = Account.objects.get(id = request.user.id),
                like    = True
            )
            return HttpResponse(status = 200)

        except Word.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status = 404)

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

                elif word.like == 1:
                    word.dislike = True
                    word.like = False
                    word.save()

                    return HttpResponse(status = 200)

                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 200)

            word = Word.objects.get(id = word_id)
            WordAccount.objects.create(
                word_id = word.id,
                account = Account.objects.get(id = request.user.id),
                dislike = True
            )
            return HttpResponse(status = 200)

        except Word.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXISTS'}, status = 404)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
