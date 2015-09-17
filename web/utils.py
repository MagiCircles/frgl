from django.conf import settings

def globalContext(request):
    context ={
        'current_url': request.get_full_path() + ('?' if request.get_full_path()[-1] == '/' else '&'),
        'debug': settings.DEBUG,
        'hidenavbar': 'hidenavbar' in request.GET,
        'images_hosting_path': settings.IMAGES_HOSTING_PATH,
    }
    if request.user.is_authenticated() and not request.user.is_anonymous():
        pass
    return context
