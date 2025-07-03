from django.conf import settings

def global_variables(request):
    return {'APP_MODE_SIMPLE': settings.APP_MODE_SIMPLE}
