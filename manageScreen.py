# -----------------------------------------------------------------------------
# Name:        manageScreen (manageScreen.py)
# Purpose:     To contain the management screen for courses, students and 
#              assignments
#
# Author:      Steven Wu
# Created:     2019/11/18
# Updated:     2019/12/22
# -----------------------------------------------------------------------------
from tkinter import *
from courses import Courses
class ManageScreen():
    '''
    Object which holds the course, student and assignment (items) management screen

    Attributes
    ----------
    mainScreen : MainScreen
        The MainScreen window
    option : str
        Type of item being managed (i.e 'Course')
    currentAccount : str
        Current account username
    courseName : str = ''
        Name of the course the item is in if applicable  
    assignmentName : str = ''
        Name of the assignment page this screen was opened from if applicable
    addEntry : Entry
        Entry box for entering new items
    addName : StringVar
        Holds the text from addEntry
    weightingEntry :  Entry
        Entry box for entering category weightings
    addWeighting : StringVar
        Holds text from weightingEntry
    addStatus : Label
        Label which displays the outcome of attempting to add an item
    deleteEntry : Entry
        Entry box for entering item to be deleted
    deleteName : StringVar
        Holds the text from deleteEntry
    deleteStatus : Label
        Label which displays the outcome of attempting to delete an item

    Methods
    -------
    add() -> None
    	Attempts to create new items
    back() -> None
        Reverts the window back to its previous state, removing the management screen
    delete() -> None
        Deletes the user entered item
    '''

    def __init__(self, mainScreen, option, currentAccount, courseName = '', assignmentName = ''):
        '''
        Constructor to build a ManageScreen object

        Parameters
        ----------
        mainScreen : MainScreen
            The MainScreen window
        option : str
            Type of item being managed (i.e 'Course')
        currentAccount : str
            Current account username
        courseName : str, optional
            Name of the course the item is in, if applicable    
        assignmentName : st, optional
            Name of the assignment page this screen was opened from, if applicable
        '''
        self.mainScreen = mainScreen
        self.option = option
        self.currentAccount = currentAccount
        self.courseName = courseName    
        self.assignmentName = assignmentName
        self.mainScreen.clearBottomFrame()

        #self.mainScreen.bottomFrame.grid(columnspan=2)
        self.mainScreen.title('Manage '+ self.option + 's')
        
        #self.mainScreen.bottomFrame.grid(row=1, columnspan=2, sticky='NSEW')
        self.mainScreen.bottomFrame.grid_columnconfigure(0, weight=1)
        #self.mainScreen.bottomFrame.grid_columnconfigure(1, weight=1)

        self.addName = StringVar()
        Label(self.mainScreen.bottomFrame, text='Enter ' + option + ' name').grid(column=0, sticky = 'N')
        self.addEntry = Entry(self.mainScreen.bottomFrame, textvariable = self.addName)
        self.addEntry.grid(column=0, sticky = 'N')
        if self.option == 'Course':
            self.mainScreen.courseManageBtn.config(text='Back to Courses' , command=self.back)
        elif self.option == 'Student':
            self.mainScreen.courseManageBtn.grid_remove()
            self.mainScreen.assignmentManageBtn.destroy()
            self.mainScreen.studentManageBtn.config(text = 'Back to '+ self.courseName, command = self.back )
        elif self.option == 'Assignment':
            self.mainScreen.courseManageBtn.grid_remove()
            self.mainScreen.studentManageBtn.destroy()
            self.mainScreen.assignmentManageBtn.config(text = 'Back to '+ self.courseName, command = self.back )
        elif self.option == 'Category':
            self.mainScreen.categoryManageBtn.config(text = 'Back to '+self.assignmentName, command = self.back)
            self.mainScreen.courseManageBtn.grid_remove()
        if self.option =='Category' or self.option =='Assignment':
            self.addWeighting = StringVar()
            Label(self.mainScreen.bottomFrame,text = 'Enter Weighting').grid(column =0, sticky = N)
            self.weightingEntry = Entry(self.mainScreen.bottomFrame, textvariable = self.addWeighting)
            self.weightingEntry.grid(column = 0, sticky =N)
        Button(self.mainScreen.bottomFrame, text ='Add '+ option, command = self.add).grid(column=0, sticky = 'N')
        self.addStatus = Label(self.mainScreen.bottomFrame,text='')
        self.addStatus.grid(sticky = 'N')

        self.deleteName = StringVar()
        Label(self.mainScreen.bottomFrame, text='Enter ' + option+ ' name').grid(row = 0,column=2, sticky = 'N')
        self.deleteEntry = Entry(self.mainScreen.bottomFrame, textvariable = self.deleteName)
        self.deleteEntry.grid(row = 1, column=2,sticky = 'N')
        Button(self.mainScreen.bottomFrame, text ='Delete '+ option, command = self.delete).grid(row =2, column=2,sticky = 'N')
        self.deleteStatus = Label(self.mainScreen.bottomFrame,text='')
        self.deleteStatus.grid(row = 3,column=2,sticky = 'N')
    def add(self) -> None:
        '''
    	Attempts to create new items

        Creates a Courses object and attempts create the item entered by the user 
        using the object. Displays the result of the attempt.

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
            
        courseObj = Courses(self.currentAccount)
        if self.option == 'Category' or self.option =='Assignment':
            self.addStatus.config(text = courseObj.createWeighted(self.addName.get().strip(), self.addWeighting.get().strip(),self.option, self.courseName))
            self.weightingEntry.delete(0,END)
        else:
            self.addStatus.config(text=courseObj.create(self.addName.get().strip(), self.courseName, self.option))
        self.addEntry.delete(0,END)

    def back(self) -> None:
        '''
        Reverts the window back to its previous state, removing the management screen
        
        Clears the bottomFrame and displays the page the management screen was opened from

        Parameters
        ----------
        None

        Returns
        -------
        None
        '''
        self.mainScreen.clearBottomFrame()
        if self.option == 'Course':
            #self.mainScreen.courseManageBtn.config(text = 'Manage Courses', command = lambda: self.mainScreen.manage('Course'))
            self.mainScreen.title('Courses')
            self.mainScreen.loadCourses()
        elif self.option == 'Student':
            self.mainScreen.courseManageBtn.grid(column=1, row=0)
            self.mainScreen.studentManageBtn.destroy()
            self.mainScreen.courseClicked(self.courseName)
        elif self.option == 'Assignment':
            self.mainScreen.courseManageBtn.grid(column=1, row=0)
            self.mainScreen.assignmentManageBtn.destroy()
            self.mainScreen.courseClicked(self.courseName)
        elif self.option == 'Category':
            self.mainScreen.courseManageBtn.grid(column = 1, row = 0)
            self.mainScreen.categoryManageBtn.destroy()
            self.mainScreen.assignmentClicked(self.assignmentName,self.courseName, 'Course')
    def delete(self) -> None:
        '''
    	Deletes the user entered item 

        Calls on the Courses.requestDelete() method to begin the deletion process
        of the entered item.

        Parameters
        ----------
        None

        Returns
        -------
        None
        
        '''
        courseObj = Courses(self.currentAccount)
        if self.option == 'Course':
            courseObj.requestDelete('GradebookCourses',self.option,self.deleteStatus,self.deleteName.get().strip())
        elif self.option =='Student':
            courseObj.requestDelete('GradebookStudents', self.option,self.deleteStatus,self.courseName, self.deleteName.get().strip() )
        elif self.option == 'Assignment':
            courseObj.requestDelete('GradebookCourses', self.option,self.deleteStatus,self.courseName, self.deleteName.get().strip() )
        elif self.option == 'Category':
            courseObj.requestDelete('GradebookCourses',self.option,self.deleteStatus,self.deleteName.get().strip())
        self.deleteEntry.delete(0,END)
