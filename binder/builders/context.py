import sys, shlex, json
import binder.config as config

from pathlib import Path

from binder.builders.project import ( 
    build_focus_project_info,
    build_project_info,
)

from binder.focus import (
    filter_controllers,
    filter_models,
    filter_custom_classes,
    filter_routes,
    filter_by_path,
)

from binder.builders.generator import build_generator

# Context
from binder.builders.laravel.context import build_laravel_context, build_laravel_focus_context
from binder.builders.python.context import build_python_context, build_python_focus_context
from binder.builders.android.context import build_android_context, build_android_focus_context

def write_context(filename, context):
    output_file = config.ROOT / filename
    
    output_file.write_text(
        json.dumps(context, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    
    print(f"Context geschreven naar: {output_file}")

def build_focused_context_graph(context_graph, focus):
    if not focus:
        return context_graph

    return {
        "focus": focus,
        "models": {
            key: value
            for key, value in context_graph.get("models", {}).items()
            if focus.lower() in key.lower()
        },
        "tables": {
            key: value
            for key, value in context_graph.get("tables", {}).items()
            if focus.lower() in key.lower()
            or (
                value.get("model")
                and focus.lower() in value.get("model", "").lower()
            )
        },
    }

def build_full_context(scan):
    project_type = scan.get("project_type", "unknown")
    
    context = {
        "generator": build_generator(
            context_mode="full",
            focus=None,
            scopes={}
        ),
        "project": build_project_info(scan, project_type),
    }
    
    executable = " ".join(
        [shlex.quote(arg) for arg in sys.argv[:1]]
    )
    
    command = " ".join(
        [Path(sys.argv[0]).name] +
        [shlex.quote(arg) for arg in sys.argv[1:]]
    )
    
    if project_type == "android":
        context.update(build_android_context(scan))
        
    if project_type in ("laravel", "mixed"):
        context.update(build_laravel_context(scan))
    
    if project_type in ("python", "mixed"):
        context.update(build_python_context(scan))
        context["generator"]["command"] = command
        context["generator"]["executable"] = executable
    
    return context

def build_focus_context(scan, focus, scopes):
    project_type = scan.get("project_type", "unknown")
    
    filtered_laravel = {
        "custom_classes": filter_custom_classes(scan.get("custom_classes", []), focus),
        "controllers": filter_controllers(scan["controllers"], focus),
        "models": filter_models(scan["models"], focus),
        "services": filter_controllers(scan["services"], focus),
        "views": filter_by_path(scan["views"], focus),
        "routes": filter_routes(scan["routes"], focus),
    }
    
    context = {
        "generator": build_generator(
            context_mode="focus",
            focus=focus,
            scopes=scopes,
        ),
        "project": build_focus_project_info(
            scan,
            project_type,
        ),
    }
    
    if project_type == "android":
        context.update(
            build_android_focus_context(scan, focus)
        )
    
    if project_type == "laravel":
        context.update(
            build_laravel_focus_context(
                filtered_laravel,
                scopes,
            )
        )
    
    if project_type == "python":
        context.update(
            build_python_focus_context(
                scan,
                focus
            )
        )
    
    return context