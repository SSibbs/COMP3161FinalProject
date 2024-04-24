from faker import Faker
from faker.providers import DynamicProvider
import random


fake = Faker()
sqls = []
sqlsStu = []
sqlsAcc = []
cids = []
lecturers = []
lecmax = []
fids = []
mtids = []
secids = []

course_provider = DynamicProvider(
    provider_name = "course",
    elements = ["Intro to Computing", "Object-oriented Programming","Math for Computing","Computing and Society", "Discrete Mathematics for Computer Science","Analysis of Algorithms","Digital Logic Design","Software Engineering","Object Technology","Net-Centric Computing","Computer Organisation"," Operating Systems","Introduction to Artificial Intelligence","Database Management Systems","Language Processors","Theory of Computation","Real-Time Embedded Systems","Group Project","Internship in Computing","Project Management"]
)

course_provider = DynamicProvider(
    provider_name = "item_type",
    elements = ["link", "file", "slide"]
)

fake.add_provider(course_provider)

def real_job(fake):
    job = fake.job()
    job = job.replace("'","")
    return job

#INSERT INTO ACCOUNT
for i in range(1):
    id = 9000 + i
    fname = fake.first_name()
    lname= fake.last_name()
    type = "Admin"
    pa = type + str(id)
    sql = "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}')".format(id, type, pa,fname,lname)
    sqls.append(sql)

for i in range(10000):
    id = i
    fname = fake.first_name()
    lname= fake.last_name()
    type = "Student"
    pa = fname + str(random.randint(0,200))
    sql = "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{})".format(id, type, pa,fname,lname)
    sqls.append(sql)


for _ in range(3):
    lid = random.randint(1011,1050)
    fname = fake.first_name()
    lname= fake.last_name()
    lecturers.append(lid) 
    pa = fname + str(random.randint(0,20))
    type = "Lecturer"

    sql = "INSERT INTO Account (UserID, uType, Pass, FirstName, LastName) VALUES ('{}','{}','{}','{}','{}')".format(lid, type, pa,fname,lname)
    sqls.append(sql)


#INSERT INTO COURSE   
for i in range(20):
    cid = 3001 + i
    c_code = "COMP" + str(cid)
    cname = fake.unique.course()
    cids.append(cid)

for cid in cids:
    sql = "INSERT INTO Course (CourseID, CourseName, CourseCode) VALUES ('{}','{}','{}')".format(cid,cname,c_code)
    sqls.append(sql)

#INSERT INTO SECTION
for cid in cids:
    for i in range(0,2):
        secid = i +1
        sql = "INSERT INTO Section(CourseID, SectionID) VALUES ('{}','{}')".format(cid,secid)
        sqls.append(sql)

#INSERT INTO ITEM
for secid in secids:
    for i in range(0,4):
        itemid = i + 20
        title = "Learning File" + " " + str(i)
        type = fake.unique.item_type()
        sql = "INSERT INTO Section(SectionID,ItemID,title,itype) VALUES ('{}','{}','{}','{}')".format(secid,itemid,title,type)


#INSERT INTO TEACHES
for cid in cids:
    lid = lecturers.pop(0)
    lecturers.append(lid)
    sql = "INSERT INTO Teaches (CourseID, UserID) VALUES ('{}','{}')".format(cid,lid)

'''
for i in range(30):
    cid = 4001 + i
    c_code = "INFO" + str(cid)
    cname = "IT" + " " + real_job(fake)
    sql = "INSERT INTO Course (CourseID, CourseName, CourseCode) VALUES ('{}','{}','{}')".format(cid,cname,c_code)
    sqls.append(sql)
    cids.append(cid)
'''

#INSERT INTO ENROLL
for s in sqls:
    if s.startswith("INSERT INTO Account"):
        id = s.split("'")[1]
        type = s.split("'")[2]

        if type == "Student":
            as_courses = set()
            i = random.randint(3,6)

            for _ in range(i):
                while True:
                    cid = random.choice(cids)
                    if cid not in as_courses:
                        as_courses.add(cid)
                        break
                grade = random.randint(0,100)
                sql = "INSERT INTO Enroll (CourseID, StudentID, AvGrade) VALUES ('{}','{}','{}')".format(cid,id,grade)
                sqls.append(sql)

#INSERT INTO ASSIGNMENT
i = 1
for s in sqls:
    if s.startswith("INSERT INTO Enroll"):
        cid = s.split("'")[1]
        id = s.split("'")[2]
        aid = 1111 + i
        i+=1
        grade = random.randint(0,100)
        sdate = fake.date()

        sql = "INSERT INTO Assignment (AssID, UserID, StudentID,Grade,date_submit) VALUES ('{}','{}','{}','{}','{}')".format(aid,id,cid,grade,sdate)
        sqls.append(sql)


#INSERT INTO EVENT
i = random.randint(0,100)
for cid in cids:
    eid = 2222 + i
    ddate = fake.date()
    i + 1
    sql = "INSERT INTO Event (EventID, CourseID, DueDate) VALUES ('{}','{}','{}')".format(eid,cid,ddate)
    sqls.append(sql)

#INSERT INTO FORUM
for i in range(5):
    fid = i
    fids.append(fid)
    cid = random.choice(cids)
    fname = "What do you think about" + fake.unique.color()
    sql = "INSERT INTO Forum (ForumID, CourseID, ForumName) VALUES ('{}','{}','{}')".format(fid,cid,fname)
    sqls.append(sql)

#INSERT INTO THREAD
for i in range(2):
    tid = 100 + random.randint(0,100)
    fid = random.choice(fids)
    title = fake.sentence(10)
    body = fake.sentence(50)
    mtids.append(tid)

    sql = "INSERT INTO Thread (ThreadID, ForumID, Title, Body) VALUES ('{}','{}','{}','{}')".format(tid,fid,title,body)
    sqls.append(sql)

#INSERT INTO REPLY
for i in range(2):
    mtid = random.choice(mtids)
    rid = 200 + random.randint(0,200)
    body = fake.sentence(20)
    
    for s in sqls:
        if s.startswith("INSERT INTO Account"):
            id = s.split("'")[1]
            sql = "INSERT INTO Reply (MainThreadID, ReplyID, UserID,ReplyBody) VALUES ('{}','{}','{}','{}')".format(mtid,rid,id,body)
            sqls.append(sql)


with open(r'/home/nacho/repos/COMP3161FinalProject/insert.sql','w') as f:
    for i, sql in enumerate(sqls):
        f.write(sql + '\n')