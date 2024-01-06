import sys
import sqlite3
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QTableWidgetItem, QTableWidget, QComboBox, QVBoxLayout, QGridLayout, QDialog, QWidget,
    QPushButton, QApplication, QMainWindow, QMessageBox, QLabel, QLineEdit, QHBoxLayout
)
from PyQt5.QtCore import QCoreApplication


class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect("sdms.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS student(sid INTEGER,Sname TEXT,dept INTEGER,year INTEGER,course_a INTEGER,course_b INTEGER,course_c INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS faculty(fid INTEGER,f_name TEXT,course INTEGER,dept INTEGER,class_room INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS Course(cid INTEGER,c_name INTEGER,faculty TEXT,credit INTEGER,type INTEGER,slot INTEGER,No_enrolled INTEGER)")

    def addStudent(self, sid, Sname, dept, year, course_a, course_b, course_c):
        try:
            self.c.execute("INSERT INTO student(sid, Sname, dept, year, course_a, course_b, course_c) VALUES (?,?,?,?,?,?,?)",(sid, Sname, dept, year, course_a, course_b, course_c))
            self.conn.commit()
            QMessageBox.information(QMessageBox(), 'Successful', 'Student is added successfully to the database.')
        except sqlite3.Error as e:
            print(f"Error adding student: {e}")
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add student to the database.')

    def searchStudent(self, sid):
        self.c.execute("SELECT * from student WHERE sid=?", (sid,))
        data = self.c.fetchone()

        if not data:
            QMessageBox.warning(QMessageBox(), 'Error', f'Could not find any student with roll no {sid}')
            return None

        student_details = list(data)
        self.c.close()
        self.conn.close()
        showStudent(student_details)

    def deleteRecord(self, sid):
        try:
            self.c.execute("DELETE from student WHERE sid=?", (sid,))
            self.conn.commit()
            QMessageBox.information(QMessageBox(), 'Successful', 'Student is deleted from the database.')
        except sqlite3.Error as e:
            print(f"Error deleting student: {e}")
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not delete student from the database.')


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.userNameLabel = QLabel("Username")
        self.userPassLabel = QLabel("Password")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QGridLayout(self)
        layout.addWidget(self.userNameLabel, 1, 1)
        layout.addWidget(self.userPassLabel, 2, 1)
        layout.addWidget(self.textName, 1, 2)
        layout.addWidget(self.textPass, 2, 2)
        layout.addWidget(self.buttonLogin, 3, 1, 1, 2)

        self.setWindowTitle("Login")

    def handleLogin(self):
        if self.textName.text() == '' and self.textPass.text() == '':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')


def showStudent(details):
    sid, sname, dept, year, course_a, course_b, course_c = details
    # ... (rest of the showStudent function remains unchanged)


class AddStudent(QDialog):
    def __init__(self):
        super().__init__()

        self.dept = -1
        self.year = -1
        self.sid = -1
        self.sname = ""
        self.course_a = -1
        self.course_b = -1
        self.course_c = -1

        # ... (rest of the AddStudent class remains unchanged)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... (rest of the Window class remains unchanged)

    def showStudent(self):
        if self.editField.text() == "":
            QMessageBox.warning(QMessageBox(), 'Error', 'You must give the roll number to show the results for.')
            return None
        self.dbhelper.searchStudent(int(self.editField.text()))

    def deleteRecord(self):
        if self.editFieldDelete.text() == "":
            QMessageBox.warning(QMessageBox(), 'Error', 'You must give the roll number to show the results for.')
            return None
        self.dbhelper.deleteRecord(int(self.editFieldDelete.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
    sys.exit(app.exec_())
