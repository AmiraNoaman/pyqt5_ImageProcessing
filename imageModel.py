## This is the abstract class that the students should implement  
from modesEnum import Modes
import numpy as np
import cv2

class ImageModel():

    # """
    # A class that represents the ImageModel"
    # """

    def __init__(self):
        pass

    def __init__(self, imgPath: str):
        self.imgPath = imgPath

        ###
        # ALL the following properties should be assigned correctly after reading imgPath 
        ###
        self.imgByte = cv2.imread(self.imgPath,0)
        self.dft =  np.fft.fft2(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude =  np.abs(self.dft)
        self.phase = np.angle(self.dft)



    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        # """
        # a function that takes ImageModel object mag ratio, phase ration 
        # """
        if mode==mode.magnitudeAndPhase:
            tempMag=(self.magnitude*magnitudeOrRealRatio)+(imageToBeMixed.magnitude*(1-magnitudeOrRealRatio))
            tempPhase=(self.phase*phaesOrImaginaryRatio)+(imageToBeMixed.phase*(1-phaesOrImaginaryRatio))
            self.FourierImg=np.multiply(tempMag, np.exp(1j*tempPhase))
        
        elif mode==mode.realAndImaginary:
            tempReal=(self.real*magnitudeOrRealRatio)+(imageToBeMixed.real*(1-magnitudeOrRealRatio))
            tempImaginary=(self.imaginary*magnitudeOrRealRatio)+(imageToBeMixed.imaginary*(1-magnitudeOrRealRatio))
            self.FourierImg= tempReal+ 1j*tempImaginary

        elif mode==mode.magnitudeAndUnitPhase:
            self.phase=np.multiply(imageToBeMixed.phase,0)
            tempMag=(self.magnitude*magnitudeOrRealRatio)+(imageToBeMixed.magnitude*(1-magnitudeOrRealRatio))
            tempPhase=(self.phase*phaesOrImaginaryRatio)+(imageToBeMixed.phase*(1-phaesOrImaginaryRatio))
            self.FourierImg=np.multiply(tempMag, np.exp(1j*tempPhase))

        elif mode==mode.phaseAndUnitMagnitude:
            self.magnitude=imageToBeMixed.magnitude/imageToBeMixed.magnitude
            tempMag=(self.magnitude*magnitudeOrRealRatio)+(imageToBeMixed.magnitude*(1-magnitudeOrRealRatio))
            tempPhase=(self.phase*phaesOrImaginaryRatio)+(imageToBeMixed.phase*(1-phaesOrImaginaryRatio))
            self.FourierImg=np.multiply(tempMag, np.exp(1j*tempPhase))




        self.img=np.real(np.fft.ifft2(self.FourierImg))
        return self.img    
     

     