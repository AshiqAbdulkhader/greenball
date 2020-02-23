# Project Description

a system that will take a visual input from the environment,
process it, present it to the user and give a tangible output.


This is a program to detect green ball from the Builtin camera,Blink an Led if when it detects the ball and Display the 
video feed along with the position and percentage of area covered by the ball in a web interface.

This project uses Arduino.Arduino is an open-source electronics platform based on easy-to-use hardware and software.
Arduino boards are able to read inputs - light on a sensor, a finger on a button, or a Twitter message - and 
turn it into an output - activating a motor, turning on an LED, publishing someth ing online.

it also uses python libraries such as

opencv -(Open Source Computer Vision Library) is an open source computer vision and machine learning software library
numpy - NumPy is the fundamental package for scientific computing with Python
flask - Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy,
            with the ability to scale up to complex applications.
pyserial - python Serial Port Extension for Win32, OSX, Linux, BSD, Jython, IronPython

## Getting Started

Download/clone the folder named final into your local directory.

### Prerequisites

You would need arduino IDE for installing the arduino code and python along with some libraries for running the programs.

The program requires the following libraries

pyserial
flask
opencv-python
numpy

for installing the libraries, Cd to the Folder named Final in the terminal and run the following command

"pip install -r requirements.txt"


### Installing/Configuring

Connect the arduino to the computer. open the arduino code in Arduino IDE and select the port and board from the tools menu. Then upload the arduino code.

connect the Red Led to the 12th pin of arduino and Green Led to the 13th pin.

## Running the tests

open the python file python_script.py in terminal using the command
 'python python_script.py'

open a web browser and go the Link 'localhost:5000' to view the detected ball


