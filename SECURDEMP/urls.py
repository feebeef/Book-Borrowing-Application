from django.contrib import admin
from django.urls import path, include
from account import views as auth_views
from catalog import views as catalog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', auth_views.signin, name = 'signin'),
    path('register/', auth_views.register, name = 'register'),
    path('catalog/',include('catalog.urls')),
    path('logout/', auth_views.logout_user, name = 'logout'),
    path('changepassword', auth_views.change_password, name = 'changepassword'),
]
