# --coding:Latin-1 -

import math
import wave
import struct
import matplotlib.pyplot as plt
#
audio = [] #cr�ation du fichier des frame du fichier audio
sample_rate = 20000.0 # =Nombre de batons par seconde
duration = 3 # 3s
num_samples = duration * sample_rate # =Nombre de baton total 60000
num_bits = int(input('Nb bits : '))
fileName = input('Nom du fichier : ')
volume = 1.0
freq = 2000.0

#random.seed(datetime.now())

def creer_blanc():
    for x in range(int(num_samples)):
        audio.append(0)
    return

def creer_sinus():
    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2.0 * math.pi * freq * x / sample_rate))

def convert():
    i = 0

    for sample in audio:
        max = math.pow(2, num_bits)/2
        s = int(sample * (max)) #[-1 � 1]*(2^8(256)/2) /2 car parit� positif et n�gatif et transformation en int
        # print(math.pow(2, num_bits)/2)

        if s < -math.pow(2, num_bits / 2):
            s = -math.pow(2, num_bits / 2)

        if s > math.pow(2, num_bits / 2) - 1:
            s = math.pow(2, num_bits / 2) -1

        # s = s * 127 / max

        audio[i] = s
        #audio[i] = sample
        i = i + 1

def creer_fichier():
    # Open up a wav file
    wav_file = wave.open(fileName, "w")
    wav_file.setparams((1, 2, sample_rate, len(audio), "NONE", "not compressed"))

    for sample in audio:
        wav_file.writeframes(struct.pack('b', 0))    # ch1
        wav_file.writeframes(struct.pack('b', int(sample)))    # ch2

    wav_file.close()
    return

def affiche_son():
    plt.plot(audio)
    plt.axis([0, 100, -128, 128])
    plt.show()

creer_sinus()
#convert()
#print(audio)
#affiche_son()
creer_fichier()
