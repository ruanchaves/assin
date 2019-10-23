import json
import subprocess
import pathlib
import concurrent.futures
import os
import copy

def preprocess(params):
    s = ""
    for i,v in params.items():
        s += " --" + i + v
    return s

def train(params):
    directory = params['output_dir'].strip('=')
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    directory = params['save_file'].strip().strip('model').strip('/')
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)

    del params['kfold']
    del params['kfold_buckets']
    cmd = "python run_glue.py" + preprocess(params)
    subprocess.call(cmd, shell=True)

def parallel_train(training_list, workers=4):
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            if 'cached_' in file_path:
                os.remove(file_path)

    new_training_list = []
    for params in training_list:
        original_params = copy.deepcopy(params)
        original_params['output_dir'] = params['output_dir'] + '/original'
        original_params['save_file'] = params['save_file'].strip('model') + '/original/model'
        new_training_list.append(original_params)
        if params['kfold'] == True:
            for idx in range(params['kfold_buckets']):
                new_params = copy.deepcopy(params)
                new_params['data_dir'] = params['data_dir'] + '/' + str(idx)
                new_params['output_dir'] = params['output_dir'] + '/' + str(idx)
                new_params['save_file'] = params['save_file'].strip('model') + str(idx) + '/model'
                new_training_list.append(new_params)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(train, new_training_list)

if __name__ == '__main__':
    pass