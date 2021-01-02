import pymongo
import random
import string
from connectionString import connectionStr
client = pymongo.MongoClient(connectionStr)
studentDB = client["GradebookStudents"]
studentCol = studentDB["123"]
#updatedAssignments = studentCol.find_one({"student name": "bill","course name" : "SCH4U9-C"})

for i in range (500000):
    
    studentCol.update_one({"course name" : "SCH4U9-C"}, { "$push" :  {"assignments":{"assignment name" : "k", "category 1": 123,"category 2": 123,"category 3": 123,"category 4": 123} }})
    print (i)
    '''
    except Exception as e:
        print (e)
        updatedAssignments = {"assignments":[{"assignment name" : ha, "category 1": 123,"category 2": 123,"category 3": 123,"category 4": 123}] }
        studentCol.update_one({"course name" : "SCH4U9-C"}, { "$set" : updatedAssignments} )
    '''
client.close()
