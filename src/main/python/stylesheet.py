# StyleSheet class to set MainWindow CSS stylesheet

class StyleSheet(object):
  def __init__(self, arg):
    super(ClassName, self).__init__()
    self.arg = arg
    
  def css():

    MainWindow = \
    "QMainWindow {" + \
    "color:rgb(255,255,255);" + \
    "background-color:rgb(150,150,150);" + \
    "}"

    QPushButton = \
    "QPushButton {" + \
    "color:rgb(255,255,255);" + \
    "background-color:rgb(150,150,150);" + \
    "}"

    QLabel = \
    "QLabel {" + \
    "color:transparent;" + \
    "background-color:transparent;" + \
    "border:0px;" + \
    "}"


    css = MainWindow + QPushButton + QLabel

    return css


