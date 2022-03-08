#!/usr/bin/python 
import math
import wave
import struct
import random
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

audio = []
sample_rate = 20000.0
num_bits = 0
nbr_periodes = 0

random.seed(datetime.now())

def append_blank(duration_milliseconds=500):
    global audio # using global variables isn't cool.
    num_samples = duration_milliseconds * (sample_rate / 1000.0)
    for x in range(int(num_samples)):
        audio.append(0)
    return

def append_nb_blank(nb):
    for x in range(int(nb)):
        audio.append(0)
    return

def append_sinewave(freq=440.0, duration_milliseconds=500, volume=1.0):

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * x / sample_rate ))

    return

def append_latency_sinewave(
        freq=440.0, 
        duration_milliseconds=500,
        volume=1.0,
        p_latency=0):

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(0, int(num_samples), 2):
        if random.random() < p_latency:
            ping = random.randrange(1, 50, 1)/100 # random latency duration, 10ns to 500ns with a step of 10ns
            num_latency = int(ping * (sample_rate / 1000.0) / 2)
            for i in range(num_latency):
                audio.append(0)
        audio.append(volume * math.sin(2 * math.pi * freq * x / sample_rate ))
        audio.append(volume * math.sin(2 * math.pi * freq * (x+1) / sample_rate ))

    return

def append_loss_sinewave(
        freq=440.0, 
        duration_milliseconds=500, 
        volume=1.0,
        p_loss=0):

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    print(int(num_samples))

    for x in range(0, int(num_samples), 2):
        if random.random() < p_loss:
            audio.append(0)
            audio.append(0)
        else:
            audio.append(volume * math.sin(2 * math.pi * freq * x / sample_rate ))
            audio.append(volume * math.sin(2 * math.pi * freq * (x+1) / sample_rate ))

    return


def append_DPCM_loss_sinewave(
        freq=440.0, 
        duration_milliseconds=500, 
        volume=1.0,
        p_loss=0):

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    print(int(num_samples))

    previous = 0

    for x in range(0, int(num_samples), 2):
        if random.random() < p_loss:
            audio.append(0)
            audio.append(0)
            previous = 0
        else:
            s_cur = volume * math.sin(2 * math.pi * freq * x / sample_rate )
            s1 = s_cur - (volume * math.sin(2 * math.pi * freq * (x-1) / sample_rate )) + previous
            s2 = volume * math.sin(2 * math.pi * freq * (x+1) / sample_rate ) - s_cur + s1
            previous = s2
            audio.append(s1)
            audio.append(s2)

    return

def append_DPCM_error_sinewave(
        freq=440.0, 
        duration_milliseconds=500, 
        volume=1.0,
        p_loss=0):

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    print(int(num_samples))

    previous = 0

    for x in range(0, int(num_samples), 2):
        if random.random() < p_loss:
            audio.append(random.random())
            se = random.random()
            audio.append(se)
            previous = se
        else:
            s_cur = volume * math.sin(2 * math.pi * freq * x / sample_rate )
            s1 = s_cur - (volume * math.sin(2 * math.pi * freq * (x-1) / sample_rate )) + previous
            s2 = volume * math.sin(2 * math.pi * freq * (x+1) / sample_rate ) - s_cur + s1
            previous = s2
            audio.append(s1)
            audio.append(s2)

    return



def append_error_sinewave(
        freq=440.0, 
        duration_milliseconds=500, 
        volume=1.0,
        p_err=0):

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    print(int(num_samples))

    for x in range(0, int(num_samples), 2):
        if random.random() < p_err:
            audio.append(random.random())
            audio.append(random.random())
        else:
            audio.append(volume * math.sin(2 * math.pi * freq * x / sample_rate ))
            audio.append(volume * math.sin(2 * math.pi * freq * (x+1) / sample_rate ))

    return


def read_write_xtine(p_lat):

    f = open("./xtine.dat")
    j = 0
    lost = 0
    for i in f:
        if lost !=0:
            audio.append(0)
            lost = lost - 1
        else: 
            if random.random() < p_lat and j%4==0:
                lost = 10
                audio.append(0)
            else:
                audio.append(float(i))
    f.close()
    return


def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1
    sampwidth = 2
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"

    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    for sample in audio:
        s = int( sample * (math.pow(2, num_bits)/2))
        if s < -128:
            s = -128
        if s > 127:
            s = 127
        wav_file.writeframes(struct.pack('b', 0 ))    # ch1
        wav_file.writeframes(struct.pack('b', s ))    # ch2

    wav_file.close()

    return

def print_courbe():
    plt.step(audio,'bo-')
    plt.axis([0, nbr_periodes, -1.25, 1.25])
    plt.title(str(num_bits)+" bits")

    # Décommenter ici pour afficher la valeur des points sur la coube
    # for i in range(10):
        # label = format(audio[i])

        # plt.annotate(label,  # this is the text
        #              (i, audio[i]),  # this is the point to label
        #              textcoords="offset points",  # how to position the text
        #              xytext=(0, 10),  # distance from text to points (x,y)
        #              ha='center')  # horizontal alignment can be left, right or center
    plt.show()
    return

def possible_values(nbBits):
    nbValues = 2 ** nbBits
    values = []
    pas = 2 / (nbValues-1)  # 2 étant l'écart entre -1 et 1

    for i in range(0,nbValues):
        values.append(-1 + (i*pas))

    list.sort(values)
    return values

def returnTo8bits():
    for i in range(0, len(audio)):
        audio[i] = audio[i]*128/((2**num_bits)/2)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def quantify():
    possibleValues = possible_values(num_bits)
    for i in range(0, len(audio)):
        audio[i] = find_nearest(possibleValues, audio[i])

# append_latency_sinewave(freq=4000, duration_milliseconds=3000, volume=1, p_latency=0.00005)
#append_loss_sinewave(freq=4000, duration_milliseconds=3000, volume=1, p_loss=0.0001)
append_sinewave(freq=2000, duration_milliseconds=3000, volume=1)
#append_error_sinewave(freq=4000, duration_milliseconds=3000, volume=1, p_err=0.0001)
#append_DPCM_loss_sinewave(freq=4000, duration_milliseconds=3000, volume=1, p_loss=0.001)
#append_DPCM_error_sinewave(freq=4000, duration_milliseconds=3000, volume=1, p_loss=0.0001)

#read_write_xtine(0) # 0 pour ne pas avoir de bruit
num_bits = int(input('Nombre de bits ?'))
fileName = input('Entrer le nom du fichier wav : ')
print("\n")
quantify()

#Décommentez ce bloc pour afficher les courbes
# nbr_periodes = int(input('Nombre de périodes à afficher ?')) * 10
# print_courbe()

returnTo8bits()
save_wav(fileName + '.wav')
#quantify()
# if(input('afficher les valeurs possibles ? (y/n)') == 'y'):
#     print("possible_values("+str(num_bits)+" : ", possible_values(num_bits))
# print('Fin du programme')