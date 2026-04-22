import argparse
from fileextraction import get_all_code_files
from permissions import extract_permissions
from scanner import scan_file
from leaks import detect_leaks
from riskcalc import calculate_risk
from analysis import save_report, print_summary


def analyze_apk(decompiled_dir, apk_name):
    print(f"\nScanning directory: {decompiled_dir}")

    # Find all .java, .kt, .smali, .xml files
    files = get_all_code_files(decompiled_dir)
    print(f"Found {len(files)} files to scan")

    # Locate AndroidManifest.xml for permissions
    manifest_path = None
    for f in files:
        if "AndroidManifest.xml" in f:
            manifest_path = f
            break

    if manifest_path:
        print(f"Manifest found: {manifest_path}")
    else:
        print("[WARNING] AndroidManifest.xml not found — permissions will be empty")

    permissions = extract_permissions(manifest_path) if manifest_path else []

    file_findings = {}
    all_third_party = set()

    print("Scanning files for sources, sinks, URLs, and third-party libs...")
    for file in files:
        result = scan_file(file)
        if any(result.values()):
            file_findings[file] = result
            all_third_party.update(result["third_party"])

    print(f"Files with findings: {len(file_findings)}")

    # Detect leaks and compute risk
    leaks = detect_leaks(file_findings)
    risk_level, score = calculate_risk(leaks, len(all_third_party))

    report = {
        "app": apk_name,
        "files_scanned": len(files),
        "permissions": permissions,
        "third_party_libraries": list(all_third_party),
        "potential_leaks": leaks,
        "risk": {"level": risk_level, "score": score}
    }

    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Android Privacy Leak Analyzer")
    parser.add_argument("directory", help="Path to decompiled APK directory")
    parser.add_argument("--app", default="unknown.apk", help="App name/identifier")
    parser.add_argument("--output", default="report.json", help="Output JSON file path")
    parser.add_argument("--html", default=None, help="Optional: output HTML report file path")

    args = parser.parse_args()

    report = analyze_apk(args.directory, args.app)
    save_report(report, args.output)
    print_summary(report)

    if args.html:
        from report_html import generate_html_report
        generate_html_report(report, args.html)
