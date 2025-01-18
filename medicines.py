import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from openpyxl import Workbook
from database_connection import create_connection, close_connection


def add_new_stock():
    """
    Function to add, edit, delete, and fetch medicines from the database.
    """

    def add_to_database(medicine_data):
        """Insert a new medicine into the database."""
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = """
                    INSERT INTO medicines (medicine_name, company, quantitiy, price_per_unit, total_price, reorde_level)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, medicine_data)
                connection.commit()
                messagebox.showinfo("Success", "Medicine added successfully!")
                fetch_data_from_db()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add medicine: {e}")
            finally:
                close_connection(connection)

    def fetch_data_from_db():
        """Fetch all medicine data from the database and populate the Treeview."""
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM medicines")
                rows = cursor.fetchall()
                # Clear the Treeview
                for item in tree.get_children():
                    tree.delete(item)
                # Insert fetched data into the Treeview
                for row in rows:
                    tree.insert("", "end", values=row)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch data: {e}")
            finally:
                close_connection(connection)

    def edit_in_database(medicine_data):
        """Update an existing medicine in the database."""
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                update_query = """
                    UPDATE medicines
                    SET medicine_name = %s, company = %s, quantitiy = %s,
                        price_per_unit = %s, total_price = %s, reorde_level = %s
                    WHERE medicine_id = %s
                """
                cursor.execute(update_query, medicine_data)
                connection.commit()
                messagebox.showinfo("Success", "Medicine updated successfully!")
                fetch_data_from_db()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update medicine: {e}")
            finally:
                close_connection(connection)

    def delete_from_database(medicine_id):
        """Delete a medicine from the database."""
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                delete_query = "DELETE FROM medicines WHERE medicine_id = %s"
                cursor.execute(delete_query, (medicine_id,))
                connection.commit()
                messagebox.showinfo("Success", "Medicine deleted successfully!")
                fetch_data_from_db()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete medicine: {e}")
            finally:
                close_connection(connection)

    def add_medicine():
        """Collect data from input fields and add it to the database."""
        try:
            total_price = float(entry_quantitiy.get()) * float(entry_price_per_unit.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or price.")
            return

        medicine_data = (
            combobox_medicine_name.get(),
            entry_company.get(),
            entry_quantitiy.get(),
            entry_price_per_unit.get(),
            str(total_price),
            entry_reorde_level.get(),
        )
        add_to_database(medicine_data)

    def edit_selected(item_id):
        """Edit the selected medicine."""
        selected_item = tree.item(item_id)
        values = selected_item["values"]
        if not values:
            return
        # Populate entry fields with selected item values
        combobox_medicine_name.set(values[1])
        entry_company.delete(0, tk.END)
        entry_quantitiy.delete(0, tk.END)
        entry_price_per_unit.delete(0, tk.END)
        entry_reorde_level.delete(0, tk.END)

        entry_company.insert(0, values[2])
        entry_quantitiy.insert(0, values[3])
        entry_price_per_unit.insert(0, values[4])
        entry_reorde_level.insert(0, values[5])

        # Update the database on save
        def save_changes():
            try:
                total_price = float(entry_quantitiy.get()) * float(entry_price_per_unit.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid input for quantity or price.")
                return

            medicine_data = (
                combobox_medicine_name.get(),
                entry_company.get(),
                entry_quantitiy.get(),
                entry_price_per_unit.get(),
                str(total_price),
                entry_reorde_level.get(),
                values[0],  # Using the existing medicine_id from the selected row
            )
            edit_in_database(medicine_data)
            save_btn.destroy()

        save_btn = tk.Button(add_medicine_frame, text="Save Changes", command=save_changes)
        save_btn.grid(row=2, column=8, padx=20, pady=10)

    def delete_selected(item_id):
        """Delete the selected medicine from the database."""
        selected_item = tree.item(item_id)
        values = selected_item["values"]
        if not values:
            return
        medicine_id = values[0]
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete Medicine ID: {medicine_id}?")
        if confirm:
            delete_from_database(medicine_id)

    def download_to_excel():
        """Export medicine data to an Excel file."""
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM medicines")
                rows = cursor.fetchall()

                wb = Workbook()
                ws = wb.active
                ws.title = "Medicines"

                # Adding headers
                ws.append(["Medicine ID", "Medicine Name", "Company", "Quantity", "Unit Price", "Total Price",
                           "Reorder Level"])

                # Adding data rows
                for row in rows:
                    ws.append(row)

                # Save the file
                wb.save("medicines_data.xlsx")
                messagebox.showinfo("Success", "Data exported to Excel successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to export to Excel: {e}")
            finally:
                close_connection(connection)

    def fetch_medicine_names():
        """Fetch all medicine names from the database to populate Combobox."""
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT medicine_name FROM medicines")
                medicines = cursor.fetchall()
                # Extract only medicine names from the result
                medicine_names = [medicine[0] for medicine in medicines]
                return medicine_names
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch medicines: {e}")
                return []
            finally:
                close_connection(connection)

    def on_type_in_combobox(event):
        """Fetch and update combobox suggestions as user types."""
        typed_value = combobox_medicine_name.get()
        medicine_names = fetch_medicine_names()

        filtered_names = [name for name in medicine_names if typed_value.lower() in name.lower()]
        combobox_medicine_name['values'] = filtered_names
        if typed_value == "":
            combobox_medicine_name['values'] = medicine_names

    win = tk.Tk()
    win.title("Medicine Management")

    # Main frame
    main_frame = tk.Frame(win)
    main_frame.pack(fill="both", expand=True)

    # Add medicine frame
    add_medicine_frame = tk.LabelFrame(main_frame, text="Add/Edit Medicine", padx=10, pady=5)
    add_medicine_frame.pack(pady=5, padx=10, fill="x")

    # Entry fields for adding medicine
    lb_medicine_name = tk.Label(add_medicine_frame, text="Medicine Name")
    lb_medicine_name.grid(row=0, column=0, pady=10, padx=10)

    combobox_medicine_name = ttk.Combobox(add_medicine_frame, state="normal")
    combobox_medicine_name.grid(row=0, column=1)

    # Bind the key release event to update the suggestions dynamically
    combobox_medicine_name.bind('<KeyRelease>', on_type_in_combobox)

    lb_company = tk.Label(add_medicine_frame, text="Company")
    lb_company.grid(row=0, column=2, pady=10, padx=10)
    entry_company = tk.Entry(add_medicine_frame)
    entry_company.grid(row=0, column=3)

    lb_quantitiy = tk.Label(add_medicine_frame, text="Quantity")
    lb_quantitiy.grid(row=1, column=0, pady=10, padx=10)
    entry_quantitiy = tk.Entry(add_medicine_frame)
    entry_quantitiy.grid(row=1, column=1)

    lb_price_per_unit = tk.Label(add_medicine_frame, text="Unit Price")
    lb_price_per_unit.grid(row=1, column=2, pady=10, padx=10)
    entry_price_per_unit = tk.Entry(add_medicine_frame)
    entry_price_per_unit.grid(row=1, column=3)

    lb_reorde_level = tk.Label(add_medicine_frame, text="Reorder Level")
    lb_reorde_level.grid(row=1, column=4, pady=10, padx=10)
    entry_reorde_level = tk.Entry(add_medicine_frame)
    entry_reorde_level.grid(row=1, column=5)

    add_btn = tk.Button(add_medicine_frame, text="Add Medicine", command=add_medicine)
    add_btn.grid(row=1, column=6, padx=20, pady=10)

    # Treeview for listing medicines
    tree_frame = tk.Frame(main_frame)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(tree_frame,
                        columns=("Name", "Company", "Quantity", "Unit Price", "Total Price", "Reorder Level"),
                        show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Company", text="Company")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Unit Price", text="Unit Price")
    tree.heading("Total Price", text="Total Price")
    tree.heading("Reorder Level", text="Reorder Level")
    tree.pack(fill="both", expand=True)

    tree.bind("<Delete>", lambda event: delete_selected(tree.focus()))  # Delete record on key press

    # Buttons for Update, Delete, and Export to Excel
    update_btn = tk.Button(main_frame, text="Update", command=lambda: edit_selected(tree.focus()))
    update_btn.pack(pady=5)

    delete_btn = tk.Button(main_frame, text="Delete", command=lambda: delete_selected(tree.focus()))
    delete_btn.pack(pady=5)

    excel_btn = tk.Button(main_frame, text="Download to Excel", command=download_to_excel)
    excel_btn.pack(pady=5)

    fetch_data_from_db()

    win.mainloop()


add_new_stock()
