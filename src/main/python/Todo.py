"""
A tasks list widget to track what has to be done.
Author: Borja Panadero
Year: 2021
Version: 0.1
==============================
TODO create random tasks ID
TODO history system
TODO Menus actions
TODO Projects
"""

from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QScrollArea, QHBoxLayout, QVBoxLayout,
                               QCheckBox, QMessageBox, QLineEdit, QAction)
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QFont
from Task import Task
import json

MENUS = [
    "&Task",
    "&Project",
    "&Help"
]


class Todo(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, parent=None)

        self.setWindowTitle("TODO")
        self.setFixedWidth(300)
        self.setMaximumHeight(550)
        self.setMinimumHeight(150)
        self.setFixedSize(QSize(300, 550))

        self._buttons_list = []
        self._tasks = []
        self.setContentsMargins(0, 0, 0, 0)

        self._create_widgets()
        self._central_page = QWidget(self)
        self._central_page.setObjectName("central-page")
        self._central_page.setLayout(self._create_layouts())

        self.setCentralWidget(self._central_page)
        self._create_connections()
        self._json_file = "tasks.json"

    def _create_widgets(self):
        """ creates required widgets for app"""
        # NEW TASK BUTTON
        self._new_task_button = QPushButton("New Task")
        self._new_task_button.setObjectName("new-task")
        for button in self._buttons_list:
            button.setObjectName(button.text())

        # MENUBAR
        self.menuBar().setObjectName("menu-bar")
        self.create_menus()

        # STATUS BAR
        self.statusBar().setObjectName("status-bar")
        self.statusBar().showMessage("Ready.", 5000)

    def _create_layouts(self):
        """
        Creates main window layouts
        returns: the main layout populated.
        """
        _buttons_layout = QHBoxLayout()
        _buttons_layout.setContentsMargins(2, 2, 2, 2)

        _scroll_area = QScrollArea(self)
        _scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        _scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        _scroll_area.setWidgetResizable(True)
        _scroll_area.verticalScrollBar().setContentsMargins(0, 0, 0, 0)
        _scroll_area.setContentsMargins(0, 0, 0, 0)

        _scroll_area.setAlignment(Qt.AlignRight)

        _scroll_widget = QWidget()
        _scroll_widget.setContentsMargins(0, 0, 0, 0)

        self._tasks_layout = QVBoxLayout()
        self._tasks_layout.setContentsMargins(2, 2, 5, 2)
        self._tasks_layout.setAlignment(Qt.AlignTop)
        _scroll_widget.setLayout(self._tasks_layout)
        _scroll_area.setWidget(_scroll_widget)

        _main_layout = QVBoxLayout()
        _main_layout.setObjectName("main_layout")

        _buttons_layout.addWidget(self._new_task_button)

        _main_layout.addWidget(_scroll_area)
        _main_layout.addLayout(_buttons_layout)

        return _main_layout

    def _create_connections(self):
        """ Creates the required connections between widgets"""
        self._new_task_button.clicked.connect(self._create_new_task)

        self.open_act.triggered.connect(self.open_file)
        self.new_act.triggered.connect(self._create_new_task)
        self.delete_act.triggered.connect(self._delete_task)
        self.save_act.triggered.connect(self.save_file)
        self.close_act.triggered.connect(self.close)
        self.about_act.triggered.connect(self.show_about_dialog)

    def _create_new_task(self):
        """ Adds a new Task to the main window scrollable area."""
        _new_task = Task()
        _new_task.label = f"Task {_new_task.id}"

        self._tasks_layout.addWidget(_new_task)
        self._tasks.append(_new_task)
        _new_task.setFocus()
        self.statusBar().showMessage("New task created", 1500)

        self._create_task_children_connections(_new_task)

    def _create_task_children_connections(self, new_task):
        # Task Delete button
        new_task_del_button = new_task.findChild(QPushButton, "delete-task")
        new_task_del_button.clicked.connect(self._delete_task)

        # Task Done Checkbox
        new_task_done_check = new_task.findChild(QCheckBox, "task-done")
        new_task_done_check.clicked.connect(self._task_is_done)

    def _delete_task(self):
        """
        Deletes task from widget after checking if its marked as done.
        Otherwise, prompts user to verify he wants the task deleted.
        """
        on_focus = QApplication.focusWidget()
        task_to_delete = self.sender().parent()
        print(f"deleting: {task_to_delete}")

        done = task_to_delete.findChild(QCheckBox, "task-done")
        if done.isChecked():
            task_to_delete.setParent(None)
            self._tasks = [task for task in self._tasks if not task.id == task_to_delete.id]
            self.statusBar().showMessage(f"{task_to_delete.label} deleted!", 1500)
        else:
            del_msg = QMessageBox(QMessageBox.Warning, "Delete Tasks",
                                  "This task isn't done yet. \nAre you sure you want to task_to_delete it?",
                                  QMessageBox.Yes | QMessageBox.No)
            answer = del_msg.exec_()
            if answer == del_msg.Yes:
                task_to_delete.setParent(None)
                self._tasks = [task for task in self._tasks if not task.unique_id == task_to_delete.unique_id]
                self.statusBar().showMessage(f"{task_to_delete.label} deleted!", 1500)

    def _task_is_done(self, checked):
        """
        Changes the Task color and LineEdit font based on the Checkbox state.
        """
        check_done = self.sender()
        current_task_done = check_done.parent()
        task_line_edit = current_task_done.findChild(QLineEdit, "task-label")
        print(f"selected: {current_task_done}")

        if checked:
            self.strikeout_task_label(task_line_edit, current_task_done)
        else:
            self.undo_strikeout_task_label(task_line_edit, current_task_done)

    def undo_strikeout_task_label(self, task_line_edit, current_task_done):
        # Change task color to original
        current_task_done.setStyleSheet("Task {background-color: #238754;}")
        print(f"changed-color: {current_task_done} to green")
        self.statusBar().showMessage(f"{current_task_done.label} is ready!", 1500)
        # Set normal label
        font = QFont("Century Gothic", 12, QFont.Normal)
        font.setStrikeOut(False)
        task_line_edit.setFont(font)
        task_line_edit.setReadOnly(False)

    def strikeout_task_label(self, task_line_edit, current_task_done):
        # Change task color to done
        current_task_done.setStyleSheet("Task {background-color: #cc253f;}")
        print(f"changed-color: {current_task_done} to red")
        self.statusBar().showMessage(f"{current_task_done.label} is done!", 1500)
        # Strike out label
        font = QFont("Century Gothic", 12, QFont.Bold)
        font.setStrikeOut(True)
        task_line_edit.setFont(font)
        task_line_edit.setReadOnly(True)

    def create_menus(self):
        for menu in MENUS:
            if menu == "&Task":
                self.task_menu = self.menuBar().addMenu(menu)
                self.new_act = QAction("&New")
                self.delete_act = QAction("&Delete")
                self.open_act = QAction("&Open")
                self.save_act = QAction("&Save")
                self.close_act = QAction("&Close")
                self.task_menu.addAction(self.new_act)
                self.task_menu.addAction(self.delete_act)
                self.task_menu.addSection("File")
                self.task_menu.addAction(self.open_act)
                self.task_menu.addAction(self.save_act)
                self.task_menu.addSection("Quit")
                self.task_menu.addAction(self.close_act)
            elif menu == "&Project":
                project_menu = self.menuBar().addMenu(menu)
            elif menu == "&Help":
                self.help_menu = self.menuBar().addMenu(menu)
                self.about_act = QAction("&About")
                self.help_menu.addAction(self.about_act)

    def show_about_dialog(self):
        text = "<center>" \
               "<h1>Todo</h1>" \
               "&#8291;" \
               "</center>" \
               "<p>Version 0.1.1<br/>" \
               "Copyright &copy; Borja Panadero. </p>"
        QMessageBox.about(self, "About Todo", text)

    def save_file(self):
        my_tasks = {"tasks": []}
        try:
            with open("tasks.json", "w+", encoding="utf8") as file_write:
                for task in self._tasks:
                    task_info = {"id": task.id, "label": task.label, "done": task.done}
                    my_tasks["tasks"].append(task_info)
                    print("writing task: ", task.label)
                json.dump(my_tasks, file_write, indent=4)
        except FileExistsError:
            print("file doesn't exists.")

    def open_file(self):
        with open("tasks.json", "r") as file_read:
            my_tasks = json.load(file_read)

            for task in my_tasks["tasks"]:
                label = task["label"]
                id = task["id"]
                done = task["done"]
                print(task)

                new_task = Task(label, id, done)

                if done:
                    new_task_label = new_task.findChild(QLineEdit, "task-label")
                    self.strikeout_task_label(new_task_label, new_task)

                self._create_task_children_connections(new_task)
                self._tasks_layout.addWidget(new_task)
                self._tasks.append(new_task)
