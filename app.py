###############################################################################
###############################################################################
# Manoj's Personal Finance Tracker
# Created: January 15, 2023
# Last Updated: January 15, 2023
# Version: 1.0
# Changes:
# v1.0 - added multi-page support
###############################################################################
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import xlrd
import time
import datetime
import calendar
import DataReadInput
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
OverallCategories = ['Salary', 'Savings','Entertainment', 'EatingOut', 'Rent', \
				  'PhoneBills', 'Travel', 'Fuel', 'Sport', 'AccountTransfer', 'Shopping',\
				  'Cash_Withdrawal', 'CreditCard_Debt_Payment', 'CreditCard_Maintainence',\
				  'Gifts', 'Groceries', 'Personal care', 'Lend', 'Loan_EMI_Payment',\
				  'EMI', 'CarMaintainence', 'Unknown']
###############################################################################s
#Create Table to add categories
def CreateTableFromReport(ListDF, report_year, report_month_str):
	st.subheader(f'Analytics for the given Month - {report_year} {report_month_str}')

	for index, row in ListDF.iterrows():
		ListDF['Year'] = report_year
		ListDF['Month'] = report_month_str
		ListDF['  '] = 'Others'
		ListDF['Category'] = 'Uncategorized'
		print(row['Narration'])

		# Personalise your categories
		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('Amazon|AMAZON|Amz'), 'Shopping',ListDF['Category']) #debit

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('Gym|GYM|Thenx|Footy|Sporting|MUTHURAAJ|WAYNERAJESH94|WARRIORS CROSS FIT'), 'Sport', ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('CREDIT INTEREST CAPITALISED'), 'CreditCard_Maintainence', ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('IB BILLPAY'), 'CreditCard_Debt_Payment', ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('BOSCH GLOBAL SOFTWARE TECHNOLOGIES PRIVATE LIMITED'), 'Salary', ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('UBER|Uber|uber|ZIPCAR|Zipcar|bird|Lim|TFL TRAVEL|Tfl Travel Charge|Ewa'),'Transport', ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('MOHANASUNDARAM|JAYGOWTHAMI1|ZERODHA'), 'Savings',ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('itunes|apple|ODEON|Odeon|MIRAJ|BOOKMYSHOW'), 'Entertainment',ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('SHANTHI SOCIAL|Kia'), 'CarMaintainence',ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('SREE ANNAPOORNA|SWIGGY|ZOMATO|HMR BIRIYANI HUT|HARIBHAVANAM|VALARMATHI|ACHARIYA HOTEL|RHR HOTELS'), 'EatingOut',ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('AIRTEL|JIO|BLD*RESUME-NOW'), 'PhoneBills',ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('NCACDOSYM'), 'EMI',ListDF['Category'])

		ListDF['Category'] = np.where(ListDF['Narration'].str.contains('Airbnb|Ryanair|Trainline|trainline|Booking|Flixbus|ABHIBUS|PAYUREDBUS'),'Travel', ListDF['Category'])

	#ListDF.configure_column(“Category”, editable = True, cellEditor =‘agSelectCellEditor’, cellEditorParams = {‘values’: OverallCategories})
	#st.write(ListDF)
	gd = GridOptionsBuilder.from_dataframe(ListDF)
	gd.configure_pagination(enabled=True)
	gd.configure_default_column(editable=True, groupable=True)
	AgGrid(ListDF)
	return ListDF

#Create Plotly Graph
def CreateAreaGraphPlotly(ListDF, report_year, report_month_str):
	# Plotly Graph Area
	figureValue = px.area(
		ListDF["ClosingBalance"],
		x=ListDF["Date"],
		y="ClosingBalance",
		title="",
		color_discrete_sequence=["#0083B8"] * len(ListDF),
		template="plotly_white",
	)
	figureValue.update_layout(
		xaxis=dict(tickmode="linear"),
		xaxis_title="Date",
		plot_bgcolor="rgba(0,0,0,0)",
		yaxis=(dict(showgrid=False)),
	)
	st.subheader(f'Balance for the given Month - {report_year} {report_month_str}')
	st.plotly_chart(figureValue, use_container_width=True)

def CreateTreeMapPlotly(ListDF, report_year, report_month_str):
	# SPEND BY CATEGORY [TREEMAP CHART]
	fig_spend_by_cateogry = px.treemap(ListDF, path=["Category"],values="DebitAmount", title="")
	fig_spend_by_cateogry.data[0].textinfo = "label+text+value+percent root"
	fig_spend_by_cateogry.update_layout(margin=dict(l=0, r=0, t=0, b=0))
	st.subheader(f'Tree Map for the given Month - {report_year} {report_month_str}')
	st.plotly_chart(fig_spend_by_cateogry, use_container_width=True)

###############################################################################
##Webpage Setup
def main():


	tabs = st.tabs(["Home", "AnalyseMontlyReport", "AnalyseYearlyReport"])

	with tabs[0]:
		##MainWebpage Setup
		st.title (":shark: Finance Dashboard")
		st.caption("Welcome Manoj :)")

		#MonthlyReport= DataReadInput.ReadCsvMontlyReport("BS_December.txt")

		#CreateAreaGraphPlotly(MonthlyReport)

	with tabs[1]:
		##Montly Data Setup
		st.title(":date: Analyse Montly Finance Data")
		st.session_state.formbtn_state = True

		st.subheader("Add New Month Report")
		# name = st.text_input("Name")
		with st.form(key='Month'):
			st.write('Add data to Analyse Month data')

			this_year = datetime.date.today().year
			this_month = datetime.date.today().month
			report_year = st.selectbox('', range(this_year, this_year - 5, -1))
			month_abbr = calendar.month_abbr[1:]
			report_month_str = st.radio('', month_abbr, index=this_month - 1, horizontal=True)
			report_month = month_abbr.index(report_month_str) + 1

			file = st.file_uploader('Upload the Monthly Report!! (DoubleCheck the report is not yearly!)')

			submit_form = st.form_submit_button(label="Analyse", help="Click Analyse to Submit Form!")

			# Checking if all the fields are non empty
			if submit_form:
				st.write(submit_form)

				if file and report_month_str and report_year:
					st.success(
						f"Report is submitted and make take a while to process"
					)
					MonthlyReport = DataReadInput.ReadCsvMontlyReport(file)
					#create a table
					ListNewDF = CreateTableFromReport(MonthlyReport, report_year, report_month_str)
					#create a Graph
					CreateAreaGraphPlotly(ListNewDF, report_year, report_month_str)
					# create a Tree Map for Categories
					CreateTreeMapPlotly(ListNewDF, report_year, report_month_str)

				else:
					st.warning("Please fill all the fields")

	with tabs[2]:
		##Yearly Data Setup
		st.title(":calendar: Analyse Yearly Finance Data")

