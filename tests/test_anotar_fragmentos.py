from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from scripts.anotar import EventWorkspace, Workspace, validate_annotation


class SelectedIntervalsTests(unittest.TestCase):
    def test_distinct_cases_preserve_unreviewed_coverage(self):
        for case, count in [('pausa', 3), ('lenta', 4), ('relectura', 3)]:
            workspace = EventWorkspace(case)
            data = validate_annotation(deepcopy(workspace.template), workspace.template)
            self.assertEqual(len(data['words']), count)
            self.assertEqual(data['reviewed_intervals'], 0)
            self.assertIsNone(workspace.draft)
            self.assertTrue(all(w['start'] is None and w['end'] is None for w in data['words']))
            self.assertNotEqual(workspace.path, Workspace().path)

    def test_repeated_story_indices_with_separate_chronological_attempts(self):
        template = EventWorkspace('relectura').template
        payload = deepcopy(template)
        for w, a, b in zip(payload['words'], [15, 19, 23], [18, 22, 24]):
            w.update(start=a, end=b, reviewed=True, timing_origin='manual')
        payload['words'][1]['story_range'] = [1, 56]
        payload['words'][1]['attempt'] = 99
        result = validate_annotation(payload, template)
        self.assertEqual(result['words'][0]['story_range'], [37, 42])
        self.assertEqual(result['words'][1]['story_range'], [37, 42])
        self.assertEqual(result['words'][1]['attempt'], 2)
        self.assertEqual(result['timing_status'], 'revision_intervalos_seleccionados_completa')
        self.assertEqual(result['reviewed_intervals'], 3)
        self.assertNotIn('reviewed_words', result)
        payload['words'][1]['start'] = 17
        with self.assertRaises(ValueError):
            validate_annotation(payload, template)

    def test_save_reload_and_backup_do_not_touch_full_annotation(self):
        workspace = EventWorkspace('pausa')
        with tempfile.TemporaryDirectory() as folder:
            workspace.path = Path(folder) / 'lectura_pausa_fragmentos.json'
            full_path = Path(folder) / 'lectura_normal.json'
            full_path.write_text('sin cambios', encoding='utf-8')
            workspace.save(workspace.template)
            payload = deepcopy(workspace.template)
            payload['words'][0].update(start=9, end=10, reviewed=True, timing_origin='manual')
            workspace.save(payload)
            self.assertEqual(workspace.current()['reviewed_intervals'], 1)
            self.assertEqual(full_path.read_text(encoding='utf-8'), 'sin cambios')
            self.assertEqual(len(list((Path(folder) / 'copias').glob('lectura_pausa_fragmentos_*.json'))), 1)


if __name__ == '__main__':
    unittest.main()
