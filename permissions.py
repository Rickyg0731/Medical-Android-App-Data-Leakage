import re

def extract_permissions(manifest_path):
    permissions = []

    try:
        with open(manifest_path, "r", errors="ignore") as f:
            content = f.read()
        # extracts whatever user permissions are required for app to function
        matches = re.findall(r'uses-permission.*android:name="([^"]+)"', content)

        # simplifies output to only show the key permission
        # ex: android.permission.INTERNET --> INTERNET
        for m in matches:
            permissions.append(m.split('.')[-1])

    except Exception as e:
        print(f"[ERROR] Manifest read failed: {e}")

    return permissions
