from Course import Course
import csv
course1 = Course("CS101", "Introduction to Programming", ["MATH100"])
course2 = Course("CS102", "Data Structures", ["CS101"])
course3 = Course("CS103", "Algorithms") # no prerequisites

#Test printing them
#print(course1)
#print(course2)
#print(course3)

# practice opening files in Python
# found from https://www.geeksforgeeks.org/reading-csv-files-in-python/
with open('Courses.csv', mode='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        print(lines)