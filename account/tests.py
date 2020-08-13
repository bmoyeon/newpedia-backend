import json
import bcrypt
import jwt

from django.test import (
    TestCase,
    Client,
    TransactionTestCase
)
from unittest.mock import patch

from .models import (
    Account,
    Social
)
from newpedia.settings import (
    SECRET_KEY,
    ALGORITHM
)

access_token = jwt.encode({'user_id' : 1}, SECRET_KEY, ALGORITHM).decode('utf-8')

class KakaoLoginTest(TransactionTestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()

    def test_kakao_login_success(self):
        with patch('account.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info  = {'id' : 1234}
                    return user_info

            user_profile            = UserInfo()
            mocked_get.return_value = user_profile
            client                  = Client()
            response                = client.post('/account/sign-in/kakao', content_type = 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "access_token" : access_token,
                "nickname" : ""
            })

    def test_kakao_login_new_account(self):
        with patch('account.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info  = {'id' : 5678}
                    return user_info

            user_profile            = UserInfo()
            mocked_get.return_value = user_profile
            client                  = Client()
            response                = client.post('/account/sign-in/kakao', content_type = 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "access_token" : jwt.encode({'user_id' : 3}, SECRET_KEY, ALGORITHM).decode('utf-8'),
                "nickname" : ""
            })

    def test_kakao_login_error(self):
        with patch('account.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info  = {'id' : 1234}
                    return user_info

            user_profile            = UserInfo()
            mocked_get.return_value = user_profile
            client                  = Client()
            response = client.post('/account/sign-in', content_type = 'application/json')
            self.assertEqual(response.status_code, 404)

class NicknameTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '이미존재하는닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()

    def test_nickname_get_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        response = client.get('/account/nickname', **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'nickname' : '이미존재하는닉네임'})

    def test_nickname_get_fail(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : '123'}
        response = client.get('/account/nickname', **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'INVALID_TOKEN'})

    def test_nickname_post_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        response = client.post('/account/nickname', json.dumps({'nickname' : '비모'}), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_nickname_post_no_value(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        response = client.post('/account/nickname', json.dumps({'nickname' : ''}), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'NO_VALUE'})

    def test_nickname_post_validation(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        response = client.post('/account/nickname', json.dumps({'nickname' : 't'}), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 401)

    def test_nickname_post_already_exists(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : access_token}
        response = client.post('/account/nickname', json.dumps({'nickname' : '이미존재하는닉네임'}), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'ALREADY_EXISTS'})
