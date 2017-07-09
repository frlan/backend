"""wepublic_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from django.conf import settings
from wp_core.views import *
from wp_core.views_answers import AnswerViewSet
from users.views import *
from wp_news.views import *

router = DefaultRouter()
router.register(r'Tags', TagViewSet)
router.register(r'Questions', QuestionsViewSet)
router.register(r'Answers', AnswerViewSet )
router.register(r'Users', UserViewSet)
router.register(r'News', NewsEntryViewSet )
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
urlpatterns += router.urls



def print_url_pattern_names(patterns):
    """Print a list of urlpattern and their names"""
    for pat in patterns:
        if pat.__class__.__name__ == 'RegexURLResolver':            # load patterns from this RegexURLResolver
            print_url_pattern_names(pat.url_patterns)
        elif pat.__class__.__name__ == 'RegexURLPattern':           # load name from this RegexURLPattern
            if pat.name is not None:
                print('[API-URL] {} \t\t\t-> {}'.format(pat.name, pat.regex.pattern))

 
if settings.DEBUG:
    print_url_pattern_names(urlpatterns)
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
