"""
_cli_tests_

Test "fizzbuzz" from the command line. Assumes package installation.
"""
import subprocess
import unittest


class TestCLI(unittest.TestCase):

    def test_fizzbuzz(self):
        """
        Test the output of the fizzbuzz command.
        We don't care about spaces or capitalization,
        just that the correct number and fizz/buzz
        are given for each line. Only allow up to 2 minutes
        for execution.
        """
        proc = subprocess.Popen(
            ['fizzbuzz', '15'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        try:
            outs, errs = proc.communicate(timeout=120)
        except subprocess.TimeoutExpired:
            proc.kill()
            self.fail(msg='Fizzbuzz took too long to execute.')

        solution = outs.decode('utf-8').splitlines()
        for idx, line in enumerate(solution):
            idx += 1
            msg = 'Incorrect or missing number on line {0}'.format(idx)
            self.assertIn(str(idx), line, msg=msg)
            if idx % 3 == 0:
                msg = 'fizz expected on line {0}'.format(idx)
                self.assertIn('fizz', line.lower(), msg=msg)
            else:
                msg = 'unexpected fizz on line {0}'.format(idx)
                self.assertNotIn('fizz', line.lower(), msg=msg)
            if idx % 5 == 0:
                msg = 'buzz expected on line {0}'.format(idx)
                self.assertIn('buzz', line.lower(), msg=msg)
            else:
                msg = 'unexpected buzz on line {0}'.format(idx)
                self.assertNotIn('buzz', line.lower(), msg=msg)
