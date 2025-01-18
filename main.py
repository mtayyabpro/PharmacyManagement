from database_connection import create_connection, close_connection
from ui import add_patient_screen
from medicines import add_new_stock


def main():
    print("Starting the application...")

    # Create a database connection
    connection = create_connection()
    if connection:
        print("Database connected successfully.")

        # Launch the UI
        add_patient_screen()
        add_new_stock()

        # Close the database connection
        close_connection(connection)
    else:
        print("Unable to start application due to database connection failure.")


if __name__ == "__main__":
    main()
