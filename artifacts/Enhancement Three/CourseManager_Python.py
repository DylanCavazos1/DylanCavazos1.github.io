from Course import Course
from BST import BinarySearchTree
from csv_loader import load_courses
from Validators import get_valid_menu_choice, is_valid_course_id, get_valid_prerequisites
from db import connect, delete_course_in_db, sync_bst_to_db, sync_db_with_bst, insert_course_in_db, print_courses_in_db, clear_courses, update_course_in_db


#Beginning of CourseManager class
class CourseManager:   

    def __init__(self):
        #self.courses = {} # replacing the dictionary with the BST
        self.bst = BinarySearchTree()
        self.loaded = False # Set the flag to false if courses aren't loaded
    
    def print_courses(self):
        """
        Prints courses alphabetically using In-Order Traversal
        Replaces the previous logic that utilized a dictionary
        """
        # if user attempts to print courses w/out loading first
        if not self.loaded:
            print("\nNo courses to display. Please load the courses first.")
            return

        print("\nCourses in Binary Search Tree:")
        sorted_courses = self.bst.in_order_traversal() # traverse BST in-order to get courses in alphabetical order
        for s_course in sorted_courses:
            print(s_course)
        print("\n")


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
        conn = connect()
        if conn: 
            insert_course_in_db(conn,new_course)
            conn.close()    

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

        # Enforce a 4 letter, 3 digit format ("CSCI101")
        if not is_valid_course_id(course_id):
            print("Invalid course ID format. Please enter 4 letters followed by 3 digits.")
            return

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
        print("Course updated in Binary Search Tree.")

        conn = connect()
        if conn:
            update_course_in_db(conn, updated_course)
            conn.close()


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

        # Enforce a 4 letter, 3 digit format ("CSCI101")
        if not is_valid_course_id(course_id):
            print("Invalid course ID format. Please enter 4 letters followed by 3 digits.")
            return

        # searches BST for course using course ID 
        course = self.bst.search(course_id)

        # if the course is in the BST, then delete using 1 of 3 cases
        if course:
            self.bst.delete(course_id)
            print(f"Course {course_id} successfully deleted.")
        else:
            print(f"Course {course_id} not found.")

        conn = connect()
        if conn:
            delete_course_in_db(conn, course_id)
            conn.close()

# Beginning of Main function
def main():

    print("----------------------------------------------------")
    print("         Welcome to the Course Manager ")
    print("----------------------------------------------------")
    print("This program allows you to manage university courses")
    print("using an in-memory Binary Search Tree (BST) and a")
    print("PostgreSQL database for persistent storage.\n")
    print("Instructions:")
    print("1. Start by loading courses from a formatted CSV file.")
    print("2. Courses are loaded into a Binary Search Tree for in-memory use.")
    print("3. The BST data is automatically synced to the PostgreSQL database.")
    print("4. Perform CRUD operations like Create, Read, Update, or Delete.")
    print("5. Changes to courses will be reflected in both the BST and database.")
    print("6. You can view or clear the database at any time.")
    print("7. Use the Sync option to overwrite the database with the current BST.")
    print("----------------------------------------------------")

    manager = CourseManager()

    while True:
        print("1. Load courses")
        print("2. Print course List")
        print("3. Search for a course")
        print("4. Add a course")
        print("5. Update a course")
        print("6. Delete a course")
        print("7. Print Database")
        print("8. Sync Database")
        print("9. Clear Database")
        print("10. Exit program")
        
        choice = get_valid_menu_choice()

        if choice == "1":
            filename = input("Enter the path to your Courses.csv file: ").strip()
            manager.bst = BinarySearchTree()
            successful = load_courses(filename, manager.bst)
            if successful:
                manager.loaded = True
                conn = connect()
                if conn:
                    print("Syncing BST to PostgreSQL...")
                    sync_bst_to_db(conn, manager.bst.root)
                    conn.close()
                    print("Sync complete.\n")
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
            conn = connect()
            if conn:
                print_courses_in_db(conn)
                conn.close()
        elif choice == "8":
            if not manager.loaded:
                print("Binary Search Tree is empty. Load or add courses before syncing.")
            else:
                conn = connect()
                if conn:
                    sync_db_with_bst(conn, manager.bst.root)
                    conn.close()
        elif choice == "9":
            conn = connect()
            if conn:
                clear_courses(conn)
                conn.close()
        elif choice == "10":
            confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm == "y":
                print("Exiting Course Manager program...")
                break
            else:
                print("Returning to main menu.")

if __name__ == "__main__":
    main()
