import sys
import MySQLdb
import getpass

UNIQUE = 0
LEVEL = 0
FIN = None

#NODE Class to save information
class NODE:
	def __init__(self, value, original):
		self.left = None
		self.right = None
		self.val = value	#Binary value
		self.orig = original	#Original value
		self.count = 1

#TREE Class to organize NODEs
class TREE:
	def __init__(self):
		self.root = None
	def getRoot(self):
		return self.root
	def add(self, value, original):
		global UNIQUE
		if(self.root == None):
			self.root = NODE(value, original)
			UNIQUE += 1
		else:
			self._add(value, self.root, original)
	def _add(self, value, node, original):
		global UNIQUE
		if(value < node.val):
			if(node.left is not None):
				self._add(value, node.left, original)
			else:
				node.left = NODE(value, original)
				UNIQUE += 1
		if(value > node.val):
			if(node.right is not None):
				self._add(value, node.right, original)
			else:
				node.right = NODE(value, original)
				UNIQUE += 1
		if(value == node.val):
			node.count = node.count + 1
	def printTREE(self, count, fin):
		global FIN
		FIN = open(fin, 'w')
		FIN.write('Frequency\tValue\n')
		if(self.root is not None):
			self._printTREE(self.root, count)
		FIN.close()
	
	def _printTREE(self, node, count):
		if(node is not None):
			self._printTREE(node.left, count)
			stat = float(node.count)/float(count)
			FIN.write('%.8f'%(stat) + '\t' + str('node val') + '\n')
			self._printTREE(node.right, count)

#Connect to the database as the root user
def init_db():
	pw = getpass.getpass('Database Password: ')
	db = MySQLdb.connect(host='127.0.0.1', user='root', passwd=pw)
	return db

#Display options to user, and prompt for a selection
def show_results(cursor, sql):
	global LEVEL
	count = 0
	option = []
	cursor.execute(sql)
	result = cursor.fetchall()

	#Database menu doesn't have a go back option
	if LEVEL != 0:
		option.insert(count, '..')
		print str(count) + ':\t' + option[count]
		count += 1

	#Print options for user
	for row in result:
		option.insert(count, row[0])
		print str(count) + ':\t' + option[count]
		count += 1
	while(True):
		ind = raw_input ('==========================\nSelection [num]: ')
		if (int(ind) < count and int(ind) >= 0):
			break
		print 'Invalid option'
	#Handle next level, and return option chosen
	if (ind == '0' and LEVEL != 0):
		LEVEL -= 1
		return None
	else:
		LEVEL += 1
		return option[int(ind)]

def main():
	global UNIQUE
	global LEVEL
	data = []
	db = init_db()
	cursor = db.cursor()

	#Allow user to choose different tables and columns from
	#the database until they no longer want to continue
	while True:
		#<LEVEL 0>
		#Allow user to select database
		if LEVEL == 0:
			print '==========================\n'
			sql = 'SHOW DATABASES'
			database = show_results(cursor, sql)
			sql = 'USE ' + database
			cursor.execute(sql)
		#<LEVEL 1>
		#Allow user to select table
		if LEVEL == 1:
			print '==========================\n'
			sql = 'SHOW TABLES'
			table = show_results(cursor, sql)
		#<LEVEL 2>
		#Allow user to select attribute
		if LEVEL == 2:
			print '==========================\n'
			sql = 'DESCRIBE ' + table
			attribute = show_results(cursor, sql)
		#<LEVEL 3>
		#Analyze data from chosen attribute
		if LEVEL == 3:
			LEVEL -= 1	#decrease level to print attributes in next loop
			sql = 'SELECT ' + attribute + ' FROM ' + table
			if (cursor.execute(sql) < 1):
				print 'No rows in this table'
				continue
			result = cursor.fetchall()
			tree = TREE()
			count = 0
			print '==========================\n'

			#Build tree from query results
			for row in result:
				count += 1
				value = str(row[0])
				#print value		#Uncomment to print values, but encrypted values may contain non-ascii characters
				binary = ' '.join(format(ord(x), 'b') for x in value)
				tree.add(binary, value)

			print '==========================\n'
			print 'Rows read:\t' + str(count)
			print 'Unique strings:\t' + str(UNIQUE)

			print '=========================='
			resp = raw_input ('\nWrite unique values to file? [Y/n] ').lower()
			if resp == 'y':
				print '==========================\n'
				tree.printTREE(count, database+'-'+table+'-'+attribute);
				print 'File "'+database+'-'+table+'-'+attribute+'" created'

			print '=========================='
			resp = raw_input ('\nContinue? [Y/n] ').lower()
			if resp == 'y':
				UNIQUE = 0
			else:
				print 'Good-Bye'
				sys.exit()

if __name__ == "__main__":
	main()
