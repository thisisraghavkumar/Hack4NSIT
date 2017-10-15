import pymysql
import json

class DB:
	db = None	
	def __init__(self):
		try:
			self.db=pymysql.connect("localhost","root","123456789","MediBOT")
		except Exception as e:
			print("Database not Found")

	def get_med(disease)
		cursor=db.cursor()
		cursor.execute("select medicine from medicines where Illness={} ".format(disease))
		result = cursor.fetchall()
		

