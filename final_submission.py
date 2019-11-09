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
        raise ValueError('not found')

def convert(source=None, 
            target=None, 
            entailment_array=None, 
            similarity_array=None,
            df_source='/run/media/user/DADOS/competition/assin_roberta/datasets/pt/assin2/similarity/subset/dev.tsv'):
    
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

if __name__ == '__main__':
    convert(
        source="/run/media/user/DADOS/competition/assin2-blind-test.xml",
        target="/run/media/user/DADOS/competition/submission-ensemble-5fold-corrected.xml",
        entailment_array="/run/media/user/DADOS/competition/assin_roberta/results/ensemble/assin2/entailment/subset/model_preds.npy",
        similarity_array="/run/media/user/DADOS/competition/assin_roberta/results/ensemble/assin2/similarity/subset/model_preds.npy"
    )
    convert(
        source="/run/media/user/DADOS/competition/assin2-blind-test.xml",
        target="/run/media/user/DADOS/competition/submission-bert-corrected.xml",
        entailment_array="/run/media/user/DADOS/competition/assin_roberta/results/pt/assin2/entailment/subset/original/model_preds.npy",
        similarity_array="/run/media/user/DADOS/competition/assin_roberta/results/pt/assin2/similarity/subset/original/model_preds.npy"
    )

    convert(
        source="/run/media/user/DADOS/competition/assin2-blind-test.xml",
        target="/run/media/user/DADOS/competition/submission-roberta-corrected.xml",
        entailment_array="/run/media/user/DADOS/competition/assin_roberta/results/en/assin2/entailment/subset/original/model_preds.npy",
        similarity_array="/run/media/user/DADOS/competition/assin_roberta/results/en/assin2/similarity/subset/original/model_preds.npy"
    )