# Framework program using sqlite database

import sqlite3

conn = sqlite3.connect("Framework.db")
cursor = conn.cursor()
config_table = 'fwconfig'
data_table = cursor.execute(f"select value from {config_table} where key = ?", ("title",)).fetchone()
data_table = data_table[0]

field_names = cursor.execute(f"PRAGMA table_info({data_table})").fetchall()
field_names	= [data[1] for data in field_names]

message = cursor.execute(f"select value from {config_table} where key = ?", ("saved_msg",)).fetchone()

def Create_record():
	data = []
	for field in field_names:
		data.append(input(f"Enter the {field}: "))
	data = tuple(data)
	cursor.execute(f"INSERT into {data_table} values {str(data)}")
	print(f"Record created {message[0]}")

def read_records():
	data = cursor.execute(f"select * from {data_table}").fetchall()
	if data:
		for record in data:
			print(f"\n{field_names[0]} = {record[0]}\n{field_names[1]} = {record[1]}\n{field_names[2]} = {record[2]}")
	else:
		print("No data found")

def update_record():
	record_id = input(f"\nEnter {field_names[0]} to update: ")
	for index in range(1, len(field_names)):
		print(f"{index}. Update {field_names[index]}")
	choice = int(input("enter your choice to update: "))
	newtext = input(f"Enter new {field_names[choice]}: ")
	cursor.execute(f"update {data_table} set \"{field_names[choice]}\" = \"{newtext}\" where \"{field_names[0]}\" = \"{record_id}\"")
	print(f"Record {record_id} updated {message[0]}")

def delete_record():
	record_id = input(f"\nEnter {field_names[0]} to delete: ")
	cursor.execute(f"delete from {data_table} where \"{field_names[0]}\" = \"{record_id}\"")
	print(f"Record with {record_id} deleted {message[0]}")

def search_record():
	record_id = input(f"\nEnter {field_names[0]} to search: ")
	data = cursor.execute(f"select * from {data_table} where \"{field_names[0]}\" = \"{record_id}\"").fetchone()
	if data:
		print(f"\n{field_names[1]} = {data[1]}\n{field_names[2]} = {data[2]}")
	else:
		print(f"Record {record_id} is not found")

def ShowMenu():
	data = cursor.execute(f"SELECT value FROM {config_table} WHERE key = 'Menu'").fetchone()
	data = data[0].replace("\\n", "\n")
	print(data)

while True:
	ShowMenu()
	Menu = [Create_record, read_records, update_record, delete_record, search_record, exit]
	Menu[int(input("\nEnter your choice: ")) - 1]()
	conn.commit()