from django.db import connection, models
from django.test import TransactionTestCase

from core.models import BaseModel


class ConcreteModel(BaseModel):
    class Meta:
        app_label = 'core'


class BaseModelTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(ConcreteModel)

    @classmethod
    def tearDownClass(cls):
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(ConcreteModel)
        super().tearDownClass()

    def setUp(self):
        ConcreteModel.objects.all().delete()
        self.instance = ConcreteModel.objects.create()

    # --- meta ---

    def test_is_abstract(self):
        self.assertTrue(BaseModel._meta.abstract)

    # --- field types ---

    def test_is_archived_field_type(self):
        field = BaseModel._meta.get_field('is_archived')
        self.assertIsInstance(field, models.BooleanField)

    def test_created_at_field_type(self):
        field = BaseModel._meta.get_field('created_at')
        self.assertIsInstance(field, models.DateTimeField)

    def test_updated_at_field_type(self):
        field = BaseModel._meta.get_field('updated_at')
        self.assertIsInstance(field, models.DateTimeField)

    # --- field options ---

    def test_is_archived_defaults_to_false(self):
        self.assertFalse(self.instance.is_archived)

    def test_created_at_has_auto_now_add(self):
        field = BaseModel._meta.get_field('created_at')
        self.assertTrue(field.auto_now_add)

    def test_updated_at_has_auto_now(self):
        field = BaseModel._meta.get_field('updated_at')
        self.assertTrue(field.auto_now)

    # --- behaviour ---

    def test_created_at_is_set_on_creation(self):
        self.assertIsNotNone(self.instance.created_at)

    def test_updated_at_is_set_on_creation(self):
        self.assertIsNotNone(self.instance.updated_at)

    def test_created_at_does_not_change_on_save(self):
        original = self.instance.created_at
        self.instance.is_archived = True
        self.instance.save()
        self.instance.refresh_from_db()
        self.assertEqual(self.instance.created_at, original)

    def test_updated_at_changes_on_save(self):
        original = self.instance.updated_at
        self.instance.is_archived = True
        self.instance.save()
        self.instance.refresh_from_db()
        self.assertGreaterEqual(self.instance.updated_at, original)

    def test_can_archive_instance(self):
        self.instance.is_archived = True
        self.instance.save()
        self.instance.refresh_from_db()
        self.assertTrue(self.instance.is_archived)
