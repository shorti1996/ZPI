from django.contrib.auth.models import User
from django.http import HttpResponse


# example
# @api_permission(['SuperUser'])
def api_permission(permission_list):
    def wrapper(func):
        def func_wrapper(self, args, **kwargs):
            try:
                print(args.user)
                user = User.objects.get(username=args.user)
                if not user.groups.filter(name__in=permission_list).exists():
                    return HttpResponse(status=403)
                return func(self, args, **kwargs)
            except Exception as e:
                return HttpResponse(status=401)
        return func_wrapper
    return wrapper
