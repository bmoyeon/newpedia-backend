from django.urls import path
from .views import (
    KakaoLogInView,
    NicknameView
)

urlpatterns = [
    path('/sign-in/kakao', KakaoLogInView.as_view()),
    path('/nickname', NicknameView.as_view())
]
