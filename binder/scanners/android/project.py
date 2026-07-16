import binder.config as config
from binder.files import read_file
from binder.extractors.android.gradle import(
    extract_android_sdk,
    extract_plugins,
    extract_dependencies,
)

def scan_android_project():
    app_gradle = find_first([
        "app/build.gradle.kts",
        "app/build.gradle",
    ])
    
    root_gradle = find_first([
        "build.gradle.kts",
        "build.gradle",
    ])
    
    app_text = read_file(app_gradle) if app_gradle else ""
    root_text = read_file(root_gradle) if root_gradle else ""
    
    return{
        "gradle_files": {
            "app": str(app_gradle.relative_to(config.ROOT)) if app_gradle else None,
            "root": str(root_gradle.relative_to(config.ROOT)) if root_gradle else None,
        },
        "sdk": extract_android_sdk(app_text),
        "plugins": extract_plugins(root_text + "\n" + app_text),
        "dependencies": extract_dependencies(root_text + "\n" + app_text),
        "features": detect_android_features(root_text + "\n" + app_text),
    }

def find_first(paths):
    for path in paths:
        candidate = config.ROOT / path
        if candidate.exists():
            return candidate
    
    return None

def detect_android_features(text):
    features = set()
    
    checks = {
        "compose": ["compose", "androidx.compose"],
        "retrofit": ["retrofit"],
        "cameraX": ["camera", "android.camera"],
        "mlkit": ["mlkit", "google.mlkit"],
        "datastore": ["datastore", "preferencesDataStore"],
        "navigation": ["navigation-compose", "androidx.navigation"],
        "material3": ["material3"],
    }
    
    lower = text.lower()
    
    for feature, needles in checks.items():
        if any(needle.lower() in lower for needle in needles):
            features.add(feature)
    
    return sorted(features)