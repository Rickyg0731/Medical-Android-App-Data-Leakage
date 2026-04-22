import json

# exists to save the entire report in a structured json
def save_report(report, output_file):
    with open(output_file, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Report saved to {output_file}")

# responsible for outputting the overall output after files are scanned, leaks are found/not found, 
# and risk score is calculated
def print_summary(report):
    print("\n=== ANALYSIS SUMMARY ===")

    print(f"\nApp: {report['app']}")

    print("\nPermissions:")
    for p in report["permissions"]:
        print(f"- {p}")

    print("\nThird-party libraries:")
    for lib in report["third_party_libraries"]:
        print(f"- {lib}")

    print("\nPotential leaks:")
    if not report["potential_leaks"]:
        print("None found")
    else:
        for i, leak in enumerate(report["potential_leaks"], 1):
            print(f"{i}. {leak['source']} → {leak['sink']} → {leak['endpoint']} (File: {leak['file']})")

    print(f"\nRisk Level: {report['risk']['level']} (Score: {report['risk']['score']})")
