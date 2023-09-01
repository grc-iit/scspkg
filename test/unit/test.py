from unittest import TestCase
from scspkg.pkg_manager import PackageManager
from scspkg.pkg import Package
import os


class TestScspkg(TestCase):
    """
    Test jarvis CLI
    """
    def test_create_pkg(self):
        self.pkg_manager = PackageManager()
        pkg = Package('test').save()
        self.assertTrue(os.path.exists(pkg.module_schema_path))
        self.assertTrue(os.path.exists(pkg.module_path))
        self.assertTrue(os.path.exists(pkg.pkg_root))
        self.assertTrue(os.path.exists(pkg.pkg_src))

        pkg.destroy()
        self.assertFalse(os.path.exists(pkg.module_schema_path))
        self.assertFalse(os.path.exists(pkg.module_path))
        self.assertFalse(os.path.exists(pkg.pkg_root))
        self.assertFalse(os.path.exists(pkg.pkg_src))
