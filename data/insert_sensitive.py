import numpy, pandas, pymysql
from time import sleep

illnesses = ['cancer', 'headache', 'pneumonia', 'flu']

names = pandas.read_csv('names_db.csv', nrows=20000).drop(['percent', 'sex'], 1)
names.drop_duplicates('name', inplace=True)


connection = pymysql.connect(host='localhost',
                             port=3307,
                             user='root',
                             password='letmein',
                             charset='utf8mb4')

age = []
illness = []

# setting illnesses with a prob distribution
for name in names['name']:
    age.append(numpy.random.randint(18, 40))
    illness.append(numpy.random.choice(illnesses, p=[0.40, 0.20, 0.10, 0.30]))
        
names['illness'] = illness
names['age'] = age

try:
    with connection.cursor() as cursor:
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS MedicalS")
        cursor.execute("USE MedicalS")
        cursor.execute("DROP TABLE IF EXISTS patients, records, pwdcryptdb__patients")        
        cursor.execute("cryptdb PRINCTYPE ext_user EXTERNAL")
        cursor.execute("cryptdb PRINCTYPE user")

    
        cursor.execute("CREATE TABLE activeusers(username VARCHAR(255), password VARCHAR(255))")        
        # create table        
        create_users = "CREATE TABLE patients(id INT(64), username VARCHAR(50), year INT(64))"



        cursor.execute(create_users)

        cursor.execute("cryptdb patients.username ext_user SPEAKSFOR patients.id user") 

        # cursor.execute("cryptdb patients.username encfor patient.id")
        
        create_records = "CREATE TABLE records(id integer, illness text, age integer)"

        cursor.execute(create_records)


        cursor.execute("cryptdb records.illness ENCFOR patients.id user")
        cursor.execute("cryptdb records.age ENCFOR patients.id user")


    # commit queries   
    connection.commit()  

    for i, row in names.iterrows():
        patient = (int(i), row[1], row[0])
        record = (int(i), row[2], row[3])


        with connection.cursor() as cursor:

            # cursor.execute("USE MedicalS")            

            insert_user = "INSERT INTO activeusers (username, password) VALUES (%s, %s)"
            
            cursor.execute(insert_user, (row[1], 'secret'+row[1]) )
          
            # inserting logged in user

            insert_patient = "INSERT INTO patients(id, username, year) VALUES (%s, %s, %s)"
    
            print 'inserting patient -> ' + str(patient)
            
            cursor.execute(insert_patient, patient)

            print 'inserting record  -> ' + str(record)


            insert_record = "INSERT INTO records(id, illness, age) VALUES (%s, %s, %s)"

            cursor.execute(insert_record, record)

            # remove_user = "DELETE FROM pwdcryptdb__patients where username=%s"

            # cursor.execute(remove_user, (row[1]))

        connection.commit()

        # giving a one second time for cryptdb to recover
        sleep(0.01)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM patients"
        cursor.execute(sql)
        result = cursor.fetchall()
        print len(result)

except Exception as e:
    print e
finally:
    connection.close()

