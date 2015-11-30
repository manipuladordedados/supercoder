#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2015 Valter Nazianzeno <manipuladordedados at gmail dot com>
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
from fcntl import lockf, LOCK_EX, LOCK_NB
from PyQt5.QtWidgets import (QApplication, QDialog, QSystemTrayIcon, QMenu, QAction, QMessageBox,
                             QLabel, QTextBrowser, QPushButton, QFrame, QListView)
from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtGui import QIcon, QFont, QPixmap, QStandardItemModel, QStandardItem, QPalette

CONFIG_FILE_PATH = os.path.expanduser("~")+"/.config/SuperCoder"

class MainWindow(QDialog):
    """
    Initializing of several functions like the main or settings
    windows, when opening the APP for the first time
    """
    def __init__(self, parent = None):
        super(MainWindow, self).__init__()

        SingleInstance()
        
        self.first_run = None
        if os.path.exists(CONFIG_FILE_PATH):
            self.first_run = False
            self.selected_languages = pickle.load(open(CONFIG_FILE_PATH, 'rb'))
            Parser.__init__(self)
            Parser.returnData(self, self.selected_languages)
            self.settings = Settings(self)
            self.initUI()
        else:
            self.first_run = True
            Parser.__init__(self)
            self.settings = Settings(self)
            self.ShowSettings()

    def initUI(self):
        """Here the look and feel of the main window are defined"""
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setFixedSize(460,370)

        icon = QIcon(self.resource_path("logo.png"))
        self.tray = QSystemTrayIcon(icon, self)
        self.tray.setToolTip('SuperCoder')
        self.tray.activated.connect(self.onTrayClick)

        self.tray_menu = QMenu()
        icon = QIcon(self.resource_path("show.png"))
        self.show_action = QAction(icon, 'Show', None)
        self.tray_menu.addAction(self.show_action)
        self.show_action.triggered.connect(self.showHide)
        
        icon = QIcon(self.resource_path("settings.png"))
        self.settings_action = QAction(icon, 'Settings', None)
        self.tray_menu.addAction(self.settings_action)
        self.settings_action.triggered.connect(self.ShowSettings)
        
        icon = QIcon(self.resource_path("about.png"))
        self.about_action = QAction(icon, 'About', None)
        self.tray_menu.addAction(self.about_action)
        self.about_action.triggered.connect(self.showAbout)

        self.tray_menu.addSeparator()
        
        icon = QIcon(self.resource_path("quit.png"))
        self.exit_action = QAction(icon, 'Exit', None)
        self.tray_menu.addAction(self.exit_action)
        self.exit_action.triggered.connect(self.trayQuit)

        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

        self.name = QLabel(self)
        self.name.setGeometry(QRect(20, 10, 441, 31))
        self.name.setText(self.names[self.count[0]][0])
        self.name.setFont(QFont('SansSerif', 16, QFont.Bold))

        self.description = QTextBrowser(self)
        self.description.setGeometry(QRect(10, 50, 441, 91))
        self.description.setText(self.descriptions[self.count[0]][0])

        self.issues_icon = QLabel(self)
        self.issues_icon.setGeometry(QRect(430, 190, 31, 31))
        self.issues_icon.setPixmap(QPixmap(self.resource_path("issues.png")))

        self.issues_number = QLabel(self)
        self.issues_number.setGeometry(QRect(303, 195, 121, 20))
        self.issues_number.setText(self.issues[self.count[0]][0])
        self.issues_number.setAlignment(Qt.AlignRight)

        self.next_button = QPushButton(self)
        self.next_button.setGeometry(QRect(370, 150, 81, 21))
        self.next_button.setText("Next")
        self.next_button.setIcon(QIcon(self.resource_path("next.png")))
        self.next_button.clicked.connect(self.nextClicked)

        self.collaborate_button = QPushButton(self)
        self.collaborate_button.setGeometry(QRect(240, 150, 121, 21))
        self.collaborate_button.setText("Collaborate")
        self.collaborate_button.setIcon(QIcon(self.resource_path("col.png")))
        self.collaborate_button.clicked.connect(self.collbaClicked)

        self.language_logo = QLabel(self)
        self.language_logo.setGeometry(QRect(10, 190, 31, 31))
        if os.path.exists((self.resource_path(self.selected_languages[self.count[0]])+".png")):
            self.language_logo.setPixmap(QPixmap(str(self.resource_path(self.selected_languages[self.count[0]])+".png")))
        else:
            self.language_logo.setPixmap(QPixmap(self.resource_path("others.png")))

        self.language_name = QLabel(self)
        self.language_name.setGeometry(QRect(39, 195, 161, 16))
        self.language_name.setText(self.selected_languages[self.count[0]])

        self.setFixedSize(QSize(462, 216))
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())
        self.setWindowTitle('SuperCoder')
        self.setWindowIcon(QIcon(self.resource_path("logo.png")))
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
            self.issues_number.setText(self.issues[self.count[0]][self.count[1]])
            
            if os.path.exists((self.resource_path(self.selected_languages[self.count[0]])+".png")):
                self.language_logo.setPixmap(QPixmap(str(self.resource_path(self.selected_languages[self.count[0]])+".png")))
            else:
                self.language_logo.setPixmap(QPixmap(self.resource_path("others.png")))

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
        if reason == QSystemTrayIcon.Trigger:
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
                 ("<center>2.0</center>"),
                 ("<center>Software to help with the development of Open Source/Free Software: Fix bugs, Add features.</center>"),
                 "<center><font size='2'>Copyright (C) 2015 Valter Nazianzeno</font></center>",
                 ("""<center><font size='2'>This program comes with ABSOLUTELY NO WARRANTY.
                  <br>See the GNU General Public License for more details.</br></font></center>"""))

        about_dialog = QMessageBox(self)
        about_dialog.setWindowIcon(QIcon(self.resource_path("about.png")))
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
    def __init__(self):
            self.languages = []
            self.names = []
            self.links = []
            self.issues = []
            self.descriptions = []
    
            self.count = [0, 0]
            
    def returnLangNames(self):
        """Returns a list of languages in order, just like on the site"""
        url = "http://www.codetriage.com"
        source = urllib.request.urlopen(url)
        soup = BeautifulSoup(source, "html.parser")
        
        self.languages = [l.a.string for l in soup.find(class_="types-filter")]
            
    def returnData(self, lang):
        """Search and stores the data of the projects selected language"""    
        for l in lang:
            url = "http://www.codetriage.com/?language="+l
            source = urllib.request.urlopen(url)
            soup = BeautifulSoup(source, "html.parser")
    
            self.names += [[n.string for n in soup.find_all(class_="repo-item-title")]]
    

            self.links += [["http://github.com"+n.a["href"] for n in soup.find(class_="repo-list")]]

            self.issues += [[i.contents[2].replace("\n  ", "") for i in soup.find_all(class_="repo-item-issues")]]

            self.descriptions += [["No description available." if str(i)=="<p></p>"
                                        else i.string for i in soup.find_all(class_="repo-item-description")]]        

class Settings(QDialog):
    """Settings window to choose the languages for the app to work with"""
    def __init__(self, parent = None):
        super(Settings, self).__init__(parent)
        
        Parser.returnLangNames(self.parent())

        self.selected_items = []

        self.setFixedSize(QSize(340, 412))
        self.move(QApplication.desktop().screen().rect().center()- self.rect().center())
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(self.parent().resource_path("settings.png")))

        self.select_languages = QLabel(self)
        self.select_languages.setGeometry(QRect(90, 10, 161, 20))
        self.select_languages.setText("Select the languages")
        self.select_languages.setFont(QFont('SansSerif', 10, QFont.Bold))

        self.confuse_icon = QLabel(self)
        self.confuse_icon.setGeometry(QRect(60, 10, 21, 21))

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.setGeometry(QRect(50, 380, 91, 27))
        self.cancel_button.setIcon(QIcon(self.parent().resource_path("cancel.png")))
        self.cancel_button.clicked.connect(self.cancelClicked)

        self.apply_button = QPushButton(self)
        self.apply_button.setText("Apply")
        self.apply_button.setGeometry(QRect(200, 380, 91, 27))
        self.apply_button.setIcon(QIcon(self.parent().resource_path("apply.png")))
        self.apply_button.clicked.connect(self.applyClicked)

        self.listview = QListView(self)
        self.listview.setGeometry(QRect(20, 41, 301, 321))

        self.model = QStandardItemModel(self.listview)

        for lista_item in self.parent().languages:
            item = QStandardItem(lista_item )

            if self.parent().first_run is False:
                if item.text() in self.parent().selected_languages:
                    item.setCheckState(Qt.Checked)
                    self.selected_items.append(item.text())
                else:
                    item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            item.setEditable(False)
            self.model.appendRow(item)

        self.model.itemChanged.connect(self.itemClicked)
        self.listview.setModel(self.model)

    def itemClicked(self, item):
        """Adds the selected language to the list of projects that will be displayed"""
        if item.checkState() == Qt.Checked:
            self.selected_items.append(item.text())
        if item.checkState() == Qt.Unchecked:
            self.selected_items.remove(item.text())

    def applyClicked(self):
        """Applies the selected options depending on the status of the app"""
        if len(self.selected_items) == 0:
            palette = QPalette()
            palette.setColor(QPalette.Foreground,Qt.red)
            self.select_languages.setPalette(palette)
            self.confuse_icon.setPixmap(QPixmap(self.parent().resource_path("what.png")))

        elif self.parent().first_run:
            self.parent().first_run = False
            pickle.dump(self.selected_items, open(CONFIG_FILE_PATH, "wb"))
            Parser.returnData(self.parent(), self.selected_items)
            self.parent().__init__()
            self.close()

        else:
            self.parent().selected_languages = self.selected_items
            pickle.dump(self.selected_items, open(CONFIG_FILE_PATH, "wb"))
            Parser.__init__(self.parent())
            Parser.returnData(self.parent(), self.selected_items)
            self.parent().showInfo()
            self.close()

    def cancelClicked(self):
        """Cancel the selected options depending on the status of the app"""
        if self.parent().first_run:
            self.close()
            sys.exit(0)
        else:
            self.close()
            
class SingleInstance(object):
    """This prevent several instances of SuperCoder running at the same time"""
    def __init__(self):
        fd = os.open('/tmp/SupCod.lock', os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        try:
           lockf(fd, LOCK_EX | LOCK_NB)
        except IOError:
            sys.exit(1)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())  

if __name__ == '__main__':
    main()