from research_intelligence.gap_analyzer import ResearchGapAnalyzer


matrix = [

    {
        "domains": [
            "Finance",
            "Corporate Governance"
        ],

        "theories": [
            "Agency Theory"
        ],

        "methodology": [
            "Regression Analysis"
        ],

        "variables_constructs": [
            "performance",
            "governance"
        ],
    },


    {
        "domains": [
            "Finance"
        ],

        "theories": [
            "Agency Theory"
        ],

        "methodology": [
            "Panel Data Analysis"
        ],

        "variables_constructs": [
            "leverage"
        ],
    }

]


analyzer = ResearchGapAnalyzer()

result = analyzer.analyze(matrix)


print("="*70)
print("AROS RESEARCH GAP ANALYZER TEST")
print("="*70)


for key,value in result.items():

    print()
    print(key)
    print(value)


print()
print("✓ Research Gap Analyzer operational")

