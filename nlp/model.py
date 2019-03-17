
# coding: utf-8

# In[1]:


import keras
from keras import regularizers
import numpy as np
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import RMSprop, Adam
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential, Input
from keras.layers import Dense, Dropout, Embedding, SpatialDropout1D
from keras.layers import LSTM, Bidirectional, Activation, CuDNNLSTM, Layer
from keras.callbacks import ModelCheckpoint
from keras import initializers, regularizers, constraints, optimizers, layers

import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from tqdm import tqdm
from sklearn.metrics import roc_auc_score 
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


import keras.backend as K
K.tensorflow_backend._get_available_gpus()


# In[17]:


tqdm.monitor_interval = 0
#hyperparamter
DATA_DIR = "../data/"
output_dir = '../data/lstm_attn/'

#data
test_size = 0.1
validation_size = 0.1
random_state = 12345

#Training 
epochs = 20
batch_size = 128

#vector-space embedding
n_dim = 64
n_unique_words = 10000
max_length = 100
pad_type = trunc_type = 'pre' # 'pre' or 'post'
drop_embed = 0.25
trainable = False

#lstm architecture 
n_lstm = 64
drop_lstm = 0.1
kernel_reg_lstm = 0.000014
activity_reg_lstm = 0.000012

#fully connected layer 
n_fc = 64
kernel_reg_fc = 0.000013
drop_fc = 0.1

#optimizer 
learning_rate = 0.0007


# In[4]:


# load the data
with open('../data/data.pkl','rb') as f:
    data = pickle.load(f)
with open('../data/labels.pkl','rb') as f:
    labels = pickle.load(f)


# In[5]:


# with open('../data/data.pkl','wb') as f:
#     pickle.dump(data,f)
# with open('../data/labels.pkl','wb') as f:
#     pickle.dump(labels,f)


# In[6]:


len(data)


# In[7]:


one_hot = MultiLabelBinarizer()
labels = one_hot.fit_transform(labels)
len(labels[0])


# In[8]:


data = np.array(data)
labels = np.array(labels)


# In[9]:


train_x,test_x, train_y, test_y = train_test_split(data, labels, test_size=test_size, random_state=random_state)


# In[10]:


len(train_x), len(train_y), len(test_x), len(test_y)


# In[11]:


train_y = [x for x in train_y.transpose()]
test_y = [x for x in test_y.transpose()]


# In[12]:


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# In[13]:


tok_1 = Tokenizer(num_words=n_unique_words)
tok_1.fit_on_texts(train_x)                                
sequences = tok_1.texts_to_sequences(train_x)
sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_length, padding=pad_type, truncating=trunc_type)


# In[14]:


EMBEDDING_FILE = '../data/embeddings/glove.840B.300d/glove.840B.300d.txt'
def get_coefs(word,*arr): return word, np.asarray(arr, dtype='float32')
embeddings_index = dict(get_coefs(*o.split(" ")) for o in open(EMBEDDING_FILE))

all_embs = np.stack(embeddings_index.values())
emb_mean,emb_std = all_embs.mean(), all_embs.std()
embed_size = all_embs.shape[1]


# In[15]:


word_index = tok_1.word_index
nb_words = min(n_unique_words, len(word_index))
embedding_matrix = np.random.normal(emb_mean, emb_std, (nb_words, embed_size))
for word, i in tqdm(word_index.items()):
    if i >= n_unique_words: continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None: embedding_matrix[i] = embedding_vector


# In[16]:


class Attention(Layer):
    def __init__(self, step_dim,
                 W_regularizer=None, b_regularizer=None,
                 W_constraint=None, b_constraint=None,
                 bias=True, **kwargs):
        self.supports_masking = True
        self.init = initializers.get('glorot_uniform')

        self.W_regularizer = regularizers.get(W_regularizer)
        self.b_regularizer = regularizers.get(b_regularizer)

        self.W_constraint = constraints.get(W_constraint)
        self.b_constraint = constraints.get(b_constraint)

        self.bias = bias
        self.step_dim = step_dim
        self.features_dim = 0
        super(Attention, self).__init__(**kwargs)

    def build(self, input_shape):
        assert len(input_shape) == 3

        self.W = self.add_weight((input_shape[-1],),
                                 initializer=self.init,
                                 name='{}_W'.format(self.name),
                                 regularizer=self.W_regularizer,
                                 constraint=self.W_constraint)
        self.features_dim = input_shape[-1]

        if self.bias:
            self.b = self.add_weight((input_shape[1],),
                                     initializer='zero',
                                     name='{}_b'.format(self.name),
                                     regularizer=self.b_regularizer,
                                     constraint=self.b_constraint)
        else:
            self.b = None

        self.built = True

    def compute_mask(self, input, input_mask=None):
        return None

    def call(self, x, mask=None):
        features_dim = self.features_dim
        step_dim = self.step_dim

        eij = K.reshape(K.dot(K.reshape(x, (-1, features_dim)),
                        K.reshape(self.W, (features_dim, 1))), (-1, step_dim))

        if self.bias:
            eij += self.b

        eij = K.tanh(eij)

        a = K.exp(eij)

        if mask is not None:
            a *= K.cast(mask, K.floatx())

        a /= K.cast(K.sum(a, axis=1, keepdims=True) + K.epsilon(), K.floatx())

        a = K.expand_dims(a)
        weighted_input = x * a
        return K.sum(weighted_input, axis=1)

    def compute_output_shape(self, input_shape):
        return input_shape[0],  self.features_dim


# In[18]:


def RNN_1():
    inputs = Input(name='inputs', shape=[max_length])
    layer = Embedding(n_unique_words, 
                      300, 
                      #input_length=max_length, 
                      weights=[embedding_matrix], 
                      trainable=trainable
                     )(inputs)  
    layer = SpatialDropout1D(drop_embed)(layer)
    layer = Bidirectional(CuDNNLSTM(n_lstm, 
#                                kernel_regularizer=regularizers.l2(kernel_reg_lstm),
#                                activity_regularizer=regularizers.l1(activity_reg_lstm),
                            return_sequences=True)
                         )(layer)
    
    layer = Attention(max_length)(layer)
    layer_lst=[]
    sigmoid_lst=[]
    for i in range(len(train_y)):
        fc1 = Dense(n_fc,
                    name='FC_1_'+str(i),
                    activation="relu"
                   )(layer)
        fc1 = Dropout(drop_fc)(fc1)
        fc2 = Dense(1,
                    name='FC_2_'+str(i)
                   )(fc1)
        sigmoid_lst.append(Activation('sigmoid')(fc2))

    model = Model(inputs=inputs, outputs=sigmoid_lst)
    return model
model = RNN_1()
model.summary()


# In[19]:


model.compile(loss='binary_crossentropy',optimizer=Adam(lr=learning_rate),metrics=['accuracy'])
modelcheckpoint = ModelCheckpoint(filepath=output_dir+"/weights.{epoch:02d}.hdf5", save_best_only=True)
history = model.fit(sequences_matrix,
          train_y,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=validation_size, 
          callbacks=[modelcheckpoint])


# In[20]:


# print(history.history.keys())
# #  "Accuracy"
# plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'validation'], loc='upper left')
# plt.show()
# "Loss"
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()


# In[ ]:


import gc
gc.collect()

