import streamlit as st
import sqlite3

# ---------- Database Functions ----------

def init_db():
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_category(name, description):
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error(f"Category '{name}' already exists!")
    finally:
        conn.close()

def get_categories():
    conn = sqlite3.connect('categories.db')
    c = conn.cursor()
    c.execute('SELECT id, name, description FROM categories')
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
    st.title("Category Manager 🗂️")

    init_db()

    menu = ["Add Category", "View Categories"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Category":
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

    elif choice == "View Categories":
        st.subheader("📋 Manage Categories")

        categories = get_categories()
        if categories:
            for id, name, description in categories:
                with st.expander(f"{name}"):
                    st.write(f"**Description:** {description}")

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
        else:
            st.info("No categories found. Add some!")

if __name__ == '__main__':
    main()
