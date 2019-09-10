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

    MainWidgetContainer = QWidget()

    self.setMinimumSize(256,256)
    self.resize(1000,750)

    self.horizBarHeight = 25
    self.vertBarWidth = 25

    # get user's screen dimensions
    self.screen = QDesktopWidget().screenGeometry()
    self.maxWidth = self.screen.width()
    self.maxheight = self.screen.height()

    # get gallery groups
    imgPath = self.appctxt.get_resource('images/')
    self.getGalleryGroups(imgPath)

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

    # counter #
    self.imageCounter = QLineEdit()
    self.imageCounter.setFixedSize(75,40)
    self.imageCounter.setAlignment(Qt.AlignCenter)

    # SELECTION ARROWS #
    self.bntPrev = QPushButton("<")
    self.btnNext = QPushButton(">")

    # GROUP BUTTONS #
    self.groupBtns = []
    for group in self.groups:
      self.groupBtns.append(QPushButton(group))

    # PREVIEW PANE #
    self.previewBtns = []
    self.numPreview = 7
    for i in range(0,self.numPreview):
      self.previewBtns.append(QPushButton())
      self.previewBtns[i].setMinimumSize(150,150)
      self.previewBtns[i].clicked.connect(self.SLOT_previewClicked)

    #############
    #  LAYOUTS  #
    #############
    # TODO: update this 
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
    self.previewLayout = QHBoxLayout()
    self.LeftVLayout   = QVBoxLayout()
    RightVLayout  = QVBoxLayout()

    # Top Horizontal Layout #
    for btn in self.groupBtns:
      TopHLayout.addWidget(btn)

    # Horizontal Preview Layout #
    for btn in self.previewBtns:
      self.previewLayout.addWidget(btn)

    # Left Vertical Layout #
    # self.LeftVLayout.addWidget(self.previewPane)

    # Right Vertical Layout #
    # RightVLayout.addWidget(spacerRight)

    # Bottom Horizontal Layout #
    BottomHLayout.addWidget(self.bntPrev)
    BottomHLayout.addWidget(self.imageCounter)
    BottomHLayout.addWidget(self.btnNext)

    # image viewer layouts
    viewerHLayout = QHBoxLayout()
    viewerHLayout.addWidget(self.imageViewer)
    viewerHLayout.addLayout(RightVLayout)

    viewerVLayout = QVBoxLayout()
    viewerVLayout.addLayout(viewerHLayout)
    viewerVLayout.addLayout(BottomHLayout)

    # Main Horizontal Layout #
    MainHLayout.addLayout(self.LeftVLayout)
    MainHLayout.addLayout(viewerVLayout)
    MainVLayout.addLayout(TopHLayout)
    MainVLayout.addLayout(MainHLayout)
    MainVLayout.addLayout(self.previewLayout)

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
    self.gallery = []       # gallery to be displayed
    self.galleryScaled = [] # display gallery images scaled 
    self.galleryIndex = 1   # display gallery image index

    # initialize 2D list of galleries, sorted by group
    self.galleryGroups = []
    self.galleryGroupsScaled = []
    for group in self.groups:
      self.galleryGroups.append([])
      self.galleryGroupsScaled.append([])

    i = 0 # initialize [0] element of each gallery as its group's name
    for gallery in self.galleryGroups:
      gallery.append(self.groups[i])
      self.galleryGroupsScaled[i].append(self.groups[i])
      i +=1

    self.initImages(imgPath)
    self.displayImage()
    self.updateTitle()
    self.show()

  # get image groups from directories in 'main/resources/base/images/'
  def getGalleryGroups(self, path):

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

    i = 0
    for gallery in self.galleryGroups:
      if (groupName == gallery[0]):
        self.galleryGroupsScaled[i].append(image)
        gallery.append(image) 
      i +=1

  # display image from gallery
  def displayImage(self):
    self.scaleImage()
    self.imageViewer.setPixmap(self.galleryScaled[self.galleryIndex])
    self.updateImageCounter()
    self.updatePreview()
    self.setFocus()

  # scale image to fit current window size
  def scaleImage(self):

    # get currennt size of image display
    viewWidth = self.imageViewer.width()
    viewHeight = self.imageViewer.height()

    # get original size of image
    imgWidth = self.gallery[self.galleryIndex].width()
    imgHeight = self.gallery[self.galleryIndex].height()

    # get scaling dimensions
    if (imgWidth != viewWidth):
      imgWidth = viewWidth 
    if (imgHeight != viewHeight):
      imgHeight = viewHeight
      
    self.imageViewer.resize(viewWidth,viewHeight)

    pixmap = self.gallery[self.galleryIndex]
    image = pixmap.scaled(imgWidth, imgHeight, Qt.KeepAspectRatio, Qt.FastTransformation)
    self.galleryScaled[self.galleryIndex] = image

  # update image counter display
  def updateImageCounter(self):
    idx = str( self.galleryIndex )
    max = str( len(self.gallery)-1 )
    self.imageCounter.setText(idx + ' / ' + max)

  # update preview pane display images
  def updatePreview(self):

    previewGallery = self.getPreviewGallery()
    previewSize = len(previewGallery)

    idxMin = self.galleryIndex-int(self.numPreview/2)
    idxMax = self.galleryIndex+int(self.numPreview/2)+1

    i = 0
    # self.clearLayout(self.previewLayout)
    for idx in range(idxMin,idxMax):
      if (idx <= 0):        
        idx = previewSize+idx-1
      elif (idx >= previewSize):
        idx = idx-previewSize+1

      image = previewGallery[idx]
      self.previewBtns[i].setText(str(idx))
      self.previewBtns[i].setIcon(QIcon(image))
      self.previewBtns[i].setIconSize(image.rect().size())
      self.previewBtns[i].resize(image.rect().size())
      i +=1

  # create image preview gallery
  def getPreviewGallery(self):

    previewGallery = []
    previewGallery.append("preview")
    for i in range(1,len(self.gallery)):
      image = self.gallery[i]
      image = image.scaled(self.previewBtns[0].size().width(), self.previewBtns[0].size().height(), Qt.KeepAspectRatio, Qt.FastTransformation)
      previewGallery.append(image)

    return previewGallery

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
    self.updatePreview()

  # SLOT: display image selected from preview
  def SLOT_previewClicked(self):

    self.galleryIndex = int(self.sender().text())
    if self.galleryIndex == 0:
      self.galleryIndex = len(self.gallery)-1
    self.displayImage()

  # critical dialog pop-up
  def dialogCritical(self, s):
    dlg = QMessageBox(self)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Critical)
    dlg.show()

  # def SLOT_resized(self):
  #   self.resize(self.width(),self.height())

  # delete all widgets in a layout
  def clearLayout(self, layout):
    while layout.count():
      child = layout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

  # update main window title
  def updateTitle(self, str=""):
    self.setWindowTitle(""+ str)

  # capture arrow key press to navigate gallery
  def keyPressEvent(self, event):

    keyCode = event.key()

    if (16777234 == keyCode):
      self.SLOT_viewPrev()

    elif (16777236 == keyCode):
      self.SLOT_viewNext()

  # # overload to emit signal
  # def resizeEvent(self, event):
  #   self.resized.emit()
  #   return super(MainWindow, self).resizeEvent(event)

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Window = MainWindow()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
