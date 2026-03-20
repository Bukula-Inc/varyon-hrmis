from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class LiteAuthentication (ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        User = get_user_model()
        print (vars (User))

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user

        return None
