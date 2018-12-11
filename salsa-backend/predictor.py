import os
import numpy as np
import librosa as lbr
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.layers import Input, Dense, Dropout, Activation, \
        TimeDistributed, Convolution1D, MaxPooling1D, BatchNormalization, GlobalAveragePooling1D

import tensorflow as tf
global graph,model
graph = tf.get_default_graph()

GENRES = ['reggae', 'salsa', 'soca']
GENRE_DESCRIPTS = [ "Reggae is a music genre that originated in Jamaica in the late 1960s. The term also denotes the modern popular music of Jamaica and its diaspora. A 1968 single by Toots and the Maytals, 'Do the Reggay' was the first popular song to use the word 'reggae,' effectively naming the genre and introducing it to a global audience. While sometimes used in a broad sense to refer to most types of popular Jamaican dance music, the term reggae more properly denotes a particular music style that was strongly influenced by traditional mento as well as American jazz and rhythm and blues, especially the New Orleans R&B practiced by Fats Domino and Allen Toussaint, and evolved out of the earlier genres ska and rocksteady.", "Salsa music is a popular dance music genre that initially arose in New York City during the 1960s. Salsa is the product of various musical genres including the Cuban son montuno, guaracha, cha cha chá, mambo, and to a certain extent bolero, and the Puerto Rican bomba and plena. Latin jazz, which was also developed in New York City, has had a significant influence on salsa arrangers, piano guajeos, and instrumental soloists.", "Soca music is a genre of music that originated within a marginalized subculture in Trinidad and Tobago in the early 1970s, and developed into a range of styles by the 1980s and later. Soca was initially developed by Lord Shorty in the early 1970s in an effort to revive traditional calypso, the popularity of which had been flagging amongst younger generations in Trinidad by the start of the 1970s due to the rise in popularity of reggae from Jamaica and soul and funk from USA. Soca is an offshoot of kaiso/calypso, with influences from chutney, Latin, cadence, funk and soul."] 
MEL_KWARGS = { 'n_fft': 2048, 'hop_length': 1024, 'n_mels': 128}

model_input = Input((None, 128), name='input')
layer = model_input
for i in range(3):
    # second convolutional layer names are used by extract_filters.py
    layer = Convolution1D(filters=256, kernel_size=5, name='convolution_' + str(i + 1))(layer)
    layer = BatchNormalization(momentum=0.9)(layer)
    layer = Activation('relu')(layer)
    layer = MaxPooling1D(2)(layer)
    layer = Dropout(0.5)(layer)

layer = TimeDistributed(Dense(3))(layer)
layer = GlobalAveragePooling1D()(layer)
layer = Activation('softmax', name='output_realtime')(layer)
model_output = layer
model = Model(model_input, model_output)
model.load_weights("model.h5")
model.compile( loss='categorical_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])

def load_track(filename, shape_x=3534):
    new_input, sample_rate = lbr.load(filename, mono=True)
    features = lbr.feature.melspectrogram(new_input, **MEL_KWARGS).T

    if features.shape[0] < shape_x:
        delta_shape = (shape_x - features.shape[0], features.shape[1])
        features = np.append(features, np.zeros(delta_shape), axis=0)
    elif features.shape[0] > shape_x:
        features = features[:shape_x, :]

    features[features == 0] = 1e-6
    return np.log(features)

def predict(filename):
    x_test     = load_track(filename)
    print(x_test, x_test.shape)
    with graph.as_default():
     
        predictions = model.predict(x_test.reshape(1, 3534, 128))
    return predictions[0]

if __name__ == '__main__':
    GENRES = ['reggae', 'salsa ', 'soca  ']

    for testdir in ["./data"]:
        results = [0, 0, 0]
        for file in os.listdir(testdir):
            filepath = os.path.join(testdir, file)
            if not filepath.endswith(".mp3"): continue
            result = predict(filepath)
            predicted_genre = np.argmax(result) # Get max probability
            print(filepath, "Predicted : ", GENRES[predicted_genre], " ".join(["%.2f%%"%(i*100.0) for i in result]))
            results[predicted_genre] += 1
        
        print(testdir, ["%s: %03d" %(GENRES[i], results[i]) for i in range(3)])
