
import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ==========================================
# MEMBERSHIP COST - BRANCH TESTING
# ==========================================

# Test 1: Valid membership plan
def test_valid_plan():
    assert membership_cost("monthly", 30, False, False) == 1500


# Test 2: Invalid membership plan
def test_invalid_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 30, False, False)


# Test 3: Age below minimum limit
def test_age_below_14():
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)


# Test 4: Age exactly 14
def test_age_exactly_14():
    assert membership_cost("monthly", 14, False, False) == 1500


# Test 5: Senior citizen discount
def test_senior_discount():
    assert membership_cost("monthly", 60, False, False) == 1125


# Test 6: Non-senior student discount
def test_student_discount():
    assert membership_cost("monthly", 25, True, False) == 1350


# Test 7: Non-senior non-student
def test_regular_member():
    assert membership_cost("monthly", 30, False, False) == 1500


# Test 8: Trainer included
def test_with_trainer():
    assert membership_cost("monthly", 30, False, True) == 3500


# Test 9: Trainer not included
def test_without_trainer():
    assert membership_cost("monthly", 30, False, False) == 1500


# Test 10: Yearly plan with trainer
def test_yearly_trainer_discount():
    assert membership_cost("yearly", 30, False, True) == 13500


# Test 11: Non-yearly plan with trainer
def test_quarterly_trainer():
    assert membership_cost("quarterly", 30, False, True) == 6000


# ==========================================
# GYM ENTRY - BRANCH TESTING
# ==========================================

# Test 12: Inactive membership
def test_inactive_membership():
    assert can_enter(10, False, False, "M") is False


# Test 13: Entry before opening time
def test_before_opening():
    assert can_enter(4, True, False, "M") is False


# Test 14: Entry after closing time
def test_after_closing():
    assert can_enter(23, True, False, "M") is False


# Test 15: Entry at opening time
def test_at_opening_time():
    assert can_enter(5, True, False, "M") is True


# Test 16: Entry at closing time
def test_at_closing_time():
    assert can_enter(22, True, False, "M") is True


# Test 17: Women-only slot with female member
def test_women_only_female():
    assert can_enter(10, True, True, "F") is True


# Test 18: Women-only slot with male member
def test_women_only_male():
    assert can_enter(10, True, True, "M") is False


# Test 19: Regular slot
def test_regular_slot():
    assert can_enter(10, True, False, "M") is True


# ==========================================
# BMI CATEGORY - BRANCH TESTING
# ==========================================

# Test 20: Invalid height
def test_invalid_height():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(60, 0)


# Test 21: Negative height
def test_negative_height():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(60, -1)


# Test 22: Underweight category
def test_underweight():
    assert bmi_category(45, 1.70) == "underweight"


# Test 23: Normal category
def test_normal():
    assert bmi_category(65, 1.70) == "normal"


# Test 24: Overweight category
def test_overweight():
    assert bmi_category(80, 1.70) == "overweight"


# Test 25: Obese category
def test_obese():
    assert bmi_category(100, 1.70) == "obese"


# Test 26: BMI exactly 18.5
def test_bmi_boundary_18_5():
    assert bmi_category(18.5, 1.0) == "normal"


# Test 27: BMI exactly 25
def test_bmi_boundary_25():
    assert bmi_category(25, 1.0) == "overweight"


# Test 28: BMI exactly 30
def test_bmi_boundary_30():
    assert bmi_category(30, 1.0) == "obese"
