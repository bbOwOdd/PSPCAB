from ckiptagger import WS, POS, NER
import ckiptagger.model_pos
import os
import json
import jieba
import re
from tqdm import tqdm
import pandas as pd
import csv

def ckip_cut(articleList):
    
    #詞性列表
    #http://ckipsvr.iis.sinica.edu.tw/papers/category_list.pdf
    
    pos_list = ['A', 'Na', 'Nb', 'Nc', 'Nd', 'Nv', 'VA', 'VAC', 'VB', 'VC', 'VCL', 'VD', 'VH', 'VHC', 'VI', 'VJ','VK']
    prevdir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    
    # 讀取字典
    with open("C:\VS code\Python\web crawler\dict\ckip_dict.json", "r", encoding='utf-8') as f:
        ckip_dict = json.load(f)
    dictionary = ckiptagger.construct_dictionary(ckip_dict) # 設定字典格式為指定格式
    
    model_path = 'C:\VS code\Python\web crawler\embedding'

    # # Load model without GPU
    # ws = WS(model_path)
    # pos = POS(model_path)
    # ner = NER(model_path)    
    
    # Load model with GPU
    ws = WS(model_path, disable_cuda=False)
    pos = POS(model_path, disable_cuda=False)
    ner = NER(model_path, disable_cuda=False)
    
    ## 實際做斷詞的地方
    # word_sentence_list = ws(sentence_list, recommend_dictionary=dictionary)
    # word_sentence_list = ws(sentence_list, coerce_dictionary=dictionary)
    ws_results = ws(articleList)
    print(ws_results)
        
    # 取詞性
    pos_results = pos(ws_results)
    print(pos_results)
        
    '''
    output = open('C:\\VS code\\Python\\web crawler\\done.xls', 'w')
    output.write('字\t')
    output.write('詞性\n')
    for i in range(len(ws_results)):
        for j in range(len(ws_results[i])):
            if pos_results[i][j] in pos_list:
                try :
                    output.write(str(ws_results[i][j])) #write函數不能寫int類型的參數，所以使用str()轉化
                    output.write('\t')   
                    output.write(str(pos_results[i][j]))
                    output.write('\n')  
                except :
                    continue
            else:
                continue
    output.close()
    '''
      
    for i in range(len(ws_results)):
        for j in range(len(ws_results[i])):
            if pos_results[i][j] in pos_list:
                data_row = [ws_results[i][j], pos_results[i][j]]
                with open('C:\\VS code\\Python\\web crawler\\done.csv', 'a', newline='', encoding='utf_8_sig') as f:
                    csv_write = csv.writer(f)
                    csv_write.writerow(data_row)
            else:
                continue
                                            
    list_out = []
    for i in range(len(ws_results)):
        temp = []
        for j in range(len(ws_results[i])):
            # print(ws_results[i][j], pos_results[i][j], sep = '  ')
            if pos_results[i][j] in pos_list:
                temp.append(ws_results[i][j])
        list_out.append(temp)
        # print(ws_results[i][j], pos_results[i][j], sep = '\t')
            # input()
    del ws
    del pos
    del ner
    return list_out        

first_row = ['字', '詞性']
with open('C:\\VS code\\Python\\web crawler\\done.csv', 'a', newline='', encoding='utf_8_sig') as f:
    csv_write = csv.writer(f)
    csv_write.writerow(first_row) 
   
df_articles_data = pd.read_csv('C:\\VS code\\Python\\web crawler\\2021_0722~2021_0731.csv')
articles_data = df_articles_data['留言'].to_list()
for i in articles_data:
    str(i)
ckip_results = ckip_cut(articles_data)