from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r"^login/$", views.login, name="account_login"),
    url(r'^', include('allauth.urls')),
]
