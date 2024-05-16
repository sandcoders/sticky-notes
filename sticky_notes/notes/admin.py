# notes/admin.py

"""
Admin Configuration for Note Model

This module configures the Django admin interface to include and manage
the Note model from this application. It facilitates administrators in
performing CRUD operations on Note entries directly from the Django
admin panel.
"""

from django.contrib import admin
from .models import Note

# Register your models here.

# Note model - registration with the admin interface
admin.site.register(Note)
