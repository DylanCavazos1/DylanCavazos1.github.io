class Course:
# Course class to create a course object for each row

    def __init__(self, course_id: str, title: str, prerequisite=None):
        self.course_id = course_id.upper() # courseID is always capitalized
        self.title = title
        self.prerequisite = prerequisite if prerequisite is not None else [] # set prerequisites to given list if provided, otherwise initialize it as an empty list 

    def __str__(self):
        # prereqs list gets padded with "n/a" if no prerequisites exist, or if only one exists then add to it
        prereqs = self.prerequisite + ["n/a"] * (2 - len(self.prerequisite))
        prereq_str = ", ".join(prereqs)
        return f"{self.course_id} | {self.title} | Prerequisuites: {prereq_str}"