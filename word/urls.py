from django.urls import path
from .views import (
    MenuView,
    SubWordListView,
    MainWordListView,
    WordDetailView,
    LikeView,
    DislikeView,
    WordCreateView,
    WordUpdateView
)

urlpatterns = [
    path('', MenuView.as_view()),
    path('/sub-list', SubWordListView.as_view()),
    path('/main-list', MainWordListView.as_view()),
    path('/<int:word_id>', WordDetailView.as_view()),
    path('/<int:word_id>/like', LikeView.as_view()),
    path('/<int:word_id>/dislike', DislikeView.as_view()),
    path('/new', WordCreateView.as_view()),
    path('/<int:word_id>/update', WordUpdateView.as_view()),
]
