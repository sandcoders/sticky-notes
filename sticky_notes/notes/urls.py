# notes/urls.py

"""
This module defines URL patterns for the Sticky Notes application.

It creates a list named urlpatterns that contains several URL patterns
used for routing in the Sticky Notes application. Each URL pattern
corresponds to a specific view relating to individual CRUD actions as
well as signing up, logging in, and logging out.
"""

from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (note_signup, note_logout, note_noteboard, note_create,
                    note_read, note_update, note_delete)

urlpatterns = [
    # URL pattern for user signup
    path('signup/', note_signup, name='signup'),

    # URL pattern for user login
    path('accounts/login/',
         LoginView.as_view(template_name='notes/note_login.html'), name='login'
         ),

    # URL pattern for user logout
    path('logout/', note_logout, name='logout'),

    # URL pattern for displaying a list of all notes
    path("", note_noteboard, name="note_noteboard"),

    # URL pattern for creating a new note
    path("note/create/", note_create, name="note_create"),

    # URL pattern for reading an existing note
    path("note/<int:pk>/read/", note_read, name="note_read"),

    # URL pattern for updating an existing note
    path("note/<int:pk>/update/", note_update, name="note_update"),

    # URL pattern for deleting an existing note
    path("note/<int:pk>/delete/", note_delete, name="note_delete"),
]
