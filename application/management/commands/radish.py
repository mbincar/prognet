import sys
from django.core.management.base import BaseCommand
from application.test.runner import RadishTestRunner


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('features', nargs='+', type=str)

    def handle(self, *args, **options):
        test_runner = RadishTestRunner(interactive=False)
        if options['features']:
            test_runner.set_radish_features(options['features'])
        result = test_runner.run_suite(None)
        if result:
            sys.exit(result)
