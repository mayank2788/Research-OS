from research_intelligence.domain_router import DomainRouter


router = DomainRouter()

topic = (
    "Impact of Ind AS 23 Borrowing Cost Capitalisation "
    "on Earnings Management and Financial Reporting Quality"
)

result = router.route(topic)

print("=" * 70)
print("AROS DOMAIN ROUTER TEST")
print("=" * 70)

print("Topic:", result["topic"])

print()
print("Domains:", result["domains"])

print()
print("Sources:", result["sources"])

print()
print("Ranking Priority:", result["ranking_priority"])

print()
print("✓ Domain Router operational")
