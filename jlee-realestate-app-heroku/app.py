#Core Pkgs
import streamlit as st
# # import streamlit.components.v1 as stc
from user_function import *
from contact_function import *
from todo_function import *
#EDA Pkgs
import pandas as pd
import os
import datetime
import time
import base64
# import matplotlib
# matplotlib.use('Agg')
import plotly.express as px
from plotly.figure_factory import create_gantt
# import plotly.graph_objs as go
from PIL import Image


#download csv/text
class FileDownloader(object):
	def __init__(self, data, filename='JLeeTeam',file_ext='txt'):
		super(FileDownloader, self).__init__()
		self.data = data
		self.filename = filename
		self.file_ext = file_ext

	def download(self):
		b64 = base64.b64encode(self.data.encode()).decode()
		timestr = time.strftime("%Y%m%d")
		new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}"> Download </a>'
		st.markdown(href,unsafe_allow_html=True)


def main():
	#home page
	img = "imgs/jleecolor200.png"
	st.markdown("""
				<style>.container {display: flex;}
				.logo-text {font-weight:700 !important;font-size:35px !important;color: purple;padding-top: 58px !important;}
				.logo-img {float:left;}
				</style>
				""",
				unsafe_allow_html=True
				)
	st.markdown(f"""
				<div class="container">
					<img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(img, "rb").read()).decode()}">
					<p class="logo-text">JLEE LUXURY REAL ESTATE </p>
				</div>
				""",
				unsafe_allow_html=True
				)
	account = st.sidebar.selectbox("Select an account",["Market Infomation","JLee Team"])


	#Customer page
	if account == "Market Infomation":
		username = st.sidebar.text_input("Username")
		password = st.sidebar.text_input("Password",type='password')
		st.sidebar.subheader(" ")
		if st.sidebar.checkbox("Login"):
			if username =="" or password == "":
				st.subheader(" ")
				st.subheader(" ")
				st.subheader(" ")
				st.warning("Please input Username/Password.")
			else:
				create_user()
				hashed_pswd_init = make_hashes(password)
				result = login_user(username, check_hashes(password, hashed_pswd_init))
				if not result:
					st.subheader(" ")
					st.subheader(" ")
					st.subheader(" ")
					st.warning("Incorrect Username/Password. Please try again or request technical support at xxx-xxxx-xxxx. If you don't have an account, please contact your agent to create one for you.")
				# else:
				# 	st.balloons()
				else:
					st.sidebar.subheader(" ")
					# task = st.sidebar.selectbox("Select a ",["Plots", "Trends"])
					st.subheader("")
					sales_df = pd.read_csv("market/sales_y.csv", parse_dates=['Mon-Yr'])
					sales_m_df = pd.read_csv("market/sales_m.csv", parse_dates=['Mon-Yr'])
					price_df = pd.read_csv("market/medianprice.csv")
					inven_df = pd.read_csv("market/inventory.csv",parse_dates=['Mon-Yr'])
					daysonmkt_df = pd.read_csv('market/daysonmkt.csv',parse_dates=['Mon-Yr'])
					#plot choices
					with st.beta_expander("Select Options"):
						all_columns = sales_df.columns.tolist()
						all_columns.remove("Mon-Yr")
						choices = st.multiselect("Select Columns", all_columns)
						if not choices:
							title = "CA vs San Francisco"
							line_y = ["CA","San Francisco"]
						else:
							s = ''
							for i in choices:
								s = s +' vs '+ i
							title = s[4:]
							line_y = choices
					#plot sales
					with st.beta_expander("Year-to-Year Percent Change in Sales"):
						fig = px.line(sales_df, x="Mon-Yr", y=line_y,title=title,color_discrete_sequence = px.colors.qualitative.Vivid)
						fig.update_xaxes(rangeslider_visible=True,title='Date')
						fig.update_yaxes(dtick=0.2,tickformat = '%',zeroline=True,zerolinecolor='#acaeae',title='YTY% Chg. in Sales')
						fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor="#f6f8f9",showlegend=False)
						st.plotly_chart(fig,use_container_width=True)
						#MTM% plot
					with st.beta_expander("Month-to-Month Percent Change in Sales"):
						fig_m = px.line(sales_m_df, x="Mon-Yr", y=line_y, title=title,color_discrete_sequence=px.colors.qualitative.Vivid)
						fig_m.update_xaxes(rangeslider_visible=True, title='Date')
						fig_m.update_yaxes(dtick=0.2, tickformat='%', zeroline=True, zerolinecolor='#acaeae',title='MTM% Chg. in Sales')
						fig_m.update_layout(paper_bgcolor='#ffffff', plot_bgcolor="#f6f8f9", showlegend=False)
						st.plotly_chart(fig_m,use_container_width=True)

					with st.beta_expander("Year-to-Year Percent Change in Price"):
						#price percent change
						pct_price_df = price_df.set_index("Mon-Yr").pct_change()
						# st.dataframe(pct_price_df)
						fig = px.line(pct_price_df, x=pct_price_df.index, y=line_y, title=title,color_discrete_sequence=px.colors.qualitative.Prism)
						fig.update_xaxes(rangeslider_visible=True, title='Date')
						fig.update_yaxes(tickformat='%', zeroline=True, zerolinecolor='#acaeae', title='YTY% Chg. in Price')
						fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor="#f6f8f9", showlegend=False)
						st.plotly_chart(fig, use_container_width=True)

					with st.beta_expander("Years of Median Price"):
						fig = px.bar(price_df, x="Mon-Yr", y=line_y, title=title, color_discrete_sequence=px.colors.qualitative.Prism)
						fig.update_xaxes(rangeslider_visible=True, title='Date')
						fig.update_yaxes(tickformat='$', zeroline=True, zerolinecolor='#acaeae', title='Median Price',dtick=200000,tick0=100000)
						fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor="#f6f8f9", showlegend=False)
						st.plotly_chart(fig, use_container_width=True)

					with st.beta_expander("Months of Inventory Index"):
						fig = px.line(inven_df, x=pct_price_df.index, y=line_y, title=title,color_discrete_sequence=px.colors.qualitative.T10)
						fig.update_xaxes(rangeslider_visible=True, title='Date')
						fig.update_yaxes(dtick=2,zeroline=True, zerolinecolor='#acaeae', title='Inventory Index')
						fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor="#f6f8f9", showlegend=False)
						st.plotly_chart(fig, use_container_width=True)

					with st.beta_expander("Median Days On Market"):
						fig = px.line(daysonmkt_df, x=pct_price_df.index, y=line_y, title=title,color_discrete_sequence=px.colors.qualitative.T10)
						fig.update_xaxes(rangeslider_visible=True, title='Date')
						fig.update_yaxes(dtick=10,zeroline=True, zerolinecolor='#acaeae', title='Days on Market')
						fig.update_layout(paper_bgcolor='#ffffff', plot_bgcolor="#f6f8f9", showlegend=False)
						st.plotly_chart(fig, use_container_width=True)

					with st.beta_expander("Note"):
						st.markdown("Sales for California are seasonally adjusted and annualized; year-to-year percent changes for California from Jan 1991 to Feb 2013 have been revised.\n LA Metro is a 5-county region that includes Los Angeles County, Orange County, Riverside County, San Bernardino County, and Ventura County.\n Inland Empire includes Riverside County and San Bernardino County.\n S.F. Bay Area includes the following counties: Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano, and Sonoma.")
						st.markdown("LA historical data has been revised going back to 1990. OC data has been refined to avoid double counting starting with Jan 2011. Historical data was not revised.Revisions were made to SLO historical data going back to Oct 2008, when Scenic Coast inventory data was added to the series. Revisions were made to Santa Barbara historical data going back to Oct 2008, when Santa Maria inventory data was revised. Santa Ynez inventory data was added to the series in Jan 2009. Riverside historical data has been revised going back to 1997; UII for Riverside County is calculated without 'Riverside Board' from June 1998 to Jan 1999 and from Apr 1999 to Apr 2001. San Bernardino historical data has been revised going back to 1998. Inland Empire (Riverside/San Bernardino) historical data has been revised going back to 1998. Sacramento started reporting total active listings, instead of new active listings, as of Aug 07. Marin, Mendocino, Napa, Solano, and Sonoma only reported new active listings between Apr 04 and Aug 07.")
						st.markdown("OC data has been refined to avoid double counting.  Historical data was only revised back to 1999.")
						st.write('SOURCE: CALIFORNIA ASSOCIATION OF REALTORS®')


	elif account == "JLee Team":
		# adm_username = st.sidebar.text_input("Administrator Username")
		adm_password = st.sidebar.text_input("Administrator Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if not (adm_username == 'JLeeTeam' and adm_password == '345678'):
			if adm_password != '654321':
				st.subheader(" ")
				st.subheader(" ")
				st.subheader(" ")
				st.warning("Incorrect Username/Password. Please try again or request technical support at xxx-xxxx-xxxx.")
			else:
				st.sidebar.subheader(" ")
				task = st.sidebar.selectbox("Select a task",["Todo List","Contacts","Sign Up"])
				st.subheader("")

				if task == "Todo List":
					todotable_lis = ["Task", "Status", "Due Date", "People", "Payment", "Property", "Task Type","Comment"]
					task_type_lis = ["","Stage", "Repair", "Paint", "Show", "Garden","Others"]
					status_lis = ["","ToDo", "Doing", "Done"]
					create_todo()
					#search a task for update
					if st.sidebar.checkbox("Add/Edit Task"):
						with st.beta_expander("Select Options"):
							col1, col2 = st.beta_columns([1,4])
							with col1:
								selected_date = st.text_input("Date",datetime.date.today())
							with col2:
								list_of_tasks = [i[0] for i in view_todo_names(selected_date)]
								list_of_tasks.insert(0, "")
								selected_task = st.selectbox("Task", list_of_tasks)
							task_result = get_todo(selected_task,selected_date)
						st.subheader("")
						if task_result:
							content = task_result[0][0]
							status = task_result[0][1]
							due_date = task_result[0][2]#datetime.datetime.strptime(task_result[0][2], '%Y-%m-%d')
							people = task_result[0][3]
							payment = task_result[0][4]
							house = task_result[0][5]
							type = task_result[0][6]
							comment = task_result[0][7]
							submit = 'Update Task'
						else:
							content = ""
							status = "Status"
							due_date = "Due Date"
							people = ""
							payment = "%.2f" % float()
							house = ""
							type = "Task Type"
							comment = ""
							submit = 'Add Task'
						#todolist layout
						clm1, clm2, clm3 = st.beta_columns(3)
						with clm1:
							# status_lis.insert(0, status)
							task_status = st.selectbox(status, status_lis)
						with clm2:
							task_due_date = st.date_input(due_date)
						with clm3:
							task_payment = st.text_input("Payment $",payment)
						col1, col2 = st.beta_columns([1,2])
						with col1:
							task_property = st.text_input("Property",house)
							# task_type_lis.insert(0, type)
							task_type = st.selectbox(type,task_type_lis)
						with col2:
							task_people = st.text_input('People',people)
							task = st.text_input('Task Content',content)
						task_comment = st.text_area("Task Comment",comment)
						#submit updated info
						clm1, clm2 = st.beta_columns([4.7, 1])
						with clm1:
							if st.button(submit):
								if submit == "Add Task":
									add_todo(task, task_status, task_due_date, task_people, task_payment, task_property,task_type, task_comment)
									st.success("Added: {}".format(task))
								elif submit == "Update Task":
									edit_todo(task, task_status, task_due_date, task_people, task_payment,task_property, task_type, task_comment, content, status, due_date, people,payment, house, type, comment)
									st.success("Updated: {}".format(task))
						# c1, c2, c3 = st.beta_columns([2.2,2.5,1])
						# with c1:
						# 	if st.button("Add Task"):
						# 		add_todo(task, task_status, task_due_date,task_people,task_payment,task_property,task_type,task_comment)
						# 		st.success("Added: {}".format(task))
						# with c2:
						# 	if st.button("Update Task"):
						# 		edit_todo(task, task_status,task_due_date,task_people,task_payment,task_property,task_type,task_comment,content,status,due_date,people,payment,house,type,comment)
						# 		st.success("Updated: {}".format(task))
						with clm2:
							if st.button("Delete Task"):
								delete_todo(task,task_due_date,task_people,task_property)
								st.success("Deleted")

						st.subheader("")
						with st.beta_expander("Add Project"):
							colm1, colm2, colm3 = st.beta_columns([1, 1, 1])
							with colm1:
								Property = st.text_input("Property Name")
								ppt_result = get_ppt(Property)
								if ppt_result:
									property = ppt_result[0][0]
									start = ppt_result[0][1]#datetime.datetime.strptime(ppt_result[0][1], '%Y-%m-%d')
									end = ppt_result[0][2]#datetime.datetime.strptime(ppt_result[0][2], '%Y-%m-%d')
									submit = "Update"
								else:
									property = ""
									start = "Start Date"
									end = "End Date"
									submit = "Add"
							with colm2:
								Start_Date = st.date_input(start)
							with colm3:
								End_Date = st.date_input(end)
							clm1, clm2 = st.beta_columns([8, 1])
							with clm1:
								if st.button(submit):
									if submit == "Add":
										add_property(Property,Start_Date,End_Date)
										st.success("Added: {}".format(Property))
									elif submit == "Update":
										edit_ppt(Property,Start_Date,End_Date,property,start,end)
										st.success("Updated: {}".format(Property))
							with clm2:
								if st.button("Delete"):
									delete_ppt(Property)
									st.warning("Deleted: '{}'".format(Property))
							# st.write(view_all_property())

					# view the entire todolist
					with st.beta_expander("Task Table"):
						todo_df = pd.DataFrame(view_all_todo(), columns=todotable_lis)
						if st.checkbox("Select Options"):
							selected_df = todo_df
							selected_columns = st.multiselect("Select Columns", todotable_lis)
							if selected_columns:
								selected_df = selected_df[selected_columns]
								selected_rows = st.multiselect("Select Rows", selected_df.index)
								if selected_rows:
									selected_df = selected_df.loc[selected_rows]
						else:
							selected_df = todo_df
							selected_columns = ["Property","Task Type","Status","People","Payment"]
						st.dataframe(selected_df)
						FileDownloader(selected_df.to_csv(), filename='JLeeTeam_TodoList',file_ext='csv').download()

					# if st.sidebar.checkbox("Data Helper"):
					st.subheader("")
					# if st.checkbox("Explore Payment"):
					if "Payment" in selected_columns:
						with st.beta_expander("Payment"):
							colm1, colm2 = st.beta_columns([1,3])
							with colm1:
								st.subheader("")
								st.subheader("")
								sum_payment = selected_df["Payment"].sum()
								st.write("Total Payment: {}".format(round(sum_payment,2)))
								stats_payment = selected_df["Payment"].describe()
								st.write(stats_payment)
							with colm2:
								fig = px.sunburst(selected_df, path=selected_columns, color='Payment',color_continuous_scale='Purples')
								st.plotly_chart(fig, use_container_width=True)
						# else:
						# 	st.warning("Payment Column does not in current selected table")
					st.subheader("")
					with st.beta_expander("Project"):
						df = pd.DataFrame(property_status_groupbydue(),columns=["Task","Finish","Status"])
						df["Start"] = ""
						list_of_property = [i[0] for i in get_ppt_names()]
						list_of_todo_property = [i[0] for i in todo_ppt_names()]
						st.write(list_of_property)
						st.write(list_of_todo_property)
						for ppt in list_of_property:
							if ppt in list_of_todo_property:
								doing_start = df.Finish[(df["Task"] == ppt) & (df["Status"] == 'Done')].to_list()[0]
								todo_start = df.Finish[(df["Task"] == ppt) & (df["Status"] == 'Doing')].to_list()[0]
								done_start = get_ppt_start(ppt)[0][0]
							else:
								doing_start = None
								todo_start = get_ppt_start(ppt)[0][0]
								done_start = None
							df.Start.loc[(df["Task"] == ppt) & (df["Status"] == 'Doing')] = doing_start
							df.Start.loc[(df["Task"] == ppt) & (df["Status"] == 'ToDo')] = todo_start
							df.Start.loc[(df["Task"] == ppt) & (df["Status"] == 'Done')] = done_start
						# st.dataframe(df)
						colors = {'ToDo': '#edeaf6','Doing': '#c9c1e3','Done': '#9383c7'}
						fig = create_gantt(df, colors=colors , index_col='Status', show_colorbar=True,group_tasks=True)
						fig.layout.title = None
						fig.update_layout(legend_orientation='h',paper_bgcolor='#ffffff',plot_bgcolor = "#f6f8f9")
						st.plotly_chart(fig, use_container_width=True)


				elif task == "Contacts":
					task = st.sidebar.selectbox("Select a task",["Search Contact","Add/Edit Contact"])
					#contact options
					gender_lis = ["", "Female", "Male"]
					race_lis = ["", "Asian", "Indian", "Black", "White"]
					type_lis = ["", "Customer", "Agent", "Staging", "Gardner", "General Worker", "Cleaner", "Inspector"]
					address_opt_lis = ["", "Home", "Company", "Listing property"]

					if task == "Add/Edit Contact":
						create_contact()
						list_of_contacts = [i[0] for i in view_contact_names()]
						list_of_contacts.insert(0, "")
						selected_contact = st.selectbox("Search a Contact", list_of_contacts)
						contact_result = get_contact(selected_contact)
						if contact_result:
							name = contact_result[0][0]
							phone = contact_result[0][1]
							email = contact_result[0][2]
							address = contact_result[0][3]
							comment = contact_result[0][4]
							type = contact_result[0][5]
							gender = contact_result[0][6]
							race = contact_result[0][7]
							add_opt = contact_result[0][8]
							submit = "Update Contact"
						else:
							name = ""
							phone = ""
							email = ""
							address = ""
							comment = ""
							type = "Group Type"
							gender = "Gender"
							race = "Race"
							add_opt = "Address Type"
							submit = "Add Contact"

						#layout
						c1, c2, c3, c4 = st.beta_columns([2, 1.5, 1.5, 3])
						with c1:
							ct_name = st.text_input("Name",name)
						with c2:
							ct_gender = st.selectbox(gender,gender_lis)
						with c3:
							ct_race = st.selectbox(race, race_lis)
						with c4:
							ct_type = st.selectbox(type, type_lis)
						cl1, cl2 = st.beta_columns([1, 3])
						with cl1:
							ct_add_opt = st.selectbox(add_opt, address_opt_lis)
						with cl2:
							ct_address = st.text_input("Address",address)
						col1, col2= st.beta_columns([1, 1])
						with col1:
							ct_phone = st.text_input("Phone",phone)
						with col2:
							ct_email = st.text_input("Email",email)
						ct_comment = st.text_area("Comment",comment)
						# Add photo
						image_file = st.file_uploader("Add a photo / business card", type=['png', 'jpeg', 'jpg'])
						if image_file is not None:
							# file_details = {"FileName": image_file.name, "FileType": image_file.type}
							# st.write(file_details)
							img = Image.open(image_file)
							st.image(img)
							with open(os.path.join("photoDir", image_file.name), "wb") as f:
								f.write(image_file.getbuffer())
							# st.success("Saved Photo")
						#put all the info into the contact_db
						clm1, clm2 = st.beta_columns([3.7,1])
						with clm1:
							if st.button(submit):
								if submit == "Add Contact":
									add_contact(ct_name,ct_phone,ct_email,ct_address,ct_comment,ct_type,ct_gender,ct_race,ct_add_opt)
									st.success("Added: {}".format(ct_name))
								elif submit == "Update Contact":
									edit_contact(ct_name,ct_phone,ct_email,ct_address,ct_comment,ct_type,ct_gender,ct_race,ct_add_opt,name,phone,email,address,comment,type,gender,race,add_opt)
									st.success("Updated: {}".format(ct_name))
						#delete contact by name
						with clm2:
							if st.button("Delete Contact"):
								delete_contact(selected_contact)
								st.warning("Deleted: '{}'".format(selected_contact))

					elif task == "Search Contact":
						contacttable_lis = ["Name","Phone","Email","Address","Comment","Group Type","Gender","Race","Address Type"]
						with st.beta_expander("Search Options"):
							clm1, clm2 = st.beta_columns([1,4])
							with clm1:
								searchby = st.selectbox("Search by", contacttable_lis)
							with clm2:
								if searchby == "Group Type":
									search = st.selectbox("Key words", type_lis)
								elif searchby == "Gender":
									search = st.selectbox("Key words", gender_lis)
								elif searchby == "Race":
									search = st.selectbox("Key words", race_lis)
								elif searchby == "Address Type":
									search = st.multiselect("Key words", address_opt_lis)
								else:
									search = st.text_input("Key words","")
						result = search_contact(searchby,search)
						contact_df = pd.DataFrame(result,columns = contacttable_lis)
						st.table(contact_df[["Name", "Phone", "Email"]])
						#more info and photo of one selected name
						with st.beta_expander("More Infomation"):
							searched_name_lis = contact_df["Name"].tolist()
							selected_name = st.selectbox("Select a name", searched_name_lis)
							temp_df = contact_df.loc[contact_df["Name"] == selected_name]
							st.table(temp_df[["Address","Comment","Group Type","Gender","Race","Address Type"]])
							if os.path.exists('photoDir/{}.jpg'.format(selected_name)):
								st.image(Image.open('photoDir/{}.jpg'.format(selected_name)))
							else:
								st.warning("No image")
							# download
						st.subheader("")
						with st.beta_expander("Download Options"):
							selected_columns = st.multiselect("Select Columns", contacttable_lis)
							selected_contact_df = contact_df[selected_columns]
							st.dataframe(selected_contact_df)
							FileDownloader(selected_contact_df.to_csv(),filename='JLeeTeam_ContactInfo', file_ext='csv').download()


				elif task == "Sign Up":
					st.subheader(" ")
					st.subheader("Create An Account")
					new_username = st.text_input("Username")
					new_password = st.text_input("Password", type='password')
					st.subheader(" ")
					if st.button("Sign Up"):
						create_user()
						hashed_pswd = make_hashes(new_password)
						sign_reslut = add_user(new_username, hashed_pswd)
						if sign_reslut:
							st.success("You have successfully created an Account.")
						else:
							st.warning("Please input the username and password.")


if __name__ == '__main__':
	main()
