from raspal.compliance import ComplianceChecker, check_compliance


def test_compliance_checker_imports():
    checker = ComplianceChecker()
    assert checker is not None


def test_check_compliance_returns_dict():
    result = check_compliance("https://example.com")
    assert isinstance(result, dict)
    assert "signals" in result or "warnings" in result
