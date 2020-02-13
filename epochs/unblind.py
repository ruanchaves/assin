import pandas as pd
import json
import xml.etree.ElementTree as ET

def unblind_dev_file(xml_file=None, tsv_file=None, save_path=None, dictionary_file=None, lang=None):
    with open(dictionary_file, 'r') as f:
        dictionary = json.load(f)

    tree = ET.parse(xml_file)
    root = tree.getroot()
    entry_list = []
    for pair in root.iter('pair'):
        if lang == 'pt':
            entry = {
                "t": pair.find('t').text,
                "h": pair.find('h').text,
                "true_score": float(pair.get('similarity'))
            }
        elif lang == 'en':
            entry = {
                "t": dictionary[pair.find('t').text],
                "h": dictionary[pair.find('h').text],
                "true_score": float(pair.get('similarity'))
            }            
        entry_list.append(entry)

    print(entry_list[30])
    xml_df = pd.DataFrame(entry_list)
    tsv_df = pd.read_csv(tsv_file, sep='\t')

    df = pd.merge(left=tsv_df,
            right=xml_df,
            how='left',
            left_on=['sentence1', 'sentence2'],
            right_on=['t', 'h'])

    df = df[['index', 'genre', 'filename', 'year', 'old_index', 'source1', 'source2', 'sentence1', 'sentence2', 'true_score']]

    df = df.rename(columns={'true_score' : 'score'})

    df.to_csv(save_path, sep='\t', index=False)

if __name__ == '__main__':
    settings = [
        {
            "xml_file": '../sources/assin2-test.xml',
            "tsv_file": "./pt/dev_blind.tsv",
            "save_path": './pt/dev.tsv',
            "dictionary_file": '../sources/dictionary.json',
            "lang": "pt"
        }, 
        {
            "xml_file": '../sources/assin2-test.xml',
            "tsv_file": "./en/dev_blind.tsv",
            "save_path": './en/dev.tsv',
            "dictionary_file": '../sources/dictionary.json',
            "lang": "en"
        }
    ]
    for item in settings:
        unblind_dev_file(**item)