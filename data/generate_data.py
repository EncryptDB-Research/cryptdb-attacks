import numpy, pandas

illnesses = ['cancer', 'headache', 'pneumonia', 'flu']

names = pandas.read_csv('names.csv').drop(['percent', 'sex'], 1)

age = []
illness = []

for name in names['name']:
    age.append(numpy.random.randint(18, 40))
    illness.append(numpy.random.choice(illnesses, p=[0.25, 0.25, 0.25, 0.25]))
        
names['illness'] = illness
names['age'] = age

names.to_csv('medical.csv', index=False)
