from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'service'

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
