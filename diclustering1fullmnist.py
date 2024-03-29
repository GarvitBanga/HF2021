# -*- coding: utf-8 -*-
"""DIClustering1fullMNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1irSN2RT8whk3ZbHr6aF0z_IDsLDKUtXU
"""

import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from tensorflow.keras.preprocessing import sequence
import tensorflow as tfs
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import LSTM

from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint

from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D,LeakyReLU
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2, random
from tensorflow.keras import backend as K

height=28
width=28
depth=1

inputShape = (height, width, depth)
# Prepare the train and test dataset.
from tensorflow import keras
batch_size = 64
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalize data
x_train = x_train.astype("float32") / 255.0
x_train = np.reshape(x_train, (-1, 28, 28, 1))

x_test = x_test.astype("float32") / 255.0
x_test = np.reshape(x_test, (-1, 28, 28, 1))

from sklearn.utils import shuffle
x_train, y_train= shuffle(x_train, y_train, random_state=0)
X=[]
Y=[]
j=0
for i in range(50):
  X.append(x_train[j:j+1200])
  Y.append(y_train[j:j+1200])
  j+=1200

X=np.array(X)
Y=np.array(Y)
print(X.shape,Y.shape)

from tensorflow.keras.layers import BatchNormalization
class MODEL:
    @staticmethod
    def build(nl):
        model = Sequential()
        model.add(Conv2D((128/nl),(3,3),strides=(2, 2), padding="same",input_shape=inputShape) )
        model.add(LeakyReLU(alpha=0.2))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1), padding="same"))
        model.add(Dropout(0.25))


        model.add(Conv2D(256/nl, (3, 3), strides=(2, 2), padding="same") )
        model.add(Flatten())
        model.add(Dense(10))#for output layer
        return model

from sklearn.metrics import accuracy_score
def test_model(X_test, Y_test,  model, comm_round):
    # cce = tf.keras.losses.SparseCategoricalCrossentropy()
    # #logits = model.predict(X_test, batch_size=100)
    # logits = model.predict(X_test)
    # loss = cce(Y_test, logits)
    # acc = accuracy_score(tf.argmax(logits, axis=1), tf.argmax(Y_test, axis=1))
    # print('comm_round: {} | global_acc: {:.3%} | global_loss: {}'.format(comm_round, acc, loss))
    model.compile(  optimizer=keras.optimizers.Adam(),
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)
    loss,acc=model.evaluate(x_test,y_test)
    # acc,loss=model.evaluate(x_test,y_test)
    return acc, loss
def scale_model_weights(weight, scalar):
    '''function for scaling a models weights'''
    weight_final = []
    steps = len(weight)
    for i in range(steps):
        weight_final.append(scalar * weight[i])
    return weight_final

def sum_scaled_weights(scaled_weight_list):
    '''Return the sum of the listed scaled weights. The is equivalent to scaled avg of the weights'''
    avg_grad = list()
    #get the average grad accross all client gradients
    for grad_list_tuple in zip(*scaled_weight_list):
        layer_mean = tf.math.reduce_sum(grad_list_tuple, axis=0)
        avg_grad.append(layer_mean)
      
    return avg_grad
# print(global_model.get_weights())
def test_modelstudent(X_test, Y_test,  gmodel, comm_round):
    gmodel.compile(optimizer=keras.optimizers.Adam(),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
    student_loss_fn=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    distillation_loss_fn=keras.losses.KLDivergence(),
    alpha=0.1,
    temperature=3
  )
    loss,acc=gmodel.evaluate(x_test,y_test)
    # acc,loss=gmodel.evaluate(x_test,y_test)

    return acc, loss

class Distiller(keras.Model):
    def __init__(self, student, teacher):
        super(Distiller, self).__init__()
        self.teacher = teacher
        self.student = student

    def compile(
        self,
        optimizer,
        metrics,
        student_loss_fn,
        distillation_loss_fn,
        alpha=0.1,
        temperature=3,
    ):
        """ Configure the distiller.

        Args:
            optimizer: Keras optimizer for the student weights
            metrics: Keras metrics for evaluation
            student_loss_fn: Loss function of difference between student
                predictions and ground-truth
            distillation_loss_fn: Loss function of difference between soft
                student predictions and soft teacher predictions
            alpha: weight to student_loss_fn and 1-alpha to distillation_loss_fn
            temperature: Temperature for softening probability distributions.
                Larger temperature gives softer distributions.
        """
        super(Distiller, self).compile(optimizer=optimizer, metrics=metrics)
        self.student_loss_fn = student_loss_fn
        self.distillation_loss_fn = distillation_loss_fn
        self.alpha = alpha
        self.temperature = temperature

    def train_step(self, data):
        # Unpack data
        x, y = data

        # Forward pass of teacher
        teacher_predictions = self.teacher(x, training=False)

        with tf.GradientTape() as tape:
            # Forward pass of student
            student_predictions = self.student(x, training=True)

            # Compute losses
            student_loss = self.student_loss_fn(y, student_predictions)
            distillation_loss = self.distillation_loss_fn(
                tf.nn.softmax(teacher_predictions / self.temperature, axis=1),
                tf.nn.softmax(student_predictions / self.temperature, axis=1),
            )
            loss = self.alpha * student_loss + (1 - self.alpha) * distillation_loss

        # Compute gradients
        trainable_vars = self.student.trainable_variables
        gradients = tape.gradient(loss, trainable_vars)

        # Update weights
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))

        # Update the metrics configured in `compile()`.
        self.compiled_metrics.update_state(y, student_predictions)

        # Return a dict of performance
        results = {m.name: m.result() for m in self.metrics}
        results.update(
            {"student_loss": student_loss, "distillation_loss": distillation_loss}
        )
        return results

    def test_step(self, data):
        # Unpack the data
        x, y = data

        # Compute predictions
        y_prediction = self.student(x, training=False)

        # Calculate the loss
        student_loss = self.student_loss_fn(y, y_prediction)

        # Update the metrics.
        self.compiled_metrics.update_state(y, y_prediction)

        # Return a dict of performance
        results = {m.name: m.result() for m in self.metrics}
        results.update({"student_loss": student_loss})
        return results



import numpy as np
import csv

path = 'survey.csv'
with open(path, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    headers = next(reader)
    data = np.array(list(reader)).astype(float)
print(data.shape)
# print(data)
data=data[:50]
data=np.delete(data, 0, 1)
print(data.shape)
data[:, [2, 0]] = data[:, [0, 2]]
print(data)

maxminarr=[]
sz=len(data[0])
for i in range(sz):
  tmp=[np.max(data,axis=0)[i],np.min(data,axis=0)[i]]
  maxminarr.append(tmp)
print(maxminarr)

V=data
normV=[]
for i in range(len(V)):
  tmpar=[]
  for j in range(len(V[i])):
    tmp=(V[i][j]-maxminarr[j][1])/(maxminarr[j][0]-maxminarr[j][1])
    # print(tmp)
    # V[i][j]=tmp
    tmpar.append(tmp)
  # print(tmpar.shape)
  normV.append(tmpar)
    
    

# print(V)
print(normV)

pov=[]
lam=[0.4,0.4,0.2]#[1.0/3,1.0/3,1.0/3]
for i in range(len(normV)):
  tmp=0
  for j in range(len(normV[i])):
    tmp+=lam[j]*normV[i][j]
  pov.append(tmp)
print(pov)

import math
def euclidean_distance(V):
  dist=[]
  for i in range(len(V)):
    tmp=[]
    for j in range(len(V)):
      disc=0
      lambd=[0.4,0.4,0.2]#[1.0/3,1.0/3,1.0/3]
      for ind in range(len(V[i])):
        disc+=math.sqrt(lambd[ind]*(V[i][ind]-V[j][ind])**2)
      tmp.append(disc)
    dist.append(tmp)
  return dist

d=euclidean_distance(normV)

import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
DIAMETER_METHODS = ['mean_cluster', 'farthest']
CLUSTER_DISTANCE_METHODS = ['nearest', 'farthest']


def inter_cluster_distances(labels, distances, method='nearest'):
    """Calculates the distances between the two nearest points of each cluster.
    :param labels: a list containing cluster labels for each of the n elements
    :param distances: an n x n numpy.array containing the pairwise distances between elements
    :param method: `nearest` for the distances between the two nearest points in each cluster, or `farthest`
    """
    if method not in CLUSTER_DISTANCE_METHODS:
        raise ValueError(
            'method must be one of {}'.format(CLUSTER_DISTANCE_METHODS))

    if method == 'nearest':
        return __cluster_distances_by_points(labels, distances)
    elif method == 'farthest':
        return __cluster_distances_by_points(labels, distances, farthest=True)


def __cluster_distances_by_points(labels, distances, farthest=False):
    n_unique_labels = len(np.unique(labels))
    cluster_distances = np.full((n_unique_labels, n_unique_labels),
                                float('inf') if not farthest else 0)

    np.fill_diagonal(cluster_distances, 0)

    for i in np.arange(0, len(labels) - 1):
        for ii in np.arange(i, len(labels)):
            if labels[i] != labels[ii] and (
                (not farthest and
                 distances[i][ii] < cluster_distances[labels[i], labels[ii]])
                    or
                (farthest and
                 distances[i][ii] > cluster_distances[labels[i], labels[ii]])):
                cluster_distances[labels[i], labels[ii]] = cluster_distances[
                    labels[ii], labels[i]] = distances[i][ii]
    return cluster_distances


def diameter(labels, distances, method='farthest'):
    """Calculates cluster diameters
    :param labels: a list containing cluster labels for each of the n elements
    :param distances: an n x n numpy.array containing the pairwise distances between elements
    :param method: either `mean_cluster` for the mean distance between all elements in each cluster, or `farthest` for the distance between the two points furthest from each other
    """
    if method not in DIAMETER_METHODS:
        raise ValueError('method must be one of {}'.format(DIAMETER_METHODS))

    n_clusters = len(np.unique(labels))
    diameters = np.zeros(n_clusters)

    if method == 'mean_cluster':
        for i in range(0, len(labels) - 1):
            for ii in range(i + 1, len(labels)):
                if labels[i] == labels[ii]:
                    diameters[labels[i]] += distances[i][ii]

        for i in range(len(diameters)):
            diameters[i] /= sum(labels == i)

    elif method == 'farthest':
        for i in range(0, len(labels) - 1):
            for ii in range(i + 1, len(labels)):
                if labels[i] == labels[ii] and distances[i][ii] > diameters[
                        labels[i]]:
                    diameters[labels[i]] = distances[i][ii]
    return diameters


def dunn(labels, distances, diameter_method='farthest',
         cdist_method='nearest'):
    """
    Dunn index for cluster validation (larger is better).
    
    .. math:: D = \\min_{i = 1 \\ldots n_c; j = i + 1\ldots n_c} \\left\\lbrace \\frac{d \\left( c_i,c_j \\right)}{\\max_{k = 1 \\ldots n_c} \\left(diam \\left(c_k \\right) \\right)} \\right\\rbrace
    
    where :math:`d(c_i,c_j)` represents the distance between
    clusters :math:`c_i` and :math:`c_j`, and :math:`diam(c_k)` is the diameter of cluster :math:`c_k`.
    Inter-cluster distance can be defined in many ways, such as the distance between cluster centroids or between their closest elements. Cluster diameter can be defined as the mean distance between all elements in the cluster, between all elements to the cluster centroid, or as the distance between the two furthest elements.
    The higher the value of the resulting Dunn index, the better the clustering
    result is considered, since higher values indicate that clusters are
    compact (small :math:`diam(c_k)`) and far apart (large :math:`d \\left( c_i,c_j \\right)`).
    :param labels: a list containing cluster labels for each of the n elements
    :param distances: an n x n numpy.array containing the pairwise distances between elements
    :param diameter_method: see :py:function:`diameter` `method` parameter
    :param cdist_method: see :py:function:`diameter` `method` parameter
    
    .. [Kovacs2005] Kovács, F., Legány, C., & Babos, A. (2005). Cluster validity measurement techniques. 6th International Symposium of Hungarian Researchers on Computational Intelligence.
    """

    labels = LabelEncoder().fit(labels).transform(labels)

    ic_distances = inter_cluster_distances(labels, distances, cdist_method)
    min_distance = min(ic_distances[ic_distances.nonzero()])
    max_diameter = max(diameter(labels, distances, diameter_method))
    # print(min_distance,max_diameter)

    return min_distance / max_diameter



dunnarray=[]
dunnvalues=[]
rng=int(math.sqrt(len(data)))
print(rng)
for ncluster in range(2,rng+1):
      kmeans = KMeans(n_clusters=ncluster)
      # c = data[1]

      k = kmeans.fit_predict(normV)
      # d = euclidean_distances(x)
      print("No of Clusters(K)= ",ncluster)
      # print(k)

      for diameter_method in DIAMETER_METHODS:
          for cdist_method in CLUSTER_DISTANCE_METHODS:
              # dund = dunn(c, d, diameter_method, cdist_method)
              
              if diameter_method=="farthest" and cdist_method=="nearest":
                dunk = dunn(k, d, diameter_method, cdist_method)
                tmp=[ncluster,dunk]
                dunnarray.append(tmp)
                dunnvalues.append(dunk)


                print(diameter_method, cdist_method, dunk)

bestnoofcluster=dunnvalues.index(max(dunnvalues))+2
print(bestnoofcluster)
d=[]
for i in range(len(dunnvalues)):
  d.append([dunnvalues[i],i+2])
print(d)
d.sort()
d.reverse()
print(d)
aa=[b for a,b in d[:3]]
print(aa)
best3kclusters=aa
print(best3kclusters)



# Ef=20
# u=0.7
# L=1.5
# B=1
# Ew=0.08
# beta=max(8*L/u,Ef)
# qf=0.05
# Rf=(1/Ef)*(((L/(2*u*u*qf))*(4*B+u*u*beta*Ew*Ew))+1-beta)
# print(Rf)
# import math
# Rf=math.ceil(Rf)
# print(Rf)

nc=bestnoofcluster

lerr=np.random.uniform(low=0.001, high=0.02, size=(100))
print(lerr)
def herr(jj,C,i):
  sumx=0
  lenx=0
  maxx=0
  minn=10
  # return len(C[jj])
  for ix in range(len(C[jj])):
    sumx+=lerr[C[jj][ix]]
    lenx+=1
    maxx=max(maxx,lerr[C[jj][ix]])
    minn=min(minn,lerr[C[jj][ix]])
  sumx+=lerr[i]
  lenx+=1
  avgerr=sumx/lenx
  tmp=max(abs(maxx-avgerr),abs(avgerr-minn))
  return tmp

# f.write(str(lerr))
# f.write(str(nc))

for nc in best3kclusters:
  print("\n","Number of Clusters=",nc,"\n")
  f = open("MyFileMNIST.txt", "a+") 
  f.write("\n Number of Clusters=%d \n" %nc)
  kmeans = KMeans(n_clusters=nc)
  k = kmeans.fit_predict(normV)
  print("Client with their cluster number",k,"\n")
  f.write("Client with their cluster number %s \n"%k)
  AccomodateM=[0 for i in range(nc)]
  su=0
  lent=0
  for i in range(nc):
    su=0
    lent=0
    for j in range(len(k)):
      if(k[j]==i):
          su+=pov[j]
          lent=lent+1
    AccomodateM[i]=su/lent
  AccomodateM.sort()
  AccomodateM.reverse()  
  print("Cluster value for which it can accomodate any client with value around this",AccomodateM,"\n")
  f.write("Cluster value for which it can accomodate any client with value around this %s \n"%AccomodateM)




  tmp=2

  # Rf=[(tmp*10) for i in range(nc)]
  R=[]
  for i in range(nc):
    R.append(tmp)
    tmp=math.ceil(tmp*1.2)
  E=[]
  tmp=5
  for i in range(nc):
    E.append(tmp)
    tmp=math.ceil(tmp*1.2)
  
  print("Global Comm Rounds",R)
  f.write("Global Comm Rounds %s \n"%R)
  print("Local Epochs",E,"\n")
  f.write("Local Epochs %s \n"%E)





  qo=[]
  tmp=0.05
  for i in range(nc):
    qo.append(tmp)
    tmp=round(tmp*1.2,2)

  delta=[]
  tmp=0.1
  for i in range(nc):
    delta.append(tmp)
    tmp=round(tmp*1.2,2)
  print(qo)
  print(delta)
  f.write("Qo %s \n" %qo)
  f.write("Delta %s \n" %delta)
  err=[]
  tmp=0.1
  for i in range(nc):
    err.append(tmp)
    tmp=round(tmp*1.2,2)
  print(err)
  theta=[]
  tmp=0.11
  for i in range(nc):
    theta.append(tmp)
    tmp=round(tmp*1.2,2)
  print(theta,"\n")
  f.write("Theta %s \n" %theta)


  C=[[] for i in range(nc)]
  accmthreshold=0.1
  for i in range((len(data))):
    flag=0
    for j in range(len(C)):
      if(flag==1):
        continue
      if len(C[j])==0:
        if(abs(pov[i]-AccomodateM[j])<=accmthreshold or (pov[i]-AccomodateM[j]>0)):
          #calculate qof
          if(qo[j]<=delta[j]):
            C[j].append(i)
            flag=1
        else:
          dwkcwdkkc=0
          #reduce ti and ni s.t. pi run Mf
      else:

        if(abs(pov[i]-AccomodateM[j])<=accmthreshold or (pov[i]-AccomodateM[j]>0)):
          #calculate qof
          tmp=herr(j,C,i)
          #  print('i',i,'j',j,tmp)
          if(qo[j]<=delta[j] and tmp<=theta[j]):
            err[j]=tmp
            C[j].append(i)
            flag=1
          else:
            print('i',i,'j',j,tmp,'theta',theta[j])

        else:
          dwkcwdkkc=0
          #reduce ti and ni s.t. pi run Mf
      if(flag==0 and j== len(C)-1):
        C[j].append(i)
      
  for tmx in range(nc):
    C[tmx]=np.array(C[tmx])
  print("Clustering Array",np.array(C,dtype=object))
  f.write("Clustering Array %s \n" %(np.array(C,dtype=object)))
  print("ERRf of each cluster",err,"\n")
  f.write("ERRf of each cluster %s \n"%err)


  #Model Training
  print("Model Training","\n")
  f.write("Model Training\n")
  flag=1
  for empclstr in range(nc):
    if(len(C[empclstr])==0):
      flag=0
      f.write("Cluster no. %d is empty" %empclstr)
      break
  f.close()
  if(flag==1):
    for clstr in range(nc):
      f = open("MyFileMNIST.txt", "a+") 
      print("CLUSTER NO.",clstr,"\n")
      f.write("CLUSTER NO.%f \n" %clstr)
      if(clstr==0):
        global1= MODEL()
        global_model = global1.build(2**clstr)
        for comm_round in range(R[clstr]):
          global_weights = global_model.get_weights()
          scaled_local_weight_list = list()
          index=list({0,1,2,3,4})
          #random.shuffle(index)
          print(index)
          for clnt in range(len(C[clstr])):
            print("CLIENT NO: ",C[clstr][clnt])

            local = MODEL()
            local_model=local.build(1)
            
            local_model.compile(optimizer=keras.optimizers.Adam(),
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=[keras.metrics.SparseCategoricalAccuracy()],
        )
            local_model.set_weights(global_weights)
            #trainy[ind]=np.array(trainy[ind]).reshape(-1,1)
            history=local_model.fit(X[C[clstr][clnt]],Y[C[clstr][clnt]], epochs=E[clstr])#,validation_data=(x_test,y_test))
            # print("Accuracy: ",history.history["accuracy"][4])
            # local_model.evaluate(x_test, y_test)
            scaling_factor=1.0/len(C[clstr]) #1/no.ofclients
            scaled_weights = scale_model_weights(local_model.get_weights(), scaling_factor)
            scaled_local_weight_list.append(scaled_weights)
            K.clear_session()
          average_weights = sum_scaled_weights(scaled_local_weight_list)
          #global_model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
          global_model.set_weights(average_weights)
          #val_acc,val_loss=global_model.evaluate(x_train,y_train)
          #print(val_loss,val_acc)
          global_acc, global_loss = test_model(x_test,y_test, global_model, comm_round)
          print("COMM_ROUNND",comm_round," GLOBAL MASTER MODEL ACCURACY",global_acc,global_loss)
          f.write("Communication Round: %f GLOBAL MASTER MODEL ACCURACY: %f LOSS: %f \n" %(comm_round ,global_acc ,global_loss))
      else:
        studentm=MODEL.build(2**clstr)
        student_model=Distiller(student=studentm, teacher=global_model)
        for comm_round in range(R[clstr]):
          global_weights = student_model.get_weights()
          scaled_local_weight_list = list()
          index=list({0,1,2,3,4})
          #random.shuffle(index)
          print(index)
          for clnt in range(len(C[clstr])):
            print("CLIENT NO: ",C[clstr][clnt])
            local_model1 = Distiller(student=studentm, teacher=global_model)
            
            local_model1.compile(optimizer=keras.optimizers.Adam(),
            metrics=[keras.metrics.SparseCategoricalAccuracy()],
            student_loss_fn=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            distillation_loss_fn=keras.losses.KLDivergence(),
            alpha=0.1,
            temperature=3
            )

            local_model1.set_weights(global_weights)
            #trainy[ind]=np.array(trainy[ind]).reshape(-1,1)
            history=local_model1.fit(X[C[clstr][clnt]],Y[C[clstr][clnt]], epochs=E[clstr])#,validation_data=(x_test,y_test))
            # print("Accuracy: ",history.history["accuracy"][4])
            # local_model.evaluate(x_test, y_test)
            scaling_factor=1.0/len(C[clstr]) #1/no.ofclients
            scaled_weights = scale_model_weights(local_model1.get_weights(), scaling_factor)
            scaled_local_weight_list.append(scaled_weights)
            K.clear_session()
          average_weights = sum_scaled_weights(scaled_local_weight_list)
          #global_model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
          student_model.set_weights(average_weights)
          #val_acc,val_loss=global_model.evaluate(x_train,y_train)
          #print(val_loss,val_acc)
          global_loss1, global_acc1 = test_modelstudent(x_test,y_test, student_model, comm_round)
          print("COMM_ROUNND",comm_round,"GLOBAL SLAVE MODEL ACCURACY",global_acc1,global_loss1)
          f.write("Communication Round: %f GLOBAL SLAVE MODEL ACCURACY: %f LOSS:%f \n" %(comm_round,global_acc1 ,global_loss1))
      f.close()

(print(len(C))











print(pov)
print(AccomodateM)

for j in range(len(k)):
  if(k[j]==3):
    print(pov[j])





# print(herr(1,C))



print(C[4])

print(AccomodateM[4])

print(pov)



