import numpy, pandas, pymysql
from time import sleep

illnesses = ['cancer', 'headache', 'pneumonia', 'flu']

names = pandas.read_csv('names_db.csv', nrows=10000).drop(['percent', 'sex'], 1)


connection = pymysql.connect(host='localhost',
                             port=3399,
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
        create_db = "CREATE DATABASE IF NOT EXISTS Medical"

        cursor.execute(create_db)

        use_medical = "USE Medical"

        cursor.execute(use_medical)

        drop_table = "DROP TABLE IF EXISTS patients"

        cursor.execute(drop_table)
                # create table        
        create_table = "CREATE TABLE patients( \
                    year INT(20), \
                    name VARCHAR(50), \
                    illness VARCHAR(50), \
                    age INT(20))" 
        
        cursor.execute(create_table)

    # commit queries   
    connection.commit()  

    for i, row in names.iterrows():
        value = (row[0], row[1], row[2], row[3])
        print 'inserting -> ' + str(i) + ' ' + str(value)

        with connection.cursor() as cursor:

            use_medical = "USE Medical"

            cursor.execute(use_medical)

            insert = "INSERT INTO patients (year, name, illness, age) VALUES (%s, %s, %s, %s)"

            cursor.execute(insert, value)


        connection.commit()

        # giving a one second time for cryptdb to recover
        sleep(1)

    with connection.cursor() as cursor:
        sql = "SELECT * FROM patients"
        cursor.execute(sql)
        result = cursor.fetchall()
        print len(result)

except Exception as e:
    print e
finally:
    connection.close()

