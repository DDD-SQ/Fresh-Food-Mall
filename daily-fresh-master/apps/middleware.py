from django.conf import settings
from df_user.models import UserInfo


class FixedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'user_id' not in request.session:
            try:
                fixed_user_id = getattr(settings, 'FIXED_USER_ID', 32)
                fixed_user = UserInfo.objects.get(id=fixed_user_id)
                request.session['user_id'] = fixed_user.id
                request.session['user_name'] = fixed_user.uname
            except UserInfo.DoesNotExist:
                pass
        return self.get_response(request)
