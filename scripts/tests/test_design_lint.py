"""Tests for design_lint.py and learn.py: the checking tools must catch deliberately broken input, and must not wrongly flag clean input.

Run: python3 -m unittest scripts/tests/test_design_lint.py -v
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import design_lint as dl  # noqa: E402
import learn  # noqa: E402
import ref_board  # noqa: E402

FX = HERE / 'fixtures'


class LintFacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        names = ['lint_slop.html', 'lint_reskin.html', 'lint_clean.html', 'lint_broken.html']
        cls.f = dict(zip(names, dl.collect([str(FX / n) for n in names])))

    def test_slop_hits_the_2026_clusters(self):
        red, yellow = dl.judge(self.f['lint_slop.html'])
        text = '\n'.join(yellow)
        fams = '\n'.join(dl.families(self.f['lint_slop.html']))
        self.assertIn('Warm-paper serif', fams)       # warm cream + terracotta + serif: descriptive only
        self.assertIn('Card kit', fams)       # cards with the same radius and same shadow: descriptive only
        self.assertNotIn('Warm-paper serif', text)    # the family no longer triggers a yellow light
        self.assertIn('Template chrome', text)       # all-caps small labels, middle dots, arrows
        self.assertIn('Single word recolored', text)
        self.assertIn('01/02/03', text)

    def test_clean_page_is_not_accused(self):
        red, yellow = dl.judge(self.f['lint_clean.html'])
        self.assertEqual(red, [])
        self.assertEqual(yellow, [])

    def test_broken_page_goes_red(self):
        red, _ = dl.judge(self.f['lint_broken.html'])
        text = '\n'.join(red)
        self.assertIn('Broken images', text)
        self.assertIn('Body text below', text)
        self.assertIn('Low contrast', text)

    def test_reskin_is_caught_by_layout_not_colour(self):
        a = dl.fingerprint(self.f['lint_slop.html'])
        b = dl.fingerprint(self.f['lint_reskin.html'])
        c = dl.fingerprint(self.f['lint_clean.html'])
        hits, pd, lc = dl.similar(a, b)
        self.assertGreater(pd, 0.06)          # the colors really did change
        self.assertTrue(any('skeleton' in h for h in hits), hits)   # but the skeleton didn't
        self.assertFalse(dl.similar(a, c)[0])  # two genuinely different versions aren't flagged

    def test_warm_cream_is_classified_warm(self):
        self.assertEqual(dl.bg_class((0xF4, 0xF1, 0xEA)), 'light · warm paper')
        self.assertEqual(dl.bg_class((0xFA, 0xF8, 0xF4)), 'light · warm paper')
        self.assertEqual(dl.bg_class((0xFA, 0xFA, 0xFA)), 'light · neutral white')
        self.assertNotEqual(dl.bg_class((0xDF, 0xEB, 0xE5)), 'light · warm paper')   # cool celadon gray is not warm cream


class LintEnglish(unittest.TestCase):
    """dstack: the body-text cutoff is language-aware (28 CJK chars, or about 10 English words)."""

    def test_short_english_labels_are_not_body_text(self):
        f = dl.collect([str(FX / 'lint_english_labels.html')])[0]
        self.assertEqual(f['bodySmall'], [])           # 34-41 char, 6-7 word labels at 13px
        red, _ = dl.judge(f)
        self.assertEqual(red, [])

    def test_real_english_paragraph_still_flagged(self):
        f = dl.collect([str(FX / 'lint_english_small_body.html')])[0]
        red, _ = dl.judge(f)
        self.assertIn('Body text below the body minimum', '\n'.join(red))


class LintEdgeCases(unittest.TestCase):
    """False positives and false negatives reported by an independent review, each pinned down as a regression test."""

    def test_no_false_red_on_svg_sibling_plate_and_caption(self):
        f = dl.collect([str(FX / 'lint_tricky_ok.html')])[0]
        red, _ = dl.judge(f)
        self.assertEqual(red, [])   # enlarged SVG text, white text on a sibling layer's dark background, and 13px captions should not be flagged red

    def test_deck_div_body_and_ghost_text_go_red(self):
        f = dl.collect([str(FX / 'lint_tricky_bad.html')], viewport=(1920, 1080), min_body=24, min_label=16)[0]
        red, yellow = dl.judge(f)
        text = '\n'.join(red)
        self.assertIn('Body text below the body minimum', text)   # 16px body text written in a div
        self.assertIn('Low contrast', text)          # white text at 8% opacity
        self.assertTrue(any('Relative-path images' in y for y in yellow))

    def test_unreachable_stylesheet_does_not_kill_the_batch(self):
        res = dl.collect([str(FX / 'lint_offline.html'), str(FX / 'lint_clean.html')])
        self.assertEqual(len(res), 2)
        self.assertNotIn('fatal', res[1])
        self.assertEqual(dl.judge(res[1])[0], [])

    def test_glob_is_expanded_by_the_script(self):
        self.assertIn(str(FX / 'lint_clean.html'), dl.expand([str(FX / 'lint_c*.html')]))

    def test_brand_mode_only_compares_skeleton(self):
        f = dl.collect([str(FX / 'lint_slop.html')])[0]
        a = dl.fingerprint(f)
        self.assertTrue(dl.similar(a, a)[0])
        b = dict(a, layout=[-x for x in a['layout']])   # same colors and fonts, completely different skeleton
        self.assertFalse(dl.similar(a, b, brand=True)[0])


class Ledger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._saved = {k: os.environ.pop(k, None) for k in ('DSTACK_HOME', 'HUASHU_DESIGN_HOME')}
        os.environ['DSTACK_HOME'] = self.tmp.name

    def tearDown(self):
        os.environ.pop('DSTACK_HOME', None)
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v
        self.tmp.cleanup()

    def test_harvest_counts_entry_logged_from_a_subfolder(self):
        # regression: ledger add on proj/out/final.html stored proj/out, so harvest proj found 0 entries
        import shutil
        proj = Path(self.tmp.name) / 'proj'
        (proj / 'out').mkdir(parents=True)
        (proj / 'direction-approved.md').write_text('chose B', encoding='utf-8')
        shutil.copy(FX / 'lint_clean.html', proj / 'out' / 'final.html')
        self.assertEqual(dl.main(['ledger', 'add', str(proj / 'out' / 'final.html'), '--project', 'Demo']), 0)
        self.assertEqual(dl.ledger_read()[0]['project_dir'], str(proj.resolve()))   # project root, not the file's folder
        self.assertIn('Look ledger: 1 entries for this project', learn.harvest(proj))

    def test_harvest_also_matches_older_rows_inside_the_project(self):
        import json
        proj = Path(self.tmp.name) / 'p2'
        (proj / 'exports').mkdir(parents=True)
        row = {'project': 'x', 'project_dir': str((proj / 'exports').resolve()), 'file': str(proj / 'exports' / 'a.html')}
        dl.ledger_file().parent.mkdir(parents=True, exist_ok=True)
        dl.ledger_file().write_text(json.dumps(row) + '\n', encoding='utf-8')
        self.assertIn('Look ledger: 1 entries for this project', learn.harvest(proj))

    def test_add_then_check_flags_the_same_look(self):
        self.assertEqual(dl.main(['ledger', 'add', str(FX / 'lint_slop.html'), '--project', '测试项目']), 0)
        rows = dl.ledger_read()
        self.assertEqual(len(rows), 1)
        self.assertIn('warm paper', rows[0]['desc'])
        # the same look a second time: must be flagged as a collision
        self.assertEqual(dl.main(['ledger', 'check', str(FX / 'lint_slop.html')]), 1)
        # a completely different look: not flagged
        self.assertEqual(dl.main(['ledger', 'check', str(FX / 'lint_clean.html')]), 0)


class Learn(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._saved = {k: os.environ.pop(k, None) for k in ('DSTACK_HOME', 'HUASHU_DESIGN_HOME')}
        os.environ['DSTACK_HOME'] = self.tmp.name

    def tearDown(self):
        os.environ.pop('DSTACK_HOME', None)
        for k, v in self._saved.items():
            if v is not None:
                os.environ[k] = v
        self.tmp.cleanup()

    def test_refuses_entries_nobody_can_check(self):
        with self.assertRaises(learn.LearnError):
            learn.add_entry('guess', 'deck', '随便', '证据')
        with self.assertRaises(learn.LearnError):
            learn.add_entry('observed', '', '没有主题', '证据')
        with self.assertRaises(learn.LearnError):
            learn.add_entry('observed', 'deck', '没有证据', '')
        with self.assertRaises(learn.LearnError):
            learn.add_entry('preference', 'color', '他喜欢暖色', '对话')  # a preference must be the user's own words

    def test_roundtrip(self):
        learn.add_entry('preference', 'color,cover', '「封面用暖纸底」——只用于他自己的封面', '2026-10-17 对话')
        learn.add_entry('observed', 'deck', '三版都用了同一个骨架被他一眼看出', 'B2 基准')
        out = learn.recall(['deck'])
        self.assertIn('封面用暖纸底', out)      # preferences are always brought along
        self.assertIn('同一个骨架', out)
        self.assertIn('L2', learn.local_file().read_text(encoding='utf-8'))
        self.assertNotIn('同一个骨架', learn.recall(['motion']).split('## Lessons from past projects')[1])

    def test_hand_edited_heading_without_trailing_dot_keeps_its_kind(self):
        learn.local_file().parent.mkdir(parents=True, exist_ok=True)
        learn.local_file().write_text('# x\n\n## 手记 · preference\n\n- 原话：「要大胆」\n', encoding='utf-8')
        self.assertEqual(learn.entries(learn.local_file(), 'local')[0]['kind'], 'preference')

    def test_topic_named_like_a_subcommand_can_be_recalled(self):
        self.assertIn('Lessons from past projects', learn.recall(['status']))
        self.assertEqual(learn.main(['--', 'status']), 0)


class RefBoard(unittest.TestCase):
    def test_blank_screenshot_counts_as_not_seen(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as d:
            blank, real = Path(d) / 'blank.jpg', Path(d) / 'real.jpg'
            Image.new('RGB', (1440, 900), (32, 26, 28)).save(blank)   # what a WebGL site looks like in a headless browser
            im = Image.new('RGB', (1440, 900), 'white')
            ImageDraw.Draw(im).rectangle([100, 100, 900, 600], fill=(20, 60, 200))
            im.save(real)
            self.assertTrue(ref_board.mostly_blank(blank))
            self.assertFalse(ref_board.mostly_blank(real))
            # minimal designs must not be misjudged as not having been seen
            sparse = HERE.parent.parent / 'assets' / 'style-specimens' / 'info' / '17-ma-emptiness.jpg'
            self.assertFalse(ref_board.mostly_blank(sparse))

    def test_local_image_goes_on_the_board(self):
        from PIL import Image, ImageDraw
        with tempfile.TemporaryDirectory() as d:
            src = Path(d) / 'src.png'
            im = Image.new('RGB', (800, 500), (240, 236, 228))
            ImageDraw.Draw(im).rectangle([60, 60, 420, 440], fill=(200, 40, 40))
            im.save(src)
            out = Path(d) / 'refs' / 'board.jpg'
            self.assertEqual(ref_board.main([str(src), '--out', str(out)]), 0)
            self.assertTrue(out.exists() and (out.parent / 'board-1.jpg').exists())


if __name__ == '__main__':
    unittest.main()
