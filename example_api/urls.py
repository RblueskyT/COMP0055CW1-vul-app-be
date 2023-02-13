from django.urls import path
from . import views

urlpatterns = [
    # /example_api/
    path('', views.index, name='index'),
    # /example_api/post_demo/
    path('post_demo', views.post_demo, name='post_demo'),
]