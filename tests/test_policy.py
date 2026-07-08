def classify(score):
    if score >= 85:
        return "accepted", 10000
    if score >= 65:
        return "revision", 5000
    if score >= 40:
        return "disputed", 2500
    return "rejected", 0


def score_evidence(evidence):
    score = 0
    score += 25 if evidence.get("contract") else 0
    score += 20 if evidence.get("tests") else 0
    score += 20 if evidence.get("frontend") else 0
    score += 20 if evidence.get("deployment_steps") else 0
    score += 15 if evidence.get("screenshots_or_logs") else 0
    return score


def test_complete_milestone_is_accepted():
    evidence = {
        "contract": True,
        "tests": True,
        "frontend": True,
        "deployment_steps": True,
        "screenshots_or_logs": True,
    }
    assert score_evidence(evidence) == 100
    assert classify(100) == ("accepted", 10000)


def test_missing_tests_requires_revision():
    evidence = {
        "contract": True,
        "tests": False,
        "frontend": True,
        "deployment_steps": True,
        "screenshots_or_logs": True,
    }
    assert score_evidence(evidence) == 80
    assert classify(80) == ("revision", 5000)


def test_thin_demo_is_rejected_or_disputed():
    evidence = {
        "contract": True,
        "tests": False,
        "frontend": False,
        "deployment_steps": False,
        "screenshots_or_logs": False,
    }
    assert score_evidence(evidence) == 25
    assert classify(25) == ("rejected", 0)


if __name__ == "__main__":
    test_complete_milestone_is_accepted()
    test_missing_tests_requires_revision()
    test_thin_demo_is_rejected_or_disputed()
    print("policy tests passed")
