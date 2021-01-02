#-----------------------------------------------------------------------------
# Name:        assignments (assignments.py)
# Purpose:     To allow the gradebook program to have functional assignments
#
# Author:      Steven Wu
# Created:     2019/11/03
# Updated:     2020/01/16
#-----------------------------------------------------------------------------

import pymongo
from connectionString import connectionStr
from courses import Courses
class Assignments():
    '''
    Object which holds the mark information of an assignment

    Attributes
    ----------
    username : str
        Account username
    courseName : str
        Name of the course the assignment is for
    assignmentMarks: dict
        Dictionary containing the marks in each category of an assignment
    studentName : str
        Name of the student the assignment belongs to, if applicable 

    Methods
    -------
    save(assignmentType : str= 'Student') -> str
        Saves the assignment to the database
    calculate() -> list
        Calculates the mark on the assignment and gets its weighting
    
    '''

    def __init__(self, username, courseName, assignmentMarks,studentName=''):
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
        studentName : str, optional
            Name of the student the assignment belongs to, if applicable 

        '''
        self.username = username
        self.courseName = courseName
        self.studentName = studentName
        self.assignmentMarks = assignmentMarks

    def save(self, assignmentType = 'Student') -> str:
        '''
        Saves the assignment to the database

        Saves the assignment information to the student's or course's database document

        Parameters
        ----------
        assignmentType : str, optional
            Type of assignment clicked (Student or Course), defaults to 'Student'
        
        Returns
        -------
        str
            'Entries cannot be negative' if a negative mark or weighting was received
            'Entries must be numbers' if a non numerical mark or weighting was received
            'Saved' if the assignment data was successfully saved

        Raise
        -------
        ValueError
            If string could not be converted to float
        KeyError
            If there is no 'assignments' key  in the student's document
        KeyError
            If there is no 'assignments' key  in the course's document
        '''

        for x in self.assignmentMarks.keys():
            if x!= 'assignment name':
                self.assignmentMarks[x] = self.assignmentMarks[x].get().strip()
                try: 
                    if float(self.assignmentMarks[x]) <0:
                        return ('Entries cannot be negative')
                    else:
                        self.assignmentMarks[x] = float(self.assignmentMarks[x])

                except:
                    return('Entries must be numbers')


        client = pymongo.MongoClient(connectionStr)
        if assignmentType == 'Student':
            if self.assignmentMarks['weighting'] ==self.assignmentMarks['adjusted weighting']:
                del self.assignmentMarks['adjusted weighting']
            database = client['GradebookStudents']
            collection = database[self.username]
            try:
                existingAssignments = Courses(self.username).docGet({'student name': self.studentName,'course name' : self.courseName},'GradebookStudents')['assignments']
                for x in existingAssignments:
                    if x['assignment name'] == self.assignmentMarks['assignment name']:
                        collection.update_one({'student name': self.studentName,'course name' : self.courseName}, { '$pull' : {'assignments' :x}})
                        break
            except:
                pass
            collection.update_one({'student name': self.studentName,'course name' : self.courseName}, { '$push' : {'assignments' :self.assignmentMarks}} )
        elif assignmentType == 'Course':
            database = client['GradebookCourses']
            collection = database[self.username]
            try:
                existingAssignments = Courses(self.username).docGet({'course name' : self.courseName},'GradebookCourses')['assignments']
                for x in existingAssignments:
                    if x['assignment name'] == self.assignmentMarks['assignment name']:
                        collection.update_one({'course name' : self.courseName}, { '$pull' : {'assignments' :x}})
                        break
            except:
                pass
            collection.update_one({'course name' : self.courseName}, { '$push' : {'assignments' :self.assignmentMarks}} )
            studentDb = client['GradebookStudents']
            studentCol = studentDb[self.username]
            studentCol.update_many({'course name' : self.courseName,'assignments.assignment name' : self.assignmentMarks['assignment name']}, {'$unset':{'assignments.$.adjusted weighting':{'$exists': True}}})
            studentCol.update_many({'course name' : self.courseName,'assignments.assignment name' : self.assignmentMarks['assignment name']}, {'$set':{'assignments.$.weighting':self.assignmentMarks["weighting"]}})
        client.close()
        return('Saved')

    def calculate(self) -> list:
        '''
        Calculates the mark on the assignment and gets its weighting

        Calculates the mark of each category on the assignment then uses a weighted average
        to calculate the overall assignment mark. 

        Parameters
        ----------
        None
        
        Returns
        -------
        list
            List including the assignment mark and the weighting of the assignment
        '''
        
        cumulativeWeight = 0
        cumulativeMark = 0
        for x in Courses(self.username).docGet({'course name' : self.courseName},'GradebookCourses')['assignments']:
            if x['assignment name'] == self.assignmentMarks['assignment name']:
                assignmentTotal = x
                break
        weightings ={}
        for x in Courses(self.username).docsGet('GradebookCourses',{'category':{'$exists': True}}):
            weightings[x['category']] = x['weighting']

        for category in assignmentTotal.keys():
            if category != 'assignment name' and category != 'weighting' and category != 'adjusted weighting' and assignmentTotal[category] != 0:
                try:
                    cumulativeMark += weightings[category] * self.assignmentMarks[category]/assignmentTotal[category] *100
                    cumulativeWeight += weightings[category]
                except Exception as e:
                    pass
                    #print(e)
        return ([cumulativeMark/cumulativeWeight, assignmentTotal['weighting']])