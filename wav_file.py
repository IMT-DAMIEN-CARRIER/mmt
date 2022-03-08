#Copyrights
#Alex Broussard, Damien Carrier, Lucas Lemaitre
# -*- coding: utf-8 -*-
#import numpy as np
#import wavio
import wave
import math

# rate = 20000  # samples per second
# T = 3         # sample duration (seconds)
# f = 2000     # sound frequency (Hz)
# t = np.linspace(0, T, T * rate, endpoint=False)
# x = np.sin(2 * np.pi * f * t)
# wavio.write("sine24.wav", x, rate, sampwidth=3)

print("Creation d'un fichier audio au format WAV (PCM 8 bits mono 2000 Hz)")

fileName = 'son.wav'
mySound = wave.open(fileName, 'w') # instanciation de l'objet mySound

freq = 2000 #2kHZ
nbChannel = 1 #mono
nbOctet = 1
freqEchan = 10 * freq
time = 3 #3 secondes
nbEchantillons = time * freqEchan

print("Nombre d'echantillons :", nbEchantillons)
parametres = (nbChannel, nbOctet, freqEchan, nbEchantillons, 'NONE', 'not compressed')
mySound.setparams(parametres)

#Quantification ??
for i in range(0, nbEchantillons):
    val = wave.struct.pack('B', int(128.0 + math.sin(2.0 * math.pi * freq * i / freqEchan)))
    mySound.writeframes(val)

mySound.close()

file = open(fileName, 'rb')
data = file.read()