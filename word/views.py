import random

from django.views import View
from django.http import (
    HttpResponse,
    JsonResponse
)

from .models import (
    Menu,
    Category
)

class MenuView(View):
    def get(self, request):
        try:
            menu_id = request.GET.get('menu_id')

            menus = Menu.objects.all()
            categories = Category.objects.select_related('menu').filter(menu=menu_id)

            menu_list = [{
                'menu_id' : menu.id,
                'menu_name' : menu.name
            } for menu in menus]

            category_list = [{
                'category_id' : category.id,
                'category_name' : category.name
            } for category in categories]

            return JsonResponse({
                'menu_list' : menu_list,
                'category_list' : category_list
            }, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
