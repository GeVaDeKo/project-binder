from binder.metrics import count_lines

def detect_warnings(path: str, text: str) -> list:
    warnings = []
    
    if "<script" in text.lower():
        warnings.append({
            "type": "inline_javascript",
            "severity": "annoying_future_geert",
            "message": "Inline JavaScript gevonden. Overweeg resource/js/components/."
        })
    
    if "<style" in text.lower():
        warnings.append({
            "type": "inline_css",
            "severity": "annoying_future_geert",
            "message": "Inline CSS gevonden. Overweeg resources/css/app.css."
        })
    
    if "192.168." in text:
        warnings.append({
            "type": "hardcoded_local_ip",
            "severity": "future_geert_will_sigh",
            "message": "Hardcoded lokaal IP-adres gevonden."
        })

    if "Storage::disk('public')" in text or 'Storage::disk("public")' in text:
        warnings.append({
            "type": "public_disk_usage",
            "severity": "check_this_friend",
            "message": "Gebruik van public disk gevonden. Controleer of dit bewust is."
        })
        
    metrics = count_lines(text)
    if metrics["total_lines"] > 400:
        warnings.append({
            "type": "large_file",
            "severity": "future_geert_will_start_refactoring",
            "message": f"Bestand is groot: {metrics['total_lines']} regels."
        })
    
    return warnings