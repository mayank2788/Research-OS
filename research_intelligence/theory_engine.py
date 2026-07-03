class TheoryIntelligenceEngine:
    """
    AROS Theory Intelligence Engine v1.

    Detects theory signals from explicit theory names
    and conceptual indicators.
    """

    def detect(self, text):
        theory_signals = {
            "Agency Theory": [
                "agency theory",
                "principal agent",
                "principal-agent",
                "monitoring",
                "board independence",
                "ownership conflict",
                "information asymmetry",
                "managerial opportunism"
            ],
            "Stakeholder Theory": [
                "stakeholder theory",
                "stakeholders",
                "csr",
                "corporate social responsibility",
                "esg",
                "sustainability"
            ],
            "Resource Dependency Theory": [
                "resource dependency",
                "external resources",
                "board resources",
                "network resources"
            ],
            "Resource Based View": [
                "resource based view",
                "rbv",
                "capabilities",
                "competitive advantage",
                "firm resources"
            ],
            "Institutional Theory": [
                "institutional theory",
                "regulation",
                "policy pressure",
                "institutional pressure",
                "compliance",
                "legitimacy"
            ],
            "Pecking Order Theory": [
                "pecking order",
                "internal financing",
                "information asymmetry",
                "financing hierarchy"
            ],
            "Trade Off Theory": [
                "trade off theory",
                "tax shield",
                "bankruptcy cost",
                "optimal capital structure"
            ],
            "Positive Accounting Theory": [
                "positive accounting theory",
                "earnings management",
                "accounting choice",
                "managerial discretion"
            ]
        }

        detected = []

        for theory, signals in theory_signals.items():
            for signal in signals:
                if signal in text:
                    detected.append(theory)
                    break

        return sorted(set(detected))
