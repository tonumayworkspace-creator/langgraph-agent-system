def validator_agent(results: list) -> str:
    """
    Simple validation logic:
    - If all expected steps executed → SUCCESS
    - Else → FAILED
    """

    expected_keywords = ["loaded", "analysis", "report"]

    results_text = " ".join(results).lower()

    for keyword in expected_keywords:
        if keyword not in results_text:
            return "FAILED"

    return "SUCCESS"