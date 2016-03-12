# INTERFACE GRAFICA PARA OBTER DADOS EXPERIMENTAIS DE GRAFICOS NO FORMATO PNG
# ALEXANDRE DE CASTRO MACIEL, DEP. DE FISICA DA UFPI
# MARCO DE 2016
# EXPLICACAO EM http://wp.me/P4JOA-fO

import sys
import os
import os.path
from scipy.misc import imread
import matplotlib.cbook as cbook
from PyQt4 import QtGui
from PyQt4.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas)
from functools import partial

Ui_MainWindow, QMainWindow = loadUiType('mainwindow004.ui')

class Main(QMainWindow, Ui_MainWindow) :
    def __init__(self, ) :
        super(Main, self).__init__()
        self.setupUi(self)

        self.thisDir = os.path.dirname(os.path.abspath(__file__))
        self.btOpenImage.clicked.connect(self.openImage)

        fig = Figure()

        self.canvas = FigureCanvas(fig)
        self.canvasGraph.addWidget(self.canvas)
        self.canvas.draw()

        self.message.setText('Escolha uma imagem')
        self.status.setText('Sem imagem')
        self.Xax.setText('Esperando calibracao')
        self.Xay.setText('Esperando calibracao')

        self.calibrateX.clicked.connect(partial(self.action, 'calX'))

        self.XaxisX = []
        self.XaxisY = []

        return

    def openImage(self) :
        texto = 'Escolha uma imagem'
        path = QtGui.QFileDialog.getOpenFileNameAndFilter(self,
                                                          texto,
                                                          self.thisDir,
                                                          "Images (*.png *.jpg)")

        datafile = cbook.get_sample_data(str(path[0]))
        img = imread(datafile)

        self.updateCanvas(self.initializeCanvas(img))

        self.message.setText('Esperando a calibracao dos eixos')
        self.status.setText('Em espera')

        return

    def initializeCanvas(self, img) :

        fig = Figure()
        fig.clear()
        Graph = fig.add_subplot(111)
        Graph.imshow(img, zorder=0, extent=[0.0, 1.0, 0.0, 1.0])

        return fig

    def updateCanvas(self, fig) :
        self.canvasGraph.removeWidget(self.canvas)
        self.canvas.close()

        self.canvas = FigureCanvas(fig)
        self.canvasGraph.addWidget(self.canvas)
        self.canvas.draw()

        def onclick(event):
            x, y = event.xdata, event.ydata
            if x != None and y != None :
                if self.currentAction == 'calX' :
                    if len(self.XaxisX) == 0 :
                        self.XaxisX.append(x)
                        self.XaxisY.append(y)
                        self.Xax.setText(str(x))
                        self.Xay.setText(str(y))
                        self.message.setText('Clique e marque onde esta Xb')

            return

        self.canvas.mpl_connect('button_press_event', onclick)

        return

    def action(self, what) :
        self.currentAction = what
        if what == 'calX' :
            self.message.setText('Clique e marque onde esta Xa')
            self.status.setText('Calibrando Eixo X')

        return

if __name__ == '__main__' :
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())