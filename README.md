# Capstone Project – Leasing House Management System

This project is a Python-based desktop application developed as part of a Master of Science capstone project.
It provides an integrated system for managing customers, employees, services, sales, and reporting through a graphical user interface.

The application focuses on service tracking, reporting, and analytics using a MySQL backend.

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

## Available Scripts

In the project directory, you can run:

### `pip install -r requirements.txt`

Installs all the required Python dependencies to run the application.

### `python "py files/main.py"`

Runs the application in desktop GUI mode.  
The main window will open using CustomTkinter.

## Fantastic Features Implemented

- **Interactive Property Location Map**
  - Uses TkinterMapView to display housing and office locations on an interactive map.
  - Selecting a property automatically zooms and centers the map on its location.
  - Location markers help users quickly understand where properties are located.

- **Map Export (PNG & PDF)**
  - The current map view can be saved as an image or a PDF file.
  - Useful for documentation, reports, and sharing location details.

- **Service Reporting Dashboard**
  - Service records are shown in a table along with a monthly bar chart.
  - The chart updates automatically based on data pulled from the database.

- **CSV and PDF Report Generation**
  - Service and sales data can be exported as CSV files for spreadsheet use.
  - PDF reports are generated for clean, professional documentation.

- **Sortable and Scrollable Data Tables**
  - Tables support scrolling and sorting by service date.
  - Analytics update automatically when sorting is applied.

- **Role-Based Modules**
  - Separate screens for admin, owner, employee, and customer roles.
  - Simple button-based navigation between modules.

- **Date Picker for Data Entry**
  - Calendar-based date selection reduces manual input errors.

- **MySQL Database Integration**
  - All application data is stored and retrieved using a MySQL database.
  - Individual job cards can be searched and exported as reports.

## Technologies Used

- Python 3.11+
- CustomTkinter (GUI)
- MySQL
- Matplotlib
- ReportLab

## Database Configuration

The application requires a MySQL database.

Before running the project:
1. Create the required database and tables
2. Update database connection details in the Python files
3. Ensure the MySQL service is running

> **Note:** Database credentials are not included in this repository for security reasons.

## Environment Notes

- A Python virtual environment (`venv`) is recommended
- The `venv` directory is excluded from version control
- Generated reports are stored locally in the `Service_Reports` and `Sales_Reports` folders

## Academic Context

This project was developed as part of a graduate-level capstone course to demonstrate applied skills 
in Python application development, database integration, and desktop software design.

## Author

Lokesh Varma
