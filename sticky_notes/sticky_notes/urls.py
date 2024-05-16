# sticky_notes/urls.py

"""
URL configuration for sticky_notes project.

The `urlpatterns` list routes URLs to views. For more information please
see:     https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# Define URL patterns for the entire project
urlpatterns = [
    # Admin URL pattern, mapping to the Django admin interface
    path("admin/", admin.site.urls),

    # Include URL patterns from the 'notes' app
    # All URLs from 'notes.urls' will be prefixed with 'notes/'
    path("", include("notes.urls")),
]
