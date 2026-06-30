import json
from pathlib import Path
from datetime import datetime

PROFILE_FILE = Path("profile/research_profile.json")
REPORTS = Path("reports")
REPORTS.mkdir(exist_ok=True)

CONNECTOR_STATUS = {
    "Consensus": "manual/export needed",
    "OpenAlex": "public API possible",
    "Crossref": "public API possible",
    "Semantic Scholar": "API possible",
    "RBI": "website/source connector needed",
    "SEBI": "website/source connector needed",
    "NITI Aayog": "website/source connector needed",
    "IMF": "public data/API possible",
    "World Bank": "public data/API possible",
    "OECD": "public data/API possible",
    "BIS": "website/source connector needed",
    "CMIE Data": "subscription/manual export likely",
    "Government Reports": "source-specific connector needed",
    "Annual Reports": "company/source-specific connector needed",
    "Peer Reviewed Journals": "metadata connector needed"
}

def load_profile():
    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def flatten_domains(domain_groups):
    domains = []
    for group, items in domain_groups.items():
        for item in items:
            domains.append({
                "group": group.replace("_", " "),
                "domain": item
            })
    return domains

def build_discovery_plan(profile):
    domains = flatten_domains(profile["research_domains"])
    sources = []

    sources.extend(profile.get("literature_sources", []))
    sources.extend(profile.get("data_sources", []))

    institutional = profile.get("institutional_sources", {})
    for group, institutions in institutional.items():
        for item in institutions:
            sources.append(item["short_name"])

    discovery_plan = []

    for domain in domains:
        for source in sources:
            discovery_plan.append({
                "domain_group": domain["group"],
                "domain": domain["domain"],
                "source": source,
                "status": CONNECTOR_STATUS.get(source, "connector not yet defined")
            })

    return discovery_plan

def write_report(discovery_plan):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = REPORTS / f"scout-discovery-plan-{timestamp}.md"

    with open(report_file, "w", encoding="utf-8") as file:
        file.write("# AROS Scout Discovery Plan\n\n")
        file.write(f"Generated: {datetime.now()}\n\n")
        file.write("## Summary\n\n")
        file.write(f"- Total discovery routes: {len(discovery_plan)}\n\n")
        file.write("## Discovery Routes\n\n")
        file.write("| Domain Group | Domain | Source | Status |\n")
        file.write("|---|---|---|---|\n")

        for item in discovery_plan:
            file.write(
                f"| {item['domain_group']} | {item['domain']} | "
                f"{item['source']} | {item['status']} |\n"
            )

    return report_file

def main():
    print("=" * 70)
    print("AROS SCOUT - DISCOVERY ENGINE FOUNDATION")
    print("=" * 70)

    profile = load_profile()
    plan = build_discovery_plan(profile)
    report_file = write_report(plan)

    unique_sources = sorted(set(item["source"] for item in plan))
    unique_domains = sorted(set(item["domain"] for item in plan))

    print()
    print("Research domains loaded :", len(unique_domains))
    print("Discovery sources loaded:", len(unique_sources))
    print("Discovery routes created:", len(plan))

    print()
    print("Sources")
    print("-------")
    for source in unique_sources:
        print("•", source)

    print()
    print("Report saved:")
    print(report_file)

    print()
    print("Status")
    print("------")
    print("✓ Scout foundation created.")
    print("✓ No external search performed yet.")
    print("✓ No files downloaded.")
    print("✓ Ready for connector development.")

if __name__ == "__main__":
    main()
