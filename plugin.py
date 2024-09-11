import time
import pytest
import sys
from io import StringIO

old_stdout = sys.stdout
new_stdout = StringIO()

class ResultsCollector:
    def __init__(self):
        self.reports = []
        self.collected = 0
        self.exitcode = 0
        self.passed = 0
        self.failed = 0
        self.xfailed = 0
        self.skipped = 0
        self.total_duration = 0

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        if report.when == 'call':
            self.reports.append(report)

    def pytest_collection_modifyitems(self, items):
        self.collected = len(items)

    def pytest_terminal_summary(self, terminalreporter, exitstatus):
        # print(exitstatus, dir(exitstatus))
        self.exitcode = exitstatus.value
        self.passed = len(terminalreporter.stats.get('passed', []))
        self.failed = len(terminalreporter.stats.get('failed', []))
        self.xfailed = len(terminalreporter.stats.get('xfailed', []))
        self.skipped = len(terminalreporter.stats.get('skipped', []))

        self.total_duration = time.time() - terminalreporter._sessionstarttime

def run(test_file='tests/test1.py'):
    collector = ResultsCollector()
    sys.stdout = new_stdout
    pytest.main(['-q', test_file], plugins=[collector])
    sys.stdout = old_stdout

    # for report in collector.reports:
    #     print('id:', report.nodeid, 'outcome:', report.outcome)  # etc
    # print('exit code:', collector.exitcode)
    # print('passed:', collector.passed, 'failed:', collector.failed, 'xfailed:', collector.xfailed, 'skipped:', collector.skipped)
    # print('total duration:', collector.total_duration)

    return collector


if __name__ == '__main__':
    results = run()

