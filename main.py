import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

qt_creator_file = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

class TodoModel(QtCore.QAbstractListModel):
    def __init__(self,*args,todos = None, **kwargs):
        super(TodoModel,self).__init__(*args,**kwargs)
        self.todos = todos or []
    #rowcount and data are standard methods we have to define for a list model
    #data is the core of our model, it handles requests for data from the view and returns the appropiate result
    def data(self, index, role):
        if role == Qt.DisplayRole:
            status, text = self.todos[index.row()]

            return text

    def rowCount(self,index):
        return len(self.todos)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.model = TodoModel(todos=[(False, 'my first todo')])
        self.todoView.setModel(self.model)  #todoView is the name of our list widget
        # connect the button
        self.addButton.pressed.connect(self.add)
        self.deleteButton.pressed.connect(self.delete)
        self.completeButton.pressed.connect(self.complete)

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.todos[index.row()]
            self.model.layoutChanged.emit()
            self.todoview.clearSelection()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.todos[row]
            self.model.todos[row] = (True,text)
            self.model.dataChanged.emit(index,index)
            self.todoView.clearSelection()    
                
    def add(self):
        """
        Add an item to our todo list, getting the text from the QLineEdit .todoEdit
        and then clearing it.
        """
        text = self.todoEdit.text()
        if text:
            self.model.todos.append((False,text))
            self.model.layoutChanged.emit() #triggering refresh
            self.todoEdit.setText("")

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()