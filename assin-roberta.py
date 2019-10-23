from utils_conv import AssinReader, assin_json_reader
from run_train import parallel_train
from ensemble import load_ensemble
from utils_submission import assin_json_writer
from report import generate_report
import sys 
import json
from getpass import getpass
import datetime

if __name__ == '__main__':

    with open(sys.argv[1]) as f:
        data = json.load(f)

    WORKERS = data['workers']

    conv_data = data['conv']
    train_data = data['train']
    ensemble_data = data['ensemble']
    submission_data = data['submission']

    # assin_json_reader(conv_data)
    # parallel_train(train_data, workers=WORKERS)
    # load_ensemble(ensemble_data)
    assin_json_writer(submission_data)