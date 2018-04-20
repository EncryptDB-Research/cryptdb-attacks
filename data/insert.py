"""
Created by Joannier Pinales 
Description: Inserts data into the database by giving a specific distrubution to the data.
"""

import numpy, pandas, pymysql
from time import sleep

illnesses = ['cancer', 'headache', 'pneumonia', 'flu']

names = pandas.read_csv('names_db.csv', nrows=50000).drop(['percent', 'sex'], 1)
names.drop_duplicates('name', inplace=True)

connection = pymysql.connect(host='127.0.0.1',
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

print 'total count: ', len(names['illness'])

try:
    with connection.cursor() as cursor:
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS Medical")
        cursor.execute("USE Medical")
        cursor.execute("DROP TABLE IF EXISTS patients, records")        

        # create table        
        create_users =  "CREATE TABLE patients(id INT(64) NOT NULL AUTO_INCREMENT, username VARCHAR(50), year INT(64), PRIMARY KEY (id))"

        cursor.execute(create_users)

        create_records = "CREATE TABLE records(id INT(64) NOT NULL AUTO_INCREMENT, illness VARCHAR(50), age INT(64), PRIMARY KEY (id) )"

        cursor.execute(create_records)

    # commit queries   
    connection.commit()  

    for i, row in names.iterrows():
        patient = (row[1], row[0])
        record = (row[2], row[3])


        with connection.cursor() as cursor:

            insert_patient = "INSERT INTO patients(username, year) VALUES (%s, %s)"
    
            print 'inserting patient -> ' + str(patient)
            
            cursor.execute(insert_patient, patient)

            print 'inserting record  -> ' + str(record)

            insert_record = "INSERT INTO records(illness, age) VALUES (%s, %s)"

            cursor.execute(insert_record, record)

        connection.commit()

        # giving a one second time for cryptdb to recover
        sleep(0.01)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM records"
        cursor.execute(sql)
        result = cursor.fetchall()
        print len(result)

except Exception as e:
    print e
finally:
    connection.close()

