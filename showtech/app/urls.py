from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.main, name='main'),
    path('result', views.result, name='result'),
    path('file', views.file, name='file'),
    path('download', views.download, name='download'),
    path('textarea', views.textarea, name='textarea'),
    path('snapshot', views.snapshot, name='snapshot'),

]