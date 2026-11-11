
import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# Membership cost tests

def test_invalid_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 25, False, False)


def test_underage_member():
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 12, False, False)


def test_senior_discount():
    assert membership_cost("monthly", 65, False, False) == 1125


def test_student_discount():
    assert membership_cost("monthly", 20, True, False) == 1350


def test_yearly_with_trainer():
    assert membership_cost("yearly", 30, False, True) == 13500


# Gym entry tests

def test_inactive_membership():
    assert can_enter(10, False, False, "M") is False


def test_outside_gym_hours():
    assert can_enter(23, True, False, "M") is False


def test_women_only_slot():
    assert can_enter(10, True, True, "F") is True


# BMI category tests

def test_invalid_height():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(60, 0)


def test_underweight():
    assert bmi_category(45, 1.70) == "underweight"


def test_normal_weight():
    assert bmi_category(65, 1.70) == "normal"


def test_overweight():
    assert bmi_category(80, 1.70) == "overweight"


def test_obese():
    assert bmi_category(100, 1.70) == "obese"

# Test 14: Normal gym slot allows entry
def test_regular_slot_allows_entry():
    assert can_enter(10, True, False, "M") is True