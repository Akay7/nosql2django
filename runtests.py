import os
import sys
import django
from django.conf import settings

test_dir = os.path.join(os.path.dirname(__file__), 'django_parser')
sys.path.insert(0, test_dir)

DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        'tests',
    ),
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3"
        }
    },
    TIME_ZONE = 'UTC',
    USE_TZ = True,
)


def runtests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from django.test.runner import DiscoverRunner
    runner_class = DiscoverRunner
    test_args = ['tests']

    failures = runner_class(
        verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()



