from html import escape

class BaseRendererMixin:
    def file_name_from_path(self, path):
        return path.replace("\\", "/").split("/")[-1]
    
    def safe_text(self, value):
        return escape(str(value))
    
    def compact_value(self, value, max_length=180):
        text = str(value).strip()

        if len(text) > max_length:
            return text[:max_length] + "…"

        return text