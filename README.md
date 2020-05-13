## Write your name and ID
### Name: Amira Ahmad Noaman
### ID: 1170400

# Steps for using the software

1. Upload the images 
2. Choose the components
3. Go to the other tab for mixing
4. Choose the output place
5. Choose the img1,img2 for both components
6. Choose both components to be mixed
7. Change the sliders and you'll get the desired output
8. In the newfile.log you'll find the logging details 

## Screenshots Description

### Main Components:
#### This shows the magnitude of image1 and the phase of image 2 

### Magnitude&Phase:
#### Image 1 for 0.7Mag of img1 and 0.3phase of img2
#### Image 2 for 0.3Mag of img1 and 0.7phase of img2

### Real&Imaginary:
#### Image 1 for 0.7real of img1 and 0.3imaginary of img2
#### Image 2 for 0.3real of img1 and 0.7imaginary of img2

### UniformMagnitude&Phase:
#### Image 1 for magnitude of img1 and uniformPhase of img2
#### Image 2 for phase of img1 and uniformMagnitude of img2


____________________________________________________________


## MagnitudePhaseMixerTemplate
Starter Template for Magnitude Phase Mixer Task


### install opencv to run the test file

### Implement the ImageModel in imageModel.py and its mix function
### run testTask.py --> python testTask.py
### assign a valid path for image1Path and image2Path
### Now when you run testTask you should get the following line
### AssertionError: This is not a numpy array, check the return value of your implemented mix function

### when you implement the mix function correctly you should get the following 2 lines
### Modes.magnitudeAndPhase passed successfully
### Modes.realAndImaginary passed successfully

### Do not forget to update the dep.txt file