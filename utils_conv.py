import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import sys
import pathlib
import argparse
import json

class AssinReader(object):

    def __init__(self, path, measure='similarity', dictionary_file=None, translate=False):
        assert(measure in ['similarity', 'entailment'])
        self.path = path
        self.df = []
        self.train = None
        self.test = None
        self.measure = measure
        self.dictionary_file = dictionary_file
        self.translate = translate

    def sort_columns(self, df):
        return df[['index', 
            'genre', 
            'filename', 
            'year',
            'old_index',
            'source1',
            'source2',
            'sentence1',
            'sentence2',
            'score']]

    def convert(self, genre="main_captions", filename="MSRvid", year="2019", source1='none', source2='none'):
        entailment_dict = {
            "Unknown": -1,
            "None": 0,
            "Entailment": 1,
            "Paraphrase": 2
        }
        if self.translate:
            with open(self.dictionary_file, 'r') as f:
                dictionary = json.load(f)
        idx = 0
        for xml_file in self.path:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for pair in root.iter('pair'):
                if pair.get('id').endswith('-rev'):
                    continue
                if self.translate:
                    sentence1 = dictionary[pair.find('t').text]
                    sentence2 = dictionary[pair.find('h').text]
                else:
                    sentence1 = pair.find('t').text
                    sentence2 = pair.find('h').text

                original_sentence1 = pair.find('t').text
                original_sentence2 = pair.find('h').text

                row = { "index": idx,
                    "genre": genre,
                    "filename": filename,
                    "year": year,
                    "old_index": idx + 1,
                    "source1": source1,
                    "source2": source2,
                    "sentence1": sentence1,
                    "sentence2": sentence2,
                    "original_sentence1": original_sentence1,
                    "original_sentence2": original_sentence2,
                    "score": pair.get(self.measure)
                    }        
                self.df.append(row)
                idx += 1
        self.df = pd.DataFrame.from_dict(self.df, orient='columns')

        if self.measure == 'entailment':
            self.df['score'] = self.df['score'].apply(lambda x: entailment_dict[x])
        elif self.measure == 'similarity':
            self.df['score'] = self.df['score'].apply(lambda x: float(x))

        self.df = self.df.drop_duplicates(subset=['original_sentence1', 'original_sentence2'])
        self.df = self.df.drop(columns=['original_sentence1', 'original_sentence2'])
        self.df = self.sort_columns(self.df)
        return self

    def split_df(self, train_size=0.6, random_state=42):
        self.train = self.df[self.df['score'] >= 0]
        self.test = self.df[self.df['score'] < 0]
        return self

    def balance(self, target='train'):
        assert( type(getattr(self,target)) != type(None) )
        if self.measure == 'similarity':
            bins = list(zip(np.arange(0,6), np.arange(1,7)))
        elif self.measure == 'entailment':
            bins = list(zip(np.arange(0,3), np.arange(1,4)))
        parts = [ getattr(self, target)[(getattr(self, target)['score'] >= x[0]) & (getattr(self, target)['score'] < x[1])].to_dict('records') for x in bins]
        new_df = []
        while any(parts):
            for item in parts:
                try:
                    row = item.pop()
                    new_df.append(row)
                except:
                    continue
        new_df = self.sort_columns(pd.DataFrame.from_dict(new_df, orient='columns')) 
        setattr(self, target, new_df)
        return self

    def save(self, target='df', directory='./', fname='df.tsv'):
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 
        self.sort_columns(getattr(self, target)).to_csv(directory + '/' + fname, sep='\t', index=False)

    def kfold(self, target='df', directory='./', fname='df.tsv', buckets=10):
        bucket_shape = ( getattr(self, target).shape[0] // buckets ) + 1
        df_list = [ getattr(self,target)[i:i+bucket_shape] for i in range(0, getattr(self, target).shape[0], bucket_shape) ]
        for item in kfold_iterator(len(df_list)):
            dev_idx = item[0]
            train_idx = item[1:]
            save_dir = directory + '/' + str(dev_idx)
            pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
            self.sort_columns(df_list[dev_idx]).to_csv(save_dir + '/' + 'dev.tsv', sep='\t', index=False)
            train_df = pd.concat([ df_list[i] for i in train_idx ])
            self.sort_columns(train_df).to_csv(save_dir + '/' + 'train.tsv', sep='\t', index=False)

def kfold_iterator(num_range):
    range_list = list(range(num_range))
    len_range_list = len(range_list)
    iterations = 0
    while iterations < len_range_list:
        yield range_list
        range_list = range_list[1:] + [range_list[0]]
        iterations += 1

def assin_json_reader(data):
    for record in data:
        if record['translate']:
            reader = AssinReader(record['path'], measure=record['measure'], translate=record['translate'], dictionary_file=record['dictionary_file'])
        else:
            reader = AssinReader(record['path'], measure=record['measure'])
        reader.convert(**record['metadata'])\
                .split_df(train_size=record['split'])
        try:
            record['balance']
            for item in record['balance']:
                reader.balance(item)
        except:
            pass
        try:
            record['save']
            for item in record['save']:
                reader.save(**item)
        except:
            pass
        try:
            record['kfold']
            for item in record['kfold']:
                reader.kfold(**item)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    pass