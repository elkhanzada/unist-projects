from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'he_digit_recognizer'
urlpatterns = [
    # two paths: with or without given image
    path('', views.index, name='index'),
    # path('output', views.output, name='output'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)