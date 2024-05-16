# notes/views.py

"""
This module contains views for handling CRUD operations for the Sticky
Notes application as well as signup and logout processes.

Each view function is connected to specific URLs configured to interact
with the database through Django's ORM to execute CRUD operations. It
includes views for signing_up, listing all notes, creating a new note,
reading details of a specific note, updating an existing note, deleting
a note, and logging out. User feedback is provided through messages as
required by each process.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Note
from .forms import NoteForm
from .forms import SignUpForm


def note_signup(request):
    """
    View for the signup process.

    :param request: HTTP request object.
    :return: Rendered template with a signup form.
    """

    # Process for signing up
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, ("Welcome to Sticky Notes!"))
            messages.success(
                request, "Click '+ Create a Note' in the menu to get started."
            )
            return redirect('note_noteboard')
    else:
        form = SignUpForm()

    return render(request, 'notes/note_signup.html', {'form': form})


@login_required
def note_noteboard(request):
    """
    View to display a list of all notes on the user's noteboard

    :param request: HTTP request object.
    :return: Rendered template with a list of notes.
    """

    notes = Note.objects.filter(user=request.user)

    # Creating a context dictionary to pass data
    context = {
        "notes": notes,
        "note_title": "List of Notes",
    }

    return render(request, "notes/note_list.html", context)


@login_required
def note_create(request):
    """
    View to create a new note.

    :param request: HTTP request object.
    :return: Rendered template for creating a new note.
    """

    # Process for creating a note
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # set the user
            note.save()
            messages.success(request, (f'"{note.title}" has been created!'))
            return redirect("note_noteboard")
    else:
        form = NoteForm()

    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_read(request, pk):
    """
    View to display details of a specific note.

    :param request: HTTP request object.
    :param pk: Primary key of the note.
    :return: Rendered template with details of the specified note.
    """

    note = get_object_or_404(Note, pk=pk)

    # Check permissions - give error message if wrong
    if note.user != request.user:
        messages.error(
            request, "You do not have permission to access this note."
        )
        return redirect('note_noteboard')

    return render(request, "notes/note_read.html", {"note": note})


@login_required
def note_update(request, pk):
    """
    View to update an existing note.

    :param request: HTTP request object.
    :param pk: Primary key of the note to be updated.
    :return: Rendered template for updating the specified note.
    """

    note = get_object_or_404(Note, pk=pk)

    # Check permissions - give error message if wrong
    if note.user != request.user:
        messages.error(
            request, "You do not have permission to edit this note."
        )
        return redirect('note_noteboard')

    # Process for updating a note
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # set the user
            note.save()
            messages.success(request, (f'"{note.title}" has been updated!'))
            return redirect("note_noteboard")
    else:
        form = NoteForm(instance=note)

    return render(request, "notes/note_form.html", {"form": form})


@login_required
def note_delete(request, pk):
    """
    View to delete an existing note.

    :param request: HTTP request object.
    :param pk: Primary key of the note to be deleted.
    :return: Redirect to the noteboard after deletion.
    """

    note = get_object_or_404(Note, pk=pk)

    # Check permissions - give error message if wrong
    if note.user != request.user:
        messages.error(
            request, "You do not have permission to delete this note."
        )
        return redirect('note_noteboard')

    # Process for deleting a note
    note.delete()
    messages.success(request, (f'"{note.title}" has been deleted!'))
    return redirect('note_noteboard')


@login_required
def note_logout(request):
    """
    View for the log out process.

    :param request: HTTP request object.
    :return: Redirect to the login page after logging out.
    """

    # Process for logging out
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')
