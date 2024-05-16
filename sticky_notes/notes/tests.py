# notes/tests.py

"""
This script evaluates the functionality of the Sticky Notes application.
It utilises the Django module 'django.test.TestCase' which is a subclass
of 'unittest.TestCase' from the Python unittest framework.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Note


class AuthTestCase(TestCase):
    """
    Test case class for authentication processes including signup,
    login, and logout in a Django application.

    Methods
    -------
    setUp(self):
        Set up function to create a test user before each test.
    test_user_signup(self):
        Test the signup functionality to ensure the user is created and
        authenticated correctly.
    def test_login(self):
        Test the login functionality with both correct and incorrect
        credentials.
    def test_logout(self):
        Test the logout process and redirection behavior to login page,
        and access restrictions post-logout.
    """

    def setUp(self):
        """Set up function to create a test user before each test."""

        # Create a User object
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_user_signup(self):
        """Test the signup functionality to ensure the user is created
        and authenticated correctly."""

        # Define the data for creating a new user
        new_user_data = {
            'username': 'newuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'newuser@example.com'
        }

        # Send a post request to the signup view
        response = self.client.post(reverse('signup'), new_user_data)

        # Check that the response redirects to the expected URL
        self.assertRedirects(response, reverse('note_noteboard'))

        # Check if the user exists in the database
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)

        # Fetch the newly registered user and check authentication
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated,
                        "User should be authenticated after signup"
                        )
        self.assertEqual(user.username, 'newuser')

        # Check if the user is logged in
        self.assertTrue(user.is_authenticated)

    def test_login(self):
        """Test the login functionality with both correct and incorrect
        credentials."""

        # Test login with correct credentials
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser',
             'password': 'testpassword'}
        )
        self.assertRedirects(response, '/')

        # Test login attempt with incorrect credentials
        response = self.client.post(
            reverse('login'),
            {'username': 'testuser',
             'password': 'wrong'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter a correct username and password."
                        in response.content.decode())

    def test_logout(self):
        """Test the logout process and redirection behavior to login
        page, and access restrictions post-logout."""

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Log out the user
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/accounts/login/')

        # Check if the redirection happened to the login page
        self.assertRedirects(response, '/accounts/login/')

        # Access a restricted view and test for redirection to login page
        response = self.client.get(reverse('note_noteboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue("/accounts/login/" in response.url)


class NoteModelTest(TestCase):
    """
    Tests that Django creates a Note object with the correct title
    and content.

    Methods
    -------
    setUp(self):
        Creates User and Note objects for the test.
    test_note_details(self):
        Tests if the Note object has the correct title and content.
    """

    def setUp(self):
        """Creates test object with example user, title, and content."""

        # Create a User object
        test_user = User.objects.create_user(
            username='tester', password='testpassword'
        )

        # Create a Note object
        Note.objects.create(user=test_user,
                            title="Test Title",
                            content="This is test content.")

    def test_note_details(self):
        """Performs a test on the title and content of the Note."""

        # Get details of the first object
        note = Note.objects.first()

        # Verify the object for expected user, title, and content
        self.assertEqual(note.user.username, "tester")
        self.assertEqual(note.title, "Test Title")
        self.assertEqual(note.content, "This is test content.")


class NoteViewTest(TestCase):
    """
    A suite of tests for validating the behaviour and functionality of
    the note views in Django.

    This class focuses primarily on testing the views responsible for
    creating, listing, reading, updating, and deleting notes in the app.

    Methods
    -------
    - setUp(self):
        Configures the test environment by creating initial objects.
    - test_note_create_view(self):
        Ensures the create view functions correctly from form display to
        note creation.
    - test_note_list_view(self):
        Validates that the list view accurately displays notes.
    - test_note_detail_view(self):
        Checks that the detail view shows correct information for a
        particular note.
    - test_note_update_view(self):
        Confirms that the update view successfully modifies an existing
        note.
    - test_note_delete_view(self):
        Tests the delete functionality of the delete view.
    """

    def setUp(self):
        """Creates objects with example user, title, and content."""

        # Create a User object
        test_user = User.objects.create_user(
            username='tester', password='testpassword'
        )

        # Log in the test user
        self.client.login(username='tester', password='testpassword')

        # Create an initial Note object for the tests
        Note.objects.create(user=test_user,
                            title="Test Title",
                            content="This is test content."
                            )

    def test_note_create_view(self):
        """Tests the 'note_create' view for proper form display,
        successful note creation, and database update."""

        # Verify the form is displayed on GET request
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create")

        # Test for successful object creation on POST request
        response = self.client.post(
            reverse("note_create"), {"title": "New Title",
                                     "content": "New content."}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302)

        # Verify new note was added to the database with correct details
        new_note = Note.objects.get(title="New Title")
        self.assertIsNotNone(new_note)
        self.assertEqual(new_note.content, "New content.")

    def test_note_list_view(self):
        """Tests the list view ('note_noteboard') to ensure it correctly
        lists notes."""

        # Test the list view (note_noteboard) is accessible
        response = self.client.get(reverse("note_noteboard"))
        self.assertEqual(response.status_code, 200)

        # Verify the response contains the corect details
        self.assertContains(response, "Test Title")
        self.assertContains(response, "This is test content.")

    def test_note_detail_view(self):
        """Tests the detail view ('note_read') to ensure it correctly
        lists note details."""

        # Test the detail view (note_read) is accessible
        note = Note.objects.first()
        response = self.client.get(reverse("note_read", args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)

        # Verify the response contains the correct details
        self.assertContains(response, "Test Title")
        self.assertContains(response, "This is test content.")
        self.assertEqual(note.user.username, "tester")

    def test_note_update_view(self):
        """Tests the 'note_update' view to ensure it correctly handles
        both GET and POST requests."""

        # Verify the form is displayed on GET request
        note = Note.objects.first()
        response = self.client.get(reverse("note_update", args=[str(note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update")

        # Test for successful object update on POST request
        response = self.client.post(
            reverse("note_update", args=[str(note.id)]),
            {"title": "Updated Title", "content": "Updated content."},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302)

        # Verify the note was updated with the correct details
        note.refresh_from_db()
        self.assertEqual(note.title, "Updated Title")
        self.assertEqual(note.content, "Updated content.")
        self.assertEqual(note.user.username, "tester")

    def test_note_delete_view(self):
        """Verifies that the `note_delete` view correctly deletes a Note
        object and redirects."""

        # Check the POST request performs the deletion
        note = Note.objects.first()
        response = self.client.post(reverse("note_delete",
                                            args=[str(note.id)]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/', status_code=302)

        # Check the database for note absence
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note.id)
