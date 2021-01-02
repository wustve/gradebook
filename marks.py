#-----------------------------------------------------------------------------
# Name:        marks (marks.py)
# Purpose:     To allow the gradebook program to calculate the mark's of students
#
# Author:      Steven Wu
# Created:     2019/11/03
# Updated:     2020/01/04
#-----------------------------------------------------------------------------

from assignments import Assignments
from assignmentsAdjusted import AssignmentsAdjusted

from courses import Courses
from math import floor

class Marks():
    '''
    Object which holds the mark information of students

    Attributes
    ----------
    username : str
        Account username
    courseName : str
        Name of the course
    studentName : str
        Name of the student
    assignmentList : List
        List of Assignments and AssignmentsAdjusted objects which are used to calculate the student's mark
    
    Methods
    -------
    totalMark() -> float
        Calculates the student's mark
    totalMarkAdjusted() -> float
        Calculates the student's adjusted mark
    defaultSort() -> None
        Sorts the assignmentList attribute
    '''

    def __init__(self,username, courseName, studentName):
        '''
        Constructor to build a Marks object

        Parameters
        ----------
        username : str
            Account username
        courseName : str
            Name of the course
        studentName : str
            Name of the student
        
        Raises
        -------
        KeyError
            If a document in 'GradebookStudents' does not have an 'assignments' key
        KeyError
            If an 'assignment' array item in a document in 'GradebookStudents' does not have an 'adjusted weighintg' key
        '''

        self.username = username
        self.courseName = courseName
        self.studentName = studentName
        self.assignmentList = []
        try:
            studentAssignments = Courses(self.username).docGet({'student name': studentName,'course name' : self.courseName}, 'GradebookStudents')['assignments']
            for assignment in studentAssignments:
                try:
                    self.assignmentList.append(AssignmentsAdjusted(self.username,self.courseName,assignment,self.studentName, assignment['adjusted weighting']))
                except:
                    self.assignmentList.append(Assignments(self.username,self.courseName,assignment,self.studentName))
        except:
            pass

    def totalMark(self) -> float:
        '''
        Calculates the student's mark

        Calculates the marks of each of the student's assignments and uses a 
        weighted average to calculate the student's mark

        Parameters
        ----------
        None
        
        Returns
        -------
        float
            The student's mark

        Raises
        -------
        ZeroDivisionError
            If there is an assignment with a total mark or weighting of 0
        '''
        cumulativeMark = 0
        cumulativeWeighting = 0
        for x in self.assignmentList:
            try: #zero division
                assignmentResult = x.calculate()
                cumulativeMark += assignmentResult[0] *assignmentResult[1]
                cumulativeWeighting += assignmentResult[1]
            except:
                pass
        return (cumulativeMark/cumulativeWeighting)

    def totalMarkAdjusted(self) -> float:
        '''
        Calculates the student's adjusted mark

        Calculates the marks of each of the student's assignments and uses a 
        weighted average (using the teacher's adjusted weightings) to calculate the student's mark

        Parameters
        ----------
        None
        
        Returns
        -------
        float
            The student's mark

        Raises
        -------
        KeyError
            If object in assignmentList does not have a calculateAdjusted method
        ZeroDivisionError
            If there is an assignment with a total mark or weighting of 0
        '''

        cumulativeMark = 0
        cumulativeWeighting = 0
        for x in self.assignmentList:
            try:
                assignmentResultAdjusted = x.calculateAdjusted()
                cumulativeMark += assignmentResultAdjusted[0]* assignmentResultAdjusted[1]
                cumulativeWeighting += assignmentResultAdjusted[1]
            except:
                try:
                    assignmentResult = x.calculate()
                    cumulativeMark += assignmentResult[0]*assignmentResult[1]
                    cumulativeWeighting += assignmentResult[1]
                except:
                    pass
        return (cumulativeMark/cumulativeWeighting)
    def defaultSort(self)-> None:
        '''
        Sorts the assignmentList attribute

        Uses the default sort method to sort the list in alphabetical order
        by assignment name

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        self.assignmentList.sort(key = lambda i: i.assignmentMarks['assignment name'].lower())
        #for x in self.assignmentList:
        #    print(x.assignmentMarks['assignment name'])

    """
    def bubbleSort(self) -> None:
        '''
        Sorts the assignmentList attribute

        Uses the bubble sort algorithm to sort the list in alphabetical order
        by assignment name

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''

        changed = True
        while changed:
            changed = False
            for x in range (1,len(self.assignmentList)):
                try:
                    if self.assignmentList[x-1].assignmentMarks['assignment name'].lower() > self.assignmentList[x].assignmentMarks['assignment name'].lower():
                        self.assignmentList[x-1], self.assignmentList[x] = self.assignmentList[x], self.assignmentList[x-1]
                        changed = True
                except:
                    continue
        #for x in self.assignmentList:
        #    print(x.assignmentMarks['assignment name'])
        
    def insertionSort(self) -> None:
        '''
        Sorts the assignmentList attribute

        Uses the insertion sort algorithm to sort the list in alphabetical order by assignment name

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        for x in range (1, len(self.assignmentList)):
            key = self.assignmentList[x]
            j = x-1
            while j >=0 and key.assignmentMarks['assignment name'].lower() < self.assignmentList[j].assignmentMarks['assignment name'].lower():
                self.assignmentList[j+1] = self.assignmentList[j]
                j -= 1
            self.assignmentList[j+1] = key
        #for x in self.assignmentList:
        #    print(x.assignmentMarks['assignment name'])
    
    def linearSearch(self, query) -> int:
        '''
        Searchs for an assignment using its name

        Uses a linear search on an unsorted list to find the Assignments and AssignmentsAdjusted object with the correct name

        Parameters
        ----------
        query : str
          Assignment name
        
        Returns
        -------
        int
            Index of the assignment or -1 if it does not exist
        '''
        for x in range( len(self.assignmentList)-1):
            if self.assignmentList[x].assignmentMarks['assignment name'].lower() == query.lower():
                return x
        return (-1)
    def binarySearch(self, query, alreadySorted) -> int:
        '''
        Searchs for an assignment using its name

        Uses a binary search on a sorted list to find the Assignments and AssignmentsAdjusted object with the correct name

        Parameters
        ----------
        query: str  
          Assignment name
        alreadySorted : bool
          If the list has been sorted or not
        
        Returns
        -------
        int
            Index of the assignment or -1 if it does not exist
        '''
        if not alreadySorted:
            self.defaultSort()
        min = 0
        max = len(self.assignmentList)
        while max>min:
            mid= floor((max+min)/2)
    
            if self.assignmentList[mid].assignmentMarks['assignment name'].lower() < query.lower():
                min = mid+1
            else:
                max = mid
        if min == max and self.assignmentList[min].assignmentMarks['assignment name'].lower() == query.lower():
            return min  
        else:
            return -1
    '''
    #Complexity analysis
    #https://docs.google.com/document/d/1f3-4oobyYtrJheiDJkIyX7egcLtTF8ALCRMuYfgdkXY/edit?usp=sharing
    """