import os
import pandas as pd
import streamlit as st
import sqlite3
import json

# ---------- Database Functions ----------
default_categories = [
    ("Groceries", "Expenses related to food and daily needs", "None"),
    ("Entertainment", "Movies, games, and fun activities", "None"),
    ("Utilities", "Bills for electricity, water, internet", "None"),
    ("Transport", "Expenses for commuting and travel", "None"),
    ("Health", "Medical and health-related expenses", "None"),
    ("Shopping", "Buying products or things for self", json.dumps(["Amazon", "AMAZON", "Amz", "Myntra", "Ajio"])),
    ("Sport", "Debit amount for any physical activity", json.dumps(["Gym", "GYM", "Thenx", "Footy", "Sporting", "WARRIORS CROSS FIT"])),
    ("CreditCard_Maintainence", "Credit card Maintainence", json.dumps(["CREDIT INTEREST CAPITALISED"])),
    ("CreditCard_Debt_Payment", "Debit amount for repaying the debt", json.dumps(["IB_BILLPAY"])),
    ("Salary", "Credit amount for Primary Occupation", json.dumps(["BOSCH GLOBAL SOFTWARE TECHNOLOGIES PRIVATE LIMITED"])),
    ("Transport", "Debit amount for any physical activity", json.dumps(["UBER", "Uber", "uber", "ZIPCAR", "Zipcar", "bird", "Lim", "TFL TRAVEL", "Tfl Travel Charge", "Ewa"])),
    ("Entertainment", "Debit amount for repaying the debt", json.dumps(["IB_BILLPAY"])),
    ("CarMaintainence", "Debit amount for repaying the debt", json.dumps(["Kia"])),
    ("EatingOut", "Debit amount for repaying the debt", json.dumps(["SREE ANNAPOORNA", "SWIGGY", "ZOMATO", "HMR BIRIYANI HUT", "HARIBHAVANAM", "VALARMATHI", "ACHARIYA HOTEL", "RHR HOTELS"])),
    ("PhoneBills", "Debit amount for repaying the debt", json.dumps(["AIRTEL", "JIO"])),
    ("EMI", "Debit amount for repaying the debt", json.dumps(["NCACDOSYM"])),
    ("Travel", "Debit amount for repaying the debt", json.dumps(["Airbnb", "Ryanair", "Trainline", "trainline", "Booking", "Flixbus", "ABHIBUS", "PAYUREDBUS"])),
    ("Fuel", "Debit amount for repaying the debt", json.dumps(["Shanti Social"])),
]

def init_db():
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT, 
            upi_client TEXT DEFAULT "None"
        )
    ''')
    # Check if 'upi_client' column exists, if not, add it
    # Insert default categories
    c.executemany('INSERT OR IGNORE INTO categories (name, description, upi_client) VALUES (?, ?, ?)', default_categories)

    
    conn.commit()
    conn.close()

def add_category(name, description):
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO categories (name, description, upi_client) VALUES (?, ?, ?)', (name, description, "None"))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error(f"Category '{name}' already exists!")
    finally:
        conn.close()

def get_categories():
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    c.execute('SELECT id, name, description, upi_client FROM categories')
    data = c.fetchall()
    conn.close()
    return data

def delete_category(category_id):
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    c.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()

def update_category(category_id, new_name, new_description):
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    try:
        c.execute('UPDATE categories SET name = ?, description = ? WHERE id = ?', (new_name, new_description, category_id))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error(f"Category name '{new_name}' already exists!")
    finally:
        conn.close()

# ---------- Streamlit App ----------

def main():
    # Set the title of the app
    st.title("Personal Finance Tracker - Settings")
    tabs = st.tabs(["List of Categories", "Category Manager", "AnalyseYearlyReport"])
    
    with tabs[0]:
        init_db()
        st.subheader("📋 Manage Categories")

        categories = get_categories()
        if categories:
            for id, name, description, upi_client in categories:
                with st.expander(f"{name}"):
                    st.write(f"**Description:** {description}")
                    st.write(f"**UPI Client:** {upi_client if upi_client else 'None'}")

                    # Edit Category
                    with st.form(f"edit_form_{id}"):
                        new_name = st.text_input("Edit Name", value=name, key=f"name_{id}")
                        new_description = st.text_area("Edit Description", value=description, key=f"desc_{id}")
                        update_btn = st.form_submit_button("Update")

                        if update_btn:
                            if new_name.strip() == "":
                                st.warning("Category name cannot be empty!")
                            else:
                                update_category(id, new_name.strip(), new_description.strip())
                                st.success(f"Category '{new_name}' updated successfully!")
                                st.experimental_rerun()

                    # Delete Category
                    if st.button(f"Delete '{name}'", key=f"delete_{id}"):
                        delete_category(id)
                        st.success(f"Category '{name}' deleted successfully!")
                        st.experimental_rerun()
    
    with tabs[1]:
        init_db()
        st.subheader("➕ Add New Category")

        with st.form(key='add_category_form'):
            name = st.text_input("Category Name")
            description = st.text_area("Category Description")
            submit = st.form_submit_button("Add")

        if submit:
            if name.strip() == "":
                st.warning("Category name cannot be empty!")
            else:
                add_category(name.strip(), description.strip())
                st.success(f"Category '{name}' added successfully!")

        else:
            st.info("No categories found. Add some!")
    


    





# ###############################################################################
