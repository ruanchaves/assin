import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json
import pathlib 

class SubmissionWriter(object):

    def __init__(self, source=None, target=None, target_filename='submission.xml', entailment_preds=None, similarity_preds=None, entailment_data=None, similarity_data=None):
        self.source = ET.parse(source)
        self.target = target + '/' + target_filename

        if similarity_preds:
            self.similarity_preds = np.load(similarity_preds)
        else:
            self.similarity_preds = None

        if entailment_preds:    
            self.entailment_preds = np.load(entailment_preds)
        else:
            self.entailment_preds = None

        if entailment_data:
            self.entailment_data = pd.read_csv(entailment_data, sep='\t')
        else:
            self.entailment_data = None

        if similarity_data:
            self.similarity_data = pd.read_csv(similarity_data, sep='\t')
        else:
            self.similarity_data = None

        self.result = None


    def get_score(self, data, preds, test, hypothesis):

        assert(data.shape[0] == len(preds) )

        test_string = test
        hypothesis_string = hypothesis
            
        idx = data.index[ (data['sentence1'].str.contains(test_string, regex=False)) & (data['sentence2'].str.contains(hypothesis_string, regex=False)) ].tolist()
        idx2 = data.index[ (data['sentence1'].str.contains(hypothesis_string, regex=False)) & (data['sentence2'].str.contains(test_string, regex=False)) ].tolist()
        if len(idx) == 0 and len(idx2) == 0:
            raise Exception('Sentence not found.')
        if len(idx) >= 1:
            return preds[idx[0]]
        elif len(idx2) >= 1:
            return preds[idx2[0]]


    def convert(self):
        entailment_dict = {
            -1: 'Unknown',
            0: 'None',
            1: 'Entailment',
            2: 'Paraphrase'
        }
        root = self.source.getroot()
        for pair in root.iter('pair'):
            test = pair.find('t').text
            hypothesis = pair.find('h').text
            entailment_score = self.get_score(self.entailment_data, self.entailment_preds, test, hypothesis)
            similarity_score = self.get_score(self.similarity_data, self.similarity_preds, test, hypothesis)
            pair.set('entailment', entailment_dict[round(entailment_score)])
            pair.set('similarity', str(similarity_score))
        self.result = root 
        return self
    
    def save(self):
        self.source.write(self.target)
        return self

def assin_json_writer(data):
    for record in data:
        directory = record['target']
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True) 
        SubmissionWriter(**record).convert().save()

if __name__ == '__main__':
    pass