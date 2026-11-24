from math import isfinite


def parse_plan(code):
    if not isinstance(code, str):
        return None

    try:
        plan, months = code.split('-')
        months = int(months)
    except ValueError:
        return None

    if not plan.strip() or months <= 0:
        return None

    return plan.upper(), months

def calculate_bmi(data):
    if not isinstance(data, str):
        return None

    try:
        weight, height = data.split(',')
        weight = float(weight)
        height = float(height)
    except ValueError:
        return None

    if not isfinite(weight) or not isfinite(height) or weight <= 0 or height <= 0:
        return None

    try:
        height_squared = height ** 2
    except OverflowError:
        return None

    if height_squared == 0 or not isfinite(height_squared):
        return None

    bmi = weight / height_squared
    if not isfinite(bmi):
        return None

    return round(bmi, 1)

def average_workout(minutes):
    if not isinstance(minutes, str):
        return None

    try:
        values = [int(value) for value in minutes.split()]
    except ValueError:
        return None

    if not values or any(value < 0 for value in values):
        return None

    return sum(values) // len(values)

def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter a plan code (e.g. GOLD-12): ")
    result = parse_plan(user_input)
    if result is None:
        print("Invalid plan code. Enter a plan name and a positive number of months.")
    else:
        print("Plan and Months:", result)

    print("\n==== Running calculate_bmi ====")
    user_input = input("Enter weight and height (e.g. 70,1.75): ")
    result = calculate_bmi(user_input)
    if result is None:
        print("Invalid BMI input. Enter a positive weight and height separated by a comma.")
    else:
        print("BMI:", result)

    print("\n==== Running average_workout ====")
    user_input = input("Enter workout minutes separated by spaces (e.g. 45 60 30): ")
    result = average_workout(user_input)
    if result is None:
        print("Invalid workout minutes. Enter one or more non-negative whole numbers.")
    else:
        print("Average Minutes:", result)

if __name__ == "__main__":
    main()
