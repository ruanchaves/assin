cd "$(dirname "${BASH_SOURCE[0]}")"
cd ..

export GLUE_DIR=/home/epochs/en
export TASK_NAME=STS-B

python -u run_glue.py \
    --model_type roberta \
    --model_name_or_path roberta-large \
    --task_name $TASK_NAME \
    --do_train \
    --do_eval \
    --logging_steps 400 \
    --save_steps 3000 \
    --max_seq_length=128 \
    --learning_rate 1e-5 \
    --warmup_steps=120 \
    --per_gpu_eval_batch_size=1 \
    --per_gpu_train_batch_size=1 \
    --gradient_accumulation_steps=16 \
    --do_lower_case \
    --data_dir $GLUE_DIR/$TASK_NAME \
    --max_seq_length 128 \
    --num_train_epochs 100.0 \
    --overwrite_cache \
    --overwrite_output_dir \
    --eval_all_checkpoints \
    --output_dir $GLUE_DIR/tmp/roberta/ >> $GLUE_DIR/$LOG_FILE