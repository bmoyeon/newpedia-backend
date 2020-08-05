from django.urls import path

from .views import (
    SearchView,
    SearchListView
)

urlpatterns = [
    path('', SearchView.as_view()),
    path('/list', SearchListView.as_view())
]
