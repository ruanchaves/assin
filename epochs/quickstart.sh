cd "$(dirname "${BASH_SOURCE[0]}")"
sudo screen -dmS epochs_portuguese-bert_gpu1 bash -c 'sudo CUDA_VISIBLE_DEVICES=1 SCRIPT_FILE=portuguese-bert.sh LOG_FILE=portuguese-bert_log.txt bash start.sh'
sudo screen -dmS epochs_roberta_gpu1 bash -c 'sudo CUDA_VISIBLE_DEVICES=1 SCRIPT_FILE=roberta.sh LOG_FILE=roberta_log.txt bash start.sh'
sudo screen -dmS epochs_bert-multilingual_gpu1 bash -c 'sudo CUDA_VISIBLE_DEVICES=1 SCRIPT_FILE=bert-multilingual.sh LOG_FILE=bert-multilingual_log.txt bash start.sh'