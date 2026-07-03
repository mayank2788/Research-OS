class ResearchIntentFilter:
    """
    AROS Research Intent Filter v1.

    Purpose:
    Keep literature aligned with the real research intent,
    not only broad keywords.
    """

    def score(self, paper, intent):
        text = " ".join([
            paper.title or "",
            paper.abstract or "",
        ]).lower()

        must_have = intent.get("must_have", [])
        preferred = intent.get("preferred", [])
        exclude = intent.get("exclude", [])

        excluded_terms = [
            term for term in exclude
            if term.lower() in text
        ]

        if excluded_terms:
            return {
                "intent_score": 0,
                "intent_label": "Rejected",
                "matched_must_have": [],
                "matched_preferred": [],
                "excluded_terms": excluded_terms,
                "decision": "Reject"
            }

        matched_must = [
            term for term in must_have
            if term.lower() in text
        ]

        matched_preferred = [
            term for term in preferred
            if term.lower() in text
        ]

        score = 0

        if must_have:
            score += (len(matched_must) / len(must_have)) * 7

        if preferred:
            score += (len(matched_preferred) / len(preferred)) * 3

        score = round(score, 2)

        if score >= 6:
            label = "Strong Match"
            decision = "Keep"
        elif score >= 3:
            label = "Possible Match"
            decision = "Review"
        else:
            label = "Weak Match"
            decision = "Reject"

        return {
            "intent_score": score,
            "intent_label": label,
            "matched_must_have": matched_must,
            "matched_preferred": matched_preferred,
            "excluded_terms": excluded_terms,
            "decision": decision
        }
