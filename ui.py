import tkinter as tk
from tkinter import ttk
from medicines import add_new_stock

# Placeholder for add_new_stock function (You can replace this with actual functionality)


def add_patient_screen():
    root = tk.Tk()
    root.title("Add Patient and Medicine Detail")

    # Set window dimensions to 80% of screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)

    # Center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Sidebar
    sidebar = tk.Frame(root, width=300, bg="lightblue", relief="raised", borderwidth=2)
    sidebar.pack(side="left", fill="y")

    # Add buttons or labels in the sidebar
    sidebar_title = tk.Label(sidebar, text="Menu", font=("Arial", 16, "bold"), bg="lightblue")
    sidebar_title.pack(pady=10)

    buttons = [
        ("Add Patient and Used Medicine", lambda: print("Navigate to Add Patient and Used Medicine")),
        ("Add medicines", add_new_stock),  # Pass the function reference, not the result of the function
        ("Add Users", lambda: print("Navigate to Add Users")),
        ("Settings", lambda: print("Navigate to Settings")),
        ("Help", lambda: print("Navigate to Help")),
        ("Exit", root.quit),  # Built-in method to exit the application
    ]

    for button_text, command in buttons:
        btn = tk.Button(sidebar, text=button_text, width=30, padx=10, pady=5, command=command)
        btn.pack(pady=5)

    # Main Frame
    main_frame = tk.Frame(root)
    main_frame.pack(side="right", fill="both", expand=True)

    # Patient Details Section
    patient_frame = tk.LabelFrame(main_frame, text="Patient Details", padx=10, pady=5)
    patient_frame.pack(pady=5, padx=10, fill="x")

    # Define labels and entries for patient details
    patient_fields = [
        ("First Name", 0, 0), ("Last Name", 0, 2),
        ("Father Name", 0, 4), ("CNIC No", 0, 6),
        ("Address", 1, 0), ("Age", 1, 2),
        ("Sex", 1, 4), ("MR No", 1, 6),
        ("Hospital No", 2, 0), ("Company No", 2, 2),
        ("Diagnosis", 2, 4), ("Operation", 2, 6),
    ]
    entries = {}
    for label_text, row, col in patient_fields:
        label = tk.Label(patient_frame, text=f"{label_text}:")
        label.grid(row=row, column=col, padx=10, pady=5, sticky="e")

        if label_text == "Sex":
            entry = ttk.Combobox(patient_frame, values=["Male", "Female", "Others"], width=27)
        else:
            entry = tk.Entry(patient_frame, width=30, bg="lightyellow")
        entry.grid(row=row, column=col + 1, padx=10, pady=5, sticky="w")
        entries[label_text] = entry

    # Medicine Details Section
    medicine_frame = tk.LabelFrame(main_frame, text="Medicine Details", padx=10, pady=5)
    medicine_frame.pack(pady=5, padx=10, fill="both", expand=False)

    # Create a scrollable canvas for medicines
    canvas = tk.Canvas(medicine_frame)
    scrollbar = ttk.Scrollbar(medicine_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    # Configure canvas and scrollbar
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Medicine names and quantity input
    medicine_names = [
             "IV Line 24", "IV Line 22", "IV LIne 20", "IV line 18", "Inj. Nalbin 10mg",
        "Inj. Toradol 30mg", "Inj. Propofol", "Inj. Sux 30mg", "Inj. Acuron 50mg", "Inj. Acuron 30mg",
        "Inj. Adrenaline 1000u", "Inj. Atropine", "Inj. Dexamethasone", "Inj. Medazolam", "Inj. Ntronal",
        "Inj. Labetalol", "Inj. Bupicain SP", "Inj. Xylocain 2% 10ml", "Inj. R/L 100ml", "Inj. N/S 1000ml",
        "Inj. Ceftriaxon 500mg", "Inj. Ceftriaxon 1g", "Inj. 2sum 2g", "Inj. Gentamycin", "Inj. Amikacin 500mg",
        "Inj. Flagyl", "Inj. Omeprazol 40mg", "Inj. Linezolid", "ETT", "Nitto 1 inch",
        "Inj. Hydrocortisone", "D/S 5cc", "D/S 10cc", "D/S 20cc", "D/S 60cc",
        "S/Gauze", "Abdominal Sponge", "Yanker set", "Diathermy Lead", "Pyodine Scrub 450ml",
        "Pyodine Solution 450ml", "S/Gloves 6.5", "S/Gloves 7", "S/Gloves 7.5", "S/Gloves 8", "crape Bandage 4 inch",
        "Crape Bandage 6 inch", "Cotton Bandage", "LP Needle No 25", "Proline 2/0 Straight", "Proline 1", "Vicryl 1", "Vicryl 2/0",
        "Silk 1", "Cap", "Mask", "Top Gloves", "Breathing Circut", "S/Blade 23", "S/Blade 15", "S/B 11", "S/Blade 10", "Softban Cotton 4 inch",
        "Softban Cotton 6 inch", "Gypsona 4 inch", "Gypsona 6 inch", "Reduvic Drain", "Nelton", "Urine Bag", "Feeding Tube",
        "Hydrogen", "Inj. Provas"
        # Add more medicines as required...
    ]
    for idx, name in enumerate(medicine_names):
        row, col = divmod(idx, 6)  # Organize into 6 columns
        label = tk.Label(scrollable_frame, text=name)
        label.grid(row=row, column=col * 2, padx=5, pady=5, sticky="w")
        entry = tk.Entry(scrollable_frame, width=10)
        entry.grid(row=row, column=col * 2 + 1, padx=5, pady=5)

    root.mainloop()


# Run the application
add_patient_screen()
