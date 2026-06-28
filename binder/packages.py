import binder.config as config
from binder.files import read_json_file

def scan_composer_packages() -> dict:
    composer = read_json_file(config.ROOT / "composer.json")
    
    require = composer.get("require", {})
    require_dev = composer.get("require-dev", {})
    
    return {
        "require": require,
        "require_dev": require_dev
    }

def scan_frontend_packages() -> dict:
    package = read_json_file(config.ROOT / "package.json")
    
    dependencies = package.get("dependencies", {})
    dev_dependencies = package.get("devDependencies", {})
    
    return {
        "dependencies": dependencies,
        "dev_dependencies": dev_dependencies
    }

def detect_laravel_version(composer: dict) -> str | None:
    require = composer.get("require", {})
    
    return require.get("laravel/framework")

def detect_php_version(composer: dict) -> str | None:
    require = composer.get("require", {})
    
    return require.get("php")

def detect_features(composer: dict, frontend: dict) -> list:
    features = []
    
    require = composer.get("require", {})
    require_dev = composer.get("require_dev", {})
    
    dependencies = frontend.get("dependencies", {})
    dev_dependencies = frontend.get("dev_dependencies", {})
    
    all_packages = {
        **require,
        **require_dev,
        **dependencies,
        **dev_dependencies
    }
    
    checks = {
        "laravel/breeze": "authentication",
        "simple-qrcode": "qrcode",
        "tailwindcss": "tailwindcss",
        "alpinejs": "alpinejs",
        "vite": "vite"
    }
    
    for package, feature in checks.items():
        if package in all_packages:
            features.append(feature)
    
    return sorted(features)