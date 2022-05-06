from PySide2.QtWidgets import QFrame, QHBoxLayout, QPushButton, QCheckBox, QLineEdit


class Task(QFrame):
    """
    The Task class inherits QFrame as a container to be populated with other widgets
    required for the UI display.
    _line_edit: acts as a label displaying by default "Task + Task.current_id"
    _check_box: toggles the Task state for done/undone.
    _del_button: deletes the task widget
    _id: class variable, incremented with each created instance.
    """
    _id = '000'

    def __init__(self, label="Task", is_done=False):
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
        Task._id = self.increase_id(Task._id)

        self._task_layout = QHBoxLayout()
        self._task_layout.addWidget(self._line_edit)
        self._task_layout.addWidget(self._check_box)
        self._task_layout.addWidget(self._del_button)

        self.setLayout(self._task_layout)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setFixedHeight(45)
        self.setContentsMargins(2, 2, 2, 2)

    def increase_id(self, current_id: str) -> str:
        """
        Returns the current_id increased by one with padding zeroes up to 3 digits as a string.
        :param current_id: the id to increase.
        :return: increased_id as a string after rising current_id by 1.
        """
        increased_id = str(int(current_id) + 1).zfill(3)
        return increased_id

    def __str__(self):
        return f"[{self.__class__.__name__}_label: {self.label} | ID: {self.id} | Done: {self.done}]"

    def __repr__(self):
        return f"[{self.__class__.__name__}@{hex(id(self))} | {self.label} | {self.id}]"

    def __eq__(self, other):
        """ Checks equality per object basis."""
        return id(self) is id(other)

    @property
    def label(self) -> str:
        return self._line_edit.text()

    @label.setter
    def label(self, value: str):
        self._line_edit.setText(value)

    @property
    def id(self) -> int:
        return self._task_id

    @property
    def done(self) -> bool:
        return self._check_box.isChecked()

    @done.setter
    def done(self, value: bool):
        self._check_box.setCheckState(value)






