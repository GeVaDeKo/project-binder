from datetime import datetime
from pathlib import Path
import shlex, sys

def scope_enabled(scopes, name):
    if not any(scopes.values()):
        return True
    
    return scopes.get(name, False)

def build_generator(context_mode="full", focus=None, scopes=None):
    command = ""
    executable = ""
    
    if context_mode == "focus":
        executable = " ".join(
            [shlex.quote(arg) for arg in sys.argv[:1]]
        )
        
        command = " ".join(
            [Path(sys.argv[0]).name]
            + [shlex.quote(arg) for arg in sys.argv[1:]]
        )
    
    return {
        "name": "Project-Binder",
        "vendor": "GeVaDeKo",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "command": command,
        "executable": executable,
        "scopes": scopes or {},
        "context_mode": context_mode,
        "focus": focus,
    }