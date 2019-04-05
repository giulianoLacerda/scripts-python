# Recorta imagem.

O código especificamente converte imagens de 128x128 para 100x100. O recorte é feito mantendo a imagem centralizada.

## Instalação das dependências
Para instalar as dependências, dentro do diretóri principal executar:
```
(venv) $ pip3 install --upgrade -r requirements.txt
```
## Execução
Recebe como parâmetro  `--path` o caminho para a pasta base que contém as pastas de `val`, `train` e `test`. Exemplo:
```
$ python3 crop_imgs.py --path /home/giuliano/Documents/base/
```
Após isso, será criada uma pasta chamada `base_cropped` com todas as imagens recortadas e salvas em suas respectivas pastas.