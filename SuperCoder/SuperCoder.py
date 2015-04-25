#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Valter Nazianzeno <manipuladordedados at gmail dot com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import pickle
import webbrowser
import urllib.request
from bs4 import BeautifulSoup
try:
    from PyQt4 import QtGui, QtCore
except ImportError:
    from PySide import QtGui, QtCore

CONFIG_FILE_PATH = os.path.expanduser("~")+"/.config/SuperCoder"

class MainWindow(QtGui.QDialog):
    """
    Initializing of several functions like the main or settings
    windows, when opening the APP for the first time
    """
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self)

        self.first_run = None
        if os.path.exists(CONFIG_FILE_PATH):
            self.first_run = False
            self.selected_languages = pickle.load(open(CONFIG_FILE_PATH, 'rb'))
            Parser.__init__(self, self.selected_languages)
            self.settings = Settings(self)
            self.initUI()
        else:
            self.first_run = True
            Parser.__init__(self)
            self.settings = Settings(self)
            self.ShowSettings()

    def initUI(self):
        """Here the look and feel of the main window are defined"""
        self.line = QtGui.QFrame(self)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setFixedSize(460,370)

        icon = QtGui.QIcon(self.resource_path("logo.png"))
        self.tray = QtGui.QSystemTrayIcon(icon, self)
        self.tray.setToolTip('SuperCoder')
        self.tray.activated.connect(self.onTrayClick)

        self.tray_menu = QtGui.QMenu()
        self.show_action = QtGui.QAction('Show', None)
        self.tray_menu.addAction(self.show_action)
        self.show_action.triggered.connect(self.showHide)

        self.settings_action = QtGui.QAction('Settings', None)
        self.tray_menu.addAction(self.settings_action)
        self.settings_action.triggered.connect(self.ShowSettings)

        self.about_action = QtGui.QAction('About', None)
        self.tray_menu.addAction(self.about_action)
        self.about_action.triggered.connect(self.showAbout)

        self.tray_menu.addSeparator()

        self.exit_action = QtGui.QAction('Exit', None)
        self.tray_menu.addAction(self.exit_action)
        self.exit_action.triggered.connect(self.trayQuit)

        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

        self.name = QtGui.QLabel(self)
        self.name.setGeometry(QtCore.QRect(20, 10, 441, 31))
        self.name.setText(self.names[self.count[0]][0])
        self.name.setFont(QtGui.QFont('SansSerif', 16, QtGui.QFont.Bold))

        self.description = QtGui.QTextBrowser(self)
        self.description.setGeometry(QtCore.QRect(10, 50, 441, 91))
        self.description.setText(self.descriptions[self.count[0]][0])

        self.issues_icon = QtGui.QLabel(self)
        self.issues_icon.setGeometry(QtCore.QRect(430, 190, 31, 31))
        self.issues_icon.setPixmap(QtGui.QPixmap(self.resource_path("issues.png")))

        self.issues_number = QtGui.QLabel(self)
        self.issues_number.setGeometry(QtCore.QRect(303, 195, 121, 20))
        self.issues_number.setText(self.issues[self.count[0]][0]+" Issues")
        self.issues_number.setAlignment(QtCore.Qt.AlignRight)

        self.next_button = QtGui.QPushButton(self)
        self.next_button.setGeometry(QtCore.QRect(370, 150, 81, 21))
        self.next_button.setText("Next")
        self.next_button.setIcon(QtGui.QIcon(self.resource_path("next.png")))
        self.next_button.clicked.connect(self.nextClicked)

        self.collaborate_button = QtGui.QPushButton(self)
        self.collaborate_button.setGeometry(QtCore.QRect(240, 150, 121, 21))
        self.collaborate_button.setText("Collaborate")
        self.collaborate_button.setIcon(QtGui.QIcon(self.resource_path("col.png")))
        self.collaborate_button.clicked.connect(self.collbaClicked)

        self.language_logo = QtGui.QLabel(self)
        self.language_logo.setGeometry(QtCore.QRect(10, 190, 31, 31))
        if os.path.exists((self.resource_path(self.selected_languages[self.count[0]])+".png")):
            self.language_logo.setPixmap(QtGui.QPixmap(str(self.resource_path(self.selected_languages[self.count[0]])+".png")))
        else:
            self.language_logo.setPixmap(QtGui.QPixmap(self.resource_path("others.png")))

        self.language_name = QtGui.QLabel(self)
        self.language_name.setGeometry(QtCore.QRect(39, 195, 161, 16))
        self.language_name.setText(self.selected_languages[self.count[0]])

        self.setFixedSize(QtCore.QSize(462, 216))
        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center())
        self.setWindowTitle('SuperCoder')
        self.setWindowIcon(QtGui.QIcon(self.resource_path("logo.png")))
        self.show()

    def resource_path(self, resource_name):
        this_module = sys.modules[__name__]
        module_dir = os.path.dirname(this_module.__file__)
        return os.path.join(module_dir, "img", resource_name)

    def ShowSettings(self):
        """Show the settings dialog"""
        self.settings.show()

    def showInfo(self):
        """Displays info on the current project"""
        try:
            self.name.setText(self.names[self.count[0]][self.count[1]])
            self.description.setText(self.descriptions[self.count[0]][self.count[1]])
            self.language_name.setText(self.selected_languages[self.count[0]])
            self.issues_number.setText(self.issues[self.count[0]][self.count[1]]+" Issues")
            
            if os.path.exists((self.resource_path(self.selected_languages[self.count[0]])+".png")):
                self.language_logo.setPixmap(QtGui.QPixmap(str(self.resource_path(self.selected_languages[self.count[0]])+".png")))
            else:
                self.language_logo.setPixmap(QtGui.QPixmap(self.resource_path("others.png")))

        except IndexError:
            self.nextClicked()

    def nextClicked(self):
        """Advances to next project and refreshes the window"""
        if self.count[0] > len(self.selected_languages)-2:
            self.count[0] = 0
            self.count[1] += 1
        else:
            self.count[0] += 1
        if self.count[1] > len(sorted(self.names, key=len, reverse=True)[0])-1:
            self.count = [0, 0]
        self.showInfo()

    def collbaClicked(self):
        """Opens the github page of the current project with the default browser"""
        webbrowser.open_new_tab(self.links[self.count[0]][self.count[1]])

    def trayQuit(self):
        """Exit of the app through the tray"""
        self.tray.hide()
        sys.exit(0)

    def onTrayClick(self, reason):
        """Show the menu options of the tray"""
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.showHide()

    def showHide(self):
        """Hide and show the main window"""
        state = not self.isVisible()
        self.setVisible(state)

    def closeEvent(self, event):
        """The main window is minimized to the tray when closed"""
        event.ignore()
        self.showHide()

    def showAbout(self):
        """Opens a dialog with info about the app"""
        about_message = ("<center><img src="+self.resource_path("logo.png")+"></center>",
                 ("<center><strong>SuperCoder</strong></center>"),
                 ("<center>1.0.1</center>"),
                 ("<center>Software to help with the development of Open Source/Free Software: Fix bugs, Add features.</center>"),
                 "<center><font size='2'>Copyright (C) 2014 Valter Nazianzeno</font></center>",
                 ("""<center><font size='2'>This program comes with ABSOLUTELY NO WARRANTY.
                  <br>See the GNU General Public License for more details.</br></font></center>"""))

        about_dialog = QtGui.QMessageBox(self)
        about_dialog.setWindowTitle("About SuperCoder")
        about_dialog.setText("""<p>%s</p>
                                <p>%s</p>
                                <p>%s</p>
                                <p>%s</p>
                                <p>%s</p>
                                <p>%s</p>
                                """ % about_message)
        about_dialog.exec_()

class Parser(object):
    """Returns lists with data from the selected languages"""
    def __init__(self, lang=None):
        url = "http://www.codetriage.com"
        source = urllib.request.urlopen(url)
        soup = BeautifulSoup(source)

        self.languages = []
        self.names = []
        self.links = []
        self.issues = []
        self.descriptions = []

        self.count = [0, 0]

        if os.path.exists(CONFIG_FILE_PATH):
            self.languages = [l for l in soup.find(id="repo-tabs").stripped_strings]

            for r in range(soup.find(class_="tab-content").contents.count("\n")):
                soup.find(class_="tab-content").contents.remove("\n")

            for l in lang:
                self.names += [[n.string for n in
                                    soup.find(class_="tab-content").contents[self.languages.index(l)].find_all("a")]]

                self.links += [["http://github.com"+n.get('href') for n in
                                    soup.find(class_="tab-content").contents[self.languages.index(l)].find_all("a")]]

                self.issues += [[i.string for i in
                                    soup.find(class_="tab-content").contents[self.languages.index(l)].find_all("span")]]

                self.descriptions += [["No description available." if str(i)=="<p></p>"
                                            else i.string for i in soup.find(class_="tab-content").contents[self.languages.index(l)].find_all("p")]]
        else:
            self.languages = [l for l in soup.find(id="repo-tabs").stripped_strings]


class Settings(QtGui.QDialog):
    """Settings window to choose the languages for the app to work with"""
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)

        self.selected_items = []

        self.setFixedSize(QtCore.QSize(340, 412))
        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center())
        self.setWindowTitle("Settings")
        self.setWindowIcon(QtGui.QIcon(self.parent().resource_path("settings.png")))

        self.select_languages = QtGui.QLabel(self)
        self.select_languages.setGeometry(QtCore.QRect(90, 10, 161, 20))
        self.select_languages.setText("Select the languages")
        self.select_languages.setFont(QtGui.QFont('SansSerif', 10, QtGui.QFont.Bold))

        self.confuse_icon = QtGui.QLabel(self)
        self.confuse_icon.setGeometry(QtCore.QRect(60, 10, 21, 21))

        self.cancel_button = QtGui.QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setGeometry(QtCore.QRect(50, 380, 91, 27))
        self.cancel_button.setIcon(QtGui.QIcon(self.parent().resource_path("cancel.png")))
        self.cancel_button.clicked.connect(self.cancelClicked)

        self.apply_button = QtGui.QPushButton(self)
        self.apply_button.setText("Apply")
        self.apply_button.setGeometry(QtCore.QRect(200, 380, 91, 27))
        self.apply_button.setIcon(QtGui.QIcon(self.parent().resource_path("apply.png")))
        self.apply_button.clicked.connect(self.applyClicked)

        self.listview = QtGui.QListView(self)
        self.listview.setGeometry(QtCore.QRect(20, 41, 301, 321))

        self.model = QtGui.QStandardItemModel(self.listview)

        for lista_item in self.parent().languages:
            item = QtGui.QStandardItem(lista_item )

            if self.parent().first_run is False:
                if item.text() in self.parent().selected_languages:
                    item.setCheckState(QtCore.Qt.Checked)
                    self.selected_items.append(item.text())
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)
            item.setCheckable(True)
            item.setEditable(False)
            self.model.appendRow(item)

        self.model.itemChanged.connect(self.itemClicked)
        self.listview.setModel(self.model)

    def itemClicked(self, item):
        """Adds the selected language to the list of projects that will be displayed"""
        if item.checkState() == QtCore.Qt.Checked:
            self.selected_items.append(item.text())
        if item.checkState() == QtCore.Qt.Unchecked:
            self.selected_items.remove(item.text())
        print(self.selected_items)

    def applyClicked(self):
        """Applies the selected options depending on the status of the app"""
        if len(self.selected_items) == 0:
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
            self.select_languages.setPalette(palette)
            self.confuse_icon.setPixmap(QtGui.QPixmap(self.parent().resource_path("what.png")))

        elif self.parent().first_run:
            self.parent().first_run = False
            pickle.dump(self.selected_items, open(CONFIG_FILE_PATH, "wb"))
            Parser.__init__(self.parent(), self.selected_items)
            self.parent().__init__()
            self.close()

        else:
            self.parent().selected_languages = self.selected_items
            pickle.dump(self.selected_items, open(CONFIG_FILE_PATH, "wb"))
            Parser.__init__(self.parent(), self.selected_items)
            self.parent().showInfo()
            self.close()

    def cancelClicked(self):
        """Cancel the selected options depending on the status of the app"""
        if self.parent().first_run:
            self.close()
            sys.exit(0)
        else:
            self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
