import json
import bcrypt
import jwt

from django.test import (
    TestCase,
    Client
)

from .models import (
    Menu,
    Category,
    Word,
    WordCategory,
    WordAccount
)
from account.models import (
    Social,
    Account
)
from newpedia.settings import (
    SECRET_KEY,
    ALGORITHM
)

user1_access_token = jwt.encode({'user_id' : 1}, SECRET_KEY, ALGORITHM).decode('utf-8')
user2_access_token = jwt.encode({'user_id' : 2}, SECRET_KEY, ALGORITHM).decode('utf-8')

class MenuTest(TestCase):
    def setUp(self):
        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

    def tearDown(self):
        Menu.objects.all().delete()

    def test_menu_get_success(self):
        client = Client()
        response = client.get('/word/menu', content_type = 'application/json')
        result = {
            "menu_list" : [
                {
                    "menu_id" : 1,
                    "menu_name" : "메뉴이름"
                }
            ]
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

class CategoryTest(TestCase):
    def setUp(self):
        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

    def tearDown(self):
        Menu.objects.all().delete()
        Category.objects.all().delete()

    def test_category_get_success(self):
        client = Client()
        response = client.get('/word/category?menu_id=1', content_type = 'application/json')
        result = {
            "category_list" : [
                {
                    "category_id" : 1,
                    "category_name" : "카테고리이름"
                }
            ]
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_category_get_fail(self):
        client = Client()
        response = client.get('/word/category', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'NOT_FOUND'})
        self.assertEqual(response.status_code, 404)

class WordListTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

        Word.objects.create(
            id          = 1,
            name        = '단어이름',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.'
        )

        WordCategory.objects.create(
            id       = 1,
            category = Category.objects.get(id = 1),
            word     = Word.objects.get(id =1)
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Word.objects.all().delete()
        WordCategory.objects.all().delete()

    def test_word_list_get_success(self):
        client = Client()
        response = client.get('/word/list', content_type = 'application/json')
        result = {
            "word_list" : [
                {
                    "word_id" : 1,
                    "word_name" : "단어이름",
                    "word_description" : "단어에 대한 설명입니다.",
                    "word_example" : "단어를 활용한 예시입니다.",
                    "word_like" : 0,
                    "word_dislike" : 0,
                    "word_category" : [
                        "카테고리이름"
                    ]
                }
            ]
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

class SearchTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

        Word.objects.create(
            id          = 1,
            name        = '단어이름',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.'
        )

        WordCategory.objects.create(
            id       = 1,
            category = Category.objects.get(id = 1),
            word     = Word.objects.get(id =1)
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Word.objects.all().delete()
        WordCategory.objects.all().delete()

    def test_search_get_success(self):
        client = Client()
        response = client.get('/word/list?search_word=단', content_type = 'application/json')
        result = {
            "word_list" : [
                {
                    "word_id" : 1,
                    "word_name" : "단어이름",
                    "word_description" : "단어에 대한 설명입니다.",
                    "word_example" : "단어를 활용한 예시입니다.",
                    "word_like" : 0,
                    "word_dislike" : 0,
                    "word_category" : [
                        "카테고리이름"
                    ]
                }
            ]
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_search_get_fail(self):
        client = Client()
        response = client.get('/word/list?search_word=', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'NO_VALUE'})
        self.assertEqual(response.status_code, 200)

    def test_search_list_get_success(self):
        client = Client()
        response = client.get('/word/list/search?search_word=단', content_type = 'application/json')
        result = {
            "search_list" : [
                {
                    "word_id" : 1,
                    "word_name" : "단어이름",
                    "word_description" : "단어에 대한 설명입니다."
                }
            ]
        }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_search_list_get_fail(self):
        client = Client()
        response = client.get('/word/list/search?search_word=', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'NO_VALUE'})
        self.assertEqual(response.status_code, 200)

class WordCreateTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

        Category.objects.create(
            id   = 2,
            name = 'ㄷ',
            menu = Menu.objects.get(id = 1)
        )

        Word.objects.create(
            id          = 1,
            name        = '단어이름',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.'
        )

        WordCategory.objects.create(
            id       = 1,
            category = Category.objects.get(id = 1),
            word     = Word.objects.get(id =1)
        )

        WordAccount.objects.create(
            id         = 1,
            account    = Account.objects.get(id = 1),
            word       = Word.objects.get(id = 1),
            is_created = True
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Word.objects.all().delete()
        WordCategory.objects.all().delete()
        WordAccount.objects.all().delete()

    def test_word_create_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        data_input = {
            "name" : "등록할단어이름",
            "description" : "단어에 대한 설명입니다.",
            "example" : "",
            "category" : ["카테고리이름"]
        }
        response = client.post('/word/new', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_word_create_no_value(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        data_input = {
            "name" : "",
            "description" : "단어에 대한 설명입니다.",
            "example" : "",
            "category" : ["카테고리이름"]
        }
        response = client.post('/word/new', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'NO_VALUE'})

    def test_word_create_already_exists(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        data_input = {
            "name" : "단어이름",
            "description" : "단어에 대한 설명입니다.",
            "example" : "",
            "category" : ["카테고리이름"]
        }
        response = client.post('/word/new', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'ALREADY_WORD'})

class WordDetailTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

        Word.objects.create(
            id          = 1,
            name        = '단어이름',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.'
        )

        WordCategory.objects.create(
            id       = 1,
            category = Category.objects.get(id = 1),
            word     = Word.objects.get(id = 1)
        )

        WordAccount.objects.create(
            id         = 1,
            account    = Account.objects.get(id = 1),
            word       = Word.objects.get(id = 1),
            is_created = True
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Word.objects.all().delete()
        WordCategory.objects.all().delete()
        WordAccount.objects.all().delete()

    def test_word_detail_get_success(self):
        client = Client()
        response = client.get('/word/1', content_type = 'application/json')
        result = {
            "word_info" : {
                "word_id" : 1,
                "word_name" : "단어이름",
                "word_description" : "단어에 대한 설명입니다.",
                "word_example" : "단어를 활용한 예시입니다.",
                "word_like" : 0,
                "word_dislike" : 0,
                "word_category" : [
                    "카테고리이름"
                ],
                "word_created_user" : "닉네임",
                "word_updated_user" : ""
            }
        }
        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_word_detail_get_fail(self):
        client = Client()
        response = client.get('/word/2', content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

class WordUpdateTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

        Category.objects.create(
            id   = 2,
            name = 'ㄷ',
            menu = Menu.objects.get(id = 1)
        )

        Category.objects.create(
            id   = 3,
            name = 'ㅅ',
            menu = Menu.objects.get(id = 1)
        )

        Word.objects.create(
            id          = 1,
            name        = '단어이름',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.',
        )

        Word.objects.create(
            id          = 2,
            name        = '단어이름2',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.',
        )

        WordCategory.objects.create(
            id       = 1,
            category = Category.objects.get(id = 1),
            word     = Word.objects.get(id =1)
        )

        WordAccount.objects.create(
            id         = 1,
            account    = Account.objects.get(id = 1),
            word       = Word.objects.get(id = 1),
            is_created = True
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Word.objects.all().delete()
        WordCategory.objects.all().delete()
        WordAccount.objects.all().delete()

    def test_word_update_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        data_input = {
            "name" : "수정한단어이름",
            "description" : "단어에 대한 설명입니다.",
            "example" : "",
            "category" : ["카테고리이름"]
        }
        response = client.put('/word/1', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_word_update_fail(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        data_input = {
            "name" : "수정한단어이름",
            "description" : "단어에 대한 설명입니다.",
            "example" : "",
            "category" : ["카테고리이름"]
        }
        response = client.put('/word/3', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

    def test_word_update_no_value(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        data_input = {
            "name" : "",
            "description" : "단어에 대한 설명입니다.",
            "example" : "",
            "category" : ["카테고리이름"]
        }
        response = client.put('/word/1', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'NO_VALUE'})

    def test_word_update_already_exists(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        data_input = {
            "name" : "단어이름2",
            "description" : "단어에 대한 설명입니다.",
            "example" : "",
            "category" : ["카테고리이름"]
        }
        response = client.put('/word/1', json.dumps(data_input), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'ALREADY_WORD'})

class LikeTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

        Account.objects.create(
            id             = 2,
            nickname       = '닉네임2',
            social_account = '5678',
            social         = Social.objects.get(id = 1)
        )

        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

        Word.objects.create(
            id          = 1,
            name        = '단어이름',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.',
        )

        Word.objects.create(
            id          = 2,
            name        = '단어이름2',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.',
        )

        WordCategory.objects.create(
            id       = 1,
            category = Category.objects.get(id = 1),
            word     = Word.objects.get(id = 1)
        )

        WordAccount.objects.create(
            id         = 1,
            account    = Account.objects.get(id = 1),
            word       = Word.objects.get(id = 1),
            is_created = True
        )

        WordAccount.objects.create(
            id         = 2,
            account    = Account.objects.get(id = 2),
            word       = Word.objects.get(id = 2),
            is_created = True,
            like       = 1
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Word.objects.all().delete()
        WordCategory.objects.all().delete()
        WordAccount.objects.all().delete()

    def test_like_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        response = client.post('/word/1/like', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'word_like' : 1})
        self.assertEqual(response.status_code, 200)

    def test_like_fail(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        response = client.post('/word/3/like', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

    def test_like_already_exists(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user2_access_token}
        response = client.post('/word/2/like', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'ALREADY_EXISTS'})
        self.assertEqual(response.status_code, 200)

class DislikeTest(TestCase):
    def setUp(self):
        Social.objects.create(
            id   = 1,
            name = 'kakao'
        )

        Account.objects.create(
            id             = 1,
            nickname       = '닉네임',
            social_account = '1234',
            social         = Social.objects.get(id = 1)
        )

        Account.objects.create(
            id             = 2,
            nickname       = '닉네임2',
            social_account = '5678',
            social         = Social.objects.get(id = 1)
        )

        Menu.objects.create(
            id   = 1,
            name = '메뉴이름'
        )

        Category.objects.create(
            id   = 1,
            name = '카테고리이름',
            menu = Menu.objects.get(id = 1)
        )

        Word.objects.create(
            id          = 1,
            name        = '단어이름',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.',
        )

        Word.objects.create(
            id          = 2,
            name        = '단어이름2',
            description = '단어에 대한 설명입니다.',
            example     = '단어를 활용한 예시입니다.',
        )

        WordCategory.objects.create(
            id       = 1,
            category = Category.objects.get(id = 1),
            word     = Word.objects.get(id = 1)
        )

        WordAccount.objects.create(
            id         = 1,
            account    = Account.objects.get(id = 1),
            word       = Word.objects.get(id = 1),
            is_created = True
        )

        WordAccount.objects.create(
            id         = 2,
            account    = Account.objects.get(id = 2),
            word       = Word.objects.get(id = 2),
            is_created = True,
            dislike    = 1
        )

    def tearDown(self):
        Social.objects.all().delete()
        Account.objects.all().delete()
        Menu.objects.all().delete()
        Category.objects.all().delete()
        Word.objects.all().delete()
        WordCategory.objects.all().delete()
        WordAccount.objects.all().delete()

    def test_dislike_success(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        response = client.post('/word/1/dislike', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'word_dislike' : 1})
        self.assertEqual(response.status_code, 200)

    def test_dislike_fail(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user1_access_token}
        response = client.post('/word/3/dislike', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'DOES_NOT_EXIST'})
        self.assertEqual(response.status_code, 404)

    def test_dislike_already_exists(self):
        client = Client()
        header = {'HTTP_AUTHORIZATION' : user2_access_token}
        response = client.post('/word/2/dislike', **header, content_type = 'application/json')
        self.assertEqual(response.json(), {'message' : 'ALREADY_EXISTS'})
        self.assertEqual(response.status_code, 200)
