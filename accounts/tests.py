from django.conf import settings
from django.test import SimpleTestCase


class StorageSettingsTests(SimpleTestCase):
    def test_default_storage_config_exists(self):
        self.assertIn('default', settings.STORAGES)
        self.assertEqual(
            settings.STORAGES['default']['BACKEND'],
            'django.core.files.storage.FileSystemStorage',
        )
