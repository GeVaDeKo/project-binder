import json, subprocess, sys, os, signal, time

from datetime import datetime
from pathlib import Path

def server_dir(project_path):
    path = Path(project_path) / "project-binder" / "server"
    path.mkdir(parents=True, exist_ok=True)
    
    return path

def server_file(project_path):
    return server_dir(project_path) / "server.json"

def start_background_server(project_path):
    project_path = Path(project_path).resolve()
    status_file = server_file(project_path)
    creationflags = 0
    
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
    
    start_new_session = sys.platform != "win32"
    
    process = subprocess.Popen(
        [
            sys.executable,
            str(Path(__file__).parents[2] / "project-binder.py"),
            str(project_path),
            "--serve-worker",
        ],
        cwd=project_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
        start_new_session=start_new_session,
    )
    
    server_data = {
        "pid": process.pid,
        "project": project_path.name,
        "project_path": str(project_path),
        "host": "127.0.0.1",
        "port": 8787,
        "started_at": datetime.now().isoformat(timespec="seconds"),
    }
    
    status_file.write_text(
        json.dumps(server_data, indent=4),
        encoding="utf-8"
    )
    
    return server_data

def process_is_running(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    
    return True

def get_server_status(project_path):
    project_path = Path(project_path).resolve()
    status_file = server_file(project_path)
    
    if not status_file.exists():
        return {
            "running": False,
            "reason": "server_file_not_found",
        }
    
    try:
        server_data = json.loads(
            status_file.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return {
            "running": False,
            "reason": "invalid_server_file",
        }
    
    pid = server_data.get("pid")
    running = process_is_running(pid)
    
    return {
        **server_data,
        "running": running,
        "reason": None if running else "process_not_running",
    }


def stop_background_server(project_path):
    status = get_server_status(project_path)
    
    if not status["running"]:
        print("Project-Binder server is not running.")
        return False
    
    try:
        os.kill(status["pid"], signal.SIGINT)
    except ProcessLookupError:
        server_file(project_path).unlink(missing_ok=True)
        return
    
    for _ in range(20):
        if not process_is_running(status["pid"]):
            break
        
        time.sleep(0.1)
    
    if process_is_running(status["pid"]):
        print("Unable to stop Project-Binder viewer.")
        return False
    
    server_file(project_path).unlink(missing_ok=True)
    print("Project-Binder viewer stopped.")
    return True