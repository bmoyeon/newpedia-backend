import json
import jwt
import requests
import re

from django.views import View
from django.http import (
    HttpResponse,
    JsonResponse
)

from newpedia.settings import (
    SECRET_KEY,
    ALGORITHM
)
from account.models import (
    Account,
    Social
)
from account.utils import login_required

class KakaoLogInView(View):
    def post(self, request):
        try:
            kakao_token        = request.headers.get('Authorization', None)
            uri                = 'https://kapi.kakao.com/v2/user/me'
            header             = {'Authorization' : f'Bearer {kakao_token}'}
            kakao_user_request = requests.get(uri, headers = header)
            kakao_user_info    = kakao_user_request.json()
            kakao_user_id      = kakao_user_info['id']

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

        user, created = Account.objects.get_or_create(
            social_account = kakao_user_id,
            social         = Social.objects.get(name = 'kakao')
        )
        access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')

        return JsonResponse({
            'access_token' : access_token,
            'nickname'     : user.nickname
        }, status = 200)

class NicknameView(View):
    @login_required
    def get(self, request):
        return JsonResponse({'nickname' : request.user.nickname}, status = 200)

    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            nickname = data['nickname']

            if nickname == ' ' or nickname == '':
                return JsonResponse({'message' : 'NO_VALUE'}, status = 200)

            if re.match("^[가-힣]{1,12}$", nickname) == None:
                return HttpResponse(status = 401)

            if Account.objects.filter(nickname = nickname).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 200)

            user = request.user
            user.nickname = nickname
            user.save()

            return HttpResponse(status = 200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)
