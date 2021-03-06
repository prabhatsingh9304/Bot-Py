#!/bin/bash
echo "Installation Process will start after you enter your password ....."
sudo apt-get update
sudo apt-get --ignore-missing install -y python3 python3-pip python3-pyaudio
pip3 install speechrecognition gtts pyttsx3 playsound selenium
#mac user uncomment the following code
#pip3 install PyObjc
#brew install portaudio
#pip install pyaudio