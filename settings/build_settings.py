import yaml
import json
import copy

def try_set(fallback, params, key):
    try:
        return params[key]
    except:
        return fallback

def get_path_list(task_name):
    if task_name == 'assin2':
        return [
            "assin2-train.xml",
            "assin2-blind-test.xml"
        ]
    elif task_name == 'assin1-ptbr':
        return [
            "assin-ptbr-train.xml",
            "assin-ptbr-blind-test.xml"
        ]
    elif task_name == 'assin1-ptpt':
        return [
            "assin-ptpt-train.xml",
            "assin-ptpt-blind-test.xml"
        ]
    
path_list_dict = {
    "assin2": [
            "assin2-train.xml",
            "assin2-blind-test.xml"
        ],
    "assin1-ptbr": [
            "assin-ptbr-train.xml",
            "assin-ptbr-blind-test.xml"
        ],
    "assin1-ptpt": [
            "assin-ptpt-train.xml",
            "assin-ptpt-blind-test.xml"        
    ]
}

def conv_template(lang, dataset, task, buckets):
    template = {
            "path": list(map(lambda x: "./sources/" + x, path_list_dict[dataset])),
            "measure": task,
            "split": 0.6,
            "balance": [
                "train",
                "df"
            ],
            "metadata": {
                "genre": "main_captions",
                "filename": "MSRvid",
                "year": "2019",
                "source1": "none",
                "source2": "none"
            },
            "save": [
                {
                    "target": "df",
                    "directory": "./datasets/{0}/{1}/{2}/whole".format(lang, dataset, task),
                    "fname": "train.tsv"
                },
                {
                    "target": "train",
                    "directory": "./datasets/{0}/{1}/{2}/subset".format(lang, dataset, task),
                    "fname": "train.tsv"
                },
                {
                    "target": "test",
                    "directory": "./datasets/{0}/{1}/{2}/subset".format(lang, dataset, task),
                    "fname": "dev.tsv"
                }
            ],
            "kfold": [
                {
                    "target": "train",
                    "directory": "./datasets/{0}/{1}/{2}/subset".format(lang, dataset, task),
                    "fname": "train.tsv",
                    "buckets": buckets
                }
            ]
        }
    if lang == 'en':
        template["translate"] = True
        template["dictionary_file"] = "./sources/dictionary.json"
    elif lang == 'pt':
        template["translate"] = False
    return template

def train_template(lang, dataset, task, dictionary):
    model = copy.deepcopy(dictionary)
    model['data_dir'] = "=./datasets/{0}/{1}/{2}/subset".format(lang, dataset, task)
    model['output_dir'] = "=./models/{0}/{1}/{2}/subset".format(lang, dataset, task)
    model['task_name'] = "=sts-b"
    model['save_file'] = " ./results/{0}/{1}/{2}/subset/model".format(lang, dataset, task)
    if params['evaluate_ensemble']:
        model['kfold'] = True
    else:
        model['kfold'] = False
    model['kfold_buckets'] = params['ensemble_folds']
    return model

params = ''
with open("config.yml", 'r') as stream:
    try:
        params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

settings = {}

settings['workers'] = 1
settings['conv'] = []
settings['train'] = []
settings['ensemble'] = []
settings['submission'] = []

settings['workers'] = try_set(settings['workers'], params, 'workers')

if params['evaluate_english_model']:
    settings['conv'].append(conv_template('en', params['dataset'], 'similarity', params['ensemble_folds']))
    settings['conv'].append(conv_template('en', params['dataset'], 'entailment', params['ensemble_folds']))
if params['evaluate_portuguese_model']:
    settings['conv'].append(conv_template('pt', params['dataset'], 'similarity', params['ensemble_folds']))
    settings['conv'].append(conv_template('pt', params['dataset'], 'entailment', params['ensemble_folds']))

model = params['english_model']

if params['evaluate_english_model']:
    settings['train'].append(train_template('en', params['dataset'], 'similarity', model))
    settings['train'].append(train_template('en', params['dataset'], 'entailment', model))

model = params['portuguese_model']

if params['evaluate_portuguese_model']:
    settings['train'].append(train_template('pt', params['dataset'], 'similarity', model))
    settings['train'].append(train_template('pt', params['dataset'], 'entailment', model))

settings['ensemble'] = [
        {
            "dir_bert": "./results/pt/assin2/similarity/subset",
            "dir_roberta": "./results/en/assin2/similarity/subset",
            "save_path": "./results/ensemble/assin2/similarity/subset"
        },
        {
            "dir_bert": "./results/pt/assin2/entailment/subset",
            "dir_roberta": "./results/en/assin2/entailment/subset",
            "save_path": "./results/ensemble/assin2/entailment/subset"
        }
    ]

settings['submission'] = [
        {
            "source": "./sources/assin2-blind-test.xml",
            "target": "./submission/assin2",
            "target_filename": "submission.xml",
            "entailment_preds": "./results/ensemble/assin2/entailment/subset/model_preds.npy",
            "similarity_preds": "./results/ensemble/assin2/similarity/subset/model_preds.npy",
            "entailment_data": "./datasets/pt/assin2/entailment/subset/dev.tsv",
            "similarity_data": "./datasets/pt/assin2/similarity/subset/dev.tsv"
        }
    ]

with open('settings.json', 'w+') as f:
    json.dump(settings, f)