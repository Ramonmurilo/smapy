# SMAPY - Dados para deck de entrada

![texto](https://img.shields.io/static/v1?label=linguagem&message=python&color=green&style=flat-square "linguagem")
![texto](https://img.shields.io/static/v1?label=ambiente&message=conda&color=orange&style=flat-square "ambiente")
![texto](https://img.shields.io/badge/Funcional.svg "status")
![texto](https://img.shields.io/badge/plataforma-wsl2--linux-lightgrey "status")



1. [Descrição do projeto](#descrição-do-projeto)  
2. [Funcionalidades](#funcionalidades)   
4. [Pré-requisitos](#pré-requisitos)  
5. [Como instalar](#como-instalar)
6. [Execução](#execucao)
7. [Desenvolvimento](#desenvolvimento)
8. [Como rodar](#como-rodar)
9. [I/O](#I/O)


## :scroll: Descrição do projeto

Baixa Dados de chuva observada do MERGE e prevista do CFSv2 e recorta por um shapefile de bacias. 

## :sparkles: Funcionalidades

:wrench: Download automatizado dos dados de rodada MERGE e CFSv2 mensal.  
:wrench: Recorta Chuva pelo contorno da bacia e calcula o valor médio.   

## :warning: Pré-requisitos

- [Python + conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) (obrigatório)

## :cd: Como instalar

```bash
# 1. no terminal, clone o projeto
git clone https://github.com/Ramonmurilo/smapy.git

# 2. entre na pasta do projeto
cd smapy

# 3. Através do seu termina conda, instale/reproduza o ambiente
conda env create -f env.yaml

# 4. Ative o ambiente
conda activate smapy

# 5. Ative o jupyter lab para ver o script main
jupyter lab
```

## :arrow_forward: Execução
### O exemplo de execução e funcionamento se encontra no arquivo (main.ipynb)

## :construction: Desenvolvimento

:dart: Gerar txt de saída: Gerar os arquivos no padrão de input para o modelo smapy

## :rotating_light: Como rodar
#### O exemplo de como rodar se encontra no arquivo (main.ipynb)

## :green_apple: I/O

Os Inputs/entradas do SMAPY ficam armazenados na pasta ```downloads``` que é criada automaticamente pelo script.
Os outputs/saídas do SMAPY ainda não são gerados.
