from django.test.runner import DiscoverRunner
import radish.main


class RadishTestRunner(DiscoverRunner):
    radish_features = []

    def run_suite(self, suite, **kwargs):
        return radish.main.main(self.radish_features)

    def suite_result(self, suite, result, **kwargs):
        return result

    def set_radish_features(self, features):
        self.radish_features = features
