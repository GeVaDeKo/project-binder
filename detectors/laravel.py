def is_laravel_project(root):
    return(
        (root / "artisan").exists()
        and (root / "composer.json").exists()
        and (root / "app").exists()
    )