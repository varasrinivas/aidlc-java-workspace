#!/usr/bin/env python3
"""
Export one Rally feature and its user stories to a Markdown file that AI-DLC can read.

AI-DLC reads only files inside the workspace, so the team snapshots the feature before
`/aidlc` and commits the snapshot with the run's record: the record then points at the exact
version of the stories that were approved, not at a live item that may change tomorrow.

    # offline: render a saved WSAPI response (how the course file was produced)
    python scripts/export-rally.py --from-json docs-in/rally/F1187.json --out docs-in/rally/F1187-reviewer-queue-filters.md

    # live: query Rally with a read-only API key (RALLY_API_KEY), save the raw JSON too
    python scripts/export-rally.py --feature F1187 --save-json docs-in/rally/F1187.json --out docs-in/rally/F1187-reviewer-queue-filters.md

Live mode follows Rally's documented Web Services API v2.0 (base URL, `zsessionid` header,
`query`/`fetch`/`order`/`pagesize`), but it has NOT been run against a Rally subscription for
this course. Check the acceptance-criteria field name in your workspace: Rally has no standard
one, so it is a custom `c_` field (default here: c_AcceptanceCriteria; --ac-field to change).

Standard library only. Python 3.9+.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

DEFAULT_URL = "https://rally1.rallydev.com/slm/webservice/v2.0"
FEATURE_FIELDS = "FormattedID,Name,Description,State,Parent,Owner,Release,LastUpdateDate"
STORY_FIELDS = "FormattedID,Name,Description,ScheduleState,PlanEstimate,Owner,PortfolioItem"


class HtmlToMarkdown(HTMLParser):
    """Rally rich-text fields are HTML; keep paragraphs, lists, bold and code, drop the rest."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.out.append("\n- ")
        elif tag in ("b", "strong"):
            self.out.append("**")
        elif tag == "code":
            self.out.append("`")
        elif tag == "br":
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("p", "ul", "ol", "div"):
            self.out.append("\n\n")
        elif tag in ("b", "strong"):
            self.out.append("**")
        elif tag == "code":
            self.out.append("`")

    def handle_data(self, data):
        self.out.append(data)


def md(html_text):
    parser = HtmlToMarkdown()
    parser.feed(html_text or "")
    lines = [line.rstrip() for line in "".join(parser.out).split("\n")]
    text = "\n".join(lines)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip()


def ref_name(value):
    """A WSAPI reference is an object; show its FormattedID and name when present."""
    if not value:
        return ""
    if isinstance(value, str):
        return value
    fid, name = value.get("FormattedID"), value.get("_refObjectName")
    return f"{fid} {name}".strip() if fid and name else (fid or name or "")


def results(response, what):
    qr = response.get("QueryResult", {})
    if qr.get("Errors"):
        sys.exit(f"Rally returned errors for {what}: {qr['Errors']}")
    return qr.get("Results", [])


def get(base, path, params, key):
    url = f"{base}/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"zsessionid": key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        hint = " Check RALLY_API_KEY (Rally keys start with an underscore)." if e.code in (401, 403) else ""
        sys.exit(f"Rally answered {e.code} {e.reason} for {path}.{hint}")
    except urllib.error.URLError as e:
        sys.exit(f"Cannot reach Rally at {base}: {e.reason}. Check RALLY_URL and your network.")


def fetch_live(feature_id, ac_field):
    key = os.environ.get("RALLY_API_KEY")
    if not key:
        sys.exit("RALLY_API_KEY is not set. Create a read-only API key in Rally and export it; never commit it.")
    base = os.environ.get("RALLY_URL", DEFAULT_URL).rstrip("/")
    feature = get(base, "portfolioitem/feature",
                  {"query": f'(FormattedID = "{feature_id}")', "fetch": FEATURE_FIELDS}, key)
    stories = get(base, "hierarchicalrequirement",
                  {"query": f'(PortfolioItem.FormattedID = "{feature_id}")',
                   "fetch": f"{STORY_FIELDS},{ac_field}", "order": "FormattedID", "pagesize": 200}, key)
    return {"feature": feature, "stories": stories}


def render(data, ac_field, source):
    features = results(data["feature"], "the feature")
    if len(features) != 1:
        sys.exit(f"expected exactly one feature, got {len(features)}")
    f = features[0]
    stories = sorted(results(data["stories"], "the stories"), key=lambda s: s["FormattedID"])

    out = [f"# {f['FormattedID']} {f['Name']}", ""]
    out.append(f"> Snapshot of a Rally feature and its user stories, written by `scripts/export-rally.py` ({source}).")
    out.append("> Rally is the source of truth: refresh this file before `/aidlc`, and cite the story IDs (US…) in requirements.")
    out.append("")
    out += ["| Field | Value |", "|---|---|"]
    for label, value in [("Epic", ref_name(f.get("Parent"))), ("State", ref_name(f.get("State"))),
                         ("Owner", ref_name(f.get("Owner"))), ("Release", ref_name(f.get("Release"))),
                         ("Last updated in Rally", (f.get("LastUpdateDate") or "")[:10]),
                         ("Stories", str(len(stories)))]:
        if value:
            out.append(f"| {label} | {value} |")
    out += ["", "## Feature description", "", md(f.get("Description")), "", "## User stories", ""]
    for s in stories:
        estimate = s.get("PlanEstimate")
        estimate = f"{estimate:g}" if isinstance(estimate, (int, float)) else "—"
        out += [f"### {s['FormattedID']} {s['Name']}", ""]
        out.append(f"Schedule state: {s.get('ScheduleState', '—')} · Estimate: {estimate} · Owner: {ref_name(s.get('Owner')) or '—'}")
        out += ["", md(s.get("Description")), "", "**Acceptance criteria**", ""]
        criteria = md(s.get(ac_field))
        out.append(criteria if criteria else f"(none: the `{ac_field}` field is empty or missing)")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Export a Rally feature and its user stories to Markdown.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--feature", help="FormattedID of the feature to fetch live, e.g. F1187")
    src.add_argument("--from-json", type=Path, help="render a saved response instead of calling Rally")
    ap.add_argument("--ac-field", default="c_AcceptanceCriteria", help="custom field that holds acceptance criteria")
    ap.add_argument("--out", type=Path, help="Markdown file to write (default: print)")
    ap.add_argument("--save-json", type=Path, help="live mode: also save the raw responses here")
    args = ap.parse_args()

    if args.from_json:
        data = json.loads(args.from_json.read_text(encoding="utf-8"))
        source = f"offline, from {args.from_json.name}"
    else:
        data = fetch_live(args.feature, args.ac_field)
        source = "live, Rally WSAPI v2.0"
        if args.save_json:
            args.save_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    text = render(data, args.ac_field, source)
    if args.out:
        args.out.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {args.out} ({text.count(chr(10))} lines)")
    else:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
