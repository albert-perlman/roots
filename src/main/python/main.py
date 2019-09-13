from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia  import *

import os
import sys

import stylesheet

class MainWindow(QMainWindow):
  resized = pyqtSignal()
  
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.appctxt = ApplicationContext()

    self.setStyleSheet(stylesheet.StyleSheet.css())

    MainWidgetContainer = QWidget()

    self.showing = False

    # Main Window sizing
    self.setMinimumSize(256,256)
    self.resize(1000,750)

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
    self.imageCounter.setReadOnly(True)
    self.imageCounter.setFixedSize(75,40)
    self.imageCounter.setAlignment(Qt.AlignCenter)

    # SELECTION ARROWS #
    self.viewPrevBtn = QPushButton("<")
    self.viewNextBtn = QPushButton(">")

    # GROUP BUTTONS #
    self.groupBtns = []
    for group in self.groups:
      self.groupBtns.append(QPushButton(group))

    # PREVIEW PANE # --> goto createPreviewBtns()
    self.previewBtns = []
    self.minPreviewSize = 50
    self.navBtnWidth = 25

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
    LeftVLayout   = QVBoxLayout()
    RightVLayout  = QVBoxLayout()

    self.PreviewLayout = QHBoxLayout()
    # self.PreviewLayout.setSpacing(1)

    # Top Horizontal Layout #
    for btn in self.groupBtns:
      TopHLayout.addWidget(btn)

    # Horizontal Preview Layout #

    # Left Vertical Layout #

    # Right Vertical Layout #

    # Bottom Horizontal Layout #
    BottomHLayout.addWidget(self.imageCounter)

    # image viewer layouts
    viewerHLayout = QHBoxLayout()
    viewerHLayout.addWidget(self.imageViewer)
    viewerHLayout.addLayout(RightVLayout)

    viewerVLayout = QVBoxLayout()
    viewerVLayout.addLayout(viewerHLayout)
    viewerVLayout.addLayout(BottomHLayout)

    # Main Horizontal Layout #
    MainHLayout.addLayout(LeftVLayout)
    MainHLayout.addLayout(viewerVLayout)
    MainVLayout.addLayout(TopHLayout)
    MainVLayout.addLayout(MainHLayout)
    MainVLayout.addLayout(self.PreviewLayout)

    MainWidgetContainer.setLayout(MainVLayout)
    self.setCentralWidget(MainWidgetContainer)

    ####################
    #  SIGNAL / SLOTS  #
    ####################
    self.resized.connect(self.SLOT_resized)

    for btn in self.groupBtns:
      btn.clicked.connect(self.SLOT_viewGroup)

    ####################
    #     GALLERIES    #
    ####################
    self.gallery = []       # gallery of images to be displayed
    self.galleryScaled = [] # display gallery images scaled 
    self.galleryIndex = 1   # display gallery index for image being viewed

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

    ####################
    #     START-UP     #
    ####################
    self.initImages(imgPath)  # import resource images into gallery groups
    self.updatePreviewPane()  # create Preview buttons
    self.updateTitle()
    self.show()
    self.showing = True

  # get image groups from directories in 'main/resources/base/images/'
  def getGalleryGroups(self, path):

    self.groups = []
    self.groups.append("All")

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

    # append all images to "All" gallery
    self.galleryGroups[0].append(image)
    self.galleryGroupsScaled[0].append(image)

    i = 0
    for gallery in self.galleryGroups:
      if (groupName == gallery[0]):
        gallery.append(image)
        self.galleryGroupsScaled[i].append(image)
      i +=1

  # display image from gallery
  def displayImage(self):
    self.scaleImage()
    self.imageViewer.setPixmap(self.galleryScaled[self.galleryIndex])
    self.updateImageCounter()
    self.updatePreviewImages()
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

  # update preview pane size and images
  def updatePreviewPane(self):

    # display as many previews as there are images in gallery
    self.numPreview = len(self.gallery)-1

    # if gallery is too large to display in preview pane, find maximum images which can be displayed
    while ( (self.numPreview*self.minPreviewSize) >= ( self.width()-(self.navBtnWidth*2)-(self.minPreviewSize*4) ) ):
      self.numPreview -=1

    # ensure odd number of images in preview pane
    if (self.numPreview % 2 == 0):
      self.numPreview +=1

    self.createPreviewBtns()
    self.displayImage()

  # update preview pane display images
  def updatePreviewImages(self):

    previewGallery = self.getPreviewGallery()
    previewSize = len(previewGallery)

    idxMin = self.galleryIndex-int(self.numPreview//2)
    idxMax = self.galleryIndex+int(self.numPreview//2)+1

    i = 0
    for idx in range(idxMin,idxMax):
      if (idx <= 0):        
        idx = previewSize+idx-1
      elif (idx >= previewSize):
        idx = idx-previewSize+1

      image = previewGallery[idx]
      self.previewBtns[i].setText(str(idx))
      self.previewBtns[i].setIcon(QIcon(image))
      self.previewBtns[i].setIconSize(image.rect().size())
      i +=1

  # scale images for preview gallery
  def getPreviewGallery(self):

    previewGallery = []
    previewGallery.append("preview")
    idxCenter = self.numPreview//2

    # scale images to match preview button size
    # center preview for currently displayed image is scaled to twice the size of all the other preview images
    for i in range(1,len(self.gallery)):
      image = self.gallery[i]
      if (i == self.galleryIndex):
        image = image.scaled(self.previewBtns[idxCenter].size().width(), self.previewBtns[idxCenter].size().height(), Qt.KeepAspectRatio, Qt.FastTransformation)        
      else:        
        image = image.scaled(self.previewBtns[idxCenter].size().width()/2, self.previewBtns[idxCenter].size().height()/2, Qt.KeepAspectRatio, Qt.FastTransformation)
      previewGallery.append(image)

    return previewGallery

  # create preview pane buttons
  def createPreviewBtns(self):
    self.clearLayout(self.PreviewLayout)

    # SELECTION ARROWS #
    self.viewPrevBtn = QPushButton("<")
    self.viewNextBtn = QPushButton(">")
    self.viewPrevBtn.setFixedWidth(self.navBtnWidth)
    self.viewNextBtn.setFixedWidth(self.navBtnWidth)
    self.viewPrevBtn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
    self.viewNextBtn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Minimum)
    self.viewPrevBtn.clicked.connect(self.SLOT_viewPrev)
    self.viewNextBtn.clicked.connect(self.SLOT_viewNext)
    self.PreviewLayout.addWidget(self.viewPrevBtn)
    
    maxSize = self.width()//15

    # PREVIEW IMAGES #
    self.previewBtns.clear()
    previewSizePolicy = QSizePolicy()
    previewSizePolicy.setHorizontalStretch(1)
    previewSizePolicy.setVerticalStretch(1)
    previewSizePolicy.setHorizontalPolicy(QSizePolicy.Expanding)
    previewSizePolicy.setVerticalPolicy(QSizePolicy.Expanding)
    for i in range(0,self.numPreview):
      self.previewBtns.append(QToolButton())
      self.previewBtns[i].setMinimumSize(self.minPreviewSize,self.minPreviewSize)
      self.previewBtns[i].setMaximumSize(maxSize,maxSize)
      self.previewBtns[i].setSizePolicy(previewSizePolicy)
      self.previewBtns[i].setStyleSheet("color:transparent; background-color:transparent; border:0px;")
      self.previewBtns[i].clicked.connect(self.SLOT_previewClicked)
      self.PreviewLayout.addWidget(self.previewBtns[i])

    # center preview #
    previewSizePolicy.setHorizontalStretch(2)
    previewSizePolicy.setVerticalStretch(2)
    self.previewBtns[self.numPreview//2].setMinimumSize(self.minPreviewSize*2,self.minPreviewSize*2)
    self.previewBtns[self.numPreview//2].setMaximumSize(maxSize*2,maxSize*2)
    self.previewBtns[self.numPreview//2].setSizePolicy(previewSizePolicy)

    self.PreviewLayout.addWidget(self.viewNextBtn)

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

    self.updatePreviewPane()

  # SLOT: display image selected from preview
  def SLOT_previewClicked(self):

    self.galleryIndex = int(self.sender().text())
    if self.galleryIndex == 0:
      self.galleryIndex = len(self.gallery)-1
    self.displayImage()

  # SLOT: Main Window has been resized
  def SLOT_resized(self):
    if (self.showing):
      self.updatePreviewPane()

  # critical dialog pop-up
  def dialogCritical(self, s):
    dlg = QMessageBox(self)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Critical)
    dlg.show()

  # delete all widgets in a layout
  def clearLayout(self, layout):
    while layout.count():
      child = layout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

  # update main window title
  def updateTitle(self, str=""):
    self.setWindowTitle("MOJO ALONSO's PHOTO VIEWER"+ str)

  # capture arrow key press to navigate gallery
  def keyPressEvent(self, event):

    keyCode = event.key()

    if (16777234 == keyCode):
      self.SLOT_viewPrev()

    elif (16777236 == keyCode):
      self.SLOT_viewNext()

  # overload Main Window resizeEvent to emit signal
  def resizeEvent(self, event):
    self.resized.emit()
    return super(MainWindow, self).resizeEvent(event)

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Window = MainWindow()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
