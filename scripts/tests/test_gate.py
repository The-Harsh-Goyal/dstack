"""gate.py: non-blocking gate default when no human is present."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gate  # noqa: E402


class Gate(unittest.TestCase):
    def test_default_writes_and_logs_then_respects_a_real_choice(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            self.assertEqual(gate.status(p), 'missing')
            self.assertEqual(gate.main(['default', d, '--pick', 'dir-1', '--reason', 'unattended run']), 0)
            self.assertEqual(gate.status(p), 'auto-default')
            self.assertIn('dir-1', (p / 'gate-log.md').read_text())
            self.assertIn('PENDING', (p / 'direction-approved.md').read_text())
            (p / 'direction-approved.md').write_text('User said: "go with dir-2"', encoding='utf-8')
            self.assertEqual(gate.main(['default', d, '--pick', 'dir-1', '--reason', 'x']), 1)   # never overwrite a real choice
            self.assertIn('dir-2', (p / 'direction-approved.md').read_text())


if __name__ == '__main__':
    unittest.main()
