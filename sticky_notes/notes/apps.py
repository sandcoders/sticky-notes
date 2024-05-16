# notes/apps.py

"""
This module contains the application configurations for the
'notes' Django app.
"""

from django.apps import AppConfig


class NotesConfig(AppConfig):
    """
    The NotesConfig class inherits from Django's AppConfig class,
    handling the settings and behaviors specific to the 'notes' app.

    Attributes
    ----------
    default_auto_field (str):
      Specifies the type of auto field to use as a primary key for
      models in this app. It defaults to BigAutoField.
    name (str):
      Defines the path to the application.
    """

    # Define the database auto field type and path to the app
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'
