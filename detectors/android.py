def is_android_project(root):
    return (
        (root / "settings.gradle").exists()
        or (root / "settings.gradle.kts").exists()
        or (root / "app" / "src" / "main" / "AndroidManifest.xml").exists()
    )