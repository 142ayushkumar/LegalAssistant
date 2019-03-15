
# coding: utf-8

# In[5]:


import keras
from keras import regularizers
import numpy as np
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.optimizers import RMSprop
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential, Input
from keras.layers import Dense, Dropout, Embedding, SpatialDropout1D
from keras.layers import LSTM, Bidirectional, Activation
from keras.callbacks import ModelCheckpoint
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from tqdm import tqdm
from sklearn.metrics import roc_auc_score 
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[28]:


tqdm.monitor_interval = 0
#hyperparamter
DATA_DIR = "../data/"
output_dir = '../data/lstm/'

#data
test_size = 0.1
validation_size = 0.1
random_state = 12345

#Training 
epochs = 8
batch_size = 128

#vector-space embedding
n_dim = 64
n_unique_words = 10000
max_length = 100
pad_type = trunc_type = 'pre' # 'pre' or 'post'
drop_embed = 0.25

#lstm architecture 
n_lstm = 64
drop_lstm = 0.1
kernel_reg_lstm = 0.000014
activity_reg_lstm = 0.00012

#fully connected layer 
n_fc = 64
kernel_reg_fc = 0.000013

#optimizer 
learning_rate = 0.0007


# In[20]:


# load the data
data, labels = [],[]
for file in tqdm(os.listdir(DATA_DIR+'pickled/')):
    with open(DATA_DIR+'pickled/'+file,'rb') as f:
        text,label = pickle.load(f)
        data.append(text)
        labels.append(label)


# In[21]:


len(data)


# In[22]:


one_hot = MultiLabelBinarizer()
labels = one_hot.fit_transform(labels)
len(labels[0])


# In[23]:


data = np.array(data)
labels = np.array(labels)


# In[24]:


train_x,test_x, train_y, test_y = train_test_split(data, labels, test_size=test_size, random_state=random_state)


# In[25]:


len(train_x), len(train_y), len(test_x), len(test_y)


# In[26]:


train_y = [x for x in train_y.transpose()]
test_y = [x for x in test_y.transpose()]


# In[27]:


if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# In[29]:


tok_1 = Tokenizer(num_words=n_unique_words)
tok_1.fit_on_texts(train_x)                                
sequences = tok_1.texts_to_sequences(train_x)
sequences_matrix = sequence.pad_sequences(sequences, maxlen=max_length, padding=pad_type, truncating=trunc_type)
def RNN_1():
    inputs = Input(name='inputs', shape=[max_length])
    layer = Embedding(n_unique_words, n_dim, input_length=max_length)(inputs)  
    layer = Bidirectional(LSTM(n_lstm, 
                               recurrent_dropout=drop_lstm, 
                               kernel_regularizer=regularizers.l2(kernel_reg_lstm),
                               activity_regularizer=regularizers.l1(activity_reg_lstm))
                         )(layer)
    layer_lst=[]
    sigmoid_lst=[]
    for i in range(len(train_y)):
        fc1 = Dense(n_fc,
                    name='FC_1_'+str(i),
                    kernel_regularizer=regularizers.l2(kernel_reg_fc)
                   )(layer)
        fc2 = Dense(1,
                    name='FC_2_'+str(i),
                    kernel_regularizer=regularizers.l2(kernel_reg_fc)
                   )(fc1)
        sigmoid_lst.append(Activation('sigmoid')(fc2))

    model = Model(inputs=inputs, outputs=sigmoid_lst)
    return model
model = RNN_1()
model.summary()


# In[ ]:


model.compile(loss='binary_crossentropy',optimizer=RMSprop(lr=learning_rate),metrics=['accuracy'])
modelcheckpoint = ModelCheckpoint(filepath=output_dir+"/weights.{epoch:02d}.hdf5", save_best_only=True)
history = model.fit(sequences_matrix,
          train_y,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_split=validation_size, 
          callbacks=[modelcheckpoint])


# In[18]:


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

