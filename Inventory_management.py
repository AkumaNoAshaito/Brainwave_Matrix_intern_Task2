import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QCheckBox, QHBoxLayout, QComboBox, QInputDialog, QSpinBox
from PyQt6.QtWidgets import QFormLayout

def connect_db():
    return mysql.connector.connect(host="localhost", user="root", password="Kamal2006", database="inventory_db")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(500, 200, 300, 200)
        
        layout = QVBoxLayout()
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton("Login", self)
        self.login_btn.clicked.connect(self.authenticate)
        
        layout.addWidget(QLabel("Inventory Management Login"))
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)
    
    def authenticate(self):
        db = connect_db()
        cursor = db.cursor()
        query = "SELECT role FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (self.username.text(), self.password.text()))
        result = cursor.fetchone()
        db.close()
        if result:
            role = result[0]
            if role == "admin":
                self.inventory_window = AdminWindow()
            else:
                self.inventory_window = UserWindow()
            self.inventory_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel - Inventory Manager")
        self.setGeometry(400, 100, 800, 500)
        
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Product ID", "Name", "Quantity"])
        self.load_data()
        
        self.add_product_btn = QPushButton("Add Product")
        self.add_product_btn.clicked.connect(self.add_product)
        self.edit_product_btn = QPushButton("Edit Product")
        self.edit_product_btn.clicked.connect(self.edit_product)
        self.delete_product_btn = QPushButton("Delete Product")
        self.delete_product_btn.clicked.connect(self.delete_product)
        self.dispatch_btn = QPushButton("Dispatch Product")
        self.dispatch_btn.clicked.connect(self.dispatch_product)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        
        layout.addWidget(QLabel("Admin Inventory List"))
        layout.addWidget(self.table)
        layout.addWidget(self.add_product_btn)
        layout.addWidget(self.edit_product_btn)
        layout.addWidget(self.delete_product_btn)
        layout.addWidget(self.dispatch_btn)
        layout.addWidget(self.logout_btn)
        self.add_user_btn = QPushButton("Add User")
        self.add_user_btn.clicked.connect(self.add_user)
        self.remove_user_btn = QPushButton("Remove User")
        self.remove_user_btn.clicked.connect(self.remove_user)
        layout.addWidget(self.add_user_btn)
        layout.addWidget(self.remove_user_btn)

        self.setLayout(layout)
    
    def load_data(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        self.table.setRowCount(len(products))
        for i, product in enumerate(products):
            for j, data in enumerate(product):
                self.table.setItem(i, j, QTableWidgetItem(str(data)))
        db.close()

    def add_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New User")
        layout = QFormLayout()
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addRow("Username:", username_input)
        layout.addRow("Password:", password_input)
        btn = QPushButton("Add User")
        btn.clicked.connect(lambda: self.confirm_add_user(dialog, username_input, password_input))
        layout.addWidget(btn)            
        dialog.setLayout(layout)
        dialog.exec()

    def confirm_add_user(self, dialog, username_input, password_input):
        username = username_input.text().strip()
        password = password_input.text().strip()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return     
        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, 'user'))
            db.commit()
            QMessageBox.information(self, "Success", "User added successfully!")
            dialog.close()
        except mysql.connector.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")
            db.close()
    
    def remove_user(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Remove User")
        layout = QVBoxLayout()
        user_list = QComboBox()
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT username FROM users WHERE role = 'user'")
        users = cursor.fetchall()
        db.close()
        if not users:
            QMessageBox.information(self, "Info", "No users available to remove.")
            return
        for user in users:
            user_list.addItem(user[0])
        btn = QPushButton("Remove Selected User")
        btn.clicked.connect(lambda: self.confirm_remove_user(dialog, user_list))
        layout.addWidget(QLabel("Select a user to remove:"))
        layout.addWidget(user_list)
        layout.addWidget(btn)
        dialog.setLayout(layout)
        dialog.exec()

    def confirm_remove_user(self, dialog, user_list):
        selected_user = user_list.currentText()
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s AND role = 'user'", (selected_user,))
        db.commit()
        db.close()
        QMessageBox.information(self, "Success", f"User '{selected_user}' removed successfully.")
        dialog.close()



    def add_product(self):
        name, ok1 = QInputDialog.getText(self, "Add Product", "Enter product name:")
        if ok1:
            quantity, ok2 = QInputDialog.getInt(self, "Add Product", "Enter quantity:")
            if ok2:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO products (name, quantity) VALUES (%s, %s)", (name, quantity))
                db.commit()
                db.close()
                self.load_data()
                QMessageBox.information(self, "Success", "Product Added Successfully!")
    
    def edit_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No product selected.")
            return
        
        product_id = self.table.item(selected_row, 0).text()
        product_name = self.table.item(selected_row, 1).text()
        current_quantity = self.table.item(selected_row, 2).text()

        new_name, ok1 = QInputDialog.getText(self, "Edit Product", "Enter new product name:", text=product_name)
        if ok1:
            new_quantity, ok2 = QInputDialog.getInt(self, "Edit Product", "Enter new quantity:", value=int(current_quantity))
            if ok2:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("UPDATE products SET name = %s, quantity = %s WHERE id = %s", (new_name, new_quantity, product_id))
                db.commit()
                db.close()
                self.load_data()
                QMessageBox.information(self, "Success", "Product updated successfully!")
    
    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "No product selected.")
            return
        
        product_id = self.table.item(selected_row, 0).text()
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.commit()
        db.close()
        self.load_data()
        QMessageBox.information(self, "Success", "Product deleted successfully!")
    
    def dispatch_product(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM products")
        products = cursor.fetchall()
        cursor.execute("SELECT id, name FROM distributors")
        distributors = cursor.fetchall()
        db.close()
        
        if not products:
            QMessageBox.warning(self, "Error", "No products available.")
            return
        if not distributors:
            QMessageBox.warning(self, "Error", "No distributors available.")
            return
        
        dispatch_dialog = QDialog(self)
        dispatch_dialog.setWindowTitle("Dispatch Products")
        layout = QVBoxLayout()
        self.product_selection = []
        
        for product in products:
            product_id, name = product
            hbox = QHBoxLayout()
            checkbox = QCheckBox(name)
            quantity_selector = QSpinBox()
            quantity_selector.setRange(1, 100)
            hbox.addWidget(checkbox)
            hbox.addWidget(quantity_selector)
            layout.addLayout(hbox)
            self.product_selection.append((product_id, checkbox, quantity_selector))
        
        distributor_combo = QComboBox()
        for distributor in distributors:
            distributor_combo.addItem(f"{distributor[0]} - {distributor[1]}", distributor[0])
        
        dispatch_btn = QPushButton("Proceed")
        dispatch_btn.clicked.connect(lambda: self.confirm_dispatch(dispatch_dialog, distributor_combo))
        
        layout.addWidget(QLabel("Select Distributor"))
        layout.addWidget(distributor_combo)
        layout.addWidget(dispatch_btn)
        dispatch_dialog.setLayout(layout)
        dispatch_dialog.exec()
    
    def confirm_dispatch(self, dialog, distributor_combo):
        selected_products = [(p[0], p[2].value()) for p in self.product_selection if p[1].isChecked()]
        
        if not selected_products:
            QMessageBox.warning(self, "Error", "No products selected.")
            return
        
        db = connect_db()
        cursor = db.cursor()
        
        for product_id, quantity in selected_products:
            cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
            available_quantity = cursor.fetchone()[0]
            if quantity > available_quantity:
                QMessageBox.warning(self, "Error", f"Insufficient stock for product ID {product_id}.")
                db.close()
                return
        
        for product_id, quantity in selected_products:
            cursor.execute("UPDATE products SET quantity = quantity - %s WHERE id = %s", (quantity, product_id))
        
        db.commit()
        db.close()
        self.load_data()
        QMessageBox.information(self, "Success", "Products dispatched successfully!")
        dialog.close()

    def logout(self):
        self.close()
        login_window = LoginWindow()
        login_window.show()
class UserWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Panel - Inventory Viewer")
        self.setGeometry(400, 100, 800, 500)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Product ID", "Name", "Quantity"])
        self.load_data()

        self.dispatch_btn = QPushButton("Dispatch Product")
        self.dispatch_btn.clicked.connect(self.dispatch_product)
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)

        layout.addWidget(QLabel("Inventory List (User View)"))
        layout.addWidget(self.table)
        layout.addWidget(self.dispatch_btn)
        layout.addWidget(self.logout_btn)

        self.setLayout(layout)

    def load_data(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        self.table.setRowCount(len(products))
        for i, product in enumerate(products):
            for j, data in enumerate(product):
                self.table.setItem(i, j, QTableWidgetItem(str(data)))
        db.close()

    def dispatch_product(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM products")
        products = cursor.fetchall()
        cursor.execute("SELECT id, name FROM distributors")
        distributors = cursor.fetchall()
        db.close()

        if not products:
            QMessageBox.warning(self, "Error", "No products available.")
            return
        if not distributors:
            QMessageBox.warning(self, "Error", "No distributors available.")
            return

        dispatch_dialog = QDialog(self)
        dispatch_dialog.setWindowTitle("Dispatch Products")
        layout = QVBoxLayout()
        self.product_selection = []

        for product in products:
            product_id, name = product
            hbox = QHBoxLayout()
            checkbox = QCheckBox(name)
            quantity_selector = QSpinBox()
            quantity_selector.setRange(1, 100)
            hbox.addWidget(checkbox)
            hbox.addWidget(quantity_selector)
            layout.addLayout(hbox)
            self.product_selection.append((product_id, checkbox, quantity_selector))

        distributor_combo = QComboBox()
        for distributor in distributors:
            distributor_combo.addItem(f"{distributor[0]} - {distributor[1]}", distributor[0])

        dispatch_btn = QPushButton("Proceed")
        dispatch_btn.clicked.connect(lambda: self.confirm_dispatch(dispatch_dialog, distributor_combo))

        layout.addWidget(QLabel("Select Distributor"))
        layout.addWidget(distributor_combo)
        layout.addWidget(dispatch_btn)
        dispatch_dialog.setLayout(layout)
        dispatch_dialog.exec()

    def confirm_dispatch(self, dialog, distributor_combo):
        selected_products = [(p[0], p[2].value()) for p in self.product_selection if p[1].isChecked()]

        if not selected_products:
            QMessageBox.warning(self, "Error", "No products selected.")
            return

        db = connect_db()
        cursor = db.cursor()

        for product_id, quantity in selected_products:
            cursor.execute("SELECT quantity FROM products WHERE id = %s", (product_id,))
            available_quantity = cursor.fetchone()[0]
            if quantity > available_quantity:
                QMessageBox.warning(self, "Error", f"Insufficient stock for product ID {product_id}.")
                db.close()
                return

        for product_id, quantity in selected_products:
            cursor.execute("UPDATE products SET quantity = quantity - %s WHERE id = %s", (quantity, product_id))

        db.commit()
        db.close()
        self.load_data()
        QMessageBox.information(self, "Success", "Products dispatched successfully!")
        dialog.close()

    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())

    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())

    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())