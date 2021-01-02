#-----------------------------------------------------------------------------
# Name:        register screen (registerScreen.py)
# Purpose:     To contain the registration screen of the Gradebook program
#
# Author:      Steven Wu
# Created:     2019/09/27
# Updated:     2019/12/18
#-----------------------------------------------------------------------------

from tkinter import *
from userAccount import UserAccount
from loginScreen import LoginScreen

class RegisterScreen(LoginScreen):
    '''
    Object which holds the registration screen of the program, inherits from the LoginScreen() class

    Attributes
    ----------
    startScreen : StartScreen
        The StartScreen window
    username : StringVar
        Holds the entered username
    password : StringVar
        Holds the entered password
    passwordConfirm : StringVar
        Holds the entered password confirmation
    passwordEntry : Entry
        Entry box for the password
    passwordConfirmEntry : Entry
        Entry box for password confirmation
    button : Button
        Trigers makeAccount()
    status : Label
        Displays outcome of registration

    Methods
    -------
    loginVerify() -> None
        Verifies user entered credentials to log them into their account (not used in this class)
    makeAccount() -> None
    	Attempts to create an account with credentials entered by the user
    
    '''

    def __init__(self, parent):
        '''
        Constructor to build a RegisterScreen object

        Parameters
        ----------
        parent : Toplevel
            The StartScreen window
        '''
        super().__init__(parent)
        self.title('Register')
        self.button.pack_forget()
        self.status.pack_forget()
        self.passwordConfirm = StringVar()
        Label(self, text='Confirm Password').pack()
        self.passwordConfirmEntry = Entry(self, show='*', textvariable=self.passwordConfirm)
        self.passwordConfirmEntry.pack(pady=10)
        self.button.config(text='Make Account', command= self.makeAccount)
        self.button.pack(pady=10)
        self.status.pack()

    def makeAccount(self) -> None:
        '''
    	Attempts to create an account with credentials entered by the user

        Creates a UserAccount object and uses that to attempt to create an account.
        Displays the outcome of the attempt.

        Parameters
        ----------
        None

        Returns
        -------
        None        
        '''

        registerAttempt = UserAccount(self.username.get().strip(), self.password.get().strip())
        self.status.config(text=registerAttempt.register(self.passwordConfirm.get().strip()))
        if self.status.cget('text') == 'Registration Successful':
            self.after(500, self.destroy)
        self.passwordEntry.delete(0, END)
        self.passwordConfirmEntry.delete(0, END)

