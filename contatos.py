import sys

from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *


class Form(QDialog):
    
    def __init__(self, parent=None, id=None):
        super().__init__(parent)
        loadUi("form.ui", self)
        #db connection instance
        self.query = QSqlQuery()
        self.btn_cancel.clicked.connect(self.close)
        
        #check if is update or create
        if id:
            self.id = id
            self.btn_save.clicked.connect(self.update)
            self.btn_delete.clicked.connect(self.delete)
            
            #Get contact data for update
            query = 'SELECT * FROM contacts WHERE id = %i' % self.id
            self.query.exec_(query)
            if self.query.next():
                #fill fields with data
                self.name.setText(self.query.value(1))
                self.cellphone.setText(self.query.value(2))
                self.phone.setText(self.query.value(3))
                self.email.setText(self.query.value(4))
        else:
            self.btn_save.clicked.connect(self.save)
            #if create hide delete button
            self.btn_delete.hide()

    def save(self):
        if False: #Add data valitation conditions
            pass #Error notification
        else:
            data = (self.name.text(), self.cellphone.text(), self.phone.text(), self.email.text())
            query = "INSERT INTO contacts (name, cellphone, phone, email) VALUES ('%s', '%s', '%s', '%s');" % data
            self.query.exec_(query)
            self.close()

    def update(self):
        data = (self.name.text(), self.cellphone.text(), self.phone.text(), self.email.text(), self.id)
        query = "UPDATE contacts SET name='%s', cellphone='%s', phone='%s', email='%s' WHERE id = %s;" % data
        self.query.exec_(query)
        self.close()
    
    def delete(self):
        query = 'DELETE FROM contacts WHERE id = %i' % self.id
        self.query.exec_(query)
        self.close()


class Contacts(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi("contacts.ui", self)
        self.connect()
        self.btn_create.clicked.connect(self.create)
        self.table.doubleClicked.connect(self.update)
        self.select()
        self.show()

    def create(self):
        '''Open form for register a contact, send id for database queries'''
        form = Form(parent=self)
        form.exec()
        self.select()

    def update(self, click):
        '''Open form for edit a contact, send id for database queries'''
        #get id from clicked row
        index = click.sibling(click.row(), 0)
        id = self.model.itemData(index)[0]
        
        form = Form(parent=self, id=id)
        form.exec()
        self.select()

    def select(self):
        '''Select all contacts and show in table'''
        self.model = QSqlQueryModel()
        self.model.setQuery("SELECT * FROM contacts", self.conn)
        self.table.setModel(self.model)
        self.table.show()

    def connect(self):
        '''Connect with database'''
        self.conn = QSqlDatabase.addDatabase("QPSQL")
        self.conn.setHostName("localhost")
        self.conn.setDatabaseName("contacts")
        self.conn.setUserName("postgres")
        self.conn.setPassword("postgres")
        self.conn.open()

app = QApplication(sys.argv)
calc = Contacts()
sys.exit(app.exec_())