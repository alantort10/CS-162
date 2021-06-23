# Author: Alan Tort
# Date: 06/19/2021
# Description: Project 1

from statistics import mean, median, mode


class Student:
    """A class Student has two private data members - the student's name and grade."""

    def __init__(self, name, grade):
        """Returns a Student object with the given name and grade"""
        # name and grade are intended to be private
        self._name = name
        self._grade = grade

    def get_grade(self):
        """Returns the grade of the Student"""
        return self._grade


def basic_stats(list_of_students):
    """Takes as a parameter a list of Student objects and returns a tuple containing the mean, median, and mode of all
    the grades"""
    # initialize an empty list
    grades = list()

    # iterate through list_of_students, appending each student's grade to grades list
    for student in list_of_students:
        grades.append(student.get_grade())

    # return a tuple containing the mean, median, and mode of grades list
    return mean(grades), median(grades), mode(grades)


def main():
    s1 = Student("Kyoungmin", 73)
    s2 = Student("Mercedes", 74)
    s3 = Student("Avanika", 78)
    s4 = Student("Marta", 74)

    student_list = [s1, s2, s3, s4]
    print(basic_stats(student_list))  # should print a tuple of three values


if __name__ == "__main__":
    main()
