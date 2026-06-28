import re

import binder.config as config
from binder.files import read_file
from binder.warnings import detect_warnings

def scan_disk() -> dict:
    file = config.ROOT / "config/filesystems.php"
    
    if not file.exists():
        return {
            "found": False,
            "disks": []
        }
        
    text = read_file(file)
    
    disk_pattern = re.compile(
        r"['\"]([^'\"]+)['\"]\s*=>\s*\[\s*['\"]driver['\"]",
        re.DOTALL
    )
    
    return {
        "found": True,
        "path": "config/filesystems.php",
        "disks": list(sorted(set(disk_pattern.findall(text)))),
        "warnings": detect_warnings("config/filesystems.php", text)
    }