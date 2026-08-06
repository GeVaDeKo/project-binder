import re

def extract_android_sdk(text):
    return {
        "compile_sdk": extract_int(text, r"compileSdk\s*(\d+)"),
        "min_sdk": extract_int(text, r"minSdk\s*=\s*(\d+)"),
        "target_sdk": extract_int(text, r"targetSdk\s*=\s*(\d+)"),
        "version_code": extract_int(text, r"versionCode\s*=\s*(\d+)"),
        "version_name": extract_string(text, r'versionName\s*=\s*"([^"]+)"'),
        "application_id": extract_string(text, r'applicationId\s*=\s*"([^"]+)"'),
    }
    
def extract_plugins(text):
    return sorted(set(
        re.findall(r'id\("([^"]+)"\)', text)
        + re.findall(r'alias\(libs\.plugins\.([A-Za-z0-9_.-]+)\)', text)
    ))
    
def extract_dependencies(text):
    return sorted(set(
        re.findall(r'implementation\("([^"]+)"\)', text)
        + re.findall(r'implementation\(libs\.([A-Za-z0-9_.-]+)\)', text)
        + re.findall(r'testImplementation\("([^"]+)"\)', text)
        + re.findall(r'androidTestImplementation\("([^"]+)"\)', text)
        + re.findall(r'debugImplementation\("([^"]+)"\)', text)
    ))

def extract_int(text, pattern):
    match = re.search(pattern, text)
    return int(match.group(1)) if match else None

def extract_string(text, pattern):
    match = re.search(pattern, text)
    return match.group(1) if match else None