def get_grade_point(letter_grade):
    """
    Returns the numeric grade point for a given letter grade.
    Returns None if the grade is invalid.
    """
    grade_map = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
    }
    return grade_map.get(letter_grade.upper())

def save_to_file(gpa, total_credits, total_quality_points):
    """
    Saves the final calculation to a text file.
    """
    try:
        with open('semester_result.txt', 'a') as file:
            file.write(f"Total Credits: {total_credits}\n")
            file.write(f"Total Quality Points: {total_quality_points}\n")
            file.write(f"Final GPA: {gpa:.2f}\n")
            file.write("-" * 20 + "\n")
        print("Result saved to 'semester_result.txt'.")
    except Exception as e:
        print(f"Failed to save result: {e}")

def main():
    print("Welcome to the University CGPA Calculator!")
    print("-" * 42)
    
    # Get the number of courses
    while True:
        try:
            num_courses = int(input("How many courses did you offer this semester? "))
            if num_courses > 0:
                break
            else:
                print("Please enter a valid number of courses (greater than 0).")
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
    total_credit_units = 0
    total_quality_points = 0
    
    # Loop through each course
    for i in range(num_courses):
        print(f"\n--- Course {i + 1} ---")
        
        # Get credit unit
        while True:
            try:
                credit_unit = int(input("Enter Credit Unit (e.g., 3): "))
                if credit_unit > 0:
                    break
                else:
                    print("Credit unit must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a valid number for credit unit.")
                
        # Get letter grade
        while True:
            letter_grade = input("Enter Letter Grade (A, B, C, D, E, F): ").strip()
            grade_point = get_grade_point(letter_grade)
            
            if grade_point is not None:
                break
            else:
                print("Invalid letter grade. Please enter A, B, C, D, E, or F.")
                
        # Calculate quality points for this course
        quality_points = credit_unit * grade_point
        
        # Keep running total
        total_credit_units += credit_unit
        total_quality_points += quality_points
        
    # Calculate and display the final GPA
    if total_credit_units > 0:
        gpa = total_quality_points / total_credit_units
        print("\n" + "=" * 42)
        print(f"Total Credit Units: {total_credit_units}")
        print(f"Total Quality Points: {total_quality_points}")
        print(f"Final GPA: {gpa:.2f}")
        print("=" * 42)
        
        # Bonus challenge: Save to file
        save_to_file(gpa, total_credit_units, total_quality_points)
    else:
        print("\nNo valid credit units entered. Cannot calculate GPA.")

if __name__ == "__main__":
    main()