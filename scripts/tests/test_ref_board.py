"""ref_board.py: dismiss common cookie/consent and promo pop-ups; detect bot challenges and fail
clearly instead of trying to get past them."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import ref_board  # noqa: E402

FX = HERE / 'fixtures'


class Popups(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.pw = sync_playwright().start()
        cls.browser = cls.pw.chromium.launch()
        # block all network so the challenge fixture's external script is never fetched
        cls.ctx = cls.browser.new_context()
        cls.ctx.route('http*://**', lambda r: r.abort())
        cls.page = cls.ctx.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def test_cookie_banner_and_promo_are_dismissed(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'shot.jpg'
            ref_board.shoot(self.page, str(FX / 'ref_cookie_banner.html'), out, False)
            self.assertEqual(self.page.evaluate("document.querySelectorAll('#consent,#promo').length"), 0)
            from PIL import Image
            im = Image.open(out).convert('RGB')
            self.assertGreater(im.getpixel((60, 80))[0], 150)   # red headline visible, not the navy banner

    def test_cloudflare_challenge_fails_clearly(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ref_board.BotChallenge) as cm:
                ref_board.shoot(self.page, str(FX / 'ref_cf_challenge.html'), Path(d) / 'x.jpg', False)
            self.assertIn('screenshot', str(cm.exception))   # tells the agent to ask the user for one


if __name__ == '__main__':
    unittest.main()
