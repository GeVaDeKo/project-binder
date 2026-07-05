#!/usr/bin/env python3
import binder.config as config

# Parsers
from binder.parsers.parsers import parse_args, parse_focus_scope

# Dectectors
from binder.detectors.project_type import detect_project_type
from binder.scanners.project import scan_project

from binder.builders.context import build_full_context, build_focus_context, write_context

def binder_dir():
    path = config.ROOT / "project-binder"
    path.mkdir(exist_ok=True)
    return path

def ensure_gitignore_entry():
    gitignore = config.ROOT / ".gitignore"
    entry = "/project-binder/"
    
    if not gitignore.exists():
        gitignore.write_text(f"# Project Binder\n{entry}\n", encoding="utf-8")
        return
    
    text = gitignore.read_text(encoding="utf-8", errors="ignore")
    
    if entry in text:
        return
    
    with gitignore.open("a", encoding="utf-8") as f:
        f.write(f"\n# Project Binder\n{entry}\n")

def main():
    args = parse_args()
    focus_type, focus, scopes = parse_focus_scope(args)
    
    config.set_root(args.project_path)
    ensure_gitignore_entry()
    
    project_type = detect_project_type(config.ROOT)
    scan = scan_project(
        focus=focus,
        project_type=project_type,
    )
    
    full_context = build_full_context(scan)
    write_context(
        binder_dir() / f"{config.ROOT.name}_project_context.json",
        full_context,
    )
    
    if focus or any(scopes.values()):
        focused_context = build_focus_context(scan, focus, scopes)
        write_context(
            binder_dir() / f"{config.ROOT.name}_{focus or 'selection'}_context.json",
            focused_context,
        )

if __name__ == "__main__":
    main()