import csv
from Course import Course
from bst import BinarySearchTree
from validators import get_valid_menu_choice, is_valid_course_id, get_valid_prerequisites



#Beginning of CourseManager class
class CourseManager:   

    def __init__(self):
        #self.courses = {} # replacing the dictionary with the BST
        self.bst = BinarySearchTree()
        self.loaded = False # Set the flag to false if courses aren't loaded

    
    def load_courses(self, filename):
        """
        Loads the courses into the BST instead of dictionary
        """
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
                    # gets the prerequisuites from the CSV row if they exist and are not empty
                    if "prereq1" in row and row["prereq1"]:
                        prerequisites.append(row["prereq1"]) # adds the first prerequisite
                    if "prereq2" in row and row["prereq2"]:
                        prerequisites.append(row["prereq2"]) # adds the second prerequisite

                    course = Course(course_id, title, prerequisites)
                    self.bst.insert(course) # inserts the course into the BST

                print('Courses loaded successfully.')
                self.loaded = True # sets the flag to true once courses are successfully loaded

        # throw exception if file doesn't exist or not found
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        # throw general exception if loading isn't successful
        except Exception as e:
            print(f"An error occured while loading the file: {e}")

    
    def print_courses(self):
        """
        Prints courses alphabetically using In-Order Traversal
        Replaces the previous logic that utilized a dictionary
        """
        # if user attempts to print courses w/out loading first
        if not self.loaded:
            print("\nNo courses to display. Please load the courses first.")
            return

        print("\nAvailable Courses:")
        sorted_courses = self.bst.in_order_traversal() # traverse BST in-order to get courses in alphabetical order
        for s_course in sorted_courses:
            print(s_course)


#Beginning of CRUD operations for user
#User can Create, Read, Update, or Delete a specific course
 
    def search_course(self):
        """
        Searches the BST for a specific course by its course ID
        Updated to use the BST's search() method instead of dictionary lookup
        """
        # Checks that courses have been loaded first before allowing searching
        if not self.loaded:
            print("Courses must be loaded prior to searching.")
            return

        course_id = input("\nEnter course ID to search: ").strip().upper()

        # if a user doesn't enter alphanumeric characters
        if not course_id.isalnum():
            print("Please enter alphanumeric characters only.")
            return

        # searches the BST for specific course ID
        search_result = self.bst.search(course_id)  

        if search_result:
            print(search_result)
        else:
            print(f"Course {course_id} not found.")

    def add_course(self):
        """
        Adds a new course to the BST
        Updated to use insert() method instead 
        """
        # checks if the courses are loaded first before allowing users to search 
        if not self.loaded:
            print("Please load courses first prior to adding a new course.")
            return

        course_id = input("Please enter a new course ID: ").strip().upper()
        
        # Enforce a 4 letter, 3 digit format ("CSCI101")
        if not is_valid_course_id(course_id):
            print("Invalid course ID format. Please enter 4 letters followed by 3 digits.")
            return

        # Prevents adding a duplicate course
        if self.bst.search(course_id):
            print("Course already exists. Enter new course ID, example 'CSCI100, CSCI200'.")
            return

        title = input("Enter course title: ").strip()

        # Checks that prerequisites are valid
        prerequisites = get_valid_prerequisites(self.bst, course_id)
        if prerequisites is None:
            print("Add operation canceled due to invalid prerequisites.")
            return

        # Create and insert the new course into the BST
        new_course = Course(course_id, title, prerequisites)
        self.bst.insert(new_course)

        print(f"Course {course_id} successfully added.")

    def update_course(self):
        """
        Updates an existing course in the BST
        Searches for the course by course ID, then deletes the old node,
        then reinserts the updated course with new course data
        """
        # checks that courses are loaded first
        if not self.loaded:
            print("Courses must be loaded first before updating.")
            return
        # input course to edit
        course_id = input("Enter course ID to update: ").strip().upper()

        # assigns course to course found in BST
        course = self.bst.search(course_id)

        # if the course doesn't exist, then return
        if not course:
            print("Course ID not found.")
            return

        new_title = input("Enter new course title: ").strip()
        # Checks that prerequisites are valid 
        prerequisites = get_valid_prerequisites(self.bst, course_id)
        if prerequisites is None:
            print("Update operation canceled due to invalid prerequisites.")
            return

        # remove the old course and insert new one
        self.bst.delete(course_id)

        # assigns updated_course with new Course object
        updated_course = Course(course_id, new_title, prerequisites)

        # inserts the updated course into the BST
        self.bst.insert(updated_course)

        print("Course successfully updated.")

    def delete_course(self):
        """
        Deletes a course from the BST using its course ID
        Checks if the course exists before attempting deletion
        """
        # checks that courses are loaded first
        if not self.loaded:
            print("Courses must be loaded first before attempting to delete.")
            return 

        course_id = input("Enter course ID to delete: ").strip().upper()
        # searches BST for course using course ID 
        course = self.bst.search(course_id)
        # if the course is in the BST, then delete using 1 of 3 cases
        if course:
            self.bst.delete(course_id)
            print(f"Course {course_id} successfully deleted.")
        else:
            print(f"Course {course_id} not found.")

# Beginning of Main function
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
            manager.search_course()
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
