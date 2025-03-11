#!/usr/bin/env python
import os
import sys
import unittest

if __name__ == '__main__':
    # Set the default settings module for Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portfolio_website.settings')

    # Initialize Django
    import django

    django.setup()

    # Discover all test modules in the "tests" directory with a filename pattern "test_*.py"
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = unittest.defaultTestLoader.discover(start_dir=tests_dir, pattern='test_*.py')

    # Run the tests with increased verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with a non-zero status if any tests failed
    sys.exit(0 if result.wasSuccessful() else 1)
