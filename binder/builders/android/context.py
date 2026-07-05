def build_android_context(scan):
    return {
        "android": scan["android"],
        "android_context_graph": scan.get("android_context_graph", {}),
    }