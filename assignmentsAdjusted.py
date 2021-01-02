#-----------------------------------------------------------------------------
# Name:        assignments (assignments.py)
# Purpose:     To allow student assignments in the gradebook program to have 
#              adjusted weightings different from the course-wide default weighting
#
# Author:      Steven Wu
# Created:     2019/11/03
# Updated:     2020/01/02
#-----------------------------------------------------------------------------

from assignments import Assignments
class AssignmentsAdjusted(Assignments):
    '''
    Object which holds the mark information of a student's assignment including
    the teacher adjusted weighting. Inherits from the Assignments() class

    Attributes
    ----------
    username : str
        Account username
    courseName : str
        Name of the course the assignment is for
    assignmentMarks: dict
        Dictionary containing the marks in each category of an assignment
    studentName : str
        Name of the student the assignment belongs to
    adjustedWeighting : int
        The teacher's customn weighting of an assignment for a student

    Methods
    -------
    save(assignmentType :str = 'Student') -> str
        Saves the assignment to the database
    calculate() -> list
        Calculates the mark on the assignment and gets its weighting
    calculateAdjusted() -> list
        Calculates the mark on the assignment and gets its teacher adjusted weighting
    '''
    
    def __init__(self,username, courseName, assignmentMarks, studentName, adjustedWeighting):
        '''
        Constructor to build a Assignments object

        Parameters
        ----------
        username : str
            Account username
        courseName : str
            Name of the course the assignment is for
        assignmentMarks: dict
            Dictionary containing the marks in each category of an assignment
        studentName : str
            Name of the student the assignment belongs to 
        adjustedWeighting : int
            The teacher's customn weighting of an assignment for a student
        '''
        super().__init__(username, courseName, assignmentMarks, studentName)
        self.adjustedWeighting = adjustedWeighting

    def calculateAdjusted(self) -> list:
        '''
        Calculates the mark on the assignment and gets its teacher adjusted weighting

        Calculates the mark of each category on the assignment then uses a weighted average
        to calculate the overall assignment mark. 

        Parameters
        ----------
        None
        
        Returns
        -------
        list
            List including the assignment mark and the teacher adjusted weighting of the assignment
        '''
        return ([self.calculate()[0], self.adjustedWeighting])