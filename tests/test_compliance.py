from raspal.compliance import ComplianceChecker, check_compliance


def test_compliance_checker_imports():
    checker = ComplianceChecker()
    assert checker is not None


def test_check_compliance_returns_dict():
    result = check_compliance("https://example.com")
    assert isinstance(result, dict)
    assert "signals" in result
    assert "warnings" in result


def test_check_compliance_invalid_url():
    result = check_compliance("not-a-url")
    assert result.get("valid") is False
    assert len(result.get("warnings", [])) > 0


def test_compliance_checker_can_fetch():
    """can_fetch returns a tuple (bool, str) without network for unknown domains."""
    checker = ComplianceChecker()
    allowed, reason = checker.can_fetch("https://thisshouldnotexist.invalid")
    # Should return True with a warning (not crash)
    assert isinstance(allowed, bool)
    assert isinstance(reason, str)
