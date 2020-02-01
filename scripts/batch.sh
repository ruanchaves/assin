cd "$(dirname "${BASH_SOURCE[0]}")"
cd ..
datasets=("assin2" "assin-ptpt" "assin-ptbr")
config_files=(settings/*.yml)
for dataset in ${datasets[@]}; do
    for filename in ${config_files[@]}; do
        single_filename="${filename##*/}"

        chosen_gpu=-1
        while [[ $chosen_gpu -lt 0 ]]
        do
            for i in $(seq 0 7); do
                status=$(nvidia smi -i $i | grep "No running processes found")
                if [[ -z $status ]]
                then
                    echo "Skipping GPU $i ."
                else
                    echo "Running on GPU $i ."
                    chosen_gpu=$i
            done
            if [[ $chosen_gpu -lt 0 ]]
            then
                sleep 5
            fi
        done

        # sudo nvidia-docker run \
        #     -v `pwd`:/home \
        #     --env DATASET=$dataset \
        #     --env CONFIG=$single_filename \
        #     --env CUDA_VISIBLE_DEVICES=$chosen_gpu \
        #     -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh &

        chosen_gpu=-1
    done
done