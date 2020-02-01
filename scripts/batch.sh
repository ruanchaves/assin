cd "$(dirname "${BASH_SOURCE[0]}")"
cd ..
datasets=("assin2" "assin-ptpt" "assin-ptbr")
config_files=(settings/$PREFIX*.yml)
for dataset in ${datasets[@]}; do
    for filename in ${config_files[@]}; do
        single_filename="${filename##*/}"

        sudo nvidia-docker run \
            -v `pwd`:/home \
            --env DATASET=$dataset \
            --env CONFIG=$single_filename \
            --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
            -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh
    done
done