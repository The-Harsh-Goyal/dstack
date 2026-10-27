"""cover.py: exact-size renders for X covers and local upscaling from a 1024x576 generation."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cover  # noqa: E402

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;width:100%;height:100%}
body{background:linear-gradient(90deg,#0b1d3a,#c8a24a);display:flex;align-items:center;justify-content:center}
h1{font:700 96px Georgia,serif;color:#fff}</style></head><body><h1>Twenty years</h1></body></html>"""


class Cover(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_render_x_presets_at_exact_size(self):
        from PIL import Image
        (self.d / 'c.html').write_text(HTML, encoding='utf-8')
        for preset, size in (('x-article', (2500, 1000)), ('x-infeed', (1600, 900))):
            out = self.d / f'{preset}.png'
            self.assertEqual(cover.main(['render', str(self.d / 'c.html'), '--preset', preset, '-o', str(out)]), 0)
            self.assertEqual(Image.open(out).size, size)
            self.assertEqual(cover.main(['check', str(out), '--preset', preset]), 0)

    @unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg missing')
    def test_upscale_1024x576_to_both_x_sizes(self):
        from PIL import Image
        src = self.d / 'gen.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=s=1024x576', '-frames:v', '1', str(src)], check=True)
        for preset, size in (('x-article', (2500, 1000)), ('x-infeed', (1600, 900))):
            out = self.d / f'up-{preset}.png'
            self.assertEqual(cover.main(['upscale', str(src), '--preset', preset, '-o', str(out), '--sharpen']), 0)
            self.assertEqual(Image.open(out).size, size)
            self.assertFalse({k for k in Image.open(out).info if k not in ('dpi', 'gamma', 'srgb')})

    def test_check_flags_wrong_size(self):
        from PIL import Image
        p = self.d / 'small.png'
        Image.new('RGB', (1024, 576), (200, 30, 30)).save(p)
        self.assertEqual(cover.main(['check', str(p), '--preset', 'x-article']), 1)


if __name__ == '__main__':
    unittest.main()
