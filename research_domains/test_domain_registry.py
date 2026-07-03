import json

with open(
    "research_domains/domain_registry.json"
) as f:

    data=json.load(f)


print("="*70)
print("AROS RESEARCH DOMAIN REGISTRY TEST")
print("="*70)

print(
    "Domains:",
    len(data["domains"])
)


for domain in data["domains"]:

    print()
    print(domain["name"])
    print("-"*40)

    for area in domain["areas"][:5]:
        print("-", area)


print()
print("✓ Research Domain Registry operational")

