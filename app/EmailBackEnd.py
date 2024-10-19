from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# User = get_user_model()
class EmailBackEnd(ModelBackend):
    def authenticate(self,  username= None , password = None ,**kwargs ):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email = username)

        except UserModel.DoesNotExist:
            return None
        
        else:
            if user.check_password(password):
                return user
            
        return None
    
    # def get_user(self, user_id):
    #     try:
    #         return User.objects.get(pk=user_id)
    #     except User.DoesNotExist:
    #         return None