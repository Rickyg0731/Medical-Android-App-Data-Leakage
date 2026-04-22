import os

def detect_leaks(file_findings):
    leaks = []

    for file, data in file_findings.items():
        # A potential leak is flagged when a sensitive SOURCE (data collection API)
        # and a SINK (data transmission/output method) both appear in the same file.
        # This co-occurrence suggests sensitive data may be collected and then sent out.
        # Note: this is a conservative heuristic — not every match is a confirmed leak.
        # False positives are possible if source and sink are unrelated code paths.
        if data["sources"] and data["sinks"]:
            for src in data["sources"]:
                for sink in data["sinks"]:
                    leaks.append({
                        "source": src,
                        "sink": sink,
                        # use first URL found in the file as the suspected endpoint
                        "endpoint": data["urls"][0] if data["urls"] else None,
                        "file": os.path.basename(file)
                    })

    return leaks
