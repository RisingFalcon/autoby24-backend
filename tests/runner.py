from django.test.runner import DiscoverRunner
import coverage

class CoverageRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        self.cov = coverage.coverage(source=['autoby24-api', 'apps'], branch=True)
        self.cov.start()
        super().__init__(*args, **kwargs)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        results = super().run_tests(test_labels, extra_tests, **kwargs)
        self.cov.stop()
        self.cov.save()
        self.cov.report()
        self.cov.html_report(directory='htmlcov')
        return results
