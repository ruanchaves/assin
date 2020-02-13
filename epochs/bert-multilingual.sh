cd "$(dirname "${BASH_SOURCE[0]}")"
cd ..

export GLUE_DIR=/home/epochs/pt
export TASK_NAME=STS-B

LOG_PATH=$GLUE_DIR/$LOG_FILE python run_glue.py \
    --model_type bert \
    --model_name_or_path bert-base-multilingual-cased \
    --task_name $TASK_NAME \
    --do_train \
    --do_eval \
    --do_lower_case \
    --data_dir $GLUE_DIR \
    --max_seq_length 128 \
    --per_gpu_eval_batch_size=1 \
    --per_gpu_train_batch_size=1 \
    --gradient_accumulation_steps=8 \
    --learning_rate 2e-5 \
    --num_train_epochs 100.0 \
    --overwrite_cache \
    --overwrite_output_dir \
    --eval_all_checkpoints \
    --evaluate_during_training \
    --logging_steps 400 \
    --save_steps 3000 \
    --output_dir $GLUE_DIR/tmp/bert-multilingual/