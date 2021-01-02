#-----------------------------------------------------------------------------
# Name:        confirmationScreen (confirmationScreen.py)
# Purpose:     To contain the confirmation screen,for confirming major decisions, of the Gradebook program
#
# Author:      Steven Wu
# Created:     2019/11/02
# Updated:     2020/01/03
#-----------------------------------------------------------------------------

from tkinter import *
from userAccount import UserAccount
from loginScreen import LoginScreen

class ConfirmationScreen(LoginScreen):
    '''
    Object which holds the confirmation screen of the program, inherits from the LoginScreen() class

    Attributes
    ----------
    username : StringVar
        Holds the entered username
    password : StringVar
        Holds the entered password
    passwordEntry : Entry
        Entry box for the password
    button : Button
        Trigers confirm()
    status : Label
        Displays outcome of login
    coursesObj : Courses
        Object which called on this class
    databaseName : str
        Name of database
    option : str
        Type of item being deleted
    deleteStatus : Label
        Label which displays the status of deletion on the MainScreen window
    docName : str
        Name of the document to be deleted
    subDocName : str 
        Name of the item to be deleted
        
    Methods
    -------
    loginVerify() -> None
        Verifies user entered credentials to log them into their account
    confirm() -> None
        Verifies user entered credentials to confirm a deletion request
    
    '''
    def __init__(self, parent,databaseName,option, deleteStatus, docName, subDocName = ''):
        '''
        Constructor to build a ConfirmationScreen object

        Parameters
        ----------
        parent : Courses
            Object which called on this class
        databaseName : str
            Name of database
        option : str
            Type of item being deleted
        deleteStatus : Label
            Label which displays the status of deletion on the MainScreen window
        docName : str
            Name of the document to be deleted
        subDocName : str, optional 
            Name of the item to be deleted, if applicable

        '''

        super().__init__()
        self.title('Confirm Deletion')
        self.coursesObj = parent
        self.databaseName = databaseName
        self.option = option
        self.deleteStatus = deleteStatus
        self.docName = docName
        self.subDocName = subDocName
        self.button.config(text = 'Confirm', command = self.confirm)

    def confirm(self) -> None:
        '''
        Verifies user entered credentials to confirm a deletion request

        Checks that the username entered matches the current account, then creates a UserAccount object 
        to verify the user's credentials. Calls on the Courses.delete() method to continue the deletion
        process.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        if self.username.get().strip() != self.coursesObj.username and self.username.get()!= '':
            self.status.config(text='Incorrect username')
        else: 
            loginAttempt = UserAccount(self.username.get().strip(), self.password.get().strip())
            self.status.config(text=loginAttempt.login())
            if loginAttempt.login() == 'Success' :
                self.coursesObj.delete(self.databaseName, self.option,self.deleteStatus,self.docName, self.subDocName)
                self.destroy()
            else:
                self.passwordEntry.delete(0, END)

