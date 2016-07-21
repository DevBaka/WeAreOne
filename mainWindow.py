# -*- coding: utf-8 -*-

import os
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import platform
import xml.etree.ElementTree as ET
import urllib2
import time
import re

startapp = 0
platform = platform.system()
opend = 0
selectedMode = 0
ManAuto = 0
DJTechnobase = " |  "
DJHousetime  = "  |  "
DJHardbase   = "   |  "
DJTrancebase = "  |  "
DJCoretime   = "   |  "
DJClubtime   = "    |  "

class WeAreOne(object):
    def setupUi(self, Mainwindow):
        global opend
        Mainwindow.setObjectName("WeAreOne Player")
        Mainwindow.resize(700, 500)
        self.centralWidget = QtWidgets.QWidget(Mainwindow)
        self.centralWidget.setObjectName("centralWidget")

        # Combobox für die Streamliste
        self.cbStreams = QtWidgets.QComboBox(self.centralWidget)
        self.cbStreams.setObjectName("cbStreams")
        self.cbStreams.setGeometry(25,0,175,25)
        self.cbStreams.addItems(["No Selected Stream","TechnoBase", "HouseTime", "HardBase", "TranceBase", "CoreTime", "ClubTime", "TeaTime"])
        self.cbStreams.currentIndexChanged.connect(self.SelectedStream)

        # Button zum Abspielen
        self.cmdPlay = QtWidgets.QPushButton(self.centralWidget)
        self.cmdPlay.setGeometry(QtCore.QRect(25,30,75,25))
        self.cmdPlay.setObjectName("cmdPlay")
        self.cmdPlay.clicked.connect(self.Play)

        # Button zum Stoppen/Pausieren
        self.cmdStop = QtWidgets.QPushButton(self.centralWidget)
        self.cmdStop.setGeometry(125,30,75,25)
        self.cmdStop.setObjectName("cmdStop")
        self.cmdStop.clicked.connect(self.Stop)

        # Slide zum Volume regeln, Audacious hat so nen premium nicht
        if platform == "Windows":
            self.slVolume = QtWidgets.QSlider(self.centralWidget)
            self.slVolume.setProperty("value", 75)
            self.slVolume.setOrientation(QtCore.Qt.Horizontal)
            self.slVolume.setGeometry(25,50,100,25)
            self.slVolume.valueChanged.connect(self.readXML)

        # Combobox um Application zum Abspielen auswählen zu können
        if platform == "Linux":
            self.cbStartApp = QtWidgets.QComboBox(self.centralWidget)
            self.cbStartApp.setObjectName("cbStartApp")
            self.cbStartApp.setGeometry(500,10,175,20)
            self.cbStartApp.addItems(["Audacious"])
            self.cbStartApp.currentIndexChanged.connect(self.setStartApp)

        # Infos zu allen Streams oder zum ausgewählten Stream detailiert ?
        self.cbShowInfos = QtWidgets.QComboBox(self.centralWidget)
        self.cbShowInfos.setObjectName("cbShowInfos")
        self.cbShowInfos.setGeometry(500, 40, 175, 20)
        self.cbShowInfos.addItems(["Alle Streams", "Ausgewählter Stream"])

        # Listbox der Streams und Stream Infos
        self.lstStreams = QtWidgets.QListWidget(self.centralWidget)
        self.lstStreams.setObjectName("lstStreams")
        self.lstStreams.setGeometry(25,75,650,140)

        # Einzelnen Track speichern
        self.cmdSaveTrack = QtWidgets.QPushButton(self.centralWidget)
        self.cmdSaveTrack.setGeometry(25, 225, 250, 25)
        self.cmdSaveTrack.setObjectName("cmdSaveTrack")
        self.cmdSaveTrack.clicked.connect(self.saveTrack)

        # Automatisch Speichern Aktivieren/Deaktivieren
        self.cmdAutoSave = QtWidgets.QPushButton(self.centralWidget)
        self.cmdAutoSave.setObjectName("cmdAutoSave")
        self.cmdAutoSave.setGeometry(275, 225, 400, 25)
        self.cmdAutoSave.clicked.connect(self.activateAutoSave)

        # Listbox für die Anzeige der Mitgeschriebenen Tracks
        self.lstTracks = QtWidgets.QListWidget(self.centralWidget)
        self.lstTracks.setObjectName("lstTracks")
        self.lstTracks.setGeometry(25, 260, 650, 195)




        Mainwindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(Mainwindow)
        self.menuBar.setGeometry(QtCore.QRect(0,0,700,30))
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1199, 26))
        self.menuBar.setObjectName("menuBar")
        Mainwindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(Mainwindow)
        self.mainToolBar.setObjectName("mainToolBar")
        Mainwindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(Mainwindow)
        self.statusBar.setObjectName("statusBar")
        Mainwindow.setStatusBar(self.statusBar)



        self.retranslateUi(Mainwindow)
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)
        self.readXML()
       # if opend == 0:
        #    self.readXML()
         #   opend = opend + 1
        # self.XMLReadTimer(0)

    def readXML(self):
        self.lstStreams.clear()
        url = urllib2.urlopen("http://tray.technobase.fm/radio.xml")
        tree = ET.parse(url)
        root = tree.getroot()
        trackinlist = 0
        i = self.cbShowInfos.currentIndex()
        print i
        if i == 0:
            for radio in root.findall('radio'):
                sender = radio.find('name').text
                if sender == "TeaTime":
                    break
                if len(sender) < 10:
                    z = len(sender)
                    y = 10 - z
                    for i in range(1,y + 4):
                        sender = sender + " "
                else:
                    for i in range(0,3):
                        sender = sender + " "
                mod = str(radio.find('moderator').text)
                track = radio.find('artist').text + " - " + radio.find('song').text
                tvar = "  Track:  "
                if mod == "None":
                    mod = "\t Kein DJ onair"
                    track = ""
                    tvar = ""
                if sender == "TechnoBase   ":
                    print "hello world"
                    item = sender + DJTechnobase + str(mod) + tvar + track
                    self.lstStreams.addItem(item)
                if sender == "HouseTime    ":
                    item = sender + DJHousetime + str(mod) + tvar + track
                    self.lstStreams.addItem(item)
                if sender == "HardBase     ":
                    item = sender + DJHardbase + str(mod) + tvar + track
                    self.lstStreams.addItem(item)
                if sender == "TranceBase   ":
                    item = sender + DJTrancebase + str(mod) + tvar + track
                    self.lstStreams.addItem(item)
                if sender == "CoreTime     ":
                    item = sender + DJCoretime + str(mod) + tvar + track
                    self.lstStreams.addItem(item)
                if sender == "ClubTime     ":
                    item = sender + DJClubtime + str(mod) + tvar + track
                    self.lstStreams.addItem(item)

        if ManAuto == 1:
            akstream = self.cbStreams.currentText()
            filen = akstream + ".txt"
            for radio in root.findall('radio'):
                if radio.find('name').text == akstream:
                    print akstream
                    aktrack = str(radio.find('artist').text) + " - " + str(radio.find('song').text)
                    try:
                        with open(filen,"r") as f:
                            for line in f:
                                if line == aktrack + "\n":
                                    trackinlist = 1
                    except:
                        with open(filen, "w+") as f:
                            f.close()
                    print "aktuell" + aktrack
                    if trackinlist == 0:
                        with open(filen, "a") as f:
                            f.write(aktrack + "\n")
                            self.lstTracks.addItem(aktrack)

        if i == 1:
            astream = self.cbStreams.currentText()
            for radio in root.findall('radio'):
                if radio.find('name').text == astream:
                    print "find it!" + astream
                    mod = str(radio.find('moderator').text)
                    showname = str(radio.find('show').text)
                    starttime = str(radio.find('starttime').text)
                    endtime = str(radio.find('endtime').text)
                    artist = str(radio.find('artist').text)
                    trackname = str(radio.find('song').text)
                    listender = str(radio.find('listener').text)
                    self.lstStreams.addItem("DJ: " + mod)
                    self.lstStreams.addItem("Show: " + showname)
                    self.lstStreams.addItem("Von " + starttime + " bis " +endtime + "Uhr")
                    self.lstStreams.addItem("Track: " + artist + " - " + trackname)
                    self.lstStreams.addItem("Listender: " + listender)

        print "baka"
        self.XMLReadTimer()

    def saveTrack(self):
        url = urllib2.urlopen("http://tray.technobase.fm/radio.xml")
        tree = ET.parse(url)
        root = tree.getroot()
        astream = self.cbStreams.currentText()
        filen = astream + ".txt"
        trackinlist = 0
        for radio in root.findall('radio'):
            if radio.find('name').text == astream:
                track = str(radio.find('artist').text) + " - " + str(radio.find('song').text)
                try:
                    with open(filen, "r") as f:
                        for line in f:
                            if line == track + "\n":
                                trackinlist = 1
                except:
                    with open(filen, "w+") as f:
                        f.close()
                print "aktuell" + track
                if trackinlist == 0:
                    with open(filen, "a") as f:
                        f.write(track + "\n")
                        self.lstTracks.addItem(track)
                        print "succesfully saved"

    def activateAutoSave(self):
        global ManAuto
        if ManAuto == 0:
            ManAuto = 1
            self.cmdAutoSave.setText("Tracks Automatisch Speichern Deativieren")
        else:
            ManAuto = 0
            print "autosave deaktiviert"
            self.cmdAutoSave.setText("Tracks Automatisch Speichern Aktivieren")

    def XMLReadTimer(self):
        timer = threading.Timer(10, self.readXML)
        timer.start()


    def Volume(self, i):
        os.system()

    def Play(self):
        import platform
        if platform.system() == "Linux":
            os.system("audacious -p")
        if platform.system() == "Windows":
            os.system("C:/Program Files (x86)/Windows Media Player/wmplayer.exe /play")
    def Stop(self):

        import platform
        if platform.system() == "Linux":
            os.system("audacious -u")
        if platform.system() == "Windows":
            os.system("C:/Program Files (x86)/Windows Media Player/wmplayer.exe /play")

    def setStartApp(self, i):
        global startapp
        startapp = i

    def SelectedStream(self, i):
        import platform
        print("Selected Stream: " + str(i))
        aplatform = platform.system()
        print aplatform
        if i == 1:
            if str(platform.system()) == "Linux":
                os.system("audacious -H http://listen.technobase.fm/dsl.pls")
            if platform.system() == "Windows":
                os.system("C:/Program Files (x86)/Windows Media Player/wmplayer.exe /play 'http://listen.housetime.fm/dsl.pls'")
        if i == 2:
            if platform.system() == "Linux":
                os.system("audacious -H http://listen.housetime.fm/dsl.pls")
        if i == 3:
            if platform.system() == "Linux":
              os.system("audacious -H http://listen.hardbase.fm/dsl.pls")
        if i == 4:
            if platform.system() == "Linux":
             os.system("audacious -H http://listen.trancebase.fm/dsl.pls")
        if i == 5:
            if platform.system() == "Linux":
                os.system("audacious -H http://listen.coretime.fm/dsl.pls")
        if i == 6:
            if platform.system() == "Linux":
                os.system("audacious -H http://listen.clubtime.fm/dsl.pls")
        if i == 7:
            if platform.system() == "Linux":
                os.system("audacious -H http://listen.teatime.fm/dsl.pls")

    def PlayStream(self, streamuri):
        if startapp == 0:
            os.system("audacious -H " + streamuri)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Mainwindow", "WeAreOne Player"))
        self.cmdPlay.setText(_translate("Mainwindow", "Play"))
        self.cmdStop.setText(_translate("Mainwindow", "Stop"))
        self.cmdSaveTrack.setText(_translate("Mainwindow", "Aktuellen Track Speichern"))
        self.cmdAutoSave.setText(_translate("Mainwindow", "Tracks Automatisch Speichern Aktivieren"))




