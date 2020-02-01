import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json
import sys
import os

dataset = os.environ['DATASET']

def get_data(s1=None, s2=None, arr=None, query=[]):
    s3 = []
    for idx, item in enumerate(s1):
        tup = [ s1[idx], s2[idx] ]
        s3.append(tup)
    for idx, item in enumerate(s3):
        i1 = item[0]
        i2 = item[1]
        q1 = query[0]
        q2 = query[1]
        if i1 == q1 and i2 == q2:
            return arr[idx]
        elif i1 == q2 and i2 == q1:
            return arr[idx]
    else:
        raise ValueError('not found')

def convert(source=None, 
            target=None, 
            entailment_array=None, 
            similarity_array=None,
            df_source='./datasets/pt/{0}/similarity/subset/dev.tsv'.format(dataset)):
    
    entailment_dict = {
        0: 'None',
        1: 'Entailment'
    }

    entailment_data = list(np.load(entailment_array))
    similarity_data = list(np.load(similarity_array))
    xml_source = ET.parse(source)
    root = xml_source.getroot()

    s1 = pd.read_csv(df_source, sep='\t')['sentence1'].values.tolist()
    s2 = pd.read_csv(df_source, sep='\t')['sentence2'].values.tolist()
    for pair in root.iter('pair'):
        test = pair.find('t').text
        hypothesis = pair.find('h').text

        entailment_score = get_data(s1=s1, 
                                    s2=s2, 
                                    arr=entailment_data, 
                                    query=[test,hypothesis])

        similarity_score = get_data(s1=s1, 
                                    s2=s2, 
                                    arr=similarity_data, 
                                    query=[test,hypothesis])

        pair.set('entailment', entailment_dict[round(entailment_score)])
        pair.set('similarity', str(similarity_score))
    xml_source.write(target)

def average(left, right, target):
    entailment_dict = {
        0: 'None',
        1: 'Entailment'
    }
    reverse_entailment_dict = {
        'None': 0,
        'Entailment': 1
    }

    xml_source = ET.parse(left)
    root = xml_source.getroot()
    
    similarity = []
    entailment = []
    for pair in root.iter('pair'):
        entailment.append([float(reverse_entailment_dict[pair.get('entailment')])])
        similarity.append([float(pair.get('similarity'))])
    
    xml_source = ET.parse(right)
    root = xml_source.getroot()
    for idx,pair in enumerate(root.iter('pair')):
        entailment[idx].append(float(reverse_entailment_dict[pair.get('entailment')]))
        similarity[idx].append([float(pair.get('similarity'))])

    for idx,item in entailment:
        value = int(np.mean(item))
        entailment[idx] = entailment_dict[value]

    for idx,item in similarity:
        similarity[idx] = str(np.mean(item))

    xml_source = ET.parse(left)
    root = xml_source.getroot()

    for idx,pair in enumerate(root.iter('pair')):
        entailment_score = entailment[idx]
        similarity_score = similarity[idx]
        pair.set('entailment', entailment_score)
        pair.set('similarity', similarity_score)
    xml_source.write(target)

if __name__ == '__main__':
    convert(
        source="./sources/{0}-blind-test.xml".format(dataset),
        target="./submission/submission-ensemble.xml",
        entailment_array="./results/ensemble/{0}/entailment/subset/model_preds.npy".format(dataset),
        similarity_array="./results/ensemble/{0}/similarity/subset/model_preds.npy".format(dataset)
    )
    convert(
        source="./sources/{0}-blind-test.xml".format(dataset),
        target="./submission/submission-portuguese.xml",
        entailment_array="./results/pt/{0}/entailment/subset/original/model_preds.npy".format(dataset),
        similarity_array="./results/pt/{0}/similarity/subset/original/model_preds.npy".format(dataset)
    )

    convert(
        source="./sources/{0}-blind-test.xml".format(dataset),
        target="./submission/submission-english.xml",
        entailment_array="./results/en/{0}/entailment/subset/original/model_preds.npy".format(dataset),
        similarity_array="./results/en/{0}/similarity/subset/original/model_preds.npy".format(dataset)
    )

    average(
        left="./submission/submission-english.xml",
        right="./submission/submission-portuguese.xml",
        target="./submission/submission-average.xml"
    )