export HTTPS_PROXY="127.0.0.1:17890"
export HTTP_PROXY="127.0.0.1:17890"
export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"

source activate UICoder

DATASET_NAME="vu2048"

python ../scripts/train/train.py \
    --stage=1 \
    --model_name_or_path="/models/pix2struct-large" \
    --batch_size=1 \
    --output_path="/xx/xx/xx/code/UICoder/checkpoints/" \
    --eval_size=1024 \
    --num_train_epochs=1 \
    --learning_rate=5e-5 \
    --name="$DATASET_NAME" \
    --path="/xx/xx/datasets/cc/arrows_8-14_processed" \
    --max_patches=1024 \
    --max_length=2048 \
    --max_num=3000000 \
    --preprocess=True \
    --make_patches_while_training=True