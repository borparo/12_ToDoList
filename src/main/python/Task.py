from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QCheckBox, QLineEdit


class Task(QFrame):
    _id = 0
    def __init__(self, label="Task", id=0, is_done=False):
        QFrame.__init__(self)
        self.setObjectName(label)
        self._line_edit = QLineEdit(label, self)
        self._line_edit.setObjectName("task-label")

        self._check_box = QCheckBox(self)
        self._check_box.setObjectName("task-done")
        self._check_box.setChecked(is_done)

        self._del_button = QPushButton("Del", self)
        self._del_button.setObjectName('delete-task')
        self._del_button.setFixedSize(55, 25)

        self._task_id = Task._id
        Task._id += 1

        self._task_layout = QHBoxLayout()
        self._task_layout.addWidget(self._line_edit)
        self._task_layout.addWidget(self._check_box)
        self._task_layout.addWidget(self._del_button)

        self.setLayout(self._task_layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setFixedHeight(45)
        self.setContentsMargins(2, 2, 2, 2)

    def __str__(self):
        return f"[{self.__class__.__name__}_label: {self.label} | ID: {self.id} | Done: {self.done}]"

    def __repr__(self):
        return f"[{self.__class__.__name__}@{hex(id(self))} | {self.label} | {self.id}]"

    def __eq__(self, other):
        return id(self) is id(other)

    @property
    def label(self):
        return self._line_edit.text()

    @label.setter
    def label(self, value: str):
        self._line_edit.setText(value)

    @property
    def id(self):
        return self._task_id

    @property
    def done(self):
        return self._check_box.isChecked()

    @done.setter
    def done(self, value: bool):
        self._check_box.setCheckState(value)






