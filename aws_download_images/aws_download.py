#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Faz o download das imagens contidas em um bucket do s3.
# Antes de executar o script, é necessário configurar as credenciais
# executando o comando `aws configure` no terminal.

from shutil import copyfile
from tqdm import tqdm
from PIL import Image
from PIL.ExifTags import TAGS
import boto3
import glob
import os

BUCKET = 'bases-cofness'
FOLDER = 'dados'

EBV12 = 1.2
EBV13 = 1.3
EBV14 = 1.4
EBV15 = 1.5
EBV16 = 1.6

EBV = ['EBV12', 'EBV13', 'EBV14', 'EBV15', 'EBV16']

def download_folder_from_s3(bucket_name, folder_name, dir_save):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    cont=0
    for it in bucket.objects.filter(Prefix=folder_name):
        cont+=1

    for it,i in zip(bucket.objects.filter(Prefix=folder_name), tqdm(range(cont))):
        # Nome do path
        classes_path = os.path.dirname(it.key)
        classes_path = dir_save+'/'+classes_path+"/"

        # Se o path da classe não existe, então cria o diretório
        # no dir_save. Se não, apenas baixa as imagens contidas 
        # neste diretório do s3 para o diretório local.
        if not os.path.exists(classes_path):
            os.makedirs(classes_path)
        bucket.download_file(it.key,classes_path+os.path.split(it.key)[-1])

def base_separate(path_base, path_to_save):
    # Cria diretórios onde serão copiadas as imagens filtradas.
    classes = os.listdir(path_base)
    for i in EBV:
        if not os.path.exists(path_to_save+i):
            os.makedirs(path_to_save+i)
        for it in classes:
            if not os.path.exists(path_to_save+i+'/'+it):
                os.makedirs(path_to_save+i+'/'+it)

    for it in classes:
        print(it)
        imgs_path = glob.glob(path_base+it+'/*.jpg')
        if imgs_path==[]:
            print("Arquivos com extensão jpg não encontrados.")
            exit(1)
        img_count = [1, 1, 1, 1, 1]

        for itt in zip(imgs_path, tqdm(range(len(imgs_path)))):
            img = Image.open(itt[0])
            ret = {}
            info = img._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            
            ev = round(ret['ExposureBiasValue'][0]*1.0/ret['ExposureBiasValue'][1], 2)
            if (ev==EBV12):
                copyfile(itt[0], path_to_save+EBV[0]+'/'+it+'/'+it+'_'+str(img_count[0])+'.jpg')
                img_count[0]+=1
            elif (ev==EBV13):
                copyfile(itt[0], path_to_save+EBV[1]+'/'+it+'/'+it+'_'+str(img_count[1])+'.jpg')
                img_count[1]+=1
            elif (ev==EBV14):
                copyfile(itt[0], path_to_save+EBV[2]+'/'+it+'/'+it+'_'+str(img_count[2])+'.jpg')
                img_count[2]+=1
            elif (ev==EBV15):
                copyfile(itt[0], path_to_save+EBV[3]+'/'+it+'/'+it+'_'+str(img_count[3])+'.jpg')
                img_count[3]+=1
            elif (ev==EBV16):
                copyfile(itt[0], path_to_save+EBV[4]+'/'+it+'/'+it+'_'+str(img_count[4])+'.jpg')
                img_count[4]+=1
            else:
                print("Erro: Valor de exposição não encontrado!! ",ev)
                exit(1)

if __name__ == "__main__":
    download_folder_from_s3(BUCKET,FOLDER,'/home/kaffee/Imagens/Cofness/DownloadS3')
    base_separate('/home/kaffee/Imagens/Cofness/DownloadS3/dados/',
                '/home/kaffee/Imagens/Cofness/DownloadS3/dados_separados/')
