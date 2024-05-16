# notes/models.py

"""
This module contains Django models for managing data for a simple
Sticky Notes application. The provided model `Note` represents a sticky
note with a user, title, and some content.

Each model in this module inherits from 'models.Model', making
integration with Django's ORM straightforward.
"""

from django.db import models
from django.conf import settings


class Note(models.Model):
    """
    Model representing a sticky note.

    Attributes / Fields
    -------------------
    user (models.ForeignKey):
        Field pointing to the user who created the note, links
        to the user model.
    title: (models.CharField):
        Field holding the note's title, limited to 50 characters.
    content (models.TextField):
        Field for storing note content.

    Methods
    -------
    __str__(self):
       Returns a string representation of the Object's title.

    :param models.Model: Django's base model class.
    """

    # Define fields for the Note model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50)
    content = models.TextField()

    # Return title as a string
    def __str__(self):
        """Returns a string representation of the title of the note."""
        return self.title
