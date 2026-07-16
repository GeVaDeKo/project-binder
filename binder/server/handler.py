import json

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote

from binder.server.renderers.base import BaseRendererMixin
from binder.server.renderers.android import AndroidRendererMixin
from binder.server.renderers.laravel import LaravelRendererMixin
from binder.server.renderers.python import PythonRendererMixin

class BinderRequestHandler(
    BaseRendererMixin,
    AndroidRendererMixin,
    LaravelRendererMixin,
    PythonRendererMixin,
    SimpleHTTPRequestHandler,
):
    binder_path: Path = Path.cwd()
    
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            return self.render_index()
        
        if self.path.startswith("/context/"):
            filename = unquote(self.path.replace("/context/", "", 1))
            return self.render_context(filename)
        
        if self.path.startswith("/static/"):
            return super().do_GET()
        
        return self.send_error(404, "Not found")
    
    def render_code_sections(self, data):
        project = data.get("project", {})
        summary = project.get("project_summary", {})
        
        project_type = project.get("project_type", "")
        
        if project_type == "android":
            return self.render_android_files(data.get("android", []))
        
        if project_type == "python":
            return self.render_python_files(data.get("python", []))
        
        if project_type == "laravel":
            return self.render_laravel_sections(data)
        
        return "<p>No supported code sections found.</p>"
    
    def render_layout(self, title, sidebar_html, content_html):
        html = f"""
        <html>
        <head>
            <title>{title} - Project-Binder</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="app-shell">
                <aside class="sidebar">
                    {sidebar_html}
                </aside>

                <main class="content">
                    {content_html}
                </main>
            </div>
        </body>
        </html>
        """

        self.send_html(html)
    
    def render_sidebar(self, active_file=None):
        files = sorted(self.binder_path.glob("*.json"))

        links = []
        contexts = []

        for file in files:
            data = self.read_context_file(file)
            
            if not data:
                continue

            generator = data.get("generator", {})
            mode = generator.get("context_mode")
            focus = generator.get("focus")

            contexts.append({
                "file": file,
                "mode": mode,
                "focus": focus,
            })

        contexts.sort(
            key=lambda item: (
                0 if item["mode"] == "full" else 1,
                str(item["focus"] or "").lower(),
            )
        )

        for context in contexts:
            file = context["file"]
            mode = context["mode"]
            focus = context["focus"]

            label = "Full project" if mode == "full" else f"Focus: {focus}"
            active = "active" if file.name == active_file else ""

            links.append(
                f'<a class="sidebar-link {active}" '
                f'href="/context/{file.name}">{label}</a>'
            )
        return f"""
        <div class="sidebar-header">
            <a href="/" class="sidebar-brand">Project-Binder</a>
        </div>

        <p class="sidebar-muted">Context files</p>

        <nav class="sidebar-nav">
            {''.join(links)}
        </nav>
        """
    
    def render_index(self):
        files = sorted(self.binder_path.glob("*.json"))
        
        contexts = []
        
        for file in files:
            data = self.read_context_file(file)
            
            if not data:
                continue
            
            generator = data.get("generator", {})
            project = data.get("project", {})
            summary = data.get("project_summary", {})
            
            contexts.append({
                "file": file.name,
                "project": project.get("name", "Unknown project"),
                "mode": generator.get("context_mode", "unknown"),
                "focus": generator.get("focus"),
                "label": self.context_label(data, file.name),
                "type": summary.get("type") if isinstance(summary, dict) else None,
            })
        
        project_name = contexts[0]["project"] if contexts else "Project-Binder"
        
        full_contexts = [c for c in contexts if c["mode"] == "full"]
        focus_contexts = [c for c in contexts if c["mode"] == "focus"]
        other_contexts = [c for c in contexts if c["mode"] not in ["full", "focus"]]
        
        def card(context):
            badge = context["type"] or context["mode"]
            return f"""
            <a class="context-card" href="/context/{context['file']}">
                <div>
                    <h3>{context['label']}</h3>
                    <p>{context['file']}</p>
                </div>
                <span class="badge">{badge}</span>
            </a>
            """
        html = f"""
        <html>
        <head>
            <title>{project_name} - Project-Binder</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <main class="page">
                <section class="hero">
                    <p class="eyebrow">Project-Binder</p>
                    <h1>{project_name}</h1>
                    <p class="subtitle">
                        Eén projectwaarheid. Twee lezers: mens en AI.
                    </p>
                </section>

                <section class="grid">
                    <div class="stat-card">
                        <strong>{len(contexts)}</strong>
                        <span>Context files</span>
                    </div>
                    <div class="stat-card">
                        <strong>{len(focus_contexts)}</strong>
                        <span>Focus areas</span>
                    </div>
                    <div class="stat-card">
                        <strong>{len(full_contexts)}</strong>
                        <span>Full contexts</span>
                    </div>
                </section>

                <section class="card">
                    <h2>Project overview</h2>
                    {''.join(card(c) for c in full_contexts) or "<p>No full project context found.</p>"}
                </section>

                <section class="card">
                    <h2>Focus areas</h2>
                    {''.join(card(c) for c in focus_contexts) or "<p>No focus contexts found.</p>"}
                </section>

                {f'''
                <section class="card">
                    <h2>Other contexts</h2>
                    {''.join(card(c) for c in other_contexts)}
                </section>
                ''' if other_contexts else ""}
            </main>
        </body>
        </html>
        """

        self.send_html(html)
    
    def render_context(self, filename):
        file_path = self.binder_path / filename
        
        if not file_path.exists() or file_path.suffix != ".json":
            return self.send_error(404, "Context file not found")
        
        data = json.loads(file_path.read_text(encoding="utf-8"))
        mode = data.get("generator", {}).get("context_mode")
        
        if mode == "full":
            return self.render_full_context(data, filename)
            
        if mode == "focus":
            return self.render_focus_context(data, file_path.name)
        
        return self.send_error(400, "Unknown context mode")
        
    def render_full_context(self, data, filename):
        project = data.get("project", {})
        
        content = f"""
        <section class="hero">
            <p class="eyebrow">Full project context</p>
            <h1>{project.get("name", "Unknown project")}</h1>
        </section>
        
        {self.render_code_sections(data)}
        
        <details class="card">
            <summary>Raw context</summary>
            <pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
        </details>
        """

        self.render_layout(
            project.get("name", "Project-Binder"),
            self.render_sidebar(filename),
            content
        )
        
    def render_focus_context(self, data, filename):
        project = data.get("project", {})
        generator = data.get("generator", {})
        focus = generator.get("focus", "Unknown focus")

        content = f"""
        <section class="hero">
            <p class="eyebrow">Focused context</p>
            <h1>{project.get("name", "Unknown project")} / {focus}</h1>
        </section>
        
        {self.render_code_sections(data)}

        <details class="card">
            <summary>Raw context</summary>
            <pre>{json.dumps(data, indent=2, ensure_ascii=False)}</pre>
        </details>
        """

        self.render_layout(
            f"{project.get('name', 'Project-Binder')} / {focus}",
            self.render_sidebar(filename),
            content
        )
    
    def send_html(self, html: str):
        encoded = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Lenght", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
    
    def read_context_file(self, file_path):
        try:
            return json.loads(file_path.read_text(encoding="utf-8"))
        except Exception:
            return None
        
    def context_label(self, data, file_name):
        generator = data.get("generator", {})
        project = data.get("project", {})
        
        mode = generator.get("context_mode", "unknown")
        focus = generator.get("focus")
        
        if mode == "full":
            return "Full project context"
        
        if mode == "focus":
            return f"Focus: {focus or file_name}"
        
        return "Unknown context"