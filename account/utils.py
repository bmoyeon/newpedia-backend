import json
import jwt

from django.http import JsonResponse

from .models import Account
from newpedia.settings import (
    SECRET_KEY,
    ALGORITHM
)

def login_required(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            access_token = request.headers['Authorization']
            user_id      = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)['user_id']
            user         = Account.objects.get(id = user_id)
            request.user = user

            return func(self, request, *args, **kwargs)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

        except Account.DoesNotExist:
            return JsonResponse({'message' : 'UNKNOWN_USER'}, status = 401)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)

    return wrapper
