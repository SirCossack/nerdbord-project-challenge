from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.loginpage),
    path('login/', views.login),
    path('signup/', views.signup),
    path('signing/', views.signing),
    path('loggedin/', views.loggedin),
    path('logout/', views.logout),
]