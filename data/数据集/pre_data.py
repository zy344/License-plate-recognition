import shutil
import random
from tqdm import tqdm
import os

directory = 'data'
datas = os.listdir(directory)
random.shuffle(datas)
total = len(datas)
# 70 20 10
train_data = datas[:int(0.9 * total)]
test_data = datas[int(0.9 * total):]

if not os.path.exists('train'):
    os.mkdir('train')

if not os.path.exists('test'):
    os.mkdir('test')

for data in tqdm(train_data):
    licen, suffix = data.split('.')
    new_dir = 'train/' + licen + '.' + suffix
    shutil.copy(os.path.join(directory, data), new_dir)
print('exec train over')

for data in tqdm(test_data):
    licen, suffix = data.split('.')
    new_dir = 'test/' + licen + '.' + suffix
    shutil.copy(os.path.join(directory, data), new_dir)
print('exec test over')