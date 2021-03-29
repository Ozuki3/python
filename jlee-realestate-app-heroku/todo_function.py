######JLee Team - TodoList database######
import sqlite3
conn = sqlite3.connect('todo1.db',check_same_thread=False)
c = conn.cursor()


def create_todo():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable (task TEXT,task_status TEXT,task_due_date DATE, task_people TEXT, task_payment FLOAT, task_property TEXT,task_type TEXT, task_comment TEXT)')

def add_todo(task,task_status,task_due_date,task_people,task_payment,task_property,task_type,task_comment):
	c.execute('INSERT INTO taskstable(task,task_status,task_due_date,task_people,task_payment,task_property,task_type,task_comment) VALUES (?,?,?,?,?,?,?,?)',(task,task_status,task_due_date,task_people,task_payment,task_property,task_type,task_comment))
	conn.commit()

def view_all_todo():
	c.execute('SELECT * FROM taskstable')
	data = c.fetchall()
	return data

def view_todo_names(date):
	if not date:
		c.execute('SELECT DISTINCT task FROM taskstable')
		data = c.fetchall()
	else:
		c.execute('SELECT DISTINCT task FROM taskstable WHERE task_due_date = "{}"'.format(date))
		data = c.fetchall()
	return data

def get_todo(task,date):
	if not date:
		c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
		data = c.fetchall()
	else:
		c.execute('SELECT * FROM taskstable WHERE task="{}" AND task_due_date ="{}"'.format(task,date))
		data = c.fetchall()
	return data

def get_date(selected_task):
	c.execute('SELECT task_due_date FROM taskstable WHERE task="{}"'.format(selected_task))
	data = c.fetchall()
	return data

def edit_todo(task, task_status, task_due_date, task_people, task_payment, task_property,task_type, task_comment, content, status, due_date, people,payment, property,type,comment):
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? ,task_people=?,task_payment=?,task_property=?,task_type=?, task_comment=? WHERE task=? and task_status=? and task_due_date=? and task_people=? and task_payment=? and task_property=? and task_type=? and task_comment=? ",(task, task_status, task_due_date, task_people, task_payment, task_property,task_type,task_comment, content, status, due_date, people,payment, property,type,comment))
	conn.commit()
	data = c.fetchall()
	return data

def delete_todo(task,task_due_date,task_people,task_property):
	c.execute('DELETE FROM taskstable WHERE task="{}" AND task_due_date="{}" AND task_people = "{}" AND task_property = "{}"'.format(task,task_due_date,task_people,task_property))
	conn.commit()

# def search_contact(searchby,search):
# 	if searchby == "Task":
# 		column = "task"
# 	elif searchby == "Status":
# 		column = "task_status"
# 	elif searchby == "Due Date":
# 		column = "task_due_date"
# 	elif searchby == "People":
# 		column = "task_people"
# 	elif searchby == "Payment":
# 		column = "task_payment"
# 	elif searchby == "Property":
# 		column = "task_property"
# 	elif searchby == "Task Type":
# 		column = "task_type"
# 	c.execute('SELECT * FROM contacttable WHERE {} = "{}"'.format(column,search))
# 	data = c.fetchall()
# 	return data
def todo_ppt_names():
	c.execute('SELECT DISTINCT task_property FROM taskstable')
	data = c.fetchall()
	return data
#
def property_status_groupbydue():
	c.execute('SELECT * FROM (SELECT task_property, task_due_date,task_status FROM taskstable ORDER BY 2 DESC) tmp GROUP BY task_status, task_property')
	data = c.fetchall()
	return data

##########property_table##################
def create_property():
	c.execute('CREATE TABLE IF NOT EXISTS propertytable (Property TEXT, Start_Date Date, End_Date Date)')

def add_property(property, start, end):
	c.execute('INSERT INTO propertytable(Property,Start_Date,End_Date) VALUES (?,?,?)', (property, start, end))
	conn.commit()


def edit_ppt(Property,Start_Date,End_Date,property,start,end):
	c.execute("UPDATE propertytable SET Property=? ,Start_Date=?, End_Date=? WHERE Property=? and Start_Date=? and End_Date=? ",(Property,Start_Date,End_Date,property,start,end))
	conn.commit()
	data = c.fetchall()
	return data

def delete_ppt(property):
	c.execute('DELETE FROM propertytable WHERE Property="{}" '.format(property))
	conn.commit()

def view_all_property():
	c.execute('SELECT * FROM propertytable')
	data = c.fetchall()
	return data

def view_ppt_names():
	c.execute('SELECT DISTINCT Property FROM propertytable')
	data = c.fetchall()
	return data

def get_ppt(ppt):
	c.execute('SELECT * FROM propertytable WHERE Property = "{}"'.format(ppt))
	data = c.fetchall()
	return data

def get_ppt_start(Property):
	c.execute('SELECT Start_Date FROM propertytable WHERE Property = "{}"'.format(Property))
	data = c.fetchall()
	return data

def get_ppt_end(Property):
	c.execute('SELECT End_Date FROM propertytable WHERE Property = "{}"'.format(Property))
	data = c.fetchall()
	return data

def get_ppt_names():
	c.execute('SELECT DISTINCT Property FROM propertytable')
	data = c.fetchall()
	return data
