import xml.etree.ElementTree as ET
import pandas as pd
import pathlib
import subprocess
import shutil
import datetime

def generate_report(lst):
    for data_idx, data in enumerate(lst):
        test_results = subprocess.run(['python','assin-eval.py', data['gold'], data['submission'] ], stdout=subprocess.PIPE).stdout.decode('utf-8')
        directory = data['report_path']
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        test_results_file = directory + '/' + 'test_results.txt'
        with open(test_results_file, 'w+') as f:
            print(test_results, file=f)
        
        info = [
            {
            "name": "submission",
            "path": data['submission']
        },
            {
            "name": "gold",
            "path": data['gold']
            }]
        df_list = []
        for xml in info:
            tree = ET.parse(xml['path'])
            root = tree.getroot()
            tmp_df = []
            for pair in root.iter('pair'):
                if pair.get('id').endswith('-rev'):
                    continue
                sentence1 = pair.find('t').text
                sentence2 = pair.find('h').text

                row = {
                    "idx": pair.get('id'),
                    "sentence1": sentence1,
                    "sentence2": sentence2,
                    "entailment_{0}".format(xml['name']) : pair.get('entailment'),
                    "similarity_{0}".format(xml['name']) : pair.get('similarity')
                }
                tmp_df.append(row)
            tmp_df = pd.DataFrame(tmp_df)
            df_list.append(tmp_df)
        output_df = df_list[0].merge(df_list[1], how='inner', on=['idx','sentence1', 'sentence2'])
        output_df["error"] = output_df["similarity_submission"].astype(float) - output_df["similarity_gold"].astype(float)
        output_df = output_df.sort_values(by='error')

        target_file = data['report_path'] + '/' + data['report_filename']

        output_df[[
            "idx",
            "sentence1",
            "sentence2",
            "entailment_gold",
            "entailment_submission",
            "similarity_gold",
            "similarity_submission",
            "error"
        ]].to_csv(target_file, sep='\t', index=False)

        output_filename = 'report_' + str(data_idx) + '_' + str(datetime.datetime.now()).replace(' ','_').replace('-','_').replace(':','_').replace('.','_')
        directory = data['report_path']
        shutil.make_archive(output_filename, 'zip', directory)
        yield [ test_results, './' + output_filename + '.zip' ]