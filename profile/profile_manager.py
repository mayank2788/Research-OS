import json
from pathlib import Path

PROFILE_FILE = Path("profile/research_profile.json")

def load_profile():
    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def print_list(items):
    for item in items:
        print("•", item)

def print_institutions(title, institutions):
    print()
    print(title)
    print("-" * len(title))
    for item in institutions:
        print(f"• {item['short_name']} - {item['name']}")

def display_profile():
    profile = load_profile()

    print("=" * 70)
    print("AROS RESEARCH PROFILE")
    print("=" * 70)

    print()
    print("Researcher")
    print("----------")
    print("Name :", profile["researcher"]["name"])
    print("Role :", profile["researcher"]["role"])

    print()
    print("Research Domains")
    print("----------------")
    for group, domains in profile["research_domains"].items():
        print()
        print(group.replace("_", " "))
        print("-" * len(group))
        print_list(domains)

    print()
    print("Literature Sources")
    print("------------------")
    print_list(profile["literature_sources"])

    print()
    print("Institutional Sources")
    print("---------------------")
    institutional = profile["institutional_sources"]

    print_institutions(
        "Central Banking and Regulators",
        institutional["central_banking_and_regulators"]
    )

    print_institutions(
        "Government and Policy",
        institutional["government_and_policy"]
    )

    print_institutions(
        "Professional Bodies",
        institutional["professional_bodies"]
    )

    print_institutions(
        "International Institutions",
        institutional["international_institutions"]
    )

    print()
    print("Data Sources")
    print("------------")
    print_list(profile["data_sources"])

    print()
    print("Document Types")
    print("--------------")
    print_list(profile["document_types"])

if __name__ == "__main__":
    display_profile()
