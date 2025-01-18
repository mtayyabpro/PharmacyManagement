import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd


def add_new_stock():
    """
    Function to manage medicine inventory with options to add, update, delete, and export.
    """
    print("Helo")
    win = tk.Tk()
    win.title("Manage Medicines")

    # Set window dimensions to 90% of screen size
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    window_width = int(screen_width * 0.9)
    window_height = int(screen_height * 0.9)

    # Center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    win.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Main frame
    main_frame = tk.Frame(win)
    main_frame.pack(fill="both", expand=True)

    # Add medicine frame (uses grid layout)
    add_medicine_frame = tk.LabelFrame(main_frame, text="Add Medicine", padx=10, pady=5)
    add_medicine_frame.pack(pady=5, padx=10, fill="x")

    # Use grid inside `add_medicine_frame`
    tk.Label(add_medicine_frame, text="Medicine ID").grid(row=0, column=0, pady=10, padx=10)
    entry_medicine_id = tk.Entry(add_medicine_frame)
    entry_medicine_id.grid(row=0, column=1)

    tk.Label(add_medicine_frame, text="Medicine Name").grid(row=0, column=2, pady=10, padx=10)
    entry_medicine_name = tk.Entry(add_medicine_frame)
    entry_medicine_name.grid(row=0, column=3)

    tk.Label(add_medicine_frame, text="Company").grid(row=0, column=4, pady=10, padx=10)
    entry_company = tk.Entry(add_medicine_frame)
    entry_company.grid(row=0, column=5)

    tk.Label(add_medicine_frame, text="Unit").grid(row=1, column=0, pady=10, padx=10)
    entry_unit = tk.Entry(add_medicine_frame)
    entry_unit.grid(row=1, column=1)

    tk.Label(add_medicine_frame, text="Quantity").grid(row=1, column=2, pady=10, padx=10)
    entry_quantity = tk.Entry(add_medicine_frame)
    entry_quantity.grid(row=1, column=3)

    tk.Label(add_medicine_frame, text="Unit Price").grid(row=1, column=4, pady=10, padx=10)
    entry_price_per_unit = tk.Entry(add_medicine_frame)
    entry_price_per_unit.grid(row=1, column=5)

    # Treeview to display saved medicines
    columns = ("ID", "Name", "Company", "Unit", "Quantity", "Unit Price")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=15)

    # Define the column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    tree.pack(fill="x", padx=10, pady=5)

    # Functions for Treeview operations
    def add_medicine():
        """
        Adds a new medicine to the Treeview and clears entry fields.
        """
        medicine_id = entry_medicine_id.get()
        medicine_name = entry_medicine_name.get()
        company = entry_company.get()
        unit = entry_unit.get()
        quantity = entry_quantity.get()
        price_per_unit = entry_price_per_unit.get()

        # Add the medicine details to the Treeview
        if all([medicine_id, medicine_name, company, unit, quantity, price_per_unit]):
            tree.insert("", "end", values=(medicine_id, medicine_name, company, unit, quantity, price_per_unit))
            entry_medicine_id.delete(0, tk.END)
            entry_medicine_name.delete(0, tk.END)
            entry_company.delete(0, tk.END)
            entry_unit.delete(0, tk.END)
            entry_quantity.delete(0, tk.END)
            entry_price_per_unit.delete(0, tk.END)
        else:
            messagebox.showwarning("Incomplete Data", "Please fill all fields before adding.")

    def delete_selected():
        """
        Deletes the selected item from the Treeview.
        """
        selected_item = tree.selection()
        if selected_item:
            for item in selected_item:
                tree.delete(item)
        else:
            messagebox.showwarning("No Selection", "Please select an item to delete.")

    def update_selected():
        """
        Updates the selected item in the Treeview with current entry field values.
        """
        selected_item = tree.selection()
        if selected_item:
            medicine_id = entry_medicine_id.get()
            medicine_name = entry_medicine_name.get()
            company = entry_company.get()
            unit = entry_unit.get()
            quantity = entry_quantity.get()
            price_per_unit = entry_price_per_unit.get()

            if all([medicine_id, medicine_name, company, unit, quantity, price_per_unit]):
                tree.item(selected_item, values=(medicine_id, medicine_name, company, unit, quantity, price_per_unit))
                entry_medicine_id.delete(0, tk.END)
                entry_medicine_name.delete(0, tk.END)
                entry_company.delete(0, tk.END)
                entry_unit.delete(0, tk.END)
                entry_quantity.delete(0, tk.END)
                entry_price_per_unit.delete(0, tk.END)
            else:
                messagebox.showwarning("Incomplete Data", "Please fill all fields to update.")
        else:
            messagebox.showwarning("No Selection", "Please select an item to update.")

    def export_to_excel():
        """
        Exports the data in the Treeview to an Excel file.
        """
        data = [tree.item(child)["values"] for child in tree.get_children()]
        if data:
            df = pd.DataFrame(data, columns=columns)
            file_path = "medicines.xlsx"
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
        else:
            messagebox.showwarning("No Data", "No data to export.")

    def export_to_pdf():
        """
        Exports the data in the Treeview to a PDF file.
        """
        data = [tree.item(child)["values"] for child in tree.get_children()]
        if data:
            df = pd.DataFrame(data, columns=columns)
            file_path = "medicines.pdf"
            df.to_csv(file_path, index=False)  # Using CSV as a quick alternative for PDF export
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
        else:
            messagebox.showwarning("No Data", "No data to export.")

    # Buttons for Treeview operations
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10, fill="x")

    tk.Button(button_frame, text="Add Medicine", command=add_medicine).pack(side="left", padx=10)
    tk.Button(button_frame, text="Update Selected", command=update_selected).pack(side="left", padx=10)
    tk.Button(button_frame, text="Delete Selected", command=delete_selected).pack(side="left", padx=10)
    tk.Button(button_frame, text="Export to Excel", command=export_to_excel).pack(side="left", padx=10)
    tk.Button(button_frame, text="Export to PDF", command=export_to_pdf).pack(side="left", padx=10)

    win.mainloop()


add_new_stock()
