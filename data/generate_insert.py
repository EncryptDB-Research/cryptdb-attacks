import numpy, pandas, pymysql
from time import sleep

illnesses = ['cancer', 'headache', 'pneumonia', 'flu']

names = pandas.read_csv('names_db.csv', nrows=10000).drop(['percent', 'sex'], 1)


connection = pymysql.connect(host='localhost',
                             port=3399,
                             user='root',
                             password='letmein',
                             charset='utf8mb4',
                             db='Medical')

age = []
illness = []

for name in names['name']:
    age.append(numpy.random.randint(18, 40))
    illness.append(numpy.random.choice(illnesses, p=[0.40, 0.20, 0.10, 0.30]))
        
names['illness'] = illness
names['age'] = age

for row in names.iterrows():
    value = (row[1][0], row[1][1], row[1][2], row[1][3])
    print(value)
    sleep(1)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO patients (year, name, illness, age) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, value)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM patients"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    except Exception as e:
        print(e)
        connection.close()
    