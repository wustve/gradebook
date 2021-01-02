#-----------------------------------------------------------------------------
# Name:        login screen (loginScreen.py)
# Purpose:     To contain the login screen of the Gradebook program
#
# Author:      Steven Wu
# Created:     2019/09/27
# Updated:     2019/01/03
#-----------------------------------------------------------------------------

from tkinter import *
from userAccount import UserAccount

class LoginScreen(Toplevel):
    '''
    Object which holds the login screen of the program, inherits from the Toplevel() class

    Attributes
    ----------
    startScreen : StartScreen
        The StartScreen window
    username : StringVar
        Holds the entered username
    password : StringVar
        Holds the entered password
    passwordEntry : Entry
        Entry box for the password
    button : Button
        Triggers loginVerify()
    status : Label
        Displays outcome of login
    
    Methods
    -------
    loginVerify() -> None
    	Verifies user entered credentials to log them into their account
    
    '''

    def __init__(self,parent = None):
        '''
        Constructor to build a LoginScreen object

        Parameters
        ----------
        parent : StartScreen, optional
            The StartScreen window, if applicable
        '''

        super().__init__()
        self.title('Login')
        self.geometry('300x250')
        self.grab_set()
        self.resizable(width=False, height=False)
        self.startScreen = parent
        self.username = StringVar()
        self.password = StringVar()
        Label(self, text='Note: Spaces on the ends of entries will be removed\nUsername').pack()
        usernameEntry = Entry(self, textvariable=self.username)
        usernameEntry.pack(pady=10)
        Label(self, text='Password').pack()
        self.passwordEntry = Entry(self, show='*', textvariable=self.password)
        self.passwordEntry.pack(pady=10)
        self.button = Button(self, text='Login', width=10, command = self.loginVerify)
        self.button.pack(pady=10)
        self.status = Label(self, text='')
        self.status.pack()

    def loginVerify(self) -> None:
        '''
        Verifies user entered credentials to log them into their account

        Creates a UserAccount object and uses that to verify the user's credentials.
        Displays the result if verification was unsucessful.

        Parameters
        ----------
        None
        
        Returns
        -------
        None
        '''
        loginAttempt = UserAccount(self.username.get().strip(), self.password.get().strip())
        self.status.config(text=loginAttempt.login())
        if loginAttempt.login() == 'Success':
            self.destroy()
            self.startScreen.mainScreen.currentAccount = loginAttempt.username
            self.startScreen.destroy()
            self.startScreen.mainScreen.deiconify()
            self.startScreen.mainScreen.state('zoomed')
            self.startScreen.mainScreen.loadCourses()

        else:
            self.passwordEntry.delete(0, END)
    
