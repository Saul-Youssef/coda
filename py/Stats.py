# Stats.py — non-invasive statistics collector (default-to-local)
#
# Defines data-level toggles:
#   stats.on  / stats.off / stats.clear / stats.file / stats.file? / stats.dump
# Mirrors existing LOG(...) calls into a JSONL buffer/file via a small proxy.
#
# Behavior:
#   • If you never call `stats.file`, enabling stats will pick a writable default
#     path automatically (./eval_stats.jsonl, or ./logs/eval.jsonl, or ~/eval_stats.jsonl).
#   • You can still set an explicit path with a single-atom RHS, e.g.:
#       stats.file : <./logs/eval.jsonl>
#     (your language turns <...> into a single atom whose domain is the path)
#   • `stats.file?` shows the current file path (or 'none' if buffering only).
#
from base import *
import time, json
from pathlib import Path

# ------------------------------ Collector core -------------------------------
class _Stats:
    def __init__(self):
        self.enabled = False
        self.file    = None        # string path or None
        self.buffer  = []          # in-memory mirror
        self.last_error = None
        # psutil is optional
        try:
            import psutil
            self._proc = psutil.Process()
        except Exception:
            self._proc = None

    def _rss(self):
        if not self._proc:
            return None
        try:
            return self._proc.memory_info().rss
        except Exception:
            return None

    def _pick_default(self):
        # Prefer CWD, then ./logs, then HOME
        candidates = [
            Path.cwd() / 'eval_stats.jsonl',
            Path.cwd() / 'logs' / 'eval.jsonl',
            Path.home() / 'eval_stats.jsonl',
        ]
        for p in candidates:
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                with open(p, 'a'):
                    pass
                return str(p)
            except Exception as e:
                self.last_error = '{}: {}'.format(type(e).__name__, e)
                continue
        return None  # stay in-memory only

    def enable(self):
        self.enabled = True
        if not self.file:
            self.file = self._pick_default()

    def disable(self):
        self.enabled = False

    def clear(self):
        self.buffer = []

    def set_file(self, path):
        """If path is None, choose a default; else honor explicit path.
        `path` should be a plain string (your angle-bracket literal becomes that).
        """
        try:
            if not path:
                self.file = self._pick_default()
                return
            p = Path(path).expanduser()
            if not p.is_absolute():
                p = (Path.cwd() / p).resolve()
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, 'a'):
                pass
            self.file = str(p)
            self.last_error = None
        except Exception as e:
            self.last_error = '{}: {}'.format(type(e).__name__, e)
            # leave prior self.file as-is

    def event(self, kind, **kw):
        if not self.enabled:
            return
        e = {"t": time.time(), "kind": kind, "rss": self._rss()}
        e.update(kw)
        self.buffer.append(e)
        if self.file:
            try:
                with open(self.file, 'a') as f:
                    f.write(json.dumps(e))
                    f.write("\n")
            except Exception as e2:
                self.last_error = '{}: {}'.format(type(e2).__name__, e2)

    def dump_text(self):
        try:
            return "\n".join(json.dumps(x) for x in self.buffer)
        except Exception:
            return ""

STATS = _Stats()

# ------------------------------ Data-level API -------------------------------

def _stats_on(context, domain, A, B):
    STATS.enable()
    return data()

def _stats_off(context, domain, A, B):
    STATS.disable()
    return data()

def _stats_clear(context, domain, A, B):
    STATS.clear()
    return data()

# If RHS is empty -> choose default. If it's a single atom -> use its domain as the path.
# This works with your angle-bracket literal: <./logs/eval.jsonl>

def _stats_file(context, domain, A, B):
    try:
        if B.empty():
            STATS.set_file(None)
        elif len(B) == 1 and B.atom(CONTEXT):
            STATS.set_file(str(B[0].domain()))
        else:
            STATS.set_file(None)
    except Exception:
        STATS.set_file(None)
    return data()


def _stats_file_q(context, domain, A, B):
    return da(STATS.file if STATS.file else 'none')


def _stats_dump(context, domain, A, B):
    return da(STATS.dump_text())

CONTEXT.define('stats.on',    _stats_on)
CONTEXT.define('stats.off',   _stats_off)
CONTEXT.define('stats.clear', _stats_clear)
CONTEXT.define('stats.file',  _stats_file)
CONTEXT.define('stats.file?', _stats_file_q)
CONTEXT.define('stats.dump',  _stats_dump)

# ---------------------------- LOG mirroring hook -----------------------------
# Replace Log.LOG with a proxy that forwards calls AND emits a stats event.
try:
    import Log as _LogMod
    _orig_LOG = _LogMod.LOG
except Exception:
    _orig_LOG = None

class _LogProxy:
    def __init__(self, target):
        self._t = target
    # Mirror into stats (respect the current logging mask to limit noise)
    def __call__(self, key, *args):
        if STATS.enabled:
            try:
                if self.logging(key):
                    msg = ' '.join(str(a) for a in args)
                    STATS.event('log', key=str(key), msg=msg)
            except Exception:
                pass
        return self._t(key, *args)
    # Delegate expected methods
    def register(self, *a, **kw):  return self._t.register(*a, **kw)
    def logging(self, *a, **kw):   return self._t.logging(*a, **kw)
    def logs(self, *a, **kw):      return self._t.logs(*a, **kw)
    def on(self, *a, **kw):        return self._t.on(*a, **kw)
    def off(self, *a, **kw):       return self._t.off(*a, **kw)
    def clear(self, *a, **kw):     return self._t.clear(*a, **kw)
    def names(self):               return self._t.names()
    # Behave like original in iteration/lookup
    def __iter__(self):            return iter(self._t)
    def __contains__(self, name):  return name in self._t
    def __getitem__(self, name):   return self._t[name]
    def __repr__(self):            return repr(self._t)
    def __getattr__(self, attr):   return getattr(self._t, attr)

def _stats_summary(context, domain, A, B):
    from collections import Counter
    c = Counter(e.get('kind','?') for e in STATS.buffer)
    # return counts like: log:12 step:34 cache.miss:5 ...
    s = ' '.join(f'{k}:{c[k]}' for k in sorted(c))
    return da(s if s else 'none')

CONTEXT.define('stats.summary', _stats_summary)

if _orig_LOG is not None:
    _LogMod.LOG = _LogProxy(_orig_LOG)

# NOTE: Ensure builtin.py imports this module BEFORE modules that import LOG
# via `from Log import LOG`, so they pick up the proxy.
