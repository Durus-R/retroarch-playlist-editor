#! /usr/bin/python3
import os
import sys

from PyQt5 import QtGui, QtWidgets, QtCore

import backend

retroarch_playlist_dir = "C:\\Retroarch_x86_64\\"
if sys.platform != "Windows":
    retroarch_playlist_dir = os.path.join(os.environ["HOME"], ".config/retroarch/playlists")

if not os.path.exists(retroarch_playlist_dir):
    retroarch_playlist_dir = os.environ["home"]

class Item(QtWidgets.QListWidgetItem):
    def __init__(self, text, parent=None, type_: int = ..., path=None):
        super().__init__(text, parent)
        self._path_ = path
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)

    def fullpath(self):
        return self._path_


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_path = None
        self.last_Edited = None
        self.setFixedWidth(220)
        self.setFixedHeight(270)

        self.data = {}  # {Name : Path}
        self.backup_data = {}  # {Index : Path}

        self.list = QtWidgets.QListWidget(self)
        self.list.resize(120, 230)
        self.list.move(10, 20)
        self.list.currentItemChanged.connect(self.item_changed)
        self.list.itemDoubleClicked.connect(self.edit_click)
        self.list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        # self.list.addItem("Test")
        # self.list.addItem("Test2")

        self.btnAdd = QtWidgets.QPushButton("Add", self)
        self.btnAdd.resize(70, 30)
        self.btnAdd.move(140, 20)
        self.btnAdd.clicked.connect(self.add_click)

        self.btnRemove = QtWidgets.QPushButton("Remove", self)
        self.btnRemove.resize(70, 30)
        self.btnRemove.move(140, 60)
        self.btnRemove.clicked.connect(self.remove_click)

        self.btnEdit = QtWidgets.QPushButton("Edit", self)
        self.btnEdit.resize(70, 30)
        self.btnEdit.move(140, 100)
        self.btnEdit.clicked.connect(self.edit_click)

        self.btnSave = QtWidgets.QPushButton("Save", self)
        self.btnSave.resize(70, 30)
        self.btnSave.move(140, 140)
        self.btnSave.clicked.connect(self.save_click)

        self.lblPath = QtWidgets.QLabel(self)
        self.lblPath.resize(220, 15)
        self.lblPath.move(11, 257)
        self.lblPath.setFont(QtGui.QFont("Arial", 9))
        self.lblPath.setText("")

        self.btnRemove.setEnabled(False)
        self.btnEdit.setEnabled(False)
        self.btnSave.setEnabled(False)

    def add_click(self):
        # self.data["test"] = "test2"
        # self.list.addItem("test")
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_names, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Files", retroarch_playlist_dir,
                                                               "All Files (*)", options=options)
        if type(file_names == list):
            for i in file_names:
                # self.data[backend.generate(i)] = i
                self.list.addItem(Item(backend.generate(i), path=i))
        elif not file_names:
            return
        else:
            assert type(file_names) == str
            # self.data[backend.generate(file_names)] = file_names
            self.list.addItem(Item(backend.generate(file_names), path=file_names))
        self.btnSave.setEnabled(True)

    def remove_click(self):
        if self.list.currentItem():
            # del self.data[self.list.currentItem().text()]
            self.list.takeItem(self.list.row(self.list.currentItem()))
            if not self.list.count():
                self.btnSave.setEnabled(False)

    def edit_click(self, _=None):
        print("Edit Click")
        # self.backup_data[self.list.currentIndex()] = self.data[self.list.currentItem().text()]
        index = self.list.currentIndex()
        if index.isValid():
            item = self.list.itemFromIndex(index)
            if not item.isSelected():
                item.setSelected(True)
            self.list.edit(index)
        # del self.data[self.list.currentItem().text()]

    def save_click(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Playlist", retroarch_playlist_dir,
                                                             "All Files (*);;Playlists (*.lpl)", options=options)
        pl = backend.Playlist()
        for i in range(self.list.count()):
            pl += [self.list.item(i).text(), self.list.item(i).fullpath()]
        pl.create_json(file_name)

    def item_changed(self, item0, item1):
        print("Changed")
        if item0:
            # try:
            #     self.lblPath.setText(self.data[item0.text()])
            #     self.lblPath.setToolTip(self.data[item0.text()])
            # except KeyError:
            #     self.data[item0.text()] = self.backup_data[self.list.currentIndex()]
            #     self.lblPath.setText(self.data[item0.text()])
            #     self.lblPath.setToolTip(self.data[item0.text()])
            self.lblPath.setToolTip(item0.fullpath())
            self.lblPath.setText(item0.fullpath())
            self.btnEdit.setEnabled(True)
            self.btnRemove.setEnabled(True)

        else:
            self.lblPath.setText("")
            self.lblPath.setToolTip("")
            self.btnRemove.setEnabled(False)
            self.btnEdit.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
