cd "$(dirname "${BASH_SOURCE[0]}")"
cd ..

DOCKER_MAJOR_VERSION_STRING=$(docker -v | grep -oP '([0-9]+)' | sed -n 1p)
DOCKER_MINOR_VERSION_STRING=$(docker -v | grep -oP '([0-9]+)' | sed -n 2p)
ps_test=$(docker ps -a)
datasets=("assin-ptbr" "assin-ptpt")

DOCKER_MAJOR_VERSION=$((10#$DOCKER_MAJOR_VERSION_STRING))
DOCKER_MINOR_VERSION=$((10#$DOCKER_MINOR_VERSION_STRING))

if [[ ! -z $ps_test ]]; then
    build_test=$(docker image ls | grep 'ruanchaves/assin.*2.0')
else
    build_test=$(sudo docker image ls | grep 'ruanchaves/assin.*2.0')
fi

if [[ -z $build_test ]] && [[ ! -z $ps_test ]]; then 
    docker build -t ruanchaves/assin:2.0 .
elif [[ -z $build_test ]] && [[ -z $ps_test ]]; then
    sudo docker build -t ruanchaves/assin:2.0 .
fi

config_files=(settings/$PREFIX*.yml)
for dataset in ${datasets[@]}; do
    for filename in ${config_files[@]}; do
        echo $dataset
        echo $filename
        single_filename="${filename##*/}"
        echo $single_filename
        CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES
        if [[ ! -z $ps_test ]] && [[ $DOCKER_MAJOR_VERSION -ge 19 ]] && [[ $DOCKER_MINOR_VERSION -ge 3 ]]; then
            echo "docker run --gpus all 
                -v `pwd`:/home 
                --env DATASET=$dataset 
                --env CONFIG=$single_filename 
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES 
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh"
            docker run --gpus all \
                -v `pwd`:/home \
                --env DATASET=$dataset \
                --env CONFIG=$single_filename \
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh
        elif [[ ! -z $ps_test ]] && [[ $DOCKER_MAJOR_VERSION -le 19 ]] && [[ $DOCKER_MINOR_VERSION -le 2 ]]; then
            echo "nvidia-docker run 
                -v `pwd`:/home 
                --env DATASET=$dataset 
                --env CONFIG=$single_filename 
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES 
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh"
            nvidia-docker run \
                -v `pwd`:/home \
                --env DATASET=$dataset \
                --env CONFIG=$single_filename \
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh
        elif [[ -z $ps_test ]] && [[ $DOCKER_MAJOR_VERSION -ge 19 ]] && [[ $DOCKER_MINOR_VERSION -ge 3 ]]; then
            echo "sudo docker run --gpus all 
                -v `pwd`:/home 
                --env DATASET=$dataset 
                --env CONFIG=$single_filename 
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES 
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh"
            sudo -E docker run --gpus all \
                -v `pwd`:/home \
                --env DATASET=$dataset \
                --env CONFIG=$single_filename \
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh
        elif [[ -z $ps_test ]] && [[ $DOCKER_MAJOR_VERSION -le 19 ]] && [[ $DOCKER_MINOR_VERSION -le 2 ]]; then
            echo "sudo nvidia-docker run 
                -v `pwd`:/home 
                --env DATASET=$dataset 
                --env CONFIG=$single_filename 
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES 
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh"
            sudo -E nvidia-docker run \
                -v `pwd`:/home \
                --env DATASET=$dataset \
                --env CONFIG=$single_filename \
                --env CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES \
                -it --rm ruanchaves/assin:2.0 bash /home/scripts/run_assin.sh
        else
            echo "Not found."
        fi
    done
done