"""
report_html.py — Generates a styled HTML report from the analysis JSON.
Usage: called automatically from main.py when --html flag is passed,
       or run standalone: python3 report_html.py report.json output.html
"""

import json
import sys
from datetime import datetime


def generate_html_report(report: dict, output_file: str):
    app_name = report.get("app", "Unknown App")
    permissions = report.get("permissions", [])
    third_party = report.get("third_party_libraries", [])
    leaks = report.get("potential_leaks", [])
    files_scanned = report.get("files_scanned", 0)
    risk_level = report["risk"]["level"]
    risk_score = report["risk"]["score"]
    timestamp = datetime.now().strftime("%B %d, %Y at %H:%M")

    risk_color = {"HIGH": "#e53e3e", "MEDIUM": "#dd6b20", "LOW": "#38a169"}.get(risk_level, "#718096")
    risk_bg    = {"HIGH": "#fff5f5", "MEDIUM": "#fffaf0", "LOW": "#f0fff4"}.get(risk_level, "#f7fafc")

    def leak_rows():
        if not leaks:
            return '<tr><td colspan="4" style="text-align:center;color:#718096;padding:24px;">No potential leaks detected</td></tr>'
        rows = ""
        for i, leak in enumerate(leaks, 1):
            ep = leak.get("endpoint") or "—"
            ep_display = f'<a href="{ep}" style="color:#3182ce;word-break:break-all;">{ep}</a>' if ep != "—" else "—"
            rows += f"""
            <tr style="background:{'#fafafa' if i % 2 == 0 else '#fff'};">
                <td style="padding:10px 14px;border-bottom:1px solid #edf2f7;font-family:monospace;font-size:13px;color:#e53e3e;">{leak['source']}</td>
                <td style="padding:10px 14px;border-bottom:1px solid #edf2f7;font-family:monospace;font-size:13px;color:#dd6b20;">{leak['sink']}</td>
                <td style="padding:10px 14px;border-bottom:1px solid #edf2f7;font-size:13px;">{ep_display}</td>
                <td style="padding:10px 14px;border-bottom:1px solid #edf2f7;font-size:13px;color:#4a5568;">{leak['file']}</td>
            </tr>"""
        return rows

    def pill_list(items, color):
        if not items:
            return '<span style="color:#a0aec0;font-size:14px;">None found</span>'
        return "".join(
            f'<span style="display:inline-block;background:{color}15;color:{color};border:1px solid {color}40;'
            f'border-radius:4px;padding:3px 10px;margin:3px;font-size:13px;font-family:monospace;">{item}</span>'
            for item in items
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Leak Report — {app_name}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'IBM Plex Sans', sans-serif;
      background: #f0f4f8;
      color: #1a202c;
      min-height: 100vh;
    }}
    .header {{
      background: #1a202c;
      color: #fff;
      padding: 36px 48px;
      border-bottom: 4px solid {risk_color};
    }}
    .header h1 {{
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.3px;
      margin-bottom: 4px;
    }}
    .header .subtitle {{
      font-size: 13px;
      color: #a0aec0;
      font-family: 'IBM Plex Mono', monospace;
    }}
    .risk-badge {{
      display: inline-block;
      background: {risk_color};
      color: #fff;
      font-family: 'IBM Plex Mono', monospace;
      font-weight: 600;
      font-size: 13px;
      padding: 4px 14px;
      border-radius: 3px;
      margin-top: 12px;
      letter-spacing: 1px;
    }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 36px 24px; }}
    .grid-top {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 16px; margin-bottom: 28px; }}
    .stat-card {{
      background: #fff;
      border-radius: 8px;
      padding: 20px 24px;
      border-top: 3px solid {risk_color};
      box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    }}
    .stat-card .num {{
      font-size: 36px;
      font-weight: 700;
      font-family: 'IBM Plex Mono', monospace;
      color: {risk_color};
    }}
    .stat-card .label {{
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #718096;
      margin-top: 2px;
    }}
    .card {{
      background: #fff;
      border-radius: 8px;
      padding: 24px 28px;
      margin-bottom: 20px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    }}
    .card h2 {{
      font-size: 14px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: #718096;
      margin-bottom: 16px;
      padding-bottom: 10px;
      border-bottom: 1px solid #edf2f7;
    }}
    table {{ width: 100%; border-collapse: collapse; }}
    th {{
      text-align: left;
      padding: 10px 14px;
      background: #f7fafc;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #718096;
      border-bottom: 2px solid #edf2f7;
    }}
    .risk-summary {{
      background: {risk_bg};
      border: 2px solid {risk_color}40;
      border-radius: 8px;
      padding: 20px 28px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 24px;
    }}
    .risk-summary .big {{
      font-size: 48px;
      font-weight: 700;
      font-family: 'IBM Plex Mono', monospace;
      color: {risk_color};
      line-height: 1;
    }}
    .risk-summary .detail {{ flex: 1; }}
    .risk-summary .detail h3 {{ font-size: 18px; color: {risk_color}; margin-bottom: 4px; }}
    .risk-summary .detail p {{ font-size: 14px; color: #4a5568; line-height: 1.6; }}
    footer {{
      text-align: center;
      font-size: 12px;
      color: #a0aec0;
      padding: 24px;
      font-family: 'IBM Plex Mono', monospace;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>Android Privacy Leak Analysis</h1>
    <div class="subtitle">Target: {app_name} &nbsp;·&nbsp; Generated: {timestamp}</div>
    <div class="risk-badge">RISK: {risk_level}</div>
  </div>

  <div class="container">

    <div class="grid-top">
      <div class="stat-card">
        <div class="num">{files_scanned:,}</div>
        <div class="label">Files Scanned</div>
      </div>
      <div class="stat-card">
        <div class="num">{len(leaks)}</div>
        <div class="label">Potential Leaks</div>
      </div>
      <div class="stat-card">
        <div class="num">{len(third_party)}</div>
        <div class="label">3rd-Party Libraries</div>
      </div>
      <div class="stat-card">
        <div class="num">{len(permissions)}</div>
        <div class="label">Permissions Requested</div>
      </div>
    </div>

    <div class="risk-summary">
      <div class="big">{risk_score}</div>
      <div class="detail">
        <h3>Risk Level: {risk_level}</h3>
        <p>Score is calculated based on the number of source/sink co-occurrences,
           presence of external network endpoints, and embedded third-party tracking libraries.</p>
      </div>
    </div>

    <div class="card">
      <h2>Potential Privacy Leaks</h2>
      <table>
        <thead>
          <tr>
            <th>Sensitive Source</th>
            <th>Data Sink</th>
            <th>Suspected Endpoint</th>
            <th>File</th>
          </tr>
        </thead>
        <tbody>
          {leak_rows()}
        </tbody>
      </table>
    </div>

    <div class="card">
      <h2>Third-Party Libraries Detected</h2>
      {pill_list(third_party, "#6b46c1")}
    </div>

    <div class="card">
      <h2>Permissions Requested (AndroidManifest.xml)</h2>
      {pill_list(permissions, "#2b6cb0")}
    </div>

  </div>

  <footer>
    CIS 5370 · Project 2 – Medical Android App Data Leakage Analysis · FIU
  </footer>
</body>
</html>"""

    with open(output_file, "w") as f:
        f.write(html)
    print(f"HTML report saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 report_html.py report.json output.html")
        sys.exit(1)
    with open(sys.argv[1]) as f:
        report_data = json.load(f)
    generate_html_report(report_data, sys.argv[2])
