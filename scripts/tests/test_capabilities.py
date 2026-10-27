"""capabilities.py tier detection (dstack): image generation that lives in the runtime
(a built-in tool such as GenerateImage) or in a skill folder outside the default list must count as T1."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import capabilities as cap  # noqa: E402


class Tier(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.saved = {k: os.environ.pop(k, None) for k in ('HOME', 'DSTACK_IMAGE_TOOL', 'DSTACK_SKILL_DIRS')}
        os.environ['HOME'] = self.tmp.name
        self.cwd = os.getcwd()
        os.chdir(self.tmp.name)

    def tearDown(self):
        os.chdir(self.cwd)
        for k, v in self.saved.items():
            os.environ.pop(k, None)
            if v is not None:
                os.environ[k] = v
        self.tmp.cleanup()

    def tier(self, **kw):
        return cap.detect(check_playwright=False, **kw)

    def test_nothing_is_t0(self):
        r = self.tier(skill_dirs_extra=[])
        self.assertEqual(r['tier'], 'T0')

    def test_runtime_image_tool_env_counts_as_t1(self):
        os.environ['DSTACK_IMAGE_TOOL'] = 'GenerateImage'
        r = self.tier(skill_dirs_extra=[])
        self.assertEqual(r['tier'], 'T0+T1')
        self.assertEqual(r['image_tools'], ['GenerateImage'])

    def test_image_tool_argument_counts_as_t1(self):
        r = self.tier(skill_dirs_extra=[], image_tools=['image_gen'])
        self.assertIn('T1', r['tier'])

    def test_image_skill_in_extra_dir_is_found(self):
        d = Path(self.tmp.name) / 'skills' / 'gpt-image-2'
        d.mkdir(parents=True)
        (d / 'SKILL.md').write_text('---\nname: gpt-image-2\ndescription: Generate images\n---\n', encoding='utf-8')
        os.environ['DSTACK_SKILL_DIRS'] = str(d.parent)
        r = self.tier(skill_dirs_extra=[])
        self.assertIn('T1', r['tier'])
        self.assertIn('gpt-image-2', r['image_skills'])

    def test_unrelated_skill_does_not_count(self):
        d = Path(self.tmp.name) / 'skills' / 'canvas-design'
        d.mkdir(parents=True)
        (d / 'SKILL.md').write_text('---\nname: canvas-design\ndescription: posters with code\n---\n', encoding='utf-8')
        os.environ['DSTACK_SKILL_DIRS'] = str(d.parent)
        self.assertEqual(self.tier(skill_dirs_extra=[])['tier'], 'T0')


if __name__ == '__main__':
    unittest.main()
