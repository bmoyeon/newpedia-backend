from django.urls import path
from .views import (
    MenuView,
    CategoryView,
    WordListView,
    WordCreateView,
    WordDetailView,
    LikeView,
    DislikeView
)

urlpatterns = [
    path('/menu', MenuView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/list', WordListView.as_view()),
    path('/new', WordCreateView.as_view()),
    path('/<int:word_id>', WordDetailView.as_view()),
    path('/<int:word_id>/like', LikeView.as_view()),
    path('/<int:word_id>/dislike', DislikeView.as_view())
]
