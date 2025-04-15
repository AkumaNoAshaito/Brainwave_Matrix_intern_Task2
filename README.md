A complete Inventory Management System built using Python, PyQt6, and MySQL, designed to handle product records, user management, and inventory dispatching with role-based access control.

📌 Project Overview
This system was developed as part of my internship at Brainwave. It provides an intuitive GUI for Admins and Users to manage and interact with the inventory efficiently.

🎯 Features
🔐 Authentication
Secure login system with role-based access.

Separate dashboards for Admin and User roles.

🛠 Admin Functionalities
Add / Edit / Delete products.

Add / Remove users.

Dispatch products to distributors.

View all inventory data in a structured table.

Logout functionality.

👤 User Functionalities
View inventory data.

Dispatch product (with limited access).

Logout functionality.

📊 GUI Design
Developed using PyQt6.

Centralized table view of inventory.

Sidebar buttons for admin/user actions.

🗄 Database
Integrated with MySQL to store:

Product details

User credentials and roles

Dispatch history

🧰 Tech Stack

Technology	Purpose
Python	Core programming language
PyQt6	GUI Development
MySQL	Database for storage
MySQL Connector	Python-MySQL DB connectivity
🚀 Getting Started
🔧 Prerequisites
Python 3.10+

MySQL Server

Required Python packages (install using pip):

bash
Copy
Edit
pip install pyqt6 mysql-connector-python
🛠 Setup Instructions
Clone the repository:

bash
Copy
Edit
git clone https://github.com/AkumaNoAshaito/Brainwave_Matrix_intern_Task2.git
cd inventory-management-system
Set up the MySQL database:

Create a new MySQL database.

Import the schema.sql file (if available) or create users and products tables manually.

Update host, user, password, and database values in the Python code.

Run the application:

bash
Copy
Edit
python Inventory_management.py
🖼️ Screenshots
(Add relevant screenshots of the Admin panel, User view, dispatching interface, etc.)

📁 Project Structure
bash
Copy
Edit
Inventory_management.py       # Main GUI logic and database integration
config.py (optional)          # DB connection credentials
assets/                       # UI assets (if any)
README.md                     # Project documentation
📌 Future Enhancements
Implement product dispatch logging

Add analytics/dashboard for admin

Enable search/filter/sort in inventory table

Role-based permission levels for users
