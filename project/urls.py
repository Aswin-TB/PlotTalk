"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from REMS.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',HomeView.as_view(),name='home'),
    path('addproperty',AddProperty.as_view(),name='add_property'),
    path('',LoginView.as_view(),name='login'),
    path('signup',SignupView.as_view(),name='signup'),
    path('logout',logoutview,name='logout'),
    path('profile',ProfileView.as_view(),name='profile'),
    path('updateprofile/<int:id>',UpdateProfileView.as_view(),name='updateprofile'),
    path('propertydetails/<int:id>',PropertyDetailView.as_view(),name='propertydetails'),
    path('profiletouser/<int:id>',ProfiletouserView.as_view(),name='profiletouser'),
    path('save/<int:id>',SaveView,name='save'),
    path('savelist',SaveList.as_view(),name='savelist'),
    path('removesave/<int:id>',RemoveSave,name='removesave'),
    path('chat/<int:id>/',chat_view, name='chat'),
    path('chats',chat_list_view, name='chatlist'),
    path('editproperty/<int:id>',EditProperty.as_view(),name='editproperty'),
    path('deleteproperty/<int:id>',DeleteProperty.as_view(),name='deleteproperty'),
    path('category/<str:cat>',category,name='category'),
    path('logout',logoutview,name='logout'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
