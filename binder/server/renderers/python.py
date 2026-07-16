from html import escape

class PythonRendererMixin:
    def render_python_files(self, python_files):
        if not python_files:
            return """
            <section class="card">
                <h2>Python files</h2>
                <p>No Python files found in this context.</p>
            </section>
            """

        file_cards = []

        for file in python_files:
            path = file.get("path", "Unknown file")
            safe_path = escape(str(path))
            metrics = file.get("metrics", {})
            imports = file.get("imports", [])
            classes = file.get("classes", [])
            functions = file.get("functions", [])
            warnings = file.get("warnings", [])

            class_blocks = []

            for class_data in classes:
                class_name = class_data.get("name", "Unknown class")
                methods = class_data.get("methods", [])

                method_items = []

                for method in methods:
                    method_name = method.get("name", "Unknown method")
                    safe_name = escape(str(method_name))
                    arguments = method.get("arguments", [])
                    returns = method.get("returns", [])

                    arguments_text = ", ".join(arguments) if arguments else "No arguments"
                    safe_arguments = escape(str(arguments_text))
                    
                    returns_html = "".join(
                        f"<li><code>{escape(str(value))}</code></li>"
                        for value in returns
                        if value is not None
                    )

                    method_items.append(
                        f"""
                        <div class="python-callable">
                            <div class="python-callable-header">
                                <code class="method-name">{safe_name}</code>
                                <span class="badge">method</span>
                            </div>

                            <code class="method-arguments">
                                {safe_arguments}
                            </code>

                            {
                                f'''
                                <div class="method-returns">
                                    <p class="section-label">Returns</p>
                                    <ul>{returns_html}</ul>
                                </div>
                                '''
                                if returns_html
                                else ""
                            }
                        </div>
                        """
                    )

                class_blocks.append(
                    f"""
                    <div class="python-class">
                        <div class="python-class-header">
                            <div>
                                <p class="section-label">Class</p>
                                <h3>{class_name}</h3>
                            </div>

                            <span class="badge">
                                {len(methods)} methods
                            </span>
                        </div>

                        <div class="python-callable-list">
                            {
                                ''.join(method_items)
                                if method_items
                                else '<p class="empty-state">No methods found.</p>'
                            }
                        </div>
                    </div>
                    """
                )

            function_items = []

            for function in functions:
                function_name = function.get("name", "Unknown function")
                safe_name = escape(str(function_name))
                arguments = function.get("arguments", [])
                returns = function.get("returns", [])
                function_type = function.get("type", "function")

                arguments_text = ", ".join(arguments) if arguments else "No arguments"
                safe_arguments = escape(str(arguments_text))

                returns_html = "".join(
                    f"<li><code>{escape(str(value))}</code></li>"
                    for value in returns
                    if value is not None
                )

                function_items.append(
                    f"""
                    <div class="python-callable">
                        <div class="python-callable-header">
                            <code class="method-name">{safe_name}</code>
                            <span class="badge">{function_type}</span>
                        </div>

                        <code class="method-arguments">
                            {safe_arguments}
                        </code>

                        {
                            f'''
                            <div class="method-returns">
                                <p class="section-label">Returns</p>
                                <ul>{returns_html}</ul>
                            </div>
                            '''
                            if returns_html
                            else ""
                        }
                    </div>
                    """
                )

            imports_html = "".join(
                f"<li><code>{escape(str(item))}</code></li>"
                for item in imports
            )

            warning_items = "".join(
                f"""
                <li>
                    <span class="badge">
                        {escape(str(warning.get("severity", "warning")))}
                    </span>

                    {escape(str(warning.get("message", "Unknown warning")))}
                </li>
                """
                for warning in warnings
            )

            file_cards.append(
                f"""
                <details class="code-file">
                    <summary>
                        <div class="file-summary">
                            <span class="file-name">
                                {self.file_name_from_path(path)}
                            </span>

                            <span class="file-path">{safe_path}</span>
                        </div>

                        <span class="badge">PYTHON</span>
                    </summary>

                    <div class="file-content">
                        <div class="metrics-row">
                            <span>{metrics.get("total_lines", 0)} lines</span>
                            <span>{metrics.get("code_lines", 0)} code</span>
                            <span>{len(classes)} classes</span>
                            <span>{len(functions)} functions</span>
                            <span>{len(imports)} imports</span>
                        </div>

                        {
                            f'''
                            <div class="python-imports">
                                <p class="section-label">Imports</p>
                                <ul>{imports_html}</ul>
                            </div>
                            '''
                            if imports_html
                            else ""
                        }

                        {
                            ''.join(class_blocks)
                            if class_blocks
                            else ""
                        }

                        {
                            f'''
                            <div class="python-functions">
                                <p class="section-label">Functions</p>

                                <div class="python-callable-list">
                                    {''.join(function_items)}
                                </div>
                            </div>
                            '''
                            if function_items
                            else ""
                        }

                        {
                            f'''
                            <div class="warning-block">
                                <p class="section-label">Warnings</p>
                                <ul>{warning_items}</ul>
                            </div>
                            '''
                            if warning_items
                            else ""
                        }
                    </div>
                </details>
                """
            )

        return f"""
        <section class="code-section">
            <div class="section-heading">
                <h2>Python files</h2>
                <span>{len(python_files)} files</span>
            </div>

            {''.join(file_cards)}
        </section>
        """