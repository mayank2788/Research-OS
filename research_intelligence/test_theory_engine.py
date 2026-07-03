from research_intelligence.theory_engine import TheoryIntelligenceEngine


engine = TheoryIntelligenceEngine()

samples = [
    "Board independence and monitoring reduce managerial opportunism.",
    "ESG and CSR disclosure improve stakeholder confidence.",
    "Tax shield and bankruptcy cost determine optimal capital structure.",
    "Earnings management reflects accounting choice and managerial discretion.",
]

print("=" * 70)
print("AROS THEORY INTELLIGENCE ENGINE TEST")
print("=" * 70)

for sample in samples:
    print()
    print("Text:", sample)
    print("Detected:", engine.detect(sample.lower()))

print()
print("✓ Theory Intelligence Engine operational")
