## Environment Installation
```
conda create -n UICoder python=3.10
conda activate UICoder
pip install -r requirements.txt
```

## Download Testing Set into your `data_path`.
```
git clone https://huggingface.co/datasets/anonymouscodee/webcode2m_test
```

## Benchmark Test
Take the inference of the UICoder model as an example.

(Other models' inferences are similar operations)
1. Download the UICoder model into your `model_path`.
```
git clone https://huggingface.co/anonymouscodee/webcoder
```
2. Edit the inference script
```
cd benchmark_test
vim end2end_inference.py
```
- Replace `model_path` and `data_path` with your corresponding absolute path
- Specify a result output path by modifying `result_path`
- `model_name` is simply used to mark your output dir, so change as you like
3. Let's go
```
python end2end_inference.py
```
This 👆 can take hours to run through the entire test set, and if you want to run only a few tests, just modify a few lines of code.

Change
```
for item in tqdm(ds):
    ...
```
To
```
for item in tqdm(ds.select(range(0,10))):
    ...
```
4. Evaluation
```
cd .. # change to the root dir, 'short' can be replaced by [short, mid, long]
python scripts/evaluation/evaluate.py -i ${result_path}/short   -o outdir
python scripts/evaluation/merge_results.py # please modify `csv_dirs` to your `result_path` in this script first
```