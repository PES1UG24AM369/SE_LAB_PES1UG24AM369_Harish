from string import ascii_letters

from hypothesis import given, strategies as st

from gym_membership import average_workout, calculate_bmi, parse_plan


unexpected_types = st.one_of(
    st.none(), st.integers(), st.binary(), st.lists(st.integers(), max_size=5)
)
letters = st.text(alphabet=ascii_letters, min_size=1, max_size=20)


@given(plan=letters, months=st.integers(min_value=1, max_value=120))
def test_parse_plan_valid(plan, months):
    assert parse_plan(f"{plan}-{months}") == (plan.upper(), months)


@given(
    code=st.one_of(
        st.sampled_from(["", " ", "-12", " -12", "GOLD-0", "GOLD--1", "GOLD-12-3"]),
        letters,
        letters.map(lambda plan: f"{plan}-abc"),
        unexpected_types,
    )
)
def test_parse_plan_no_crash(code):
    assert parse_plan(code) is None


@given(
    weight=st.integers(min_value=30, max_value=300),
    height_cm=st.integers(min_value=100, max_value=250),
)
def test_calculate_bmi_valid(weight, height_cm):
    height = height_cm / 100
    assert calculate_bmi(f"{weight},{height}") == round(weight / height**2, 1)


@given(
    data=st.one_of(
        st.sampled_from([
            "70,0", "", " ", "70", "70,", "70,1.75,2", "70,-1.75",
            "0,1.75", "-70,1.75", "nan,1.75", "70,inf", "70,1e-300", "70,1e300",
        ]),
        letters.map(lambda weight: f"{weight}!,1.75"),
        unexpected_types,
    )
)
def test_calculate_bmi_no_crash(data):
    assert calculate_bmi(data) is None


@given(values=st.lists(st.integers(min_value=0, max_value=600), min_size=1))
def test_average_workout_valid(values):
    minutes = " \t ".join(str(value) for value in values)
    assert average_workout(f"  {minutes}  ") == sum(values) // len(values)


@given(
    minutes=st.one_of(
        st.sampled_from(["", " \t ", "30 -5", "3.5", "30,45"]),
        letters.map(lambda token: f"30 {token}"),
        unexpected_types,
    )
)
def test_average_workout_no_crash(minutes):
    assert average_workout(minutes) is None
