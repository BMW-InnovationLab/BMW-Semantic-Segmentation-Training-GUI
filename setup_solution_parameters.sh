#!/bin/bash
sudo apt-get install jq

json_path='docker_sdk_api/assets/paths.json'

# change training api image name based on architecture CPU/GPU
change_image_name() {
  jq '."image_name"="'$1'"' "$json_path" >temp.$$.json && mv temp.$$.json "$json_path"
}

adjust_base_dir() {

  #Adjust basedir path
  python3 adjust_basedir_path.py
}

CPU_docker_image="gluoncv_semantic_segmentation_training_api_cpu"
CPU_MKL_docker_image="gluoncv_semantic_segmentation_training_api_cpu_mkl"
GPU_docker_image="gluoncv_semantic_segmentation_training_api_gpu"
GPU_MKL_docker_image="gluoncv_semantic_segmentation_training_api_gpu_mkl"

echo '----------------------------------------------'
echo 'Please choose docker image build architecture'

PS3='Please enter your choice: '
options=("GPU" "CPU" "GPU with MKL" "CPU with MKL")

adjust_base_dir

select opt in "${options[@]}"; do
  case $opt in
  "GPU")
    change_image_name "$GPU_docker_image"
    break
    ;;
  "CPU")
    change_image_name "$CPU_docker_image"
    break
    ;;

  "GPU with MKL")
    change_image_name "$GPU_MKL_docker_image"
    break
    ;;
  "CPU with MKL")
    change_image_name "$CPU_MKL_docker_image"
    break
    ;;
  *) echo "invalid option $REPLY" ;;
  esac
done
