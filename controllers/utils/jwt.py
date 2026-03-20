import datetime
from django.conf import settings
from multitenancy.settings import SECRET_KEY
from functools import wraps
from django.http import JsonResponse
import jwt

class JWT:
    def decode_token(self, token, key=SECRET_KEY, algo=['HS256']):
        try:
            return {"status": 200, "data": jwt.decode(token, key, algorithms=algo)}
        except Exception as e:
            return {"status": 402, "error_message": e}
        
    def generate_token (self, user):
        expiration_time = datetime.datetime.utcnow () + settings.TOKEN_EXPIRATION_TIME
        payload = {
            'tnt': user.tenant,
            'user_id': user.id,
            'email': user.email,
            "company": user.default_company,
            "cid":user.company_id,
            'exp': expiration_time,
        }
        token = jwt.encode (payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def verify_token (self, token):
        try:
            payload = jwt.decode (token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            email = payload['email']
            user = user_id
            return {'user': user, 'status': True}
        except jwt.ExpiredSignatureError:
            return {"message": "Your Token Has Expired", 'status': None}
        except jwt.InvalidTokenError:
            return {"message": "your JWT is Invalid", 'status': None}
        
    def jwt_required(self, view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs): 
            if request.headers.get ('Authorization') is not None:
                token = request.headers.get('Authorization', '').split(' ')[1]
                response = self.verify_token(token)
                if response['status']:
                    request.user = response['user']
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse(response, status=401)
            return JsonResponse ({'message': 'Access denied. Missing Authorization Header'}, status=401)

        return _wrapped_view
