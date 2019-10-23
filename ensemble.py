import numpy as np
import sys
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split
import json
import pathlib
import os


class Ensemble(object):

    def __init__(self, train_left=None, train_right=None, train_target=None, test_left=None, test_right=None):
        self.train_left = train_left
        self.train_right = train_right
        self.train_target = train_target
        self.test_left = test_left
        self.test_right = test_right
        self.model = None
        self.prediction = None

    def train(self):
        self.model = Sequential()
        self.model.add(Dense(64, input_dim=2,  activation='relu'))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dense(1, activation='linear'))
        self.model.compile(loss='mean_absolute_error',
                           optimizer='adam', metrics=['mean_squared_error'])

        input_values = np.array([ np.array(x).flatten() for x in list(zip(self.train_left, self.train_right)) ])
        self.model.fit(input_values, self.train_target,
                       nb_epoch=20, batch_size=8)
        return self


    def predict(self):
        input_values = np.array([ np.array(x).flatten() for x in list(zip(self.test_left, self.test_right)) ])
        self.prediction = self.model.predict(input_values).flatten()
        return self

    def save(self, directory):
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        save_file_name = directory + '/' + 'model_preds.npy'
        np.save(save_file_name, self.prediction)
        return self


def sorted_walk(path):
    for root, dirs, files in os.walk(path):
        dirs.sort()
        for dirname in dirs:
            yield {
                "dirname": dirname,
                "root": root,
                "path": os.path.join(root, dirname)
            }

def read_array(params, models=['bert', 'roberta']):
    kfold = []
    original = []
    for model in models:
        model_dir = 'dir_' + model
        preds = []
        labels = []
        for item in sorted_walk(params[model_dir]):
            preds_path = item['path'] + '/' + 'model_preds.npy'
            labels_path = item['path'] + '/' + 'model_out_label_ids.npy'
            tmp_preds = np.load(preds_path)
            tmp_labels = np.load(labels_path)
            if not item['dirname'].endswith('original'):
                preds = np.concatenate([preds, tmp_preds])
                labels = np.concatenate([labels, tmp_labels])
            else:
                original.append({
                    "preds": tmp_preds,
                    "labels": tmp_labels
                })
        kfold.append({
            "preds": preds,
            "labels": labels
        })
    return original, kfold

def load_ensemble(data):
    for params in data:
        original, kfold = read_array(params)
        ensemble = Ensemble(train_left=kfold[0]['preds'], \
            train_right=kfold[1]['preds'], 
            train_target=kfold[1]['labels'], 
            test_left=original[0]['preds'], 
            test_right=original[1]['preds'])
        ensemble.train().predict().save(params['save_path'])


if __name__ == '__main__':
    pass