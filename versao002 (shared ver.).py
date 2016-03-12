# INTERFACE GRAFICA PARA OBTER DADOS EXPERIMENTAIS DE GRAFICOS NO FORMATO PNG
# ALEXANDRE DE CASTRO MACIEL, DEP. DE FISICA DA UFPI
# MARCO DE 2016
# EXPLICACAO EM http://wp.me/P4JOA-fO

import sys
import os
import os.path
from PyQt4 import QtGui
from PyQt4.uic import loadUiType

Ui_MainWindow, QMainWindow = loadUiType('mainwindow002.ui')

class Main(QMainWindow, Ui_MainWindow) :
    def __init__(self, ) :
        super(Main, self).__init__()
        self.setupUi(self)
        
        self.thisDir = os.path.dirname(os.path.abspath(__file__))
        self.btOpenImage.clicked.connect(self.openImage)
        
    def openImage(self) :
        texto = 'Escolha uma imagem'
        path = QtGui.QFileDialog.getOpenFileNameAndFilter(self,
                                                          texto,
                                                          self.thisDir,
                                                          "Images (*.png *.jpg)")

        print str(path[0])
        
        return

if __name__ == '__main__' :
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())