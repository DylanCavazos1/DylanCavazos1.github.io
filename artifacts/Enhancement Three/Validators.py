# validators.py


def get_valid_menu_choice():
    """
    Prompts the user to enter a valid menu choice between 1 and 7. 
    Limits number of invalid attempts to 4 before exiting the program.
    """
    max_attempts = 4 # Max number of attempts allowed
    attempts = 0 # counter for failed attempts
    while attempts < max_attempts:
        choice = input("\nEnter your choice: ").strip()

        # Check if the input is a digit and within the valid set of choices
        if choice.isdigit() and choice in {"1","2","3","4","5","6","7","8","9","10"}:
            return choice
        else:
            attempts += 1
            print(f"Invalid input. You have {max_attempts - attempts} attempts remaining.")
    # if too many invalid attempts, exit the program
    print("Too many attempts. Exiting program.")
    exit() 


def is_valid_course_id(course_id):
    """
    Checks that user enters a valid course ID for add_course()
    """
    # Course ID must be exactly 7 characters: 4 letters + 3 digits (ex. "CSCI100")
    if len(course_id) != 7:
        return False
    # String slicing:  https://www.w3schools.com/python/python_strings_slicing.asp
    ID_alpha = course_id[:4] # Extracts the first 4 characters, which should be letters
    ID_digit = course_id[4:] # Extracts the last 3 characters, which should be digits
    return ID_alpha.isalpha() and ID_digit.isdigit()


def get_valid_prerequisites(bst, current_course_id=None):
    """
    Checks that user enters valid prerequisites for add_course() and update_course()
    """
    # Requests user to enter comma-separated prerequisites 
    prereqs_input = input("Enter prerequisites (separate multiples with commas, otherwise leave blank): ").strip()
    # Inputs into a list, forces uppercase and removes extra spaces
    prereqs_format = [p.strip().upper() for p in prereqs_input.split(",")] if prereqs_input else []

    valid_list = []
    # makes current_course_id uppercase for comparison below
    if current_course_id:
        current_course_id = current_course_id.strip().upper()

    # Validates each prerequisite in the list
    for p in prereqs_format:
        # Ignore any blanks or 'N/A'
        if p == "" or p == "N/A":
            continue

        # Prevents a course being its own prerequisite
        if current_course_id and p == current_course_id:
            print(f"DEBUG: Comparing prerequisite {p} to current course {current_course_id}")
            print(f"Course {p} cannot be a prerequisite of itself.")
            return None

        # Checks if course ID is a valid format. 4 letters + 3 digits (ex."CSCI100")
        if not is_valid_course_id(p):
            print(f"Invalid format: {p}. Must be 4 letters followed by 3 digits.")
            return None

        # Ensures the course exists in the current BST
        if not bst.search(p):
            print(f"Course {p} not found in system. Please enter existing course.")
            return None

        # Prevents duplication
        if p in valid_list:
            print(f"Duplicate prerequisite detected: {p}")
            print("Update not successful. Returning to Menu.")
            return None

        # Check for same department higher-level course
        if  p[:4] == current_course_id[:4]: # if course code for prereq and course ID match
            # Ensures that both course IDs are in valid format
            if is_valid_course_id(p) and is_valid_course_id(current_course_id): 
                    # Extracts the numeric portion of the course ID's
                    prereq_num = int(p[4:])
                    course_num = int(current_course_id[4:])
                    # If the prerequisite is a higher-level course, block it
                    if prereq_num > course_num:
                        print(f"{p} is a higher-level course than {current_course_id}. Cannot add as a prerequisite.")
                        return None

        # Appends the valid prerequisite into the list
        valid_list.append(p)

    # Ensures the returned list always 2 elements:
    # If valid_list has 1 item, adds one "n/a"
    # If valid_list is empty, adds two "n/a"
    # If valid_list has 2 items, nothing is added
    return valid_list + ["n/a"] * (2 - len(valid_list))