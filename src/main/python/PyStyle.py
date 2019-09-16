# StyleSheet class returns CSS stylesheets for QWidgets

class StyleSheet(object):
  def __init__(self, arg):
    super(ClassName, self).__init__()
    self.arg = arg
    
  def css(widget=None):

    if ("window" == widget):

        MainWindow = \
        "color:rgb(255,255,255);" + \
        "background-color:" + \
        "qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1," + \
        "stop: 0.0 rgb(35,35,35)" + \
        "stop: 0.2 rgb(50,50,50)" + \
        "stop: 0.7 rgb(50,50,50)," + \
        "stop: 1.0 rgb(25,25,25));"

        return MainWindow

    elif ("button" == widget):

        button = \
        "QPushButton {" + \
        "font-size: 16px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "border:3px solid transparent;" + \
        "padding:5px;" + \
        "}" + \
        "QPushButton::hover {" + \
        "background-color:rgb(60,60,60);" + \
        "}"

        return button

    elif ("image" == widget):

        DisplayImage = \
        "color:transparent;" + \
        "background-color:transparent;" + \
        "border:0px;"

        return DisplayImage

    elif ("counter"== widget):

        ImageCounter = \
        "font-size: 15px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(60,60,60);" + \
        "border:1px solid transparent;" + \
        "border-radius:10px;" + \
        "margin:5;" + \
        "padding:px;"

        return ImageCounter

    elif ("navBtn" == widget):

        navBtn = \
        "QPushButton {" + \
        "font-size: 28px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:transparent;" + \
        "border:3px solid transparent;" + \
        "border-radius:15px;" + \
        "padding:25px;" + \
        "}" + \
        "QPushButton::hover {" + \
        "background-color:rgb(60,60,60);" + \
        "}"

        return navBtn

    elif ("group" == widget):

        group = \
        "QPushButton {" + \
        "font-size: 16px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:transparent;" + \
        "border:3px solid transparent;" + \
        "padding:5px;" + \
        "}" + \
        "QPushButton::hover{" + \
        "background-color:rgb(50,50,50);" + \
        "}"

        return group

    elif ("groupActive" == widget):

        groupActive = \
        "QPushButton {" + \
        "font-size: 16px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "border:3px solid transparent;" + \
        "border-bottom:3px solid white;" + \
        "padding:5px;" + \
        "}"

        return groupActive
    
    elif ("collapse" == widget):

        collapseBtn = \
        "QPushButton {" + \
        "font-size: 15px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:transparent;" + \
        "border:3px solid transparent;" + \
        "border-radius:15px;" + \
        "padding:5px;" + \
        "}" + \
        "QPushButton::hover {" + \
        "background-color:rgb(60,60,60);" + \
        "}"

        return collapseBtn

    elif ("preview" == widget):

        PreviewPane = \
        "QWidget {" + \
        "border-radius:10px;" + \
        "color:rgb(255,255,255);" + \
        "background-color:transparent;" + \
        "}"

        return PreviewPane
