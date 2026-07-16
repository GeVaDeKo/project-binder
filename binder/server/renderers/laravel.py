class LaravelRendererMixin:
    def render_laravel_sections(self, data):
        controllers = data.get("controllers", [])
        models = data.get("models", [])
        services = data.get("services", [])
        routes = data.get("routes", [])
        views = data.get("views", [])
        
        sections = []
        
        if controllers:
            sections.append(
                self.render_laravel_files(
                    title="Controllers",
                    files=controllers,
                    item_type="controller",
                )
            )
        
        if models:
            sections.append(
                self.render_laravel_files(
                    title="Models",
                    files=models,
                    item_type="model",
                )
            )
        
        if services:
            sections.append(
                self.render_laravel_files(
                    title="Services",
                    files=services,
                    item_type="service",
                )
            )
        
        if routes:
            sections.append(
                self.render_laravel_routes(routes)
            )
        
        if views:
            sections.append(
                self.render_laravel_views(views)
            )
        
        database_html = self.render_laravel_database(data)
        
        if database_html:
            sections.append(database_html)
        
        if not sections:
            return """
            <section class="card">
                <p>No Laravel code sections found.</p>
            </section>
            """
        
        return "".join(sections)
    
    def render_laravel_files(self, title, files, item_type):
        file_cards = []

        for file in files:
            path = file.get("path", "Unknown file")
            file_name = self.file_name_from_path(path)
            methods = file.get("methods", [])
            warnings = file.get("warnings", [])
            relations = file.get("relations", [])
            metrics = file.get("metrics", {})

            method_items = []

            for method in methods:
                name = method.get("name", "Unknown method")
                arguments = method.get("arguments", "")
                visibility = method.get("visibility", "unknown")
                returns = method.get("returns", [])

                returns_html = "".join(
                    f"<li><code>{value}</code></li>"
                    for value in returns
                )

                method_items.append(
                    f"""
                    <div class="laravel-method">
                        <div class="method-heading">
                            <code class="method-name">{name}</code>
                            <span class="badge">{visibility}</span>
                        </div>

                        <code class="method-arguments">
                            {arguments or "No arguments"}
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

            methods_html = (
                "".join(method_items)
                if method_items
                else '<p class="empty-state">No methods found.</p>'
            )

            extra_html = ""

            if item_type == "model":
                table = file.get("table", "Unknown table")

                relation_items = "".join(
                    f"""
                    <li>
                        <span class="badge">{relation.get("type", "relation")}</span>
                        <code>{relation.get("name", "Unknown")}</code>
                        <span>→ {relation.get("target", "Unknown")}</span>
                    </li>
                    """
                    for relation in relations
                )

                extra_html = f"""
                <div class="model-meta">
                    <p>Table: <code>{table}</code></p>

                    {
                        f'''
                        <p class="section-label">Relations</p>
                        <ul class="relation-list">{relation_items}</ul>
                        '''
                        if relation_items
                        else ""
                    }
                </div>
                """

            warning_items = "".join(
                f"""
                <li>
                    <span class="badge">{warning.get("severity", "warning")}</span>
                    {warning.get("message", "Unknown warning")}
                </li>
                """
                for warning in warnings
            )

            file_cards.append(
                f"""
                <details class="code-file">
                    <summary>
                        <div class="file-summary">
                            <span class="file-name">{file_name}</span>
                            <span class="file-path">{path}</span>
                        </div>

                        <span class="badge">PHP</span>
                    </summary>

                    <div class="file-content">
                        <div class="metrics-row">
                            <span>{metrics.get("total_lines", 0)} lines</span>
                            <span>{metrics.get("code_lines", 0)} code</span>
                            <span>{len(methods)} methods</span>
                        </div>

                        {extra_html}

                        <p class="section-label">Methods</p>
                        <div class="laravel-method-list">
                            {methods_html}
                        </div>

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
                <h2>{title}</h2>
                <span>{len(files)} files</span>
            </div>

            {''.join(file_cards)}
        </section>
        """
    
    def render_laravel_database(self, data):
        shared_context = data.get("shared_context", {})
        database = shared_context.get("database", {})
        
        if not isinstance(database, dict):
            return ""
        
        table_cards = []
        
        for table_name, table_data in database.items():
            if not isinstance(table_data, dict):
                continue
            
            columns = table_data.get("columns", [])
            
            column_rows = []
            
            for column in columns:
                if not isinstance(column, dict):
                    continue
                
                column_name = column.get("name", "Unknown column")
                column_type = column.get("type", "unknown")
                
                    
                column_rows.append(
                    f"""
                    <div class="database-column">
                        <code class="column-name">
                            {column_name}
                        </code>

                        <code class="column-type">
                            {column_type}
                        </code>
                    </div>
                    """
                )
            columns_html = (
                "".join(column_rows)
                if column_rows
                else '<p class="empty-state">No columns found.</p>'
            )

            table_cards.append(
                f"""
                <details class="database-table">
                    <summary>
                        <div>
                            <p class="section-label">
                                Database table
                            </p>

                            <h3>{table_name}</h3>
                        </div>

                        <span class="badge">
                            {len(columns)} columns
                        </span>
                    </summary>

                    <div class="database-table-content">
                        <div class="database-column-header">
                            <span>Column</span>
                            <span>Type</span>
                            <span>Attributes</span>
                        </div>

                        <div class="database-columns">
                            {columns_html}
                        </div>
                    </div>
                </details>
                """
            )

        if not table_cards:
            return ""

        return f"""
        <section class="code-section database-section">
            <div class="section-heading">
                <h2>Database</h2>
                <span>{len(table_cards)} tables</span>
            </div>

            {''.join(table_cards)}
        </section>
        """
    
    def render_laravel_routes(self, route_files):
        file_cards = []

        for route_file in route_files:
            path = route_file.get("path", "Unknown route file")
            file_name = self.file_name_from_path(path)
            routes = route_file.get("routes", [])
            warnings = route_file.get("warnings", [])

            route_rows = []

            for route in routes:
                method = route.get("method", "UNKNOWN")
                uri = route.get("uri", "/")
                controller = route.get("controller")
                action = route.get("action")

                if controller and action:
                    target = f"{controller} → {action}"
                elif controller:
                    target = controller
                else:
                    target = "Closure / framework route"

                route_rows.append(
                    f"""
                    <div class="route-row">
                        <span class="route-method route-{method.lower()}">
                            {method}
                        </span>

                        <code class="route-uri">{uri}</code>

                        <span class="route-target">{target}</span>
                    </div>
                    """
                )

            routes_html = (
                "".join(route_rows)
                if route_rows
                else '<p class="empty-state">No routes found.</p>'
            )

            warning_items = "".join(
                f"""
                <li>
                    <span class="badge">
                        {warning.get("severity", "warning")}
                    </span>
                    {warning.get("message", "Unknown warning")}
                </li>
                """
                for warning in warnings
            )

            file_cards.append(
                f"""
                <details class="code-file">
                    <summary>
                        <div class="file-summary">
                            <span class="file-name">{file_name}</span>
                            <span class="file-path">
                                {len(routes)} routes
                            </span>
                        </div>

                        <span class="badge">ROUTES</span>
                    </summary>

                    <div class="file-content">
                        <div class="route-list">
                            {routes_html}
                        </div>

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
                <h2>Routes</h2>
                <span>{len(route_files)} route files</span>
            </div>

            {''.join(file_cards)}
        </section>
        """
    
    def render_laravel_views(self, views):
        view_cards = []

        for view in views:
            path = view.get("path", "Unknown view")
            file_name = self.file_name_from_path(path)
            metrics = view.get("metrics", {})
            warnings = view.get("warnings", [])

            metrics_html = ""

            if metrics:
                metrics_html = f"""
                <div class="metrics-row">
                    <span>{metrics.get("total_lines", 0)} lines</span>
                    <span>{metrics.get("code_lines", 0)} code</span>
                    <span>{metrics.get("comment_lines", 0)} comments</span>
                </div>
                """

            warning_items = "".join(
                f"""
                <li>
                    <span class="badge">
                        {warning.get("severity", "warning")}
                    </span>
                    {warning.get("message", "Unknown warning")}
                </li>
                """
                for warning in warnings
            )

            view_cards.append(
                f"""
                <details class="code-file">
                    <summary>
                        <div class="file-summary">
                            <span class="file-name">{file_name}</span>
                            <span class="file-path">{path}</span>
                        </div>

                        <span class="badge">BLADE</span>
                    </summary>

                    <div class="file-content">
                        {metrics_html}

                        {
                            f'''
                            <div class="warning-block">
                                <p class="section-label">Warnings</p>
                                <ul>{warning_items}</ul>
                            </div>
                            '''
                            if warning_items
                            else '<p class="empty-state">No warnings found.</p>'
                        }
                    </div>
                </details>
                """
            )

        return f"""
        <section class="code-section">
            <div class="section-heading">
                <h2>Views</h2>
                <span>{len(views)} files</span>
            </div>

            {''.join(view_cards)}
        </section>
        """