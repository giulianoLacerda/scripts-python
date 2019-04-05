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
RESIZED = 'resized'
OLD_SIZE = 128
NEW_SIZE = 100

def mkdir_dir(path):
    """ Cria os diretórios correspondentes para salvar as imagens recortadas. """
    # Remove a barra final do path.
    path_new = path[:-1]
    new_path_val = path_new+'_'+RESIZED+'/'+VAL
    new_path_train = path_new+'_'+RESIZED+'/'+TRAIN
    new_path_test = path_new+'_'+RESIZED+'/'+TEST
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


def main(path):
    # Cria os diretórios correspondentes, caso não existam.
    new_path_train, new_path_val, new_path_test = mkdir_dir(args.path)

    # Para cada pasta (val,train e test) obtém um vetor com o caminho das imagens em png.
    val_imgs = glob.glob(path+VAL+'/*.png')
    train_imgs = glob.glob(path+TRAIN+'/*.png')
    test_imgs = glob.glob(path+TEST+'/*.png')

    i = 0
    for it in [train_imgs, val_imgs, test_imgs]:
        save_path = ''
        if i==0:
    	    print('Recortando imagens do treino')
    	    save_path = new_path_train
        elif i==1:
	        print('Recortando imagens da validação')
	        save_path = new_path_val
        else:
            print('Recortando imagens do teste')
            save_path = new_path_test
        for itt in zip(it, tqdm(range(len(it)))):
            img_name = itt[0].split('/')[-1]
            crop_image(itt[0], save_path+'/'+img_name)
        i += 1

if __name__ == '__main__':
    main(args.path)