import csv
from Course import Course

def load_courses(filename, bst):
        """
        Loads the courses into the BST instead of dictionary
        """
        # check that user enters csv filetype
        if not filename.lower().endswith(".csv"): # Found "endswith()" string method in https://www.w3schools.com/python/python_strings_methods.asp
            print("Invalid file type. Please provide a .csv file")
            return False

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
                    bst.insert(course) # inserts the course into the BST

                print("Courses successfully loaded to Binary Search Tree.")
                return True # sets the flag to true once courses are successfully loaded

        # throw exception if file doesn't exist or not found
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        # throw general exception if loading isn't successful
        except Exception as e:
            print(f"An error occured while loading the file: {e}")

        return False
