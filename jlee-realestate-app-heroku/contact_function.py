######JLee Team - Contact database##################
import sqlite3
conn = sqlite3.connect('contact.db',check_same_thread=False)
c = conn.cursor()

def create_contact():
	c.execute('CREATE TABLE IF NOT EXISTS contacttable(Name TEXT,Phone TEXT,Email TEXT,Address TEXT,Comment TEXT,Group_type TEXT,Gender TEXT,Race TEXT,Address_type TEXT)')

def add_contact(ct_name,ct_phone,ct_email,ct_address,ct_comment,ct_type,ct_gender,ct_race,ct_add_opt):
	c.execute('INSERT INTO contacttable(Name,Phone,Email,Address,Comment,Group_type,Gender,Race,Address_type) VALUES (?,?,?,?,?,?,?,?,?)',(ct_name,ct_phone,ct_email,ct_address,ct_comment,ct_type,ct_gender,ct_race,ct_add_opt))
	conn.commit()

def view_contact_names():
	c.execute('SELECT DISTINCT Name FROM contacttable')
	data = c.fetchall()
	return data

def get_contact(name):
	c.execute('SELECT * FROM contacttable WHERE Name="{}"'.format(name))
	data = c.fetchall()
	return data

def edit_contact(ct_name,ct_phone,ct_email,ct_address,ct_comment,ct_type,ct_gender,ct_race,ct_add_opt,name,phone,email,address,comment,type,gender,race,add_opt):
	c.execute("UPDATE contacttable SET Name=?,Phone=?,Email=?,Address=?,Comment=?,Group_type=?,Gender=?,Race=?,Address_type=? WHERE Name=? and Phone=? and Email=? and Address=? and Comment=? and Group_type=? and Gender=? and Race=? and Address_type=? ",(ct_name,ct_phone,ct_email,ct_address,ct_comment,ct_type,ct_gender,ct_race,ct_add_opt,name,phone,email,address,comment,type,gender,race,add_opt))
	conn.commit()
	data = c.fetchall()
	return data

def delete_contact(name):
	c.execute('DELETE FROM contacttable WHERE Name="{}"'.format(name))
	conn.commit()

def search_contact(searchby,search):
	if searchby == "Group Type":
		column = "Group_type"
	elif searchby == "Address Type":
		column = "Address_type"
	else:
		column = searchby
	c.execute('SELECT * FROM contacttable WHERE {} = "{}"'.format(column,search))
	data = c.fetchall()
	return data
