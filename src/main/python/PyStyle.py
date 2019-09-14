# StyleSheet class returns CSS stylesheets for QWidgets

class StyleSheet(object):
  def __init__(self, arg):
    super(ClassName, self).__init__()
    self.arg = arg
    
  def css(widget=None):

    if (not widget):

        MainWindow = \
        "QMainWindow {" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "}"

        QPushButton = \
        "QPushButton {" + \
        "font-size: 16px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "border:3px solid transparent;" + \
        "border-radius:10px;" + \
        "padding:5px;" + \
        "}" + \
        "QPushButton::hover{" + \
        "background-color:rgb(60,60,60);" + \
        "}"

        QLabel = \
        "QLabel {" + \
        "color:transparent;" + \
        "background-color:transparent;" + \
        "border:0px;" + \
        "}"

        QLineEdit = \
        "QLineEdit {" + \
        "font-size: 15px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "border:0px;" + \
        "margin:-10px;" + \
        "padding:0px;" + \
        "}"

        css = MainWindow + QPushButton + QLabel + QLineEdit

        return css

    elif ("navBtn" == widget):

        QPushButton = \
        "QPushButton {" + \
        "font-size: 28px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "border:3px solid transparent;" + \
        "border-radius:10px;" + \
        "padding:25px;" + \
        "}" + \
        "QPushButton::hover{" + \
        "background-color:rgb(60,60,60);" + \
        "}"

        return QPushButton

    elif ("group" == widget):

        QPushButton = \
        "QPushButton {" + \
        "font-size: 16px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "border:3px solid transparent;" + \
        "border-radius:10px;" + \
        "padding:5px;" + \
        "}" + \
        "QPushButton::hover{" + \
        "background-color:rgb(60,60,60);" + \
        "}"

        return QPushButton


    elif ("groupActive" == widget):

        QPushButton = \
        "QPushButton {" + \
        "font-size: 16px; font-weight:bold;" + \
        "color:rgb(255,255,255);" + \
        "background-color:rgb(50,50,50);" + \
        "border:3px solid transparent;" + \
        "border-bottom:3px solid white;" + \
        "border-radius:0px;" + \
        "padding:5px;" + \
        "}" + \
        "QPushButton::hover{" + \
        "background-color:rgb(60,60,60);" + \
        "}"

        return QPushButton
