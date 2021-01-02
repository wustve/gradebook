#-----------------------------------------------------------------------------
# Name:        startScreen (startScreen.py)
# Purpose:     To contain the start screen of the Gradebook program
#
# Author:      Steven Wu
# Created:     2019/09/27
# Updated:     2019/10/28
#-----------------------------------------------------------------------------

from tkinter import *
from loginScreen import LoginScreen
from registerScreen import RegisterScreen

class StartScreen(Toplevel):
    '''
    Object which holes the start screen of the program, inherits from the Toplevel() class

    Attributes
    ----------
    mainScreen : MainScreen
        The MainScreen window

    
    Methods
    -------
    closed() -> None
        Closes the MainScreen window
    login() -> None
    	Opens the login window
    register() -> None
    	Opens the registration window

    
    '''
    def __init__(self,parent):
        '''
        Constructor to build a StartScreen object

        Parameters
        ----------
        parent : MainScreen
            The MainScreen window

        '''
        super().__init__()
        self.mainScreen = parent
        self.geometry('300x250')
        self.title('Welcome')
        self.resizable(width=False, height=False)
        loginBtn = Button(self, text='Login', font=('Helvetica', 20), command = self.login)
        loginBtn.pack(expand=True, fill = BOTH, pady=20, padx=30)
        registerBtn = Button(self, text='Register', font=('Helvetica', 20), command = self.register)
        registerBtn.pack(expand=True, fill = BOTH, pady=20, padx=30)
        self.protocol('WM_DELETE_WINDOW', self.closed)
    def closed(self) -> None:
        '''
        Closes the MainScreen Window

        Closes the MainScreen Window when the StartScreen is closed

        Parameters
        ----------
        None

        Returns
        -------
        None        
        '''

        self.mainScreen.destroy()
        
    def login(self) -> None:
        '''
        Opens the login window

        Opens the login in window by creating a LoginScreen object when the
        login button is pressed

        Parameters
        ----------
        None

        Returns
        -------
        None        
        '''
        LoginScreen(self)
    def register(self) -> None:
        '''
        Opens the registration window

        Opens the registration in window by creating a RegisterScreen object when the
        register button is pressed

        Parameters
        ----------
        None

        Returns
        -------
        None        
        '''
        RegisterScreen(self)
        