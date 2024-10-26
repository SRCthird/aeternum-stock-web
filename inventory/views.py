from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings


@login_required(login_url=f'/{settings.SITE_PREFIX}accounts/login')
def index(request):
    response: str = "Hello, test inventory here"
    return HttpResponse(
        response.encode("utf-8")
    )
