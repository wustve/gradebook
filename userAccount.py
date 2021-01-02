#-----------------------------------------------------------------------------
# Name:        userAccount (userAccount.py)
# Purpose:     To provide login and registration functionality to the Gradebook program
#
# Author:      Steven Wu
# Created:     2019/09/25
# Updated:     2020/01/02
#-----------------------------------------------------------------------------
import pymongo
from connectionString import connectionStr
class UserAccount():
    '''
    Account registration and login object which holds the entered username and password

    Attributes
    ----------
    username : str
    	Entered username
    password : str
    	Entered password

    Methods
    -------
    login() -> str
    	Verifies login details against the account record
    register(passwordConfirm : str) -> str
    	Attempts to create new accounts
    
    '''

    def __init__(self,username,password):
        '''
        Constructor to build a UserAccount object

        Parameters
        ----------
        username : str
        	Entered username
        password : str
        	Entered password

        '''
        
        self.username = username
        self.password = password

    def login(self) -> str:
        '''
        Verifies login details against the account record

        Checks if the username matches a username in a loginDB document,
        and if the password matches the password in that document.

        Parameters
        ----------
        None

        Returns
        -------
        str
        	'Success' if the method was successful
        	'Incorrect Password' if password did not match the password found in the document
        	'Username Not Found' if the method couldn't find a datbase document containing the username
            'No username entered' if no username was entered
            'No password entered' if no password was entered
        '''
        client = pymongo.MongoClient(connectionStr)
        loginDB = client['GradebookLogin']
        loginCol = loginDB['login']
        if self.username == '':
            client.close()
            return('No username entered')
        elif self.password =='':
            client.close()
            return('No password entered')
        else:
            for x in loginCol.find({'username' : self.username}):
                if self.username == x['username']:
                    if self.password == x['password']:
                        client.close()
                        return('Success')
                    else:
                        client.close()
                        return('Incorrect Password')
            client.close()
            return ('Username Not Found')

    def register(self, passwordConfirm) -> str:
        '''
        Attempts to create new accounts

        Checks if the username already exists in the loginDB and if the password confirmation matches the password,
        then creates a loginDB document containing the username password. Also creates a
        file directory with their username to store their course information

        Parameters
        ----------
        passwordConfirm : str
            Entered password confirmation that the password attribute is compared to

        Returns
        -------
        str
        	'Registration Successful' if the method was successful
        	'Username Taken' if the method found a document containing the same username
            'Passwords do not match' if password did not match passwordConfirm
            'No username entered' if no username was entered
            'No password entered' if no password was entered
        '''

        client = pymongo.MongoClient(connectionStr)
        loginDB = client['GradebookLogin']
        loginCol = loginDB['login']
        if self.username == '':
            client.close()
            return('No username entered')
        elif self.password =='':
            client.close()
            return('No password entered')

        existingUsernames = []

        for x in loginCol.find():
            existingUsernames.append(x['username'])

        if self.username in existingUsernames:
            client.close()
            return('Username Taken')
        elif passwordConfirm == self.password:
            mydict = {'username':self.username, 'password' : self.password}
            x = loginCol.insert_one(mydict)
            client.close()
            return('Registration Successful')
        else:
            return('Passwords do not match')