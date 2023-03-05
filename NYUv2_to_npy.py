import numpy as np
import mat73
import os
import shutil
import urllib.request
import sys

DATA_PATH = 'data'
DATA_SET_PATH = os.path.join(DATA_PATH, 'datset')


def img_to_npy(file_name):
    img_path = 'image'
    res_path = os.path.join(DATA_SET_PATH, img_path)
    os.makedirs(res_path, exist_ok=True)

    data = mat73.loadmat(file_name, only_include='images')
    data = data['images']
    cnt = data.shape[3]
    for i in range(0, cnt):
        file = f'{i}.npy'
        with open(os.path.join(res_path, file), 'wb') as f:
            np.save(f, data[:, :, :, i])
    del data
    return cnt


def label_to_npy(file_name):
    img_path = 'label'
    res_path = os.path.join(DATA_SET_PATH, img_path)
    os.makedirs(res_path, exist_ok=True)

    data = mat73.loadmat(file_name, only_include='labels')
    data = data['labels']
    cnt = data.shape[2]

    for i in range(0, cnt):
        file = f'{i}.npy'
        with open(os.path.join(res_path, file), 'wb') as f:
            np.save(f, data[:, :, i])
    del data
    return cnt


def depth_to_npy(file_name):
    img_path = 'depth'
    res_path = os.path.join(DATA_SET_PATH, img_path)
    os.makedirs(res_path, exist_ok=True)

    data = mat73.loadmat(file_name, only_include='depths')
    data = data['depths']
    cnt = data.shape[2]

    for i in range(0, cnt):
        file = f'{i}.npy'
        with open(os.path.join(res_path, file), 'wb') as f:
            np.save(f, data[:, :, i])
    del data
    return cnt


def make_datasets(cnt, test_per=0.25):
    # Get the paths to train and test datasets
    train_path = os.path.join(DATA_PATH, 'train')
    test_path = os.path.join(DATA_PATH, 'test')
    # Get the paths to train dataset items
    image_train_path = os.path.join(train_path, 'image')
    label_train_path = os.path.join(train_path, 'label')
    depth_train_path = os.path.join(train_path, 'depth')
    # Get the paths to test dataset items
    image_test_path = os.path.join(test_path, 'image')
    label_test_path = os.path.join(test_path, 'label')
    depth_test_path = os.path.join(test_path, 'depth')
    # Get the paths to default dataset items
    image_dataset_path = os.path.join(DATA_SET_PATH, 'image')
    label_dataset_path = os.path.join(DATA_SET_PATH, 'label')
    depth_dataset_path = os.path.join(DATA_SET_PATH, 'depth')

    # Remove the previous datasets
    clean_datasets([train_path, test_path])

    # Make directories
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    os.makedirs(image_train_path, exist_ok=True)
    os.makedirs(label_train_path, exist_ok=True)
    os.makedirs(depth_train_path, exist_ok=True)

    os.makedirs(image_test_path, exist_ok=True)
    os.makedirs(label_test_path, exist_ok=True)
    os.makedirs(depth_test_path, exist_ok=True)

    test_i = 0
    train_i = 0

    for i in range(0, cnt):
        # put img to train data if random value is bigger than  test percentage
        if np.random.rand(1)[0] > test_per:
            # Copy image
            sr = os.path.join(image_dataset_path, f'{i}.npy')
            dt = os.path.join(image_train_path, f'{train_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy label
            sr = os.path.join(label_dataset_path, f'{i}.npy')
            dt = os.path.join(label_train_path, f'{train_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy depth
            sr = os.path.join(depth_dataset_path, f'{i}.npy')
            dt = os.path.join(depth_train_path, f'{train_i}.npy')
            shutil.copyfile(sr, dt)
            train_i += 1
        else:
            # Copy image
            sr = os.path.join(image_dataset_path, f'{i}.npy')
            dt = os.path.join(image_test_path, f'{test_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy label
            sr = os.path.join(label_dataset_path, f'{i}.npy')
            dt = os.path.join(label_test_path, f'{test_i}.npy')
            shutil.copyfile(sr, dt)
            # Copy depth
            sr = os.path.join(depth_dataset_path, f'{i}.npy')
            dt = os.path.join(depth_test_path, f'{test_i}.npy')
            shutil.copyfile(sr, dt)
            test_i += 1


def clean_datasets(dirs):
    for i in range(len(dirs)):
        shutil.rmtree(dirs[i], True)


if __name__ == '__main__':

    data_file = 'nyu_depth_v2_labeled.mat'
    img_dir = os.path.join(DATA_SET_PATH, 'image')
    file_cnt = 0
    test_per = 0.25

    # Get the file if it doesn't exist
    if not os.path.isfile(data_file):
        print('Downloading the dataset (Can be long)...')
        urllib.request.urlretrieve('http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat',
                                   data_file)
        print('Dataset dowloaded')

    # Check if dataset hqs already been converted. Convert it if needed
    if os.path.exists(img_dir):
        # Not beautifull...
        file_cnt = len([entry for entry in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, entry))])
    else:
        print('Convert images...')
        img_to_npy(data_file)
        print('Convert labels...')
        label_to_npy(data_file)
        print('Convert depths...')
        file_cnt = depth_to_npy(data_file)

    make_datasets(file_cnt, test_per)
