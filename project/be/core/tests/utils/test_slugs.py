from django.contrib.auth.models import User
from django.test import TestCase

from board.models import Board
from core.utils.slugs import generate_unique_slug


class GenerateUniqueSlugTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')

    # --- base slug ---

    def test_returns_slugified_title(self):
        slug = generate_unique_slug(Board, 'My Board', self.user)
        self.assertEqual(slug, 'my-board')

    def test_lowercases_title(self):
        slug = generate_unique_slug(Board, 'UPPER CASE', self.user)
        self.assertEqual(slug, 'upper-case')

    def test_special_chars_are_slugified(self):
        slug = generate_unique_slug(Board, 'Hello World!', self.user)
        self.assertEqual(slug, 'hello-world')

    # --- collision handling ---

    def test_appends_suffix_on_collision(self):
        Board.objects.create(title='My Board', user=self.user)  # slug='my-board'
        slug = generate_unique_slug(Board, 'My Board', self.user)
        self.assertEqual(slug, 'my-board-2')

    def test_increments_suffix_on_multiple_collisions(self):
        Board.objects.create(title='My Board', user=self.user)  # slug='my-board'
        board2 = Board.objects.create(title='Other', user=self.user)
        Board.objects.filter(pk=board2.pk).update(slug='my-board-2')  # force collision
        slug = generate_unique_slug(Board, 'My Board', self.user)
        self.assertEqual(slug, 'my-board-3')

    # --- exclude_pk ---

    def test_exclude_pk_ignores_own_slug(self):
        board = Board.objects.create(title='My Board', user=self.user)  # slug='my-board'
        slug = generate_unique_slug(Board, 'My Board', self.user, exclude_pk=board.pk)
        self.assertEqual(slug, 'my-board')

    # --- user scoping ---

    def test_scoped_to_user(self):
        other_user = User.objects.create_user(username='user2', password='pass123')
        Board.objects.create(title='My Board', user=other_user)  # slug='my-board' for other_user
        slug = generate_unique_slug(Board, 'My Board', self.user)
        self.assertEqual(slug, 'my-board')

    # --- max_length ---

    def test_max_length_truncates_base(self):
        long_title = 'a' * 200
        slug = generate_unique_slug(Board, long_title, self.user, max_length=10)
        self.assertEqual(slug, 'a' * 10)
