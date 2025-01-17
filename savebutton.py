def save_data():
    # Retrieve patient details
    patient_data = {
        "First Name": entry_first_name.get(),
        "Last Name": entry_last_name.get(),
        "Father Name": entry_father_name.get(),
        "CNIC": entry_cnic_no.get(),
        "Address": entry_address.get(),
        "Age": entry_age.get(),
        "Sex": entry_sex.get(),
        "MR No": entry_mr_no.get(),
        "Hospital No": entry_hospital_no.get(),
        "Company No": entry_company_no.get(),
        "Diagnosis": entry_diagnosis.get(),
        "Procedure": entry_procedure.get(),
    }

    # Retrieve medicine data
    medicine_data = {}
    for i, medicine in enumerate(medicine_names):
        column = i // rows_per_column
        row = i % rows_per_column
        quantity_entry = scrollable_frame.grid_slaves(row=row, column=column + 1)[0]
        medicine_data[medicine] = quantity_entry.get()

    # Print or save the data (e.g., to a file or database)
    print("Patient Data:", patient_data)
    print("Medicine Data:", medicine_data)
