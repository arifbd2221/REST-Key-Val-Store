from django.contrib import admin
from django.urls import path
from app.views import KeyVal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('values/', KeyVal.as_view(), name='kv')
,]
