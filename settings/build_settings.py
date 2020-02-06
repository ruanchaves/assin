import yaml
import json
import copy
import os

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
    elif task_name == 'assin-ptbr':
        return [
            "assin-ptbr-train.xml",
            "assin-ptbr-blind-test.xml"
        ]
    elif task_name == 'assin-ptpt':
        return [
            "assin-ptpt-train.xml",
            "assin-ptpt-blind-test.xml"
        ]
    
path_list_dict = {
    "assin2": [
            "assin2-train.xml",
            "assin2-blind-test.xml"
        ],
    "assin-ptbr": [
            "assin-ptbr-train.xml",
            "assin-ptbr-blind-test.xml"
        ],
    "assin-ptpt": [
            "assin-ptpt-train.xml",
            "assin-ptpt-blind-test.xml"        
    ],
    "toy": [
        "toy-train.xml",
        "toy-blind-test.xml"
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
        try:
            os.environ['DICTIONARY_FILE']
            template["dictionary_file"] = './sources/' + os.environ['DICTIONARY_FILE']
        except:
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
try:
    config_file = os.environ['CONFIG']
except:
    config_file = 'config.yml'

with open(config_file, 'r') as stream:
    try:
        params = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

try:
    params['dataset']
except:
    params['dataset'] = os.environ['DATASET']

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
            "dir_bert": "./results/pt/{0}/similarity/subset".format(params['dataset']),
            "dir_roberta": "./results/en/{0}/similarity/subset".format(params['dataset']),
            "save_path": "./results/ensemble/{0}/similarity/subset".format(params['dataset'])
        },
        {
            "dir_bert": "./results/pt/{0}/entailment/subset".format(params['dataset']),
            "dir_roberta": "./results/en/{0}/entailment/subset".format(params['dataset']),
            "save_path": "./results/ensemble/{0}/entailment/subset".format(params['dataset'])
        }
    ]

settings['submission'] = [
        {
            "source": "./sources/{0}-blind-test.xml".format(params['dataset']),
            "target": "./submission",
            "target_filename": "submission.xml",
            "entailment_preds": "./results/ensemble/{0}/entailment/subset/model_preds.npy".format(params['dataset']),
            "similarity_preds": "./results/ensemble/{0}/similarity/subset/model_preds.npy".format(params['dataset']),
            "entailment_data": "./datasets/pt/{0}/entailment/subset/dev.tsv".format(params['dataset']),
            "similarity_data": "./datasets/pt/{0}/similarity/subset/dev.tsv".format(params['dataset'])
        }
    ]

with open('settings.json', 'w+') as f:
    json.dump(settings, f)