# -----------------------------------------------------------------------------
# Name:        Gradebook Main File (main.py)
# Purpose:     To contain the main screen of the Gradebook program
#
# Author:      Steven Wu
# Created:     2019/09/05
# Updated:     2020/01/08
# -----------------------------------------------------------------------------
from tkinter import *
from courses import Courses
from startScreen import StartScreen
from manageScreen import ManageScreen
from marks import Marks
from assignments import Assignments
from math import floor
#pymongo and dnspython libraries MUST BE INSTALLED

class MainScreen(Tk):
    '''
    Object which holds the main window of the program, inherits from the TK() class.

    Attributes
    ----------
    currentAccount : str
        Current account username
    topFrame : Frame
        Frame which holds the navigation buttons
    courseManageBtn : Button
        Triggers the course management screen
    scrollCanvas : Canvas
        Canvas which holds the bottom frame so that it is scrollable
    bottomFrame : Frame
        Frame which holds the main widgets of the window
    yScroll: ScrollBar
        Vertical scroll bar
    studentManageBtn : Button
        Triggers the student management screen
    assignmentManageBtn : Button
        Triggers the assignment management screen
    categoryManageBtn : Button
        Triggers the category management screen
    saveStatus : Label
        Label which displays the result of trying to save an assignment

    Methods
    -------
    loadCourses() -> None
        Displays existing courses as buttons
    clearBottomFrame() -> None
    	Reinitializes/creates the bottomFrame
    courseClicked(courseName : str)-> None
    	Loads the page of a specific course
    studentClicked(studentName : str, courseName : str)-> None
        Loads the page of a specific student
    assignmentClicked(assignmentName : str, courseName : str, assignmentType : str, studentName : str='',markObj : Marks= None)-> None
    	Loads the page of a specific assignment
    saveAssignment(assignmentName : str,courseName : str, assignmentType : str, entries : str, studentName : str ='') -> None
        Saves an assignment to the database
    '''

    def __init__(self):
        '''
        Constructor for MainScreen objects

        Parameters
        ----------
        None

        '''

        super().__init__()
        self.geometry('640x360')
        self.currentAccount = ''
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1,weight = 0)
        self.topFrame = Frame(self, bg='Red')
        self.topFrame.grid(row=0, columnspan = 2,sticky='EW')
        self.topFrame.grid_rowconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure(0, weight=1)
        self.topFrame.grid_columnconfigure(1, weight=1)
        self.topFrame.grid_columnconfigure(2, weight=1)
        
        self.clearBottomFrame()
        self.courseManageBtn = Button(self.topFrame, height=1, width=14, text='Manage Courses',command=lambda: ManageScreen(self, 'Course', self.currentAccount))
        self.courseManageBtn.grid(column=1, row=0)
        self.withdraw()
        StartScreen(self)
    def loadCourses(self) -> None:
        '''
    	Displays existing courses as buttons

        Creates a button for every course document found under the current account in the database.
        Each button has a course name as its text and they are displayed in alphanumeric order.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        -------
        AttributeError
            If the MainScreen object (self) does not have a studentManageBtn or assignmentManageBtn attribute
        KeyError
            If a document in 'GradebookCourses' does not have an 'assignments' key
        '''
        self.clearBottomFrame()
        self.title('Courses')

        try:
            self.studentManageBtn.destroy()
            self.assignmentManageBtn.destroy()
        except Exception as e:
            pass
        courseObj = Courses(self.currentAccount)
        coursesList = courseObj.docsGet('GradebookCourses',{'course name':{'$exists': True}})
        row = 0
        for x in sorted(coursesList, key=lambda y: y['course name'].lower()):
            Button(self.bottomFrame, text=x['course name'], font=('Helvetica', 40),command=lambda y=x: self.courseClicked(y['course name'])).grid(row = row,column=0, sticky='EW')
            try:
                Label(self.bottomFrame, text = str(len(x['assignments']))+'\nAssignment(s)').grid(row = row,column =2, sticky = 'EW')
            except:
                Label(self.bottomFrame, text = '0\nAssignment(s)').grid(row = row,column =2, sticky = 'EW')
            studentCount = 0
            Label(self.bottomFrame, text = str(len(courseObj.docsGet('GradebookStudents',{'course name':x['course name']})))+'\nStudent(s)').grid(row = row, column = 1, sticky = 'EW')

            row += 1
        self.courseManageBtn.config(text='Manage Courses',command=lambda:  ManageScreen(self, 'Course', self.currentAccount))

    def clearBottomFrame(self) -> None:
        '''
    	Reinitializes/creates the bottomFrame

        Reinitializes/creates the bottomFrame (and the canvas it is inside) to clear the widgets from it

        Parameters
        ----------
        None

        Returns
        -------
        None

        '''

        self.scrollCanvas = Canvas(self)
        self.scrollCanvas.grid(row = 1,column=0,sticky='NSEW')
        self.bottomFrame = Frame(self.scrollCanvas)

        self.scrollCanvasFrame = self.scrollCanvas.create_window((0,0),window = self.bottomFrame, anchor = 'nw', tags = 'self.bottomFrame')
        self.yScroll = Scrollbar(self, orient='vertical', command = self.scrollCanvas.yview)
        self.scrollCanvas.configure(yscrollcommand=self.yScroll.set)
        #self.xScroll = Scrollbar(self, orient='horizontal', command = self.scrollCanvas.xview)
        #self.scrollCanvas.configure(xscrollcommand=self.xScroll.set)

        self.bottomFrame.bind('<Configure>',  lambda event: self.scrollCanvas.configure(scrollregion=self.scrollCanvas.bbox('all')))
        self.scrollCanvas.bind('<Configure>',lambda event: self.scrollCanvas.itemconfig(self.scrollCanvasFrame,width = event.width))
        self.scrollCanvas.bind_all('<MouseWheel>', lambda event: self.scrollCanvas.yview_scroll(int(-1 * (event.delta / 120)), 'units'))
        #self.bottomFrame.grid(sticky='EW')
        self.bottomFrame.grid_columnconfigure(0, weight=2)
        self.bottomFrame.grid_columnconfigure(1, weight=1)
        self.bottomFrame.grid_columnconfigure(2, weight=1)
        self.yScroll.grid(row = 1,column = 1,sticky = NS)
        
    def courseClicked(self, courseName) -> None:
        '''
    	Loads the page of a specific course

        Displays the students, assignments and assignment weightings in the course

        Parameters
        ----------
        courseName : str
            Name of the course

        Returns
        -------
        None
        
        Raises
        -------
        AttributeError
            If the MainScreen object (self) does not have a categoryManageBtn attribute
        KeyError
            If the document in 'GradebookCourses' does not have an 'assignments' key
        '''

        self.clearBottomFrame()
        try:
            self.categoryManageBtn.destroy()
        except Exception as e:
            pass
        self.title(courseName)
        self.courseManageBtn.config(text='Return to courses', command=self.loadCourses)
        self.studentManageBtn = Button(self.topFrame, text='Manage Students ', height=1, width=14,command=lambda: ManageScreen(self, 'Student', self.currentAccount, courseName))
        self.studentManageBtn.grid(column=0, row=0)
        self.assignmentManageBtn = Button(self.topFrame, text='Manage Assignments', height=1, width=14,command=lambda: ManageScreen(self, 'Assignment', self.currentAccount, courseName))
        self.assignmentManageBtn.grid(column=2, row=0)
        studentInfo = Courses(self.currentAccount).docsGet('GradebookStudents',{'course name':courseName})
        assignmentInfo = Courses(self.currentAccount).docGet({'course name':courseName}, 'GradebookCourses')
        Label(self.bottomFrame, text = 'Students').grid(row = 0, column = 0, sticky= EW)
        row = 1
        for x in sorted(studentInfo, key = lambda y: y['student name'].lower()):
            #if x['course name'] == courseName:
            Button(self.bottomFrame, text=x['student name'], font=('Helvetica', 40), command=lambda y = x: self.studentClicked(y['student name'],courseName)).grid(row = row,column=0, sticky='EW')
            row+=1
        Label(self.bottomFrame, text = 'Assignments').grid(row = 0, column = 1, sticky= EW)
        Label(self.bottomFrame, text='Weightings').grid(row=0, column=2, sticky=EW)
        row = 1
        try:
            for x in sorted(assignmentInfo['assignments'], key = lambda y: y['assignment name'].lower()):
                Button(self.bottomFrame, text=x['assignment name'], font=('Helvetica', 40),command=lambda y = x: self.assignmentClicked(y['assignment name'],courseName, 'Course')).grid(row = row,column=1, sticky='EW')
                Label(self.bottomFrame,text = x['weighting'], font=('Helvetica', 40)).grid(row = row,column=2, sticky='EW')
                row+=1
        except:
            pass

    def studentClicked(self, studentName, courseName)-> None:
        '''
    	Loads the page of a specific student

        Displays the student's assignments, assignment weightings and marks in the specified course

        Parameters
        ----------
        studentName : str
            Name of the student
        courseName : str
            Name of the course

        Returns
        -------
        ZeroDivisionError
            If there are no assignments with categories (with >0 weighting) assigned more than 0 marks
        KeyError
            If the document in 'GradebookCourses' does not have an 'assignments' key
        ZeroDivisionError
            If there is no instance of the assignment in the student's document (mark of 0 is divided by a weighting of 0)
        IndexError
            If index used on markObj.assignmentMarks is out of range
        KeyError
            If dict in markObj.assignmentList does not have an 'adjusted weighting' key
        '''
        self.clearBottomFrame()
        self.title(studentName)
        self.studentManageBtn.destroy()
        self.assignmentManageBtn.destroy()
        self.courseManageBtn.config(text = 'Return to '+courseName, command = lambda:self.courseClicked(courseName))
        markObj = Marks(self.currentAccount, courseName, studentName)
        markObj.defaultSort()

        Label(self.bottomFrame, text = 'Default Mark(%)').grid(row = 0, column = 1, sticky= EW)
        Label(self.bottomFrame, text = 'Adjusted Mark(%)').grid(row = 0, column = 2, sticky= EW)
        Label(self.bottomFrame, text='Total Mark', font=('Helvetica', 40)).grid(row = 1,column=0, sticky='EW')
        try:
            Label(self.bottomFrame, text=str(round(markObj.totalMark(),2)), font=('Helvetica', 40)).grid(row = 1,column=1, sticky='EW')
            Label(self.bottomFrame, text=str(round(markObj.totalMarkAdjusted(),2)), font=('Helvetica', 40)).grid(row = 1,column=2, sticky='EW')
        except Exception as e:
            #print (e)
            Label(self.bottomFrame, text='N/A', font=('Helvetica', 40)).grid(row = 1,column=1, sticky='EW')
            Label(self.bottomFrame, text='N/A', font=('Helvetica', 40)).grid(row = 1,column=2, sticky='EW')
        Label(self.bottomFrame, text = 'Assignments').grid(row = 2, column = 0, sticky= EW)
        Label(self.bottomFrame, text = 'Effective Weighting').grid(row = 2, column = 1, sticky= EW)
        Label(self.bottomFrame, text = 'Mark(%)').grid(row = 2, column = 2, sticky= EW)

        row = 3
        minIndex = 0
        try:
            for x in sorted(Courses(self.currentAccount).docGet({'course name':courseName},'GradebookCourses')["assignments"], key = lambda y:y['assignment name'].lower()):
                try: 
                    Button(self.bottomFrame, text=x['assignment name'], font=('Helvetica', 40),command=lambda y = x: self.assignmentClicked(y['assignment name'],courseName, 'Student', studentName, markObj)).grid(row = row,column=0, sticky='EW')
                    if markObj.assignmentList[minIndex].assignmentMarks['assignment name'] == x['assignment name']:
                        Label(self.bottomFrame, text=str(round(markObj.assignmentList[minIndex].calculate()[0],2)), font=('Helvetica', 40)).grid(row = row,column=2, sticky='EW')
                        try:
                            Label(self.bottomFrame, text=str(round(markObj.assignmentList[minIndex].assignmentMarks['adjusted weighting'],2)), font=('Helvetica', 40)).grid(row = row,column=1, sticky='EW')
                        except:
                            Label(self.bottomFrame, text=str(round(x['weighting'],2)), font=('Helvetica', 40)).grid(row = row,column=1, sticky='EW')
                        minIndex+=1
                    else:
                        Label(self.bottomFrame, text='N/A', font=('Helvetica', 40)).grid(row = row,column=2, sticky='EW')
                        Label(self.bottomFrame, text='0', font=('Helvetica', 40)).grid(row = row,column=1, sticky='EW')
                except ZeroDivisionError as e:
                    #print(e)
                    Label(self.bottomFrame, text='N/A', font=('Helvetica', 40)).grid(row = row,column=2, sticky='EW')
                    Label(self.bottomFrame, text='0', font=('Helvetica', 40)).grid(row = row,column=1, sticky='EW')
                    minIndex+=1
                except IndexError as e:
                    #print(e)
                    Label(self.bottomFrame, text='N/A', font=('Helvetica', 40)).grid(row = row,column=2, sticky='EW')
                    Label(self.bottomFrame, text='0', font=('Helvetica', 40)).grid(row = row,column=1, sticky='EW')
                row+=1
        except:
            pass
    def assignmentClicked(self, assignmentName, courseName, assignmentType, studentName='', markObj = None)-> None:
        '''
    	Loads the page of a specific assignment

        Displays and allows for editing of course wide master assignments (which contain the total marks, weightings, etc.) 
        as well as student specific assignment results.

        Parameters
        ----------
        assignmentName : str
            Name of the assignment
        courseName : str
            Name of the course
        assignmentType : str
            Type of assignment clicked
        studentName : str, optional
            Name of the student who the assignment belongs to, if applicable
        markObj : Marks, optional
            Mark object containing the student's saved assignment info

        Returns
        -------
        None

        Raises
        -------
        KeyError
            If document in database does not contain 'assignments' key
        IndexError
            If markObj.assignmentList has a size of 0
        KeyError
            If existingAssignment does not contain a category name as a key
        KeyError
            If existingAssignment does not contain a 'adjusted weighting' as a key
        KeyError
            If existingAssignment does not contain a 'weighting' as a key
        '''
        self.clearBottomFrame()
        self.bottomFrame.grid_columnconfigure(0, weight=1)
        self.title(assignmentName)
        self.studentManageBtn.destroy()
        self.assignmentManageBtn.destroy()
        if assignmentType == 'Course':
            self.courseManageBtn.config(text = 'Return to '+courseName, command = lambda:self.courseClicked(courseName))
            self.categoryManageBtn = Button(self.topFrame, text='Manage Categories', height=1, width=14,command=lambda: ManageScreen(self, 'Category', self.currentAccount, courseName, assignmentName))
            self.categoryManageBtn.grid(column = 0,row =0)
            query = {'course name':courseName}
            database= 'GradebookCourses'
            Label(self.bottomFrame, text='Weighting', font=('Helvetica', 20)).grid(column=1, row=0, sticky=EW)
        elif assignmentType == 'Student':
            self.courseManageBtn.config(text = 'Return to '+studentName, command = lambda:self.studentClicked(studentName, courseName))
            query = {'course name':courseName, 'student name': studentName}
            database= 'GradebookStudents'
            Label(self.bottomFrame, text="Student's Marks", font=('Helvetica', 20)).grid(column=1, row=0, sticky=EW)

        row = 0
        Label(self.bottomFrame, text='Category', font=('Helvetica', 20)).grid(column=0, row=0, sticky=EW)
        Label(self.bottomFrame, text='Total Marks', font=('Helvetica', 20)).grid(column=2, row=0, sticky=EW)
        entries = {'assignment name':assignmentName}
        existingAssignment = {}
        if markObj == None:
            try:
                for x in Courses(self.currentAccount).docGet(query, database)['assignments']:
                    if x['assignment name'] == assignmentName:
                        existingAssignment = x
                        break
            except:
                pass
        else:
            try:
                min = 0
                max = len(markObj.assignmentList)
                while max>min:
                    mid= floor((max+min)/2)
                    if markObj.assignmentList[mid].assignmentMarks['assignment name'].lower() < assignmentName.lower():
                        min = mid+1
                    else:
                        max = mid
                if min == max and markObj.assignmentList[min].assignmentMarks['assignment name'].lower() == assignmentName.lower():
                    existingAssignment = markObj.assignmentList[min].assignmentMarks    
            except:
                pass

        if assignmentType == 'Course':
            categories = Courses(self.currentAccount).docsGet('GradebookCourses', {'category':{'$exists': True}})
            for x in sorted(categories, key = lambda y : y['category'].lower()):
                #try:
                row += 1
                Label(self.bottomFrame, text = x['category'],font=('Helvetica', 10)).grid(column = 0, row = row, sticky= EW)
                Label(self.bottomFrame, text = str(x['weighting']),font=('Helvetica', 10)).grid(column = 1, row = row, sticky= EW)
                entries[x['category']]= StringVar()
                try:
                    assignmentEntry = Entry(self.bottomFrame, textvariable = entries[x['category']])
                    assignmentEntry.grid(column = 2, row = row, sticky = EW)
                    assignmentEntry.insert(0, existingAssignment[x['category']])
                except:
                    assignmentEntry.insert(0,'0')

                #except:
                #    pass
            row+=1

            Label(self.bottomFrame, text = 'Total assignment weighting',font=('Helvetica', 10)).grid(column = 0, row = row, sticky= EW)
            entries['weighting'] = StringVar()
            assignmentEntry = Entry(self.bottomFrame, textvariable = entries['weighting'])
            assignmentEntry.grid(column = 1, row = row, sticky = EW)
            assignmentEntry.insert(0, existingAssignment['weighting'])

        elif assignmentType == 'Student':
            

            masterAssignment = {}
            try:
                for x in Courses(self.currentAccount).docGet({'course name':courseName},'GradebookCourses')['assignments']:
                    if x['assignment name'] == assignmentName:
                        masterAssignment = x
                        break
            except:
                pass
            for x in sorted(list(masterAssignment.keys()), key = lambda y: y.lower()):
                if x!= 'assignment name' and x!= 'weighting' and masterAssignment[x] != '0' and masterAssignment[x] != 0:
                    row += 1
                    Label(self.bottomFrame, text = x,font=('Helvetica', 10)).grid(column = 0, row = row, sticky= EW)
                    entries[x]= StringVar()
                    try:
                        assignmentEntry = Entry(self.bottomFrame, textvariable = entries[x])
                        assignmentEntry.grid(column = 1, row = row, sticky = EW)
                        assignmentEntry.insert(0, existingAssignment[x])
                    except:
                        assignmentEntry.insert(0,'0.0')
                    Label(self.bottomFrame, text = masterAssignment[x],font=('Helvetica', 10)).grid(column = 2, row = row, sticky= EW)
            row+=1

            Label(self.bottomFrame, text = 'Effective assignment weighting',font=('Helvetica', 10)).grid(column = 0, row = row, sticky= EW)
            entries['adjusted weighting'] = StringVar()
            entries['weighting'] = StringVar()
            try:
                assignmentEntry = Entry(self.bottomFrame, textvariable = entries['adjusted weighting'])
                assignmentEntry.grid(column = 1, row = row, sticky = EW)
                assignmentEntry.insert(0, existingAssignment['adjusted weighting'])
            except:
                try:
                    assignmentEntry.insert(0,existingAssignment['weighting'])
                except:
                    assignmentEntry.insert(0,masterAssignment['weighting'])
            row+=1
            Label(self.bottomFrame, text = 'Default assignment weighting',font=('Helvetica', 10)).grid(column = 0, row = row, sticky= EW)
            assignmentEntry = Entry(self.bottomFrame, textvariable = entries['weighting'])
            assignmentEntry.grid(column = 1, row = row, sticky = EW)
            assignmentEntry.insert(0, masterAssignment['weighting'])
            assignmentEntry.config(state = DISABLED)
        self.saveStatus = Label(self.bottomFrame, text = '')
        Button(self.bottomFrame, text = 'Save', command = lambda : self.saveAssignment(assignmentName,courseName,assignmentType,entries,studentName)).grid(column = 1, sticky =EW)
        self.saveStatus.grid(column = 1, sticky = EW)

    def saveAssignment(self, assignmentName,courseName, assignmentType, entries, studentName ='') -> None:
        '''
        Saves an assignment to the database

        Calls on the Assignment class to save assignment marks and weightings

        Parameters
        ----------
        assignmentName : str
            Name of the assignment
        courseName : str
            Name of the course
        assignmentType : str
            Type of assignment
        entires : dict
            Marks and weightings entered into the assignment
        studentName : str
            Name of the student who the assignment belongs to, if applicable

        Returns
        -------
        None

        Raises
        -------
        AttributeError
            If the MainScreen object (self) does not have a categoryManageBtn attribute

        '''
        saveMessage = Assignments(self.currentAccount, courseName, entries, studentName).save(assignmentType)
        try:
            self.categoryManageBtn.destroy()
        except:
            pass
        self.assignmentClicked(assignmentName, courseName,assignmentType,studentName)
        self.saveStatus.config(text= saveMessage)
MainScreen().mainloop()
'''
Since computer memory is not unlimited, variables cannot store an infinite number information.
This can become an issue where extremely long values cannot be stored properly, which leads to errors
where values cant be stored or values being approximated. For example, long repeating decimals will not have an infinite number 
of digits stored by the computer, only a certain amount will be and the number will be rounded, leading to inaccuracies
Float max = 6-9 digits
Double = 15-17 digits
Int = max value typically 2^31-1 on 32 bit, but in newer python there is no hard limit, based on available memory
String,list, etc. = 2^31 - 1 on 32 bit systems
Long has no limit
Byte: 8 bits, 2^8
dict, Object = 2^31-1 bytes (~2GB) on 32 bit systems, 
'''