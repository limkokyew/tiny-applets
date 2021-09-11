SEMESTER_GRADES = {
    1: {
        "Programmieren 1": {
             "grade": 1.7,
             "credits": 8
        },
        "Grundlagen der Informatik 1": {
            "grade": 1.0,
            "credits": 5
        },
        "Rechnerstrukturen 1": {
            "grade": 2.0,
            "credits": 8
        },
        "Software Engineering 1": {
            "grade": 1.0,
            "credits": 5
        },
        "Mathematik 1": {
            "grade": 1.3,
            "credits": 6
        },
        "English Grammar": {
            "grade": 1.0,
            "credits": 2
        }
    },
    2: {
        "Programmieren 2": {
             "grade": 1.0,
             "credits": 8
        },
        "Grundlagen der Informatik 2": {
            "grade": 1.0,
            "credits": 5
        },
        "Datenkommunikation": {
            "grade": 3.0,
            "credits": 5
        },
        "Software Engineering 2": {
            "grade": 1.0,
            "credits": 5
        },
        "Mathematik 2": {
            "grade": 1.0,
            "credits": 6
        },
        "Englisch": {
            "grade": 1.3,
            "credits": 4
        }
    },
    3: {
        "Programmieren 3": {
             "grade": 1.0,
             "credits": 8
        },
        "Datenbanken": {
            "grade": 1.0,
            "credits": 8
        },
        "Statistik": {
            "grade": 1.0,
            "credits": 6
        },
        "Software Engineering 3": {
            "grade": 1.0,
            "credits": 5
        },
        "Systemnahe Programmierung": {
            "grade": 1.7,
            "credits": 6
        }
    },
    4: {
        "Projektarbeit 1": {
             "grade": 1.3,
             "credits": 8
        },
        "Betriebssysteme": {
            "grade": 1.0,
            "credits": 5
        },
        "Rechnerstrukturen 2": {
            "grade": 1.7,
            "credits": 5
        },
        "Numerische Mathematik": {
            "grade": 1.0,
            "credits": 5
        },
        "Single-Page-Anwendungen": {
            "grade": 1.3,
            "credits": 5
        }
    },
    5: {
        "DV-Recht": {
            "grade": 3.0,
            "credits": 2
        },
        "BWL": {
            "grade": 1.3,
            "credits": 4
        }
    },
    6: {
        "Methoden der KI": {
            "grade": 1.3,
            "credits": 7.5
        },
        "Digitale Bildverarbeitung": {
            "grade": 1.0,
            "credits": 7.5
        },
        "DVA-Seminar": {
            "grade": 1.3,
            "credits": 3
        }
    },
    7: {
        "Bachelorarbeit": {
            "grade": 1.3,
            "credits": 36
        },
        "Projektarbeit 2": {
            "grade": 1.0,
            "credits": 10
        },
        "Agile Softwareentwicklung (Scrum)": {
            "grade": 1.0,
            "credits": 5
        },
        "Kommunikationspsychologie": {
            "grade": 1.0,
            "credits": 2
        },
    }
}


class GradeCalculator():
    EXIT_COMMANDS = ["exit", "q", "quit"]

    def __init__(self, grades=None):
        self.semester_grades = grades
        
    def calculate(self, semester):
        semester_keys = list(self.semester_grades.keys())
        grade = 0
        ects = 0
        
        try:
            semester = int(semester)
            if semester not in semester_keys:
                print("Could not fetch grades for semester {}.".format(semester))
                return
        except ValueError:
            if semester == "all":
                for semester, semester_info in self.semester_grades.items():
                    for subject, subject_info in semester_info.items():
                        grade += subject_info["grade"] * subject_info["credits"]
                        ects += subject_info["credits"]

                print("\nYour overall performance is:")
                print(grade / ects)
                print(f"ECTS: {ects}")
                return
            else:
                print("Invalid input.")
                return
        
        for subject, subject_info in self.semester_grades[semester].items():
            grade += subject_info["grade"] * subject_info["credits"]
            ects += subject_info["credits"]
        
        print("\nYour overall performance in semester {} is:".format(semester))
        print(grade / ects)
        print(f"ECTS: {ects}")
        
    
    def start(self):
        print("""Welcome to the grade calculator! I hope you've been doing well these past semesters.
Enter any numerical value corresponding to one of your semesters or 'all' to view your overall performance.""")
        while True:
            user_input = input()
            if user_input in GradeCalculator.EXIT_COMMANDS:
                return
            self.calculate(user_input)


if __name__ == "__main__":
    grade_calculator = GradeCalculator(SEMESTER_GRADES)
    grade_calculator.start()
    
