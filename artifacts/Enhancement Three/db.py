import psycopg2
from BST import BinarySearchTree
from csv_loader import load_courses

DB_NAME = "course_manager"
DB_USER = "postgres"
DB_PASS = "SNHU1234"
DB_HOST = "localhost"
DB_PORT = "5432"

# Test connection
# Connect to PostgreSQL - https://www.geeksforgeeks.org/introduction-to-psycopg2-module-in-python/
def connect():
    try:
        return psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
        print("Database connected successfully")

    except:
        print("Database not connected successfully")

# BST inserts data via in-order traversal utilizing recrusive function
# Insert node(data) into DB using in-order traversal
def sync_bst_to_db(conn, node):
    """
    Uses in-order traversal in the BST and inserts each course into the PostgreSQL database.
    If there are duplicate course entries, then they are ignored. 
    """

    if node is None:
        # prevent recursion if node is None
        return

    # recurse through left subtree
    sync_bst_to_db(conn, node.left)

    # insert this course
    course = node.course

    with conn.cursor() as cur:

        cur.execute("""
        INSERT INTO courses (course_id, title, prerequisites)
        VALUES (%s, %s, %s)
        ON CONFLICT (course_id) DO NOTHING;
        """, (course.course_id, course.title, course.prerequisite)) 

        conn.commit()

    # right subtree
    sync_bst_to_db(conn, node.right)

def sync_db_with_bst(conn, bst_root):
    """
    Clears all data in the courses table and re-syncs it from the current data in the BST.
    If memory is out of sync, it useful for having the database match the BST.
    """
    with conn.cursor() as cur:

        cur.execute("DELETE FROM courses;")

        conn.commit()

    # Insert the courses in BST To Database
    sync_bst_to_db(conn, bst_root)

    print("Database successfully synced.\n")
# Referenced tutorial for insertion from - https://www.geeksforgeeks.org/postgresql-insert/
def insert_course_in_db(conn, course):
    """
    Inserts a singlecourse into the PostgreSQL database.
    IF the course_id already exists, it does nothing. 
    """
    with conn.cursor() as cur:

        cur.execute("""
        INSERT INTO courses (course_id, title, prerequisites)
        VALUES (%s, %s, %s)
        ON CONFLICT (course_id) DO NOTHING;
        """, (course.course_id, course.title, "{" + ', '.join(course.prerequisite) + "}"
              ))

        conn.commit()

    print("Course succesfully updated in Database.\n")
# Referenced info from - https://www.w3schools.com/postgresql/index.php
def print_courses_in_db(conn):
    """
    Uses a query to get all the courses from the PostgreSQL database and prints them.
    The results are sorted alphabetically by course_id.
    """
    with conn.cursor() as cur:

        cur.execute("SELECT * FROM courses ORDER BY course_id ASC;")

        rows = cur.fetchall()

        print("\nCourses stored in database:")

        if not rows:
            print("No courses currently stored in database.")
            return
        # iterate through the rows and print formatted
        for row in rows:
            course_id, title, prerequisites = row
            print(f"{course_id} | {title} | Prerequisites: {prerequisites}")
        print("\n")
# Referenced info from - https://www.w3schools.com/postgresql/postgresql_update.php
def update_course_in_db(conn, course):
    """
    Updates the title and prerequisites of an existing course in the database. 
    """
    with conn.cursor() as cur:

        cur.execute("""
        UPDATE courses
        SET title = %s, prerequisites = %s
        WHERE course_id = %s;
        """, (course.title, "{" + ', '.join(course.prerequisite)  + "}" ,course.course_id)) 

        conn.commit()

        print(f"Course {course.course_id} updated in the database.\n")
# Referenced info from - https://www.w3schools.com/postgresql/postgresql_delete.php
def delete_course_in_db(conn, course_id):
    """
    Deletes a course from the database using the course_id. 
    """
    with conn.cursor() as cur:

        cur.execute("DELETE FROM courses WHERE course_id = %s;", (course_id,))

        conn.commit()

    print(f"Course {course_id} deleted from the database.\n")

def clear_courses(conn):
    """
    Deletes all courses from the database. 
    """
    with conn.cursor() as cur:

        cur.execute("DELETE FROM courses;")

        conn.commit()

    print("PostgreSQL database has been cleared.\n")


if __name__ == "__main__":
    bst = BinarySearchTree()
    
    load_courses("courses.csv", bst)

    print("Courses loaded into BST. Now syncing to PostgreSQL..")
    
    conn = connect()
    if conn:
        sync_bst_to_db(conn, bst.root)
        conn.close()
        print("Sync complete.\n")
    