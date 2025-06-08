"""booking-sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path, include
from hr.views import FrontendAppView
from django.conf import settings
from django.views.static import serve
from hr import handlers

handler404 = handlers.Handlers.handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hr.urls')),
    # path('api/', include('api.urls')),  # your API URLs
    # path('static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT, })
    re_path(r'^(?!api/).*$', FrontendAppView.as_view()),  # everything else to frontend
]

# from django.urls import path, re_path, include
# from .views import FrontendAppView

# urlpatterns = [
#     path('api/', include('api.urls')),  # your API URLs
#     re_path(r'^(?!api/).*$', FrontendAppView.as_view()),  # everything else to frontend
# ]
