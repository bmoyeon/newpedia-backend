from django.urls import path
from .views import (
    MenuView,
    SubWordListView,
    MainWordListView
)

urlpatterns = [
    path('', MenuView.as_view()),
    path('/sub-list', SubWordListView.as_view()),
    path('/main-list', MainWordListView.as_view()),
]
