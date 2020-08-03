from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('word', include('word.urls')),
    path('search', include('search.urls')),
]
