from pathlib import Path

ROOT = None

SKIP_COLUMN_TYPES = {
    "index", "foreign", "dropColumn"
}

IGNORE_DIRS= {
    "vendor", "node_modules", "storage", "bootstrap/cache",
    ".git", ".idea", ".vscode", "public"
}

OUTPUT_FILE = "project_context.json"

ALLOWED_ENV_KEYS = {
    "APP_ENV",
    "APP_DEBUG",
    "APP_URL",
    
    "DB_CONNECTION",
    
    "CACHE_STORE",
    "SESSION_DRIVER",
    "QUEUE_CONNECTION",
    
    "MAIL_MAILER",
    
    "FILESYSTEM_DISK",
    
    "BROADCAST_CONNECTION",
}

def set_root(path):
    global ROOT
    ROOT = Path(path).resolve()