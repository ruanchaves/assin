import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import json
import sys

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
        print(query)
        raise ValueError('not found')

def convert(source=None, 
            target=None, 
            entailment_array=None, 
            similarity_array=None,
            df_source=None,
            convert_labels=True):
    
    entailment_dict = {
        0: 'None',
        1: 'Entailment',
        2: 'Paraphrase'
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

        if convert_labels == True:
            pair.set('entailment', entailment_dict[round(entailment_score)])
        else:
            pair.set('entailment', str(entailment_score) )
        pair.set('similarity', str(similarity_score))
    xml_source.write(target)

def submission_average(source1=None, source2=None, target=None):
    entailment_dict = {
        0: 'None',
        1: 'Entailment',
        2: 'Paraphrase'
    }
    s1_source = ET.parse(source1)
    s2_source = ET.parse(source2)
    s1_root = s1_source.getroot()
    s2_root = s2_source.getroot()
    s1_similarity = []
    s2_similarity = []
    s1_entailment = []
    s2_entailment = []
    for pair in s1_root.iter('pair'):
        s1_similarity.append(float(pair.get('similarity')))
        s1_entailment.append(float(pair.get('entailment')))
    for pair in s2_root.iter('pair'):
        s2_similarity.append(float(pair.get('similarity')))
        s2_entailment.append(float(pair.get('entailment')))
    final_similarity = np.array(s1_similarity) + np.array(s2_similarity)
    final_similarity = final_similarity / 2.0
    final_entailment = np.array(s1_entailment) + np.array(s2_entailment)
    final_entailment = final_entailment / 2.0
    for idx, pair in enumerate(s1_root.iter('pair')):
        entailment_score = final_entailment[idx]
        similarity_score = final_similarity[idx]
        pair.set('entailment', entailment_dict[round(entailment_score)])
        pair.set('similarity', str(similarity_score))
    s1_source.write(target)


def generate_submissions(batch_convert_lst, submission_average_lst):
    for item in batch_convert_lst:
        convert(
            source=item['source'],
            target=item['target'],
            entailment_array=item['entailment_array'],
            similarity_array=item['similarity_array'],
            df_source=item['df_source'],
            convert_labels=item['convert_labels']
        )
    for item in submission_average_lst:
        submission_average(
            source1=item['source1'],
            source2=item['source2'],
            target=item['target']
        )

if __name__ == '__main__':
    pass