"""
URL configuration for robot_controller project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path , include
from . import views
# from .views import SignalingView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('stream/', views.stream_page, name='stream'),
    path('signaling/', views.streaming_view, name="signaling"),
    path("command/",   views.command_view,   name="command"),
    path('reset/', views.reset_signaling),
    path('', include('telepilot_users.urls')),
]
