import os,sys
import pandas as pd

# all the result dirs
csv_dirs=["/xx/xx/projects/UICoder/outputs/eval_gpt4v",
          "/xx/xx/projects/UICoder/outputs/eval_cogvlm",         
         "/xx/xx/projects/UICoder/outputs/eval_ws",
         "/xx/xx/projects/UICoder/outputs/eval_d2c",
         "/xx/xx/projects/UICoder/outputs/eval_stage0",
         "/xx/xx/projects/UICoder/outputs/eval_stag0ws",
         ]




def format_decimal(num):
    formatted = "{:.2f}".format(num)
    if formatted.startswith("0"):
        return formatted[1:]
    else:
        return formatted


def format_csv(path):
    with open(path) as f:
        data= f.read()
    splits = data.split('\n')
    if len(splits) != 2:
        df_tmp=pd.read_csv(path)
        df_tmp.columns = [c.strip() for c in df_tmp.columns]
        return df_tmp
    head, tail=data.split('\n')
    
    with open('tmp.csv', 'w') as f:
        f.write(f"{head}\n")
    key = '/xx'
    start = 0
    while start<len(tail):
        pos1 = tail.find(key, start)
        if pos1==-1:
            break
        pos2 = tail.find(key, pos1+1)
        if pos2==-1:
            break
        pos3=tail.find(key, pos2+1)
        line = tail[pos1:pos3]
        start = pos3
        with open('tmp.csv', 'a+') as f:
            f.write(f"{line}\n")
    df_tmp = pd.read_csv('tmp.csv')
    df_tmp.columns = [c.strip() for c in df_tmp.columns]
    return df_tmp

rows=[]
column_names=[]
for dir in csv_dirs:
    for root,dirs,files in os.walk(dir):
        if len(files) > 0 and files[0] != 'metrics_result.csv':
            continue
        files = sorted(files, key=lambda x : x.split('_')[0])
        for file in files:
            if file == 'metrics_result.csv':
                row=[]
                model_name = root.split('/')[-2].split('_')[-1]
                dataset_name = 'v2u_'+root.split('/')[-1].split('_')[-2]
                full_path = os.path.join(root, file)
                #df = pd.read_csv(full_path)
                print(full_path)
                df=format_csv(full_path)
                df['visual_score']=df[['block_match', 'text_match', 'position_match', 'text_color_match', 'clip_score']].mean(axis=1)
                row.extend([model_name, dataset_name])
                columns = []
                for c in df.columns:
                    if c not in ["origin","pred"]:
                        columns.append(c)
                        value=f"{df[c].mean():.2f} (±{df[c].std():.2f})"
                        row.append(value)                           
                rows.append(row) 
                if len(column_names) ==0:
                    column_names = ['model', 'dataset']+columns
                    
df_res = pd.DataFrame(rows, columns=column_names)
sort_keys = ['dataset', 'tree_rouge_1','block_match', 'position_match', 'text_match', 'text_color_match', 'clip_score']
df1 = df_res.sort_values(sort_keys)
keys_1=['dataset','tree_rouge_1',  'clip_sim','visual_score'] # the 'tree_rouge_1' denote the 'TreeBLEU' in the paper.
df2=df1[['dataset','model','tree_rouge_1',  'clip_sim','visual_score']].sort_values(keys_1)
#df2=df2[df2['model'] != 'stage2'].reset_index(drop=True)
df2.to_csv('/xx/xx/projects/UICoder/outputs/dataset_track_res.csv')