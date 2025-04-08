import csv
from Course import Course


def get_valid_menu_choice():
        max_attempts = 4
        attempts = 0
        # Terminate program after so many attempts
        while attempts < max_attempts:
            choice = input("\nEnter your choice: ").strip()

            if choice.isdigit() and choice in {"1","2","3","4","5","6","7"}:
                return choice
            else:
                attempts += 1
                print(f"Invalid input. You have {max_attempts - attempts} attempts remaining.")

        print("Too many attempts. Exiting program.")
        exit() # exit program

class CourseManager:
# create courseManager class    

    def __init__(self):
        self.courses = {}

    def load_courses(self, filename):
        # check that user enters csv filetype
        if not filename.lower().endswith(".csv"): # Found "endswith()" string method in https://www.w3schools.com/python/python_strings_methods.asp
            print("Invalid file type. Please provide a .csv file")
            return
        # Try block that opens file if successful
        try:
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                """
                https://www.geeksforgeeks.org/reading-csv-files-in-python/?ref=ml_lbp
                """
                csvFile = csv.DictReader(file) 

                # Check that file contains the required headers
                required_headers = {"course", "title", "prereq1", "prereq2"}
                if not required_headers.issubset(csvFile.fieldnames):
                    print("Error: CSV is missing one or more required headers: course, title, prereq1, prereq2")
                    return
                
                # iterate over courses
                for row in csvFile:
                    course_id = row["course"] # access values in keys
                    title = row["title"]
                    prerequisites = []

                    if "prereq1" in row and row["prereq1"]:
                        prerequisites.append(row["prereq1"])
                    if "prereq2" in row and row["prereq2"]:
                        prerequisites.append(row["prereq2"])

                    # store course object in dictionary for now before implementing BST
                    self.courses[course_id] = Course(course_id, title, prerequisites)

                print('courses loaded successfully.')
        # throw exception if file doesn't exist or not found
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        # throw general exception if loading isn't successful
        except Exception as e:
            print(f"An error occured while loading the file: {e}")

    # print courses
    def print_courses(self):
        # if user attempts to print courses w/out loading first
        if not self.courses:
            print("\nNo course to display. Please load the courses first.")
            return

        print("\nAvailable Courses:")
        for course_id in sorted(self.courses.keys()): # sort the courses by course_id
            print(self.courses[course_id])

# Beginning of CRUD operations for user
# User can Create, Read, Update, or Delete a specific course
#

        # allows user to search for specific course using a course ID
    def search_course(self, course_id):
        # if a user doesn't enter alphanumeric characters
        if not course_id.isalnum():
            print("Please enter alphanumeric characters only.")
            return

        course_id = course_id.upper() # force capitalization
        if course_id in self.courses:
            print(self.courses[course_id])
        else:
            print(f"Course {course_id} not found.")
    
    # Add a course
    def add_course(self):
        course_id = input("Please enter a new course ID: ").strip().upper()
        if course_id in self.courses:
            print("Course already exists. Enter new course ID, example 'CSCI100, CSCI200'.")
            return
        title = input("Enter course title: ").strip()
        prereqs = input("Enter prequisites: (Must be comma separated, otherwise leave blank): ").strip()
        # clean up user input for prereqs and add to list
        prerequisite_list = [p.strip().upper() for p in prereqs.split(",")] if prereqs else []
        # add to courses dictionary
        self.courses[course_id] = Course(course_id, title, prerequisite_list)
        print(f"Course {course_id} successfully added.")

    # Update a course
    def update_course(self):
        course_id = input("Enter course ID to update: ").strip().upper()
        if course_id not in self.courses:
            print("Course ID not found.")
            return
        new_title = input("Enter new course title: ").strip()
        new_prereqs = input("Enter new prerequisites (Must be comma separated, otherwise leave blank): ")
        prerequisite_list = [p.strip().upper() for p in new_prereqs.split(",")] if new_prereqs else []

        # access existing course object and update the attributes
        course = self.courses[course_id]
        course.title = new_title
        course.prerequisite = prerequisite_list

        print("Course successfully updated.")

    # Delete a course
    def delete_course(self):
        course_id = input("Enter course ID to delete: ").strip().upper()
        if course_id in self.courses:
            del self.courses[course_id]
            print(f"Course {course_id} successfully deleted.")
        else:
            print(f"Course {course_id} not found.")



def main():

    print("Course Manager is starting")

    manager = CourseManager()

    while True:
        print("\nCourse Manager Menu")
        print("1. Load Courses")
        print("2. Print Course List")
        print("3. Search for a course")
        print("4. Add a course")
        print("5. Update a course")
        print("6. Delete a course")
        print("7. Exit Program")
        
        choice = get_valid_menu_choice()

        if choice == "1":
            filename = input("Enter the path to your Courses.csv file: ").strip()
            manager.load_courses(filename)
        elif choice == "2":
            manager.print_courses()
        elif choice == "3":
            course_id = input(f"\nEnter course ID to search: ") # add input validation and sanitization
            manager.search_course(course_id)
        elif choice == "4":
            manager.add_course()
        elif choice == "5":
            manager.update_course()
        elif choice == "6":
            manager.delete_course()
        elif choice == "7":
            print("Exiting Course Manager program...")
            break


if __name__ == "__main__":
    main()
