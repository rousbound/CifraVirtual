#!/usr/bin/env python3.6
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from GUI import*
import os

class Main:
    def __init__(self):
        self.ui = Ui_CifraVirtual()
        self.mainWindow = QMainWindow()
        self.ui.setupUi(self.mainWindow)
        self.mainWindow.resize(791, 808)
        self.connect()
        self.state = ""

    def connect(self):
       self.ui.actionOpenSongs.triggered.connect\
        (lambda: self.OpenWindow("songs"))

       self.ui.actionOpenCompositions.triggered.connect\
        (lambda: self.OpenWindow("compositions"))

       self.ui.musicList.itemClicked.connect\
        (lambda: self.openItem(self.ui.musicList,self.ui.musicTextDisplay))

       self.ui.musicSaveButton.clicked.connect\
        (lambda: self.save(self.ui.musicList, self.ui.musicTextDisplay))

       self.ui.musicAddEntryButton.clicked.connect\
        (lambda: self.newListItem(self.ui.musicLineEntry,self.ui.musicList,self.ui.musicTextDisplay))
      
       self.ui.actionDelete_Song.triggered.connect\
        (lambda: self.deleteListItem(self.ui.musicList))

    def save(self,listWidget,display):
        text = display.toPlainText()
        def overwrite(path):
            file = open(path,"w")
            file.write(str(text))
            file.close()
        #path = self.state + listWidget.currentItem().text() + ".txt"
        filePath = self.getTxtFilePath(listWidget.currentItem().text())
        overwrite(filePath)

    def openFile(self,path,display):
        try:
            file = open(path)
            with file:
                text = file.read()
            display.setText(text)
        except:
            print("File not found")

    def openItem(self,list,display):
        filePath = ""
        itemTitle = list.currentItem().text()
        #filePath = self.state + itemTitle + ".txt"
        filePath = self.getTxtFilePath(itemTitle)
        self.openFile(filePath,display)

    def newListItem(self,lineEntry,listWidget,textDisplay):
        item = lineEntry.text()
        items = listWidget.findItems(item,QtCore.Qt.MatchExactly)
        if len(items) == 0:
            if item != "":
                textDisplay.clear()
                lineEntry.clear()
                listWidget.addItem(item)

    def getTxtFilePath(self,title):
      return self.state + title + ".txt"

    def deleteListItem(self,listWidget):
          if(listWidget.currentItem()):
            title = listWidget.currentItem().text()
            items = listWidget.findItems(title,QtCore.Qt.MatchExactly)
            listWidget.takeItem(listWidget.row(items[0]))
            path = self.getTxtFilePath(title)
            os.remove(path)
        
            self.ui.musicTextDisplay.clear()
            
          else:
            print("No item selected")

    def loadListFiles(self,path,list):
        for el in os.listdir(path):
            if el[-4:] == ".txt":
                list.addItem(el[:-4])
  
    def clearListWidget(self,list):
        listItems=[list.item(i) for i in range(list.count())]
        for item in listItems:
           list.takeItem(list.row(item))

    def OpenWindow(self,definer):
      self.clearListWidget(self.ui.musicList)
      if definer == "songs":
        self.state = "Music/"
        self.loadListFiles("Music/",self.ui.musicList)
      if definer == "compositions":
        self.state = "MyMusic/"
        self.loadListFiles("MyMusic/",self.ui.musicList)
  
  
if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  main = Main()
  main.mainWindow.show()
  sys.exit(app.exec_())
