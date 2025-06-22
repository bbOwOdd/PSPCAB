import pandas as pd
from sklearn.model_selection import train_test_split
from simpletransformers.classification import ClassificationModel
from transformers import logging

data = pd.read_csv(r"C:\Users\s2569\Desktop\bert0725\demo.csv")
print(data)

train_df, test_df = train_test_split(data, test_size = 0.2, random_state = 927)
model = ClassificationModel('bert', 'hfl/chinese-bert-wwm', use_cuda=False)

if __name__ == '__main__': 
    logging.set_verbosity_error()
    model.train_model(train_df, args = {'overwrite_output_dir': True}, num_labels=0-1)

