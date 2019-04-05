#!/usr/bin/env python3
from tqdm import tqdm

import cv2
import argparse
import numpy
import glob
import sys
import os

# Parseia o caminho para a base que será processada.
parser = argparse.ArgumentParser(description='Crop images')
parser.add_argument('--path', required=True, default='/', type=str, help='Caminho para a pasta raiz contendo val, train e test.')
args = parser.parse_args()

# Define as strings para as subpastas.
VAL = 'val'
TRAIN = 'train'
TEST = 'test'
CROPPED = 'cropped'
OLD_SIZE = 128
NEW_SIZE = 100

def mkdir_dir(path):
    """ Cria os diretórios correspondentes para salvar as imagens recortadas. """
    # Remove a barra final do path.
    path_new = path[:-1]
    new_path_val = path_new+'_'+CROPPED+'/'+VAL
    new_path_train = path_new+'_'+CROPPED+'/'+TRAIN
    new_path_test = path_new+'_'+CROPPED+'/'+TEST
    os.makedirs(new_path_val,exist_ok=True)
    os.makedirs(new_path_train,exist_ok=True)
    os.makedirs(new_path_test,exist_ok=True)
    return new_path_train, new_path_val, new_path_test
    #print(os.path.normpath(path+os.sep+os.pardir))


def crop_image(img_path, save_path):
    """ Carrega a imagem, recorta e salva no diretorio correspondente. """
    delta = int((OLD_SIZE-NEW_SIZE)/2)
    img = cv2.imread(img_path, 1)  # Carrega imagem com 3 canais.
    croped_img = img[delta:OLD_SIZE-delta, delta:OLD_SIZE-delta, :]
    cv2.imwrite(save_path, croped_img)


def mkdir_dir_classes(path, classes):
    for it in classes:
        os.makedirs(path+'/'+it, exist_ok=True)

def main(path):
    classes = os.listdir(path+TRAIN)

    # Cria os diretórios correspondentes, caso não existam.
    new_path_train, new_path_val, new_path_test = mkdir_dir(args.path)
    mkdir_dir_classes(new_path_train, os.listdir(path+TRAIN))
    mkdir_dir_classes(new_path_val, os.listdir(path+VAL))
    mkdir_dir_classes(new_path_test, os.listdir(path+TEST))

    for it in classes:
        print('Recortando imagens da classe: ',it)
        print('Conjunto de treino')
        path_imgs = glob.glob(path+TRAIN+'/'+it+'/*.png')
        save_path = new_path_train+'/'+it
        for itt in zip(path_imgs, tqdm(range(len(path_imgs)))):
            img_name = itt[0].split('/')[-1]
            crop_image(itt[0], save_path+'/'+img_name)

        print('Conjunto de validação')
        path_imgs = glob.glob(path+VAL+'/'+it+'/*.png')
        save_path = new_path_val+'/'+it
        for itt in zip(path_imgs, tqdm(range(len(path_imgs)))):
            img_name = itt[0].split('/')[-1]
            crop_image(itt[0], save_path+'/'+img_name)

        print('Conjunto de teste')
        path_imgs = glob.glob(path+TEST+'/'+it+'/*.png')
        save_path = new_path_test+'/'+it
        for itt in zip(path_imgs, tqdm(range(len(path_imgs)))):
            img_name = itt[0].split('/')[-1]
            crop_image(itt[0], save_path+'/'+img_name)

if __name__ == '__main__':
    main(args.path)
