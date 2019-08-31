from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia  import *

import os
import sys

class MainWindow(QMainWindow):
  # resized = pyqtSignal()
  
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.appctxt = ApplicationContext()

    #############
    #  WIDGETS  #
    #############

    # status bar #
    self.status = QStatusBar()
    self.status.setStyleSheet("color:rgb(255,255,255);")    
    self.setStatusBar(self.status)

    # IMAGE VIEW #
    self.imageViewer = QLabel()
    self.initImages()

    #  SELECTION ARROWS  #
    self.bntPrev = QPushButton("<")
    self.btnNext = QPushButton(">")

    #############
    #  LAYOUTS  #
    #############

    #--------------------------------------------------#
    #                   MainVLayout      
    #              
    #  #--------------------------------------------#
    #  |                 TopHLayout                 |
    #  #--------------------------------------------#
    #
    #  #--------------------------------------------#
    #  |                MainHLayout                 |
    #  |                                            |
    #  | #-------------# #-------# #--------------# |
    #  | | LeftVLayout | | IMAGE | | RightVLayout | |
    #  | #-------------# #-------# #--------------# |
    #  |                                            |
    #  #--------------------------------------------#
    #
    #  #--------------------------------------------#
    #  |                BottomHLayout               |
    #  #--------------------------------------------#
    #
    #--------------------------------------------------#

    MainVLayout   = QVBoxLayout()
    MainHLayout   = QHBoxLayout()
    TopHLayout    = QHBoxLayout()
    BottomHLayout = QHBoxLayout()
    LeftVLayout   = QVBoxLayout()
    RightVLayout  = QVBoxLayout()

    BottomHLayout.addWidget(self.bntPrev)
    BottomHLayout.addWidget(self.btnNext)

    MainHLayout.addLayout(LeftVLayout)
    MainHLayout.addWidget(self.imageViewer)
    MainHLayout.addLayout(RightVLayout)

    MainVLayout.addLayout(TopHLayout)
    MainVLayout.addLayout(MainHLayout)
    MainVLayout.addLayout(BottomHLayout)

    MainWidgetContainer = QWidget()
    MainWidgetContainer.setLayout(MainVLayout)
    self.setCentralWidget(MainWidgetContainer)

    ####################
    #  SIGNAL / SLOTS  #
    ####################
    # self.resized.connect(self.SLOT_updateDisplaySize)
    self.bntPrev.clicked.connect(self.SLOT_viewPrev)
    self.btnNext.clicked.connect(self.SLOT_viewNext)

    self.updateTitle()
    self.displayImage()
    self.show()

  # initialize image gallery
  def initImages(self, path='/home/mojo/devel/git/roots/src/main/resources/base/images/'):

    self.gallery = []
    self.galleryIndex = 0

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
          image = QPixmap( self.appctxt.get_resource(os.path.join(r, file)) )
          self.gallery.append(image)
          print(os.path.join(r, file))

    try:
      self.imageViewer.setPixmap(self.gallery[0])
    except:
      self.SLOT_dialogCritical("no images loaded")

  # display image from gallery
  def displayImage(self):
    self.updateDisplaySize()
    self.imageViewer.setPixmap(self.gallery[self.galleryIndex])

  # SLOT: view previous gallery image
  def SLOT_viewPrev(self):
    if (self.galleryIndex > 0):
      self.galleryIndex -= 1
      self.displayImage()
    else:
      self.galleryIndex = len(self.gallery)-1
      self.displayImage()

  # SLOT: view next gallery image
  def SLOT_viewNext(self):
    if (self.galleryIndex < len(self.gallery)-1):
      self.galleryIndex += 1
      self.displayImage()
    else:
      self.galleryIndex = 0
      self.displayImage()

  # SLOT: update display size and scale image to fit
  def updateDisplaySize(self):

    screen = QDesktopWidget().screenGeometry()
    maxWidth = screen.width()
    maxheight = screen.height()

    width = self.gallery[self.galleryIndex].width()
    height = self.gallery[self.galleryIndex].height()

    if (width >= maxWidth or height >= maxheight):
      print("overmax")
      width  = maxWidth - 128
      height = maxheight - 128
      self.resize(width,height)

    pixmap = self.gallery[self.galleryIndex]
    image = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.FastTransformation)
    self.gallery[self.galleryIndex] = image

  # critical dialog pop-up
  def SLOT_dialogCritical(self, s):
    dlg = QMessageBox(self)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Critical)
    dlg.show()

  # update main window title
  def updateTitle(self, str=""):
    self.setWindowTitle(""+ str)

  # # overload to emit signal
  # def resizeEvent(self, event):
  #   self.resized.emit()
  #   return super(MainWindow, self).resizeEvent(event)

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Window = MainWindow()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
