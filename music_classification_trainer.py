
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn.model_selection import train_test_split
import  pandas as pd
import pickle

#Libraries to create the Multi-class Neural Network
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier

#Import tensorflow
import tensorflow as tf

#Library to evaluate the model
from sklearn.model_selection import cross_val_score, KFold

#load songs data
df = pd.read_csv("data_base/data/training_data/data_moods.csv")

#Define the features and the target
col_features = df.columns[6:-3]
X = df[col_features]
Y = df['mood']
#Normalize the features
# print(X.head(30))
scaler = MinMaxScaler()
scaler.fit(X)
pickle.dump(scaler,open('scaler.pkl','wb'))
#print(X.head(30))
X=scaler.transform(X)
#print(X[0:30])

#Encode the labels (targets)
encoder = LabelEncoder()
encoder.fit(Y)
encoded_y = encoder.transform(Y)
# print(encoded_y)

#Split train and test data with a test size of 20%
X_train,X_test,Y_train,Y_test = train_test_split(X,encoded_y,test_size=0.2,random_state=15)

#disable the v2 behavior and eager mode
tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()

#Function that creates the structure of the Neural Network
def base_model():
    #Create the model
    model = Sequential()
    #Add 1 layer with 8 nodes,input of 4 dim with relu function
    model.add(Dense(8,input_dim=10,activation='relu'))
    #Add 1 layer with output 3 and softmax function
    model.add(Dense(4,activation='softmax'))
    #Compile the model using logistic loss function and adam     optimizer, accuracy correspond to the metric displayed
    model.compile(loss='categorical_crossentropy',optimizer='adam',
              metrics=['accuracy'])
    return model

#Configure the estimator with 300 epochs and 200 batchs. the build_fn takes the function defined above.
# model = keras.models.load_model()

estimator = KerasClassifier(build_fn=base_model,epochs=300,
                            batch_size=200)
#estimator.predict_proba()


#Evaluate the model using KFold cross validation
kfold = KFold(n_splits=10,shuffle=True)
results = cross_val_score(estimator,X,encoded_y,cv=kfold)
#print("%.2f%% (%.2f%%)" % (results.mean()*100,results.std()*100))

#Train the model with the train data
estimator.fit(X_train,Y_train)
#Predict the model with the test data
y_preds = estimator.predict(X_test)

estimator.model.save("data_base/data/trained_models/music_clisifier_model")

# lll = estimator.predict_proba(X_test)
# lll = [[round(i,4) for i in l] for l in lll]
# print(lll)
# Pipeline()