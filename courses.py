# -----------------------------------------------------------------------------
# Name:        courses (courses.py)
# Purpose:     To provide course management functionality to the Gradebook program
#
# Author:      Steven Wu
# Created:     2019/10/03
# Updated:     2020/01/16
# -----------------------------------------------------------------------------
import pymongo
from confirmationScreen import ConfirmationScreen
from connectionString import connectionStr
#from assignments import Assignments

class Courses():
    '''
    Object which holds the account username for use in managing courses

    Attributes
    ----------
    username : str
    	Account username

    Methods
    -------
    create(newName : str, courseName : str, option : str) -> str
    	Attempts to create new courses or students
    createWeighted(newName : str, weighting : str,option : str, courseName : str= '') -> str
        Attempts to create mark categories or assignments (items with weightings)
    docsGet(databaseName : str, query : dict = {}) -> list
        Returns list of specified database documents
    requestDelete(databaseName: str,option : str,deleteStatus : label, docName : str, subDocName : str = '') -> None
        Checks if the course requested to be deleted exists and then continues the deletion process
    delete(databaseName : str, option: str,deleteStatus : label, docName : str, subDocName : str = '') -> None
        Deletes the requested document/item in document
    docGet(query : dict, databaseName : str) -> dict
        Returns a single specified document
    '''

    def __init__(self, username):
        '''
        Constructor to build a Courses object

        Parameters
        ----------
        username : str
            Account username

        '''

        self.username = username

    def create(self, newName, courseName, option) -> str:
        '''
        Attempts to create new courses or student

        Checks if the item to be added already exists in the user's database, then creates or updates documents
        to include that item

        Parameters
        ----------
        newName : str
            Name of the item
        courseName : str
            Name of the course the item is in (N/A if item is a course)
        option : str
            Indicates the type of item being added


        Returns
        -------
        str
            'Please enter a name' if the method found newName was empty
        	'Course already exists' if the method found a document containing the same course
        	'Course has been added' if a course was sucessfully added
        	'Student already exists' if the method found a document containing the same student
        	'Student has been added' if a student was sucessfully added
        Raises
        -------
        KeyError
            If a document in 'GradebookCourses' does not have a 'course name' key
        '''
        if newName == '':
            return ('Please enter a name')
        client = pymongo.MongoClient(connectionStr)
        courseDB = client['GradebookCourses']
        courseCol = courseDB[self.username]
        
        existingEntries = []
        if option == 'Course':
            for x in courseCol.find({'course name':{'$exists': True}}):
                existingEntries.append(x['course name'].lower())
            if newName.lower() in existingEntries:
                client.close()
                return ('Course already exists')
            else:
                courseCol.insert_one({'course name': newName})
                client.close()
                return ('Course has been added')
        elif option == 'Student':
            studentDB = client['GradebookStudents']
            studentCol = studentDB[self.username]
            for x in studentCol.find({'course name': courseName}):
                existingEntries.append(x['student name'].lower())
            if newName.lower() in existingEntries:
                client.close()
                return ('Student already exists')
            else:
                studentCol.insert_one({'student name': newName, 'course name': courseName})
                return ('Student has been added')

    def createWeighted(self, newName, weighting, option, courseName = '') -> str:
        '''
        Attempts to create mark categories or assignments (items with weightings)

        Checks if the category/assignment already exists and if weighting is a non-negative number.
        Then creates an courseDB document with the category/assignment name and weighting

        Parameters
        ----------
        newName : str
            Name of the item to be added
        weighting : str
            Weighting of the item
        option : str
            Type of item being added
        courseName : str, optional
            Name of the course the assignment is in, if applicable

        Returns
        -------
        str
            'Please enter a name' if the name entered was blank
            'Category already exists' if the method found a document containing the same category name
        	'Category Added' if a category was successfully added
        	'Those names aren't allowed' if the name entered is reserved by the program for other uses
        	'Weighting can't be negative' if the method found the weighting was negative
            'Weighting must be a number' if the method found that the weighting was not numerical
            'Assignment already exists' if the method found a course document containing the same assignment
        	'Assignment has been added' if an assignment was successfully added

        Raises
        -------
        KeyError
            If a document in 'GradebookCourses' does not have an 'assignments' key
        KeyError
            If a document in 'GradebookCourses' does not have a 'category' key
        ValueError
            If string could not be converted to float
        '''
        if newName == '':
            return ('Please enter a name')

        client = pymongo.MongoClient(connectionStr)
        courseDB = client['GradebookCourses']
        courseCol = courseDB[self.username]

        existingEntries = []
        if option == 'Assignment':
            try:
                for x in courseCol.find_one({'course name': courseName})['assignments']:
                    existingEntries.append(x['assignment name'].lower())
            except:
                pass
        elif option == 'Category':    
            for x in courseCol.find({'category':{'$exists': True}}):
                existingEntries.append(x['category'].lower())

        if newName.lower() in existingEntries:
            client.close()
            return (option+' already exists')
        elif newName.lower() == 'adjusted weighting' or newName.lower() =='weighting' or newName.lower() == 'assignment name':
            return ("Those names aren't allowed")
        else:
            try:
                weighting = float(weighting.strip())
                if weighting >= 0:
                    if option =='Category':
                        courseCol.insert_one({'category': newName, 'weighting': weighting})
                    elif option == 'Assignment':
                        courseCol.update({'course name': courseName}, {'$push': {'assignments': {'assignment name' : newName, 'weighting':weighting}}})
                        studentDB = client['GradebookStudents']
                        studentCol = studentDB[self.username]
                        studentCol.update_many({'course name':courseName},{'$push': {'assignments': {'assignment name' : newName,'weighting':weighting}}})
                        client.close()
                    client.close()
                    return (option+' Added')
                else:
                    client.close()
                    return ("Weighting can't be negative")
            except:
                client.close()
                return ('Weighting must be a number')

    def docsGet(self, databaseName, query = {}) -> list:
        '''
        Returns list of specified database documents

        Returns a list of the documents matching the query in the specified
        database.

        Parameters
        ----------
        databaseName : str
            Name of the database
        query : dict
            Search query
        Returns
        -------
        list
        	List of documents

        '''

        client = pymongo.MongoClient(connectionStr)
        database = client[databaseName]
        collection = database[self.username]
        docs = list(collection.find(query))
        client.close()
        return (docs)

    def requestDelete(self,databaseName, option, deleteStatus, docName, subDocName='') -> None:
        '''
        Checks if the document/item in document requested to be deleted exists and then continues the deletion process

        Checks if a database document/item under the current user contains the has name requested,
        then calls on the ConfirmationScreen class to continue the deletion process

        Parameters
        ----------
        databaseName : str
            Name of database
        option : str
            Type of item being deleted
        deleteStatus : Label
            Label which displays the status of deletion on the MainScreen window
        docName : str
            Name of the document
        subDocName : str, optional
            Name of the item in the document, if applicable

        Returns
        -------
        None
        
        Raises
        -------
        KeyError
            If a document in 'GradebookCourses' does not have a 'course name' key
        KeyError
            If a document in 'GradebookCourses' does not have an 'assignments' key
        KeyError
            If a document in 'GradebookCourses' does not have a 'category' key
        '''
        client = pymongo.MongoClient(connectionStr)
        database = client[databaseName]
        collection = database[self.username]
        if docName == '':
            deleteStatus.config(text='Please enter a name')
            return
        elif subDocName =='' and option =='Assignment':
            deleteStatus.config(text='Please enter a name')
            return
        elif option == 'Assignment':
            try:
                for x in collection.find_one({'course name':docName})['assignments']:
                    if x['assignment name'].lower() == subDocName.lower():
                        subDocName = x['assignment name']
                        ConfirmationScreen(self,databaseName,option, deleteStatus, docName, subDocName)
                        deleteStatus.config(text="Please confirm deletion of '" + x['assignment name'] + "'")
                        return
            except:
                pass
        else:
            for x in collection.find():
                try:
                    if (option == 'Course' and x['course name'].lower() == docName.lower()):  
                        docName =x['course name']
                        ConfirmationScreen(self,databaseName,option, deleteStatus, docName, subDocName)
                        deleteStatus.config(text="Please confirm deletion of '" + x['course name'] + "'")
                        return
                    elif (option == 'Category' and x['category'].lower() == docName.lower()) :
                        docName = x['category']
                        ConfirmationScreen(self,databaseName,option, deleteStatus, docName, subDocName)
                        deleteStatus.config(text="Please confirm deletion of '" + x['category'] + "'")
                        return
                    elif (option =='Student' and x['course name'].lower() == docName.lower() and x['student name'].lower() == subDocName.lower()):
                        subDocName =x['student name']
                        ConfirmationScreen(self,databaseName,option, deleteStatus, docName, subDocName)
                        deleteStatus.config(text="Please confirm deletion of '" + x['student name'] + "'")
                        return
                except:
                    continue
        deleteStatus.config(text=option+' not found')

    def delete(self,databaseName, option, deleteStatus, docName, subDocName='') -> None:
        '''
        Deletes the requested document/item in document

        Last stage of the deletion process, deletes the database document or item in a document

        Parameters
        ----------
        databaseName : str
            Name of database
        option : str
            Type of item being deleted
        deleteStatus : Label
            Label which displays the status of deletion on the MainScreen window
        docName : str
            Name of the document
        subDocName : str, optional
            Name of the item in the document, if applicable

        Returns
        -------
        None

        '''
        client = pymongo.MongoClient(connectionStr)
        database = client[databaseName]
        collection = database[self.username]
        if option == 'Course':
            collection.delete_one({'course name': docName})
            studentDB = client['GradebookStudents']
            studentCol = studentDB[self.username]
            studentCol.delete_many({'course name':docName})

        elif option == 'Student':
            collection.delete_one({'course name': docName, 'student name': subDocName})
        elif option == 'Category':
            collection.delete_one({'category': docName})
            categoryKey = 'assignments.$[].'+docName
            collection.update_many({'course name': {'$exists': True}}, {'$unset':{categoryKey : {'$exists': True}}})
            studentDB = client['GradebookStudents']
            studentCol = studentDB[self.username]
            studentCol.update_many({},{'$unset':{categoryKey : {'$exists': True}}})
        elif option == 'Assignment':
            collection.update_one({'course name': docName},{'$pull':{'assignments':{ 'assignment name': subDocName }}})
            studentDB = client['GradebookStudents']
            studentCol = studentDB[self.username]
            studentCol.update_many({'course name': docName},{'$pull':{'assignments':{ 'assignment name': subDocName }}})

        deleteStatus.config(text=option+' deleted')

        client.close()

    def docGet(self, query, databaseName) -> dict:
        '''
        Returns a single specified document

        Finds the specified document in a database and returns it

        Parameters
        ----------
        query : dict
            Search query
        databaseName : str
            Name of the database

        Returns
        -------
        dict
            The document
        '''
        client = pymongo.MongoClient(connectionStr)
        database = client[databaseName]
        collection = database[self.username]
        return (collection.find_one(query))
