# %matplotlib inline
import pickle
import os
import seaborn, sys
import numpy, scipy, matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display
plt.rcParams['figure.figsize'] = (13, 5)

files = []

a = False
if len(sys.argv) < 2:
	audio_path = os.getcwd() + "\\audio"
	files = os.listdir(audio_path)
	print(files)
else:
	a = True
	for f in sys.argv[1::]:
		files.append(f)
	print(files)

for filename in files:
	f = ["audio/", ""][a] + filename

	print("Loading " + f + "...")
	x, sr = librosa.load(f)

	# 	Primary feature extraction: get Mel-frequency cepstral coefficients from the original signal
	# Replace "x" with "P" or "H" to narrow the coefficients down to focus on percussion or harmony.
	n_mfcc = 12 # 12 is only the example number of features, this can be tinkered with
	mfcc = librosa.feature.mfcc(x,sr,n_mfcc=n_mfcc)

	output_name = [filename, filename[6::]][a][:-4]
	print("Storing features in: ", + output_name)
	output = open(output_name, 'wb')
	pickle.dump(x,output)
	pickle.dump(sr,output)
	# pickle.dump(P,output)
	# pickle.dump(H,output)
	pickle.dump(mfcc,output)
	output.close()

	# # Uncomment to separate harmonic and percussive sources
	# # Get short time fourier transform of signal
	# D = librosa.stft(x)

	# # hpss = harmonic percussion source separation
	# D_harmonic, D_percussive = librosa.decompose.hpss(D)

	# # Construct separate signals for percussive and harmonic sources
	# P = librosa.istft(D_percussive)
	# H = librosa.istft(D_harmonic)



####################
# TEMPO ESTIMATION #
# AND PLOTTING #####
####################


# Get tempo
# tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=120, units='time')
# print("tempo: {0:.2f}".format(tempo))

# plt.figure(figsize=(14, 5))
# librosa.display.waveplot(x, alpha=0.6)
# plt.vlines(beat_times, -1, 1, color='r')
# plt.ylim(-1, 1)
# plt.show()

# print(type(x),type(x[0]),type(D_percussive),type(D_percussive[0]))
# print(len(x))
# print(len(P))

# Pre-compute a global reference power from the input spectrum
# rp = numpy.max(numpy.abs(D))

# plt.figure(figsize=(12, 8))

# plt.subplot(3, 1, 1)
# librosa.display.specshow(librosa.amplitude_to_db(numpy.abs(D), ref=rp), y_axis='log')
# plt.colorbar()
# plt.title('Full spectrogram')

# plt.subplot(3, 1, 2)
# librosa.display.specshow(librosa.amplitude_to_db(numpy.abs(D_harmonic), ref=rp), y_axis='log')
# plt.colorbar()
# plt.title('Harmonic spectrogram')

# plt.subplot(3, 1, 3)
# librosa.display.specshow(librosa.amplitude_to_db(numpy.abs(D_percussive), ref=rp), y_axis='log', x_axis='time')
# plt.colorbar()
# plt.title('Percussive spectrogram')
# plt.tight_layout()
# plt.show()