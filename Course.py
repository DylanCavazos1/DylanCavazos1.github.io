class Course:
    # Course class to create a course object for each row

    """
    Initializes a course with an ID, title, and any prerequisites
    If no prerequisites exist, default to an empty list
    """
    def __init__(self, course_id: str, title: str, prerequisite=None):
        self.course_id = course_id.upper() # courseID is always capitalized
        self.title = title
        self.prerequisite = prerequisite if prerequisite is not None else [] # set prerequisites to given list if provided, otherwise initialize it as an empty list 
    
    """
    Returns a formatted string representation of the course
    Adds n/a for prerequisites if none exist
    """
    def __str__(self):
        # prereqs list gets padded with "n/a" if no prerequisites exist, or if only one exists then add to it
        prereqs = [(p if p.lower() != 'n/a' else 'n/a') for p in self.prerequisite]
        prereqs += ["n/a"] * (2 - len(prereqs))
        prereq_str = ", ".join(prereqs)
        return f"{self.course_id} | {self.title} | Prerequisites: {prereq_str}"