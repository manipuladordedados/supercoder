#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
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

import os
import sys
import urllib.request
from bs4 import BeautifulSoup


class SuperCoderCLI(object):
    """Main application class"""

    def __init__(self):

        self.languages = []
        self.names = []
        self.links = []
        self.issues = []
        self.descriptions = []

        self.WHITE = "\033[37m"
        self.NORMAL = "\033[0m"

        self.count = 0

        self.returnLangNames()
        self.Controls()

    def returnLangNames(self):
        """Returns a list of languages in order, just like on the site"""

        self.url = "http://www.codetriage.com"
        self.source = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.source, "html.parser")

        self.languages = [l.a.string for l in self.soup.find(class_="types-filter")]
        
    def returnData(self, lang):
        """Search and stores the data of the projects selected language"""
        
        self.url = "http://www.codetriage.com/?language="+self.languages[lang]
        self.source = urllib.request.urlopen(self.url)
        self.soup = BeautifulSoup(self.source, "html.parser")
        
        self.names = [n.string for n in
                            self.soup.find_all(class_="repo-item-title")]
        
        self.links = ["http://github.com"+n.a["href"] for n in
                            self.soup.find(class_="repo-list")]
                
        self.issues = [i.contents[2].replace("\n  ", "") for i in self.soup.find_all(class_="repo-item-issues")]

        self.descriptions = ["No description available." if str(i)=="<p></p>"
                                            else i.string for i in self.soup.find_all(class_="repo-item-description")]

    def showData(self):
        """Show data projects"""

        os.system(['clear', 'cls'][os.name == 'nt'])
        print("\n"+self.WHITE+self.names[self.count]+"\n"+self.NORMAL)
        print(self.descriptions[self.count]+"\n")
        print(self.issues[self.count]+"\n")
        print(self.links[self.count])

    def Controls(self):
        """Mostra o menu e controla as teclas"""

        os.system(['clear', 'cls'][os.name == 'nt'])
        print("{0}Select a Language:{1}".rjust(50).format(self.WHITE, self.NORMAL))
        print('  '.join([self.WHITE+str(x+1)+self.NORMAL+" - "+self.languages[x]
                                for x in range(len(self.languages))]))
        print("\n{0}Q{1}:Exit\n".format(self.WHITE, self.NORMAL))
        menu = input(">> ")
        if menu not in map(str, range(1,len(self.languages)+1)) and menu not in ["q", "Q"]:
            self.Controls()
        elif menu in ["q", "Q"]:
            sys.exit()
        else:
            self.returnData(int(menu)-1)
            self.showData()
            while True:
                option = input("\n\n\n\nQ:Exit      Enter:Next\n")
                if option not in ["", "q", "Q"]:
                    self.showData()
                    continue
                elif option == "":
                    if self.count == len(self.names)-1:
                        self.count = 0
                        self.showData()
                    else:
                        self.count += 1
                        self.showData()
                elif option == "q" or "Q":
                    sys.exit()

Program = SuperCoderCLI()