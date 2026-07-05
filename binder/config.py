from pathlib import Path

ROOT = None
BINDER_DIR = None

SKIP_COLUMN_TYPES = {
    "index", "foreign", "dropColumn"
}

IGNORE_DIRS = {
    "vendor",
    "node_modules",
    "storage",
    "bootstrap/cache",

    ".git",
    ".idea",
    ".vscode",

    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",

    "env",
    ".env",
    "venv",
    ".venv",

    "dist",
    "build",
}

IGNORE_FILES = {
    ".DS_Store",
    "Thumbs.db",
}

IGNORE_EXTENSIONS = {
    ".pyc",
    ".pyo",
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