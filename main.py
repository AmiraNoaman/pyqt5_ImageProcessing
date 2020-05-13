from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, 
    QLabel, QApplication, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import  QPushButton, QMessageBox

from new import Ui_MainWindow
from imageModel import ImageModel
from modesEnum import Modes
import numpy as np
from matplotlib import pyplot as plt
import pyqtgraph as pg
import logging 
import sys
import cv2

logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 

logger=logging.getLogger() 

logger.setLevel(logging.DEBUG) 

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        pg.setConfigOption('background','w')
        self.ui.setupUi(self)

        self.ui.inputImage1Component_2.getPlotItem().hideAxis('bottom')
        self.ui.inputImage1Component_2.getPlotItem().hideAxis('left')
 
        self.ui.inputImage2Component.getPlotItem().hideAxis('bottom')
        self.ui.inputImage2Component.getPlotItem().hideAxis('left')

        self.ui.output1.getPlotItem().hideAxis('bottom')
        self.ui.output1.getPlotItem().hideAxis('left')

        self.ui.output2.getPlotItem().hideAxis('bottom')
        self.ui.output2.getPlotItem().hideAxis('left')

        self.ui.Upload_2.clicked.connect(self.UploadImage)
        self.ui.Upload2.clicked.connect(self.UploadImage)

        self.ui.inputComponents1_2.addAction(self.ui.actionMagnitude)
        self.ui.inputComponents1_2.addAction(self.ui.actionPhase)
        self.ui.inputComponents1_2.addAction(self.ui.actionReal)
        self.ui.inputComponents1_2.addAction(self.ui.actionImaginary)

        self.ui.inputComponents2.addAction(self.ui.actionMagnitude_2)
        self.ui.inputComponents2.addAction(self.ui.actionPhase_2)
        self.ui.inputComponents2.addAction(self.ui.actionReal_2)
        self.ui.inputComponents2.addAction(self.ui.actionImaginary_2)

        self.ui.actionMagnitude.triggered.connect(self.magnitudeTrigger) 
        self.ui.actionPhase.triggered.connect(self.phaseTrigger)
        self.ui.actionReal.triggered.connect(self.realTrigger)
        self.ui.actionImaginary.triggered.connect(self.imagTrigger)

        self.ui.actionMagnitude_2.triggered.connect(self.magnitudeTrigger)
        self.ui.actionPhase_2.triggered.connect(self.phaseTrigger)
        self.ui.actionReal_2.triggered.connect(self.realTrigger)
        self.ui.actionImaginary_2.triggered.connect(self.imagTrigger)

        self.ui.imgChoice1.addAction(self.ui.actionImage1)
        self.ui.imgChoice1.addAction(self.ui.actionImage2)

        self.ui.actionImage1.triggered.connect(self.image1or2)
        self.ui.actionImage2.triggered.connect(self.image1or2)

        self.ui.imgChoice2.addAction(self.ui.actionImage11)
        self.ui.imgChoice2.addAction(self.ui.actionImage22)

        self.ui.actionImage11.triggered.connect(self.image1or2)
        self.ui.actionImage22.triggered.connect(self.image1or2)

        self.ui.componentsChoice1.addAction(self.ui.actionMagnitude_3)
        self.ui.componentsChoice1.addAction(self.ui.actionPhase_3)
        self.ui.componentsChoice1.addAction(self.ui.actionReal_3)
        self.ui.componentsChoice1.addAction(self.ui.actionImaginary_3)
        self.ui.componentsChoice1.addAction(self.ui.actionUniform_Magnitude)
        self.ui.componentsChoice1.addAction(self.ui.actionUniform_Phase)

        self.ui.actionMagnitude_3.triggered.connect(lambda: self.componentValue(1))
        self.ui.actionPhase_3.triggered.connect(lambda: self.componentValue(1))
        self.ui.actionReal_3.triggered.connect(lambda: self.componentValue(1))
        self.ui.actionImaginary_3.triggered.connect(lambda: self.componentValue(1))
        self.ui.actionUniform_Magnitude.triggered.connect(lambda: self.componentValue(1))
        self.ui.actionUniform_Phase.triggered.connect(lambda: self.componentValue(1))

        self.ui.componentsChoice2.addAction(self.ui.actionMagnitude_4)
        self.ui.componentsChoice2.addAction(self.ui.actionPhase_4)
        self.ui.componentsChoice2.addAction(self.ui.actionReal_4)
        self.ui.componentsChoice2.addAction(self.ui.actionImaginary_4)
        self.ui.componentsChoice2.addAction(self.ui.actionUniform_Magnitude_2)
        self.ui.componentsChoice2.addAction(self.ui.actionUniform_Phase_2)

        self.ui.actionMagnitude_4.triggered.connect(lambda: self.componentValue(2))
        self.ui.actionPhase_4.triggered.connect(lambda: self.componentValue(2))
        self.ui.actionReal_4.triggered.connect(lambda: self.componentValue(2))
        self.ui.actionImaginary_4.triggered.connect(lambda: self.componentValue(2))
        self.ui.actionUniform_Magnitude_2.triggered.connect(lambda: self.componentValue(2))
        self.ui.actionUniform_Phase_2.triggered.connect(lambda: self.componentValue(2))
 
        self.ui.outputChoice.addAction(self.ui.actionOutput_1)
        self.ui.outputChoice.addAction(self.ui.actionOutput_2)

        self.ui.actionOutput_1.triggered.connect(self.outputImage)
        self.ui.actionOutput_2.triggered.connect(self.outputImage)

        self.ui.slider1.valueChanged.connect(self.changedValue)
        self.ui.slider2.valueChanged.connect(self.changedValue)

        self.ui.slider1.setMinimum(0)
        self.ui.slider1.setMaximum(100)
        self.ui.slider1.setTickPosition(QSlider.TicksBelow)

        self.ui.slider2.setMinimum(0)
        self.ui.slider2.setMaximum(100)
        self.ui.slider2.setTickPosition(QSlider.TicksBelow)
    
        
        self.var=[]
        self.componentVal=[]

        self.ratio1=None
        self.ratio2=None
        
    def UploadImage(self):
        
        logger.info("Uploading Images") 
        senderUpload = self.sender()
        senderUpload= str(senderUpload.objectName())

        fileOpen = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',"~/Desktop/",'*.jpg')
        filePath=fileOpen[0]
        # self.img=cv2.imread(filePath,0)
        # imageClass=ImageModel(filePath)
        pixmap = QPixmap(filePath)
        pixmap=pixmap.scaled(QtCore.QSize(self.ui.inputImage1_2.width(),self.ui.inputImage1_2.height()))            
        
        if senderUpload=="Upload_2":
            self.IMG1=ImageModel(filePath)
            self.ui.inputImage1_2.setPixmap(pixmap)
            logger.info("Uploaded first picture") 

        elif senderUpload=="Upload2":
            # 1) Check if 2 images are equals

            self.IMG2=ImageModel(filePath)
            if self.IMG1.imgByte.shape == self.IMG2.imgByte.shape:
                self.ui.inputImage2.setPixmap(pixmap)
                logger.info("Uploading 2nd picture successfully") 
            else:
                errorMessage = QMessageBox.question(self, 'Error message', "Pictures aren't of same size", QMessageBox.Ok)
                if errorMessage == QMessageBox.Ok:
                    print('Ok clicked.')
                logger.warning("Warning: 2nd picture is not of same size so failed process") 


    def magnitudeTrigger(self):
        magTrig = self.sender()
        magTrig= str(magTrig.objectName())

        if magTrig=="actionMagnitude":
            mag=self.IMG1.magnitude
            mag=20*np.log(mag)
            self.displayComponent(mag,1)
        elif magTrig == "actionMagnitude_2":
            mag=self.IMG2.magnitude
            mag=20*np.log(mag)
            self.displayComponent(mag,2)
        logger.info("Chose the magnitude component") 


    def phaseTrigger(self):
        phaseTrig = self.sender()
        phaseTrig= str(phaseTrig.objectName())

        if phaseTrig=="actionPhase":
            self.displayComponent(self.IMG1.phase,1)
        elif phaseTrig == "actionPhase_2":
            self.displayComponent(self.IMG2.phase,2)
        logger.info("Chose the phase component") 


    def realTrigger(self):
        realTrig = self.sender()
        realTrig = str(realTrig.objectName())

        if realTrig == "actionReal":
            self.displayComponent(self.IMG1.real,1)
        elif realTrig=="actionReal_2":
            self.displayComponent(self.IMG2.real,2)
        logger.info("Chose the real component") 


    def imagTrigger(self):
        imagTrig=self.sender()
        imagTrig= str(imagTrig.objectName())

        if imagTrig=="actionImaginary":
            self.displayComponent(self.IMG1.imaginary,1)
        elif imagTrig=="actionImaginary_2":
            self.displayComponent(self.IMG2.imaginary,2)
        logger.info("Chose the imaginary component") 


    def image1or2(self):
        image=self.sender()
        image=str(image.objectName())
        
        if (image=="actionImage1"):
            self.var.append(1)
        elif(image=="actionImage2"):
            self.var.append(2)

        if (image=="actionImage11"):
            self.var.append(1)
        elif( image == "actionImage22"):
            self.var.append(2)
        return self.var
        logger.info("Chose the images") 


    def displayComponent(self, array,n):    
        img=pg.ImageItem(array)
        if n==1:
            self.ui.inputImage1Component_2.addItem(img)
        elif n==2:
            self.ui.inputImage2Component.addItem(img)
        img.rotate(270)
        logger.info("Displaying component successfully") 



    def changedValue(self):
        sliderTrigger=self.sender()
        sliderTrigger=str(sliderTrigger.objectName())

        if sliderTrigger=="slider1":
            self.ratio1 = self.ui.slider1.value()
            self.ui.s1Value.setText(str(self.ratio1))
            
        elif sliderTrigger=="slider2":
            self.ratio2 = self.ui.slider2.value()
            self.ui.s2Value.setText(str(self.ratio2))

        if(self.ratio1 is not None and self.ratio2 is not None):
            self.finalOutputFunction()
            logger.info("Changed the sliders' value") 

        



    def finalOutputFunction(self):
#First know which image we will works on
        arr=self.image1or2()
        if arr[0]==1:
            self.usedimg1=self.IMG1
        elif arr[0]==2:
            self.usedimg1=self.IMG2
        if arr[1]==1:
            self.usedimg2=self.IMG1
        elif arr[1]==2:
            self.usedimg2=self.IMG2

        if (self.componentVal[0]=="actionMagnitude_3"  or self.componentVal[0]=="actionReal_3"  or self.componentVal[0]=="actionUnifrom_Magnitude" ):
            self.MagnitudeOrRealRatio= self.ratio1/100
        elif (self.componentVal[0]=="actionPhase_3"  or self.componentVal[0]=="actionImaginary_3" or self.componentVal[0]=="actionUniform_Phase"):
            self.PhaseOrImaginaryRatio= self.ratio1/100
        
        if (self.componentVal[1]=="actionMagnitude_4"  or self.componentVal[1]=="actionReal_4"  or self.componentVal[1]=="actionUnifrom_Magnitude_2" ):
            self.MagnitudeOrRealRatio=self.ratio2/100
        elif (self.componentVal[1]=="actionPhase_4"  or self.componentVal[1]=="actionImaginary_4" or self.componentVal[1]=="actionUniform_Phase_2"):
            self.PhaseOrImaginaryRatio=self.ratio2/100

    
        #Calling Mix Function Now
        if(self.componentVal[0]=="actionMagnitude_3" and self.componentVal[1]=="actionPhase_4"):
            self.output=self.usedimg1.mix(self.usedimg2,self.MagnitudeOrRealRatio, 1-self.PhaseOrImaginaryRatio, Modes.magnitudeAndPhase)
        elif(self.componentVal[0]=="actionMagnitude_3" and self.componentVal[1]=="actionUniform_Phase_2"):
            self.output=self.usedimg1.mix(self.usedimg2,self.MagnitudeOrRealRatio, 100, Modes.magnitudeAndUnitPhase)
        elif(self.componentVal[0]=="actionPhase_3" and self.componentVal[1]=="actionMagnitude_4"):
            self.output=self.usedimg2.mix(self.usedimg1,self.MagnitudeOrRealRatio, 1-self.PhaseOrImaginaryRatio, Modes.magnitudeAndPhase)
        elif(self.componentVal[0]=="actionUniform_Phase" and self.componentVal[1]=="actionMagnitude_4"):
            self.output=self.usedimg2.mix(self.usedimg1, self.MagnitudeOrRealRatio, 100, Modes.magnitudeAndUnitPhase)
        elif(self.componentVal[0]=="actionPhase_3" and self.componentVal[1]=="actionUniform_Magnitude_2"):
            self.output=self.usedimg2.mix(self.usedimg1, 100,self.PhaseOrImaginaryRatio, Modes.phaseAndUnitMagnitude)
        elif(self.componentVal[0]=="actionUniform_Magnitude" and self.componentVal[1]=="actionPhase_4"):
            self.output=self.usedimg1.mix(self.usedimg2, 100, self.PhaseOrImaginaryRatio, Modes.phaseAndUnitMagnitude)
        elif(self.componentVal[0]=="actionReal_3" and self.componentVal[1]=="actionImaginary_4"):
            self.output=self.usedimg1.mix(self.usedimg2, self.MagnitudeOrRealRatio, 1-self.PhaseOrImaginaryRatio, Modes.realAndImaginary)
        elif(self.componentVal[0]=="actionImaginary_3" and self.componentVal[1]=="actionReal_4"):
            self.output=self.usedimg2.mix(self.usedimg1, self.MagnitudeOrRealRatio, 1-self.PhaseOrImaginaryRatio, Modes.realAndImaginary)
        print(self.output)


        
        self.img1=pg.ImageItem(self.output)
        if self.outputImage()==1:
            self.ui.output1.addItem(self.img1)
        elif self.outputImage()==2:       
            self.ui.output2.addItem(self.img1)
        self.img1.rotate(270)
        logger.info("Final Output success") 



    def componentValue(self,n):
        component=self.sender()
        component=str(component.objectName())

        if n==1:
            self.c1=component
            self.componentVal.append(self.c1)

        elif n==2:
            self.c2=component 
            self.componentVal.append(self.c2)

        return self.componentVal


        # return (self.output)
        

    def outputImage(self):
        
        output=self.sender()
        output=str(output.objectName())

        if output=="actionOutput_1":        
            self.outputVariable=1
        elif output=="actionOutput_2":        
            self.outputVariable=2

        return self.outputVariable        




    
def main(): 
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()