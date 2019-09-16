from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia  import *

import os
import sys

from random import shuffle

from PyStyle import *

class MainWindow(QMainWindow):
  resized = pyqtSignal()
  
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.showing = False
    self.appctxt = ApplicationContext()

    MainWidgetContainer = QWidget()
    MainWidgetContainer.setStyleSheet(StyleSheet.css("window"))

    # get user's screen dimensions
    self.screen = QDesktopWidget().screenGeometry()
    self.maxWidth = self.screen.width()
    self.maxHeight = self.screen.height()

    # Main Window sizing
    self.setMinimumSize(self.maxWidth//2.5,self.maxHeight//2.5)
    self.resize(self.maxWidth//1.5,self.maxHeight//1.5)

    # get gallery groups
    imgPath = self.appctxt.get_resource('images/')
    self.getGalleryGroups(imgPath)

    #############
    #  WIDGETS  #
    #############

    # status bar #
    self.status = QStatusBar()
    self.status.setStyleSheet("color:rgb(255,255,255);")    
    # self.setStatusBar(self.status)

    # IMAGE VIEW #
    self.imageViewer = QLabel()
    self.imageViewer.setStyleSheet(StyleSheet.css("image"))
    self.imageViewer.setAlignment(Qt.AlignCenter)
    self.imageViewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    # counter #
    self.imageCounter = QLineEdit()
    self.imageCounter.setStyleSheet(StyleSheet.css("counter"))
    self.imageCounter.setReadOnly(True)
    self.imageCounter.setFixedSize(125,40)
    self.imageCounter.setAlignment(Qt.AlignCenter)

    # GROUP BUTTONS #
    self.groupBtns = []
    for group in self.groups:
      self.groupBtns.append(QPushButton(group))

    # PREVIEW PANE # --> goto createPreviewBtns()
    self.previewBtns = []
    self.minPreviewSize = 50
    self.oldPreviewWidth = 50
    self.oldPreviewHeight = 50
    self.navBtnWidth = 35
    self.navBtnHeight = 115
    self.maxNumPreview = 13

    # collapse #
    self.collapseBtn = QPushButton("Collapse Preview")
    self.collapseBtnWidth = 200
    self.collapseBtn.setFixedWidth(self.collapseBtnWidth)
    self.collapseBtn.setCheckable(True)
    self.collapseBtn.setChecked(True)
    self.collapseBtn.setStyleSheet(StyleSheet.css("collapse"))

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

    # Top Horizontal Layout #
    TopHLayout = QHBoxLayout()
    for btn in self.groupBtns:
      TopHLayout.addWidget(btn)

    # Bottom Horizontal Layout #
    BottomHLayout       = QHBoxLayout()
    BottomLeftLayout    = QHBoxLayout()
    BottomCenterLayout  = QHBoxLayout()
    BottomRightLayout   = QHBoxLayout()

    # left spacer
    spacerL = QWidget()
    spacerL.setStyleSheet("background-color:transparent;")
    spacerL.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
    BottomLeftLayout.addWidget(spacerL)

    # right spacper
    spacerR = QWidget()
    spacerR.setStyleSheet("background-color:transparent;")
    spacerR.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
    BottomRightLayout.addWidget(spacerR)
    BottomRightLayout.setAlignment(Qt.AlignRight)

    BottomCenterLayout.addWidget(self.imageCounter)
    BottomRightLayout.addWidget(self.collapseBtn)
    BottomHLayout.addLayout(BottomLeftLayout)
    BottomHLayout.addLayout(BottomCenterLayout)
    BottomHLayout.addLayout(BottomRightLayout)

    # Preview Layout #
    self.PreviewLayout = QHBoxLayout()
    # self.previewPane.setLayout(self.PreviewLayout)

    # Image Viewer Layout #
    viewerVLayout = QVBoxLayout()
    viewerVLayout.addWidget(self.imageViewer)
    viewerVLayout.addLayout(BottomHLayout)
    viewerVLayout.addLayout(self.PreviewLayout)

    # Main Horizontal Layout #
    MainHLayout       = QHBoxLayout()
    self.LeftVLayout  = QVBoxLayout()
    self.RightVLayout = QVBoxLayout()
    MainHLayout.addLayout(self.LeftVLayout)
    MainHLayout.addLayout(viewerVLayout)
    MainHLayout.addLayout(self.RightVLayout)

    # Main Vertical Layout
    MainVLayout = QVBoxLayout()
    MainVLayout.addLayout(TopHLayout)
    MainVLayout.addLayout(MainHLayout)

    MainWidgetContainer.setLayout(MainVLayout)
    self.setCentralWidget(MainWidgetContainer)

    ####################
    #  SIGNAL / SLOTS  #
    ####################
    self.resized.connect(self.SLOT_resized)
    self.collapseBtn.clicked.connect(self.SLOT_collapseBtnClicked)

    for btn in self.groupBtns:
      btn.clicked.connect(self.SLOT_viewGroup)

    ####################
    #     GALLERIES    #
    ####################
    self.gallery       = [] # gallery of images to be displayed
    self.galleryScaled = [] # display gallery images scaled 
    self.galleryIndex  = 1  # display gallery index for image being viewed

    # initialize 2D list of galleries, sorted by group
    self.galleryGroups       = []
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
    self.initImages(imgPath)        # import resource images into gallery groups
    self.SLOT_collapseBtnClicked()  # create left / right navigation buttons
    self.updatePreviewPane()        # create Preview Pane
    self.styleGroupBtns("All")      # style group buttons
    self.updateTitle()
    self.show()

    # clean up sizing after show
    self.displayImage()
    self.collapseBtn.setChecked(False)
    self.SLOT_collapseBtnClicked()
    self.showing = True

  # get image groups from directories in 'main/resources/base/images/'
  def getGalleryGroups(self, path):

    self.groups = []
    self.groups.append("All")

    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
      for dir in sorted(d):
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

    # randomize the order of images in the "All" gallery
    tmp = self.galleryGroups[0][1:]
    shuffle(tmp)
    self.galleryGroups[0][1:] = tmp

  # sort image into a gallery group (based on containin directory name)
  def sortImage(self,dir,image):

    groupName = dir[dir.rfind('/')+1:] # strip path down to last directory name
    if (groupName.find('\\') != -1):
      groupName = dir[dir.rfind('\\')+1:] # . . . fucking windows

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
    if (not self.collapseBtn.isChecked()):
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
    while ( (self.numPreview*self.minPreviewSize) >= ( self.width()-(self.navBtnWidth*2)-(self.minPreviewSize*2) ) ):
      self.numPreview -=1

    # ensure odd number of images in preview pane
    if (self.numPreview % 2 == 0):
      self.numPreview +=1

    if (self.numPreview > self.maxNumPreview):
      self.numPreview = self.maxNumPreview

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
        # image = image.scaled(self.oldPreviewWidth, self.oldPreviewHeight, Qt.KeepAspectRatio, Qt.FastTransformation)        
      else:        
        image = image.scaled(self.previewBtns[idxCenter].size().width()/2, self.previewBtns[idxCenter].size().height()/2, Qt.KeepAspectRatio, Qt.FastTransformation)
        # image = image.scaled(self.oldPreviewWidth/2, self.oldPreviewHeight/2, Qt.KeepAspectRatio, Qt.FastTransformation)
      previewGallery.append(image)

    return previewGallery

  # create preview pane buttons
  def createPreviewBtns(self):
    self.clearLayout(self.PreviewLayout)

    # spacers #
    spacerL = QWidget()
    spacerR = QWidget()
    
    maxSize = self.width()//self.numPreview

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

  # create navigation buttons
  def createNavBtns(self):
    self.viewPrevBtn = QPushButton("<")
    self.viewNextBtn = QPushButton(">")
    self.viewPrevBtn.setStyleSheet(StyleSheet.css("navBtn"))
    self.viewNextBtn.setStyleSheet(StyleSheet.css("navBtn"))
    self.viewPrevBtn.clicked.connect(self.SLOT_viewPrev)
    self.viewNextBtn.clicked.connect(self.SLOT_viewNext)

    self.vspacerLT = QWidget()
    self.vspacerLB = QWidget()
    self.vspacerRT = QWidget()
    self.vspacerRB = QWidget()
    self.vspacerLT.setStyleSheet("background-color:transparent;")
    self.vspacerLB.setStyleSheet("background-color:transparent;")
    self.vspacerRT.setStyleSheet("background-color:transparent;")
    self.vspacerRB.setStyleSheet("background-color:transparent;")

  # style groups buttons
  def styleGroupBtns(self, group):
    for btn in self.groupBtns:
      if (btn.text() == group):
        btn.setStyleSheet(StyleSheet.css("groupActive"))
      else :
        btn.setStyleSheet(StyleSheet.css("group"))

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
    
    i = 0 # change display gallery
    for gallery in self.galleryGroups:
      if (gallery[0] == groupName):
        self.gallery = gallery
        self.galleryScaled = self.galleryGroupsScaled[i]
      i +=1

    self.styleGroupBtns(groupName)
    self.displayImage()

  # SLOT: display image selected from preview
  def SLOT_previewClicked(self):

    self.galleryIndex = int(self.sender().text())
    if self.galleryIndex == 0:
      self.galleryIndex = len(self.gallery)-1
    self.displayImage()

  # SLOT: collapse button clicked
  def SLOT_collapseBtnClicked(self):

    self.clearLayout(self.LeftVLayout)
    self.clearLayout(self.RightVLayout)

    self.createNavBtns()

    # Collapse Preview Pane
    if (self.collapseBtn.isChecked()):
      self.collapseBtn.setText("Expand Preview ▲")
      self.vspacerLT.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
      self.vspacerLB.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
      self.vspacerRT.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
      self.vspacerRB.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
      self.viewPrevBtn.setFixedSize(self.navBtnWidth, self.navBtnHeight*2)
      self.viewNextBtn.setFixedSize(self.navBtnWidth, self.navBtnHeight*2)
      self.LeftVLayout.addWidget(self.viewPrevBtn)
      self.LeftVLayout.addWidget(self.vspacerLT)
      self.LeftVLayout.addWidget(self.viewPrevBtn)
      self.LeftVLayout.addWidget(self.vspacerLB)
      self.RightVLayout.addWidget(self.vspacerRT)
      self.RightVLayout.addWidget(self.viewNextBtn)
      self.RightVLayout.addWidget(self.vspacerRB)

      if (self.showing):
        self.oldPreviewWidth = self.previewBtns[self.numPreview//2].size().width()
        self.oldPreviewHeight = self.previewBtns[self.numPreview//2].size().height()
      self.clearLayout(self.PreviewLayout)

    # Expand Preview Pane
    else:
      self.collapseBtn.setText("Collapse Preview ▼")
      self.vspacerLT.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
      self.vspacerRT.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
      self.vspacerLB.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
      self.viewPrevBtn.setFixedSize(self.navBtnWidth, self.navBtnHeight)
      self.viewNextBtn.setFixedSize(self.navBtnWidth, self.navBtnHeight)
      self.vspacerLB.setMinimumSize(0,self.oldPreviewHeight//4)
      self.LeftVLayout.addWidget(self.vspacerLT)
      self.LeftVLayout.addWidget(self.viewPrevBtn)
      self.LeftVLayout.addWidget(self.vspacerLB)
      self.RightVLayout.addWidget(self.vspacerRT)
      self.RightVLayout.addWidget(self.viewNextBtn)
      self.RightVLayout.addWidget(self.vspacerRB)
      self.updatePreviewPane()

    self.displayImage()

  # SLOT: Main Window has been resized
  def SLOT_resized(self):
    if (self.showing):
      self.minPreviewSize = self.width()/self.numPreview//1.5
      if (not self.collapseBtn.isChecked()):
        self.updatePreviewPane()
      self.SLOT_collapseBtnClicked()

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
    self.setWindowTitle("Perlman Family Photo Album"+ str)

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
