class AndroidRendererMixin:
    def render_android_files(self, android_files):
        if not android_files:
            return """
            <section class="card">
                <h2>Android files</h2>
                <p>No Android files found in this context.</p>
            </section>
            """
        
        file_cards = []
        
        for file in android_files:
            path = file.get("path", "Unknown file")
            file_name = self.file_name_from_path(path)
            package = file.get("package", "Unknown package")
            declarations = file.get("declarations", [])
            methods = file.get("methods", [])
            
            declaration_items = []
            
            for declaration in declarations:
                declaration_type = declaration.get("type", "declaration")
                declaration_name = declaration.get("name", "Unknown")
                
                declaration_items.append(
                    f"""
                    <li class="declaration-item">
                        <span class="badge">{declaration_type}</span>
                        <code>{declaration_name}</code>
                    </li>
                    """
                )
            
            declarations_html = (
                f"""
                <ul class="declaration-list">
                    {''.join(declaration_items)}
                </ul>
                """
                if declaration_items
                else '<p class="empty-state">No declarations found.</p>'
            )
            
            method_items = []
                
            for method in methods:
                method_name = method.get("name", "Unknown method")
                arguments = method.get("arguments", "")
                return_type = method.get("returns", "Unit")
                visibility = method.get("visibility", "default")
                suspend = method.get("suspend", False)
                
                suspend_badge = (
                    '<span class="badge">suspend</span>'
                    if suspend
                    else ""
                )
                
                method_items.append(
                    f"""
                    <li class="method-item">
                        <div class="method-main>
                            <code class="method-name>{method_name}</code>
                            
                            <code class="method-arguments">
                                {arguments or "No arguments"}
                            </code>
                            
                            <div class="method-meta">
                                <span>{visibility}</span>
                                {suspend_badge}
                            </div>
                        </div>
                        
                        <span class="return-type">→ {return_type}</span>
                    </li>
                    """
                )
                
            methods_html = (
                f"""
                <ul class="method-list">
                    {''.join(method_items)}
                </ul>
                """
                if method_items
                else '<p class="empty-state">No methods found.</p>'
            )
                
            file_cards.append(
                f"""
                <details class="code-file">
                    <summary>
                        <div class="file-summary">
                            <span class="file-name">{file_name}</span>
                            <span class="package-name">
                                Package: <code>{package}</code>
                            </span>
                        </div>
                        
                        <span class="badge">{file.get("extension", "")}</span>
                    </summary>
                    
                    <div class="file-content">
                        <div class="file-header">
                            <p class="section-label">Android file</p>
                            <p class="file-path">{file_name}</p>
                        </div>

                        <div class="class-block">
                            <p class="section-label">Declarations</p>
                            {declarations_html}

                            <p class="section-label">Methods</p>
                            {methods_html}
                        </div>
                    </div>
                </details>
                """
            )
        
        return f"""
        <section class="code-section">
            <div class="section-heading">
                <h2>Android files</h2>
                <span>{len(android_files)} files</span>
            </div>
            
            {''.join(file_cards)}
        </section>
        """