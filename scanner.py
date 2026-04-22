import re
from config import SENSITIVE_SOURCES, SINKS, THIRD_PARTY_LIBS, URL_REGEX

def scan_file(filepath):
    findings = {
        "sources": [],
        "sinks": [],
        "urls": [],
        "third_party": []
    }

    try:
        # open source code
        with open(filepath, "r", errors="ignore") as f:
            content = f.read()
            # looks for sensitive APIs 
            for src in SENSITIVE_SOURCES:
                if src in content:
                    findings["sources"].append(src)
            # attempts to look for any data leaving app
            for sink in SINKS:
                if sink in content:
                    findings["sinks"].append(sink)

            # looks for urls 
            urls = re.findall(URL_REGEX, content)
            findings["urls"].extend(urls)
            # attempt to find third party libraries 
            for lib_name, lib_path in THIRD_PARTY_LIBS.items():
                if lib_path in content:
                    findings["third_party"].append(lib_name)

    except Exception as e:
        print(f"[ERROR] Could not read {filepath}: {e}")

    return findings
