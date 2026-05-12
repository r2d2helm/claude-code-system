"""Battery de tests pour les 7 evolutions B0.
Usage: python test_b0_evolutions.py [N_RUNS]
"""
import sys, os, io, json, re, importlib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.join(os.path.expanduser('~'), '.claude', 'hooks'))

HOME = os.path.expanduser('~')
CLAUDE = os.path.join(HOME, '.claude')
VAULT = os.path.join(HOME, 'Documents', 'Knowledge')


class TestRunner:
    def __init__(self):
        self.ok = 0
        self.fail = 0
        self.errors = []

    def check(self, name, condition, detail=""):
        if condition:
            self.ok += 1
        else:
            self.fail += 1
            self.errors.append(f"{name}: {detail}")

    def run_all(self, run_id=1):
        self.ok = 0
        self.fail = 0
        self.errors = []
        self._test_imports()
        self._test_config()
        self._test_new_hooks()
        self._test_dry_runs()
        self._test_settings()
        self._test_regression()
        self._test_files()
        self._test_vault()
        self._test_retrieval()
        self._test_edge_cases()
        return {"run": run_id, "ok": self.ok, "fail": self.fail, "errors": self.errors[:]}

    def _test_imports(self):
        mods = {
            'lib.paths': ['LOGS_DIR', 'CONFIG_DIR', 'SKILLS_DIR', 'VAULT_PATH', 'PERSONALITY_DIR', 'MEMORY_DIR'],
            'lib.memory_db': ['insert_memory', 'get_recent_memories', 'search_memories', 'upsert_fact'],
            'lib.memory_retriever': ['retrieve_for_startup', 'retrieve_for_prompt'],
            'lib.utils': ['read_stdin_json', 'log_audit', 'append_jsonl', 'now_paris'],
        }
        for mod, items in mods.items():
            try:
                m = importlib.import_module(mod)
                for item in items:
                    self.check(f'import:{mod}.{item}', hasattr(m, item), f'{item} not found')
            except Exception as e:
                self.check(f'import:{mod}', False, str(e))

    def _test_config(self):
        try:
            import yaml
            path = os.path.join(CLAUDE, 'hooks', 'config', 'memory_v2.yaml')
            with open(path, encoding='utf-8') as f:
                c = yaml.safe_load(f)
            checks = [
                ('retrieval.startup.max_chars', c['retrieval']['startup']['max_chars'], 1500),
                ('retrieval.startup.max_facts', c['retrieval']['startup']['max_facts'], 8),
                ('retrieval.startup.max_memories', c['retrieval']['startup']['max_memories'], 8),
                ('retrieval.startup.memories_days_back', c['retrieval']['startup']['memories_days_back'], 14),
                ('retrieval.startup.memories_min_importance', c['retrieval']['startup']['memories_min_importance'], 5.5),
                ('retrieval.per_prompt.max_chars', c['retrieval']['per_prompt']['max_chars'], 800),
                ('retrieval.per_prompt.max_results', c['retrieval']['per_prompt']['max_results'], 5),
                ('retrieval.deep.max_chars', c['retrieval']['deep']['max_chars'], 5000),
                ('retrieval.deep.max_facts', c['retrieval']['deep']['max_facts'], 15),
                ('convergence.enabled', c['convergence']['enabled'], True),
                ('degradation.enabled', c['degradation']['enabled'], True),
                ('degradation.repeat_error_threshold', c['degradation']['repeat_error_threshold'], 3),
                ('feedback_loop.enabled', c['feedback_loop']['enabled'], True),
                ('feedback_loop.auto_generate', c['feedback_loop']['auto_generate'], True),
            ]
            for name, actual, expected in checks:
                self.check(f'config:{name}', actual == expected, f'expected {expected}, got {actual}')
            for section in ['extraction', 'retrieval', 'consolidation', 'signals', 'stopwords',
                            'heartbeat', 'infrastructure', 'convergence', 'degradation', 'feedback_loop']:
                self.check(f'config:section:{section}', section in c, 'section missing')
        except Exception as e:
            self.check('config:load', False, str(e))

    def _test_new_hooks(self):
        for mod in ['convergence_tracker', 'degradation_detector', 'feedback_loop']:
            try:
                m = importlib.import_module(mod)
                self.check(f'hook:{mod}:import', True)
                self.check(f'hook:{mod}:has_main', hasattr(m, 'main'), 'no main()')
            except Exception as e:
                self.check(f'hook:{mod}:import', False, str(e))

    def _test_dry_runs(self):
        try:
            from convergence_tracker import _analyze_convergence
            for lines, label in [
                (['Parfait', 'Error', 'Exactement', 'Non corrige', 'Interessant'], '5mix'),
                ([], 'empty'),
                (['hello'], 'minimal'),
                (['Error'] * 10, 'all_errors'),
                (['Parfait'] * 10, 'all_success'),
            ]:
                m = _analyze_convergence(lines)
                self.check(f'convergence:dry:{label}', isinstance(m, dict) and 'score' in m)
                self.check(f'convergence:range:{label}', 0 <= m['score'] <= 10, f'score={m["score"]}')
        except Exception as e:
            self.check('convergence:dry', False, str(e))

        try:
            from feedback_loop import _extract_feedback, _format_feedback
            fb = _extract_feedback(['Parfait travail', 'Non recommence', 'Tres interessant'])
            self.check('feedback:extract', isinstance(fb, dict))
            fmt = _format_feedback(fb)
            self.check('feedback:format', isinstance(fmt, str))
            fb2 = _extract_feedback([])
            self.check('feedback:empty', all(len(v) == 0 for v in fb2.values()))
            fmt2 = _format_feedback(fb2)
            self.check('feedback:empty_format', fmt2 == '', f'got "{fmt2}"')
        except Exception as e:
            self.check('feedback:dry', False, str(e))

        try:
            from degradation_detector import _check_repeat_errors, _check_skill_atrophy, _check_convergence_drop
            a1 = _check_repeat_errors({'repeat_error_threshold': 3})
            self.check('degradation:repeat', isinstance(a1, list))
            a2 = _check_skill_atrophy({'skill_atrophy_days': 30})
            self.check('degradation:atrophy', isinstance(a2, list))
            self.check('degradation:no_false_pos', len(a2) == 0, f'{len(a2)} false positives')
            a3 = _check_convergence_drop()
            self.check('degradation:conv_drop', isinstance(a3, list))
        except Exception as e:
            self.check('degradation:dry', False, str(e))

    def _test_settings(self):
        try:
            with open(os.path.join(CLAUDE, 'settings.json'), encoding='utf-8') as f:
                settings = json.load(f)
            hooks = settings.get('hooks', {})
            for event in ['SessionStart', 'PreToolUse', 'Stop', 'SubagentStop',
                          'UserPromptSubmit', 'PostToolUse', 'Notification']:
                self.check(f'settings:{event}', event in hooks, 'event missing')
            stop_cmds = [h['command'].split('/')[-1] for h in hooks['Stop'][0]['hooks']]
            for exp in ['memory_extractor_v2.py', 'convergence_tracker.py',
                        'degradation_detector.py', 'feedback_loop.py']:
                self.check(f'settings:stop:{exp}', exp in stop_cmds)
            self.check('settings:no_dupes', len(stop_cmds) == len(set(stop_cmds)),
                        f'dupes in {stop_cmds}')
            for h in hooks['Stop'][0]['hooks']:
                py = h['command'].split('python ')[-1].strip()
                self.check(f'settings:exists:{py.split("/")[-1]}', os.path.exists(py), f'{py}')
        except Exception as e:
            self.check('settings', False, str(e))

    def _test_regression(self):
        for mod in ['security_validator', 'path_guard', 'error_capture', 'memory_extractor_v2',
                     'prompt_analyzer', 'subagent_capture', 'memory_consolidator']:
            try:
                importlib.import_module(mod)
                self.check(f'regression:{mod}', True)
            except Exception as e:
                self.check(f'regression:{mod}', False, str(e))

    def _test_files(self):
        files = {
            'flow.md': os.path.join(CLAUDE, 'commands', 'flow.md'),
            'skill-relations.yaml': os.path.join(CLAUDE, 'skills', 'references', 'skill-relations.yaml'),
            'Convergence-Dashboard.md': os.path.join(VAULT, '_Index', 'Convergence-Dashboard.md'),
            'Evolution-B0.md': os.path.join(VAULT, 'Projets', 'R2D2-Matrix-Evolution-B0.md'),
        }
        for name, path in files.items():
            exists = os.path.exists(path)
            self.check(f'file:{name}', exists, 'not found')
            if exists:
                with open(path, encoding='utf-8') as f:
                    content = f.read()
                self.check(f'file:{name}:size', len(content) > 50, f'{len(content)} chars')

        try:
            import yaml
            rp = os.path.join(CLAUDE, 'skills', 'references', 'skill-relations.yaml')
            with open(rp, encoding='utf-8') as f:
                rels = yaml.safe_load(f)
            skills = list(rels.get('relations', {}).keys())
            self.check('relations:count', len(skills) >= 15, f'{len(skills)}')
        except Exception as e:
            self.check('relations', False, str(e))

    def _test_vault(self):
        notes = ['C_R2D2-Matrix-Framework.md', 'C_R2D2-Matrix-B0-Emergence.md',
                 'C_R2D2-Matrix-E8-Fusion.md', 'C_R2D2-Matrix-Synthese.md']
        for note in notes:
            path = os.path.join(VAULT, 'Concepts', note)
            try:
                with open(path, encoding='utf-8') as f:
                    content = f.read()
                self.check(f'vault:{note}:exists', True)
                self.check(f'vault:{note}:frontmatter', content.startswith('---'))
                self.check(f'vault:{note}:evergreen', 'status: evergreen' in content)
                wl = len(re.findall(r'\[\[C_R2D2-Matrix', content))
                self.check(f'vault:{note}:crossrefs', wl >= 2, f'{wl} refs')
            except Exception as e:
                self.check(f'vault:{note}', False, str(e))

    def _test_retrieval(self):
        try:
            from lib.memory_retriever import retrieve_for_startup, retrieve_for_prompt
            r1 = retrieve_for_startup()
            self.check('retrieval:startup:str', isinstance(r1, str))
            self.check('retrieval:startup:limit', len(r1) <= 1500, f'{len(r1)}')
            r2 = retrieve_for_prompt('test convergence B0')
            self.check('retrieval:prompt:str', isinstance(r2, str))
            self.check('retrieval:prompt:limit', len(r2) <= 800, f'{len(r2)}')
            r3 = retrieve_for_prompt('')
            self.check('retrieval:empty:str', isinstance(r3, str))
            r4 = retrieve_for_prompt('x ' * 500)
            self.check('retrieval:long:str', isinstance(r4, str))
        except Exception as e:
            self.check('retrieval', False, str(e))

    def _test_edge_cases(self):
        try:
            from convergence_tracker import _analyze_convergence, _load_config
            m = _analyze_convergence(['Accent: e, a, u', 'Symboles: @#$%^&*'])
            self.check('edge:unicode', isinstance(m, dict))
            c = _load_config()
            self.check('edge:ct_config', 'enabled' in c)
        except Exception as e:
            self.check('edge:convergence', False, str(e))

        try:
            from feedback_loop import _extract_feedback, _load_config as fl_cfg
            fb = _extract_feedback(['Parfait! @#$', '', None] if False else ['Parfait! @#$', ''])
            self.check('edge:feedback_special', isinstance(fb, dict))
            c = fl_cfg()
            self.check('edge:fl_config', 'enabled' in c)
        except Exception as e:
            self.check('edge:feedback', False, str(e))

        try:
            from degradation_detector import _load_config as dd_cfg
            c = dd_cfg()
            self.check('edge:dd_config', 'enabled' in c)
        except Exception as e:
            self.check('edge:degradation', False, str(e))


def run_batch(n_runs):
    runner = TestRunner()
    results = []
    all_errors = set()
    for i in range(1, n_runs + 1):
        r = runner.run_all(run_id=i)
        results.append(r)
        for e in r['errors']:
            all_errors.add(e)
    total_ok = sum(r['ok'] for r in results)
    total_fail = sum(r['fail'] for r in results)
    return total_ok, total_fail, sorted(all_errors)


if __name__ == '__main__':
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    ok, fail, errors = run_batch(runs)
    total = ok + fail
    print(f'Batch {runs}x: {ok}/{total} OK | {fail} FAIL')
    if errors:
        for e in errors:
            print(f'  ! {e}')
    sys.exit(1 if errors else 0)
