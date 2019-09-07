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

    self.setMinimumSize(256,256)

    self.horizBarHeight = 25
    self.vertBarWidth = 25

    # get user's screen dimensions
    self.screen = QDesktopWidget().screenGeometry()
    self.maxWidth = self.screen.width()
    self.maxheight = self.screen.height()

    # get gallery groups
    imgPath = self.appctxt.get_resource('images/')
    self.getImageGroups(imgPath)

    #############
    #  WIDGETS  #
    #############

    # status bar #
    self.status = QStatusBar()
    self.status.setStyleSheet("color:rgb(255,255,255);")    
    self.setStatusBar(self.status)

    # IMAGE VIEW #
    self.imageViewer = QLabel()
    self.imageViewer.setAlignment(Qt.AlignCenter)
    self.imageViewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # SELECTION ARROWS #
    self.bntPrev = QPushButton("<")
    self.btnNext = QPushButton(">")

    # GROUP BUTTONS #
    self.groupBtns = []
    for group in self.groups:
      self.groupBtns.append(QPushButton(group))

    self.btnGroup0 = QPushButton("All")
    self.btnGroup1 = QPushButton("Family")
    self.btnGroup2 = QPushButton("Kids")
    self.btnGroup3 = QPushButton("Mom-n-Dad")
    self.btnGroup4 = QPushButton("other")
    self.btnGroup5 = QPushButton("wallpapers")

    # spacers #
    spacerTop = QLabel("T O P")
    spacerLeft = QLabel("L E F T")
    spacerRight = QLabel("R I G H T")
    spacerTop.setFixedSize(self.width(),self.horizBarHeight)
    spacerLeft.setFixedSize(self.vertBarWidth,self.height())
    spacerRight.setFixedSize(self.vertBarWidth,self.height())
    spacerTop.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    spacerLeft.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
    spacerRight.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

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

    # Top Horizontal Layout #
    for btn in self.groupBtns:
      TopHLayout.addWidget(btn)

    # Left Vertical Layout #
    LeftVLayout.addWidget(spacerLeft)

    # Right Vertical Layout #
    RightVLayout.addWidget(spacerRight)

    # Bottom Horizontal Layout #
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
    # self.resized.connect(self.SLOT_resized)
    self.bntPrev.clicked.connect(self.SLOT_viewPrev)
    self.btnNext.clicked.connect(self.SLOT_viewNext)

    for btn in self.groupBtns:
      btn.clicked.connect(self.SLOT_viewGroup)

    ####################
    #     GALLERIES    #
    ####################

    # display gallery #
    self.gallery = []
    self.galleryScaled = []
    self.galleryIndex = 1

    # initialize 2D list of galleries for each group
    self.galleryGroups = []
    self.galleryGroupsScaled = []
    for group in self.groups:
      self.galleryGroups.append([])
      self.galleryGroupsScaled.append([])

    i = 0
    for gallery in self.galleryGroups:
      gallery.append(self.groups[i])
      self.galleryGroupsScaled.append(self.groups[i])
      i +=1

    self.updateTitle()
    self.initImages(imgPath)
    self.displayImage()
    self.show()

  # get image groups from directories in 'main/resources/base/images/'
  def getImageGroups(self, path):

    self.groups = []

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
      for dir in d:
        self.groups.append(dir)

  # import resouce images into gallery
  def initImages(self, path):

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
          image = QPixmap( self.appctxt.get_resource(os.path.join(r, file)) )
          self.sortImage(r,image)

    self.gallery = self.galleryGroups[0]
    self.galleryScaled = self.galleryGroupsScaled[0]

  # sort image into a gallery group (based on containin directory name)
  def sortImage(self,dir,image):

    groupName = dir[dir.rfind('/')+1:] # strip path down to last directory name

    for gallery in self.galleryGroups:
      if (groupName == gallery[0]):
        gallery.append(image)

    self.galleryGroupsScaled = self.galleryGroups

  # display image from gallery
  def displayImage(self):
    self.scaleImage()
    self.imageViewer.setPixmap(self.galleryScaled[self.galleryIndex])

  # scale image to fit current window size
  def scaleImage(self):

    viewWidth = self.imageViewer.width()
    viewHeight = self.imageViewer.height()

    imgWidth = self.gallery[self.galleryIndex].width()
    imgHeight = self.gallery[self.galleryIndex].height()

    if (imgWidth > viewWidth):
      imgWidth = viewWidth 
    if (imgHeight > viewHeight):
      imgHeight = viewHeight
      
    self.imageViewer.resize(viewWidth,viewHeight)

    pixmap = self.gallery[self.galleryIndex]
    image = pixmap.scaled(imgWidth, imgHeight, Qt.KeepAspectRatio, Qt.FastTransformation)
    self.galleryScaled[self.galleryIndex] = image

  # SLOT: view previous gallery image
  def SLOT_viewPrev(self):
    if (self.galleryIndex > 1):
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
      self.galleryIndex = 1
      self.displayImage()

  # SLOT: view gallery group All
  def SLOT_viewGroup(self):
    
    groupName = self.sender().text()
    self.galleryIndex = 1
    
    i = 0
    for gallery in self.galleryGroups:
      if (gallery[0] == groupName):
        self.gallery = gallery
        self.galleryScaled = self.galleryGroupsScaled[i]
      i +=1

    self.displayImage()

  # critical dialog pop-up
  def SLOT_dialogCritical(self, s):
    dlg = QMessageBox(self)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Critical)
    dlg.show()

  # def SLOT_resized(self):
  #   self.resize(self.width(),self.height())

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
