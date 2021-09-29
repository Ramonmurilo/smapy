import requests
import pendulum
import sys
import os
from pathlib import Path

def busca_ultimo_dado_disponivel(data_requerida:pendulum.date, url_base:str) -> tuple[pendulum.date,str] :
    """Verifica qual o último dia e horário de rodada disponíveis no NOAA
        Esta é uma subfunção da "baixa_mensal"

    Args:
        data_requerida (pendulum.date): data requerida no formato pendulum
        url_base (str): base do caminho para o arquivo cfs diário do NOAA

    Returns:
        tuple[pendulum.date,str]: data e horário da rodada mais próxima da requerida.
    """
    data = data_requerida
    while True:
        for horario_de_rodada in ['00','06','12','18']:
            
            data_formatada = data.format("YYYYMMDD")
            lead1_para_teste = data.add(months=1).format("YYYYMM")
            arquivo = f'cfs.{data_formatada}/{horario_de_rodada}/monthly_grib_01/pgbf.01.{data_formatada}{horario_de_rodada}.{lead1_para_teste}.avrg.grib.grb2'
            
            url = f'{url_base}/{arquivo}'
            resp=requests.get(url)

            if resp.status_code == 200:

                return data, horario_de_rodada

            elif resp.status_code == 404:
                print(f'{data_formatada} | {horario_de_rodada} : Não disponível')
                pass
        data = data.subtract(days=1)



def baixa_mensal(data_requerida:str=None,hoje:bool=False,output:str=os.getcwd()) -> str:
    """Baixa 7 leads da previsão mensal com atualização diária do modelo cfs.

    Args:
        data_requerida (str, optional): Data requerida. Defaults to None.
        hoje (bool, optional): Utiliza a data atual de São Paulo na execução. Defaults to False.
        output (str, optional): Pasta de saída para os downloads. Defaults to os.getcwd().

    Returns:
        str: mensagem de sucesso.
    """
    data_requerida = pendulum.now('America/Sao_Paulo') if hoje else pendulum.from_format(data_string, 'DD-MM-YYYY')
    
    url_base = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs'

    data, hora_da_rodada = busca_ultimo_dado_disponivel(data_requerida, url_base)
    data_formatada = data.format('YYYYMMDD')

    for previsao in [1,2,3,4,5,6,7,8]:

        lead = data.add(months=previsao).format("YYYYMM")
        arquivo = f'cfs.{data_formatada}/{hora_da_rodada}/monthly_grib_01/pgbf.01.{data_formatada}{hora_da_rodada}.{lead}.avrg.grib.grb2'

        url=f'{url_base}/{arquivo}'

        resp=requests.get(url)
    
        if resp.status_code == 200:

            resp=requests.get(url).content
            nome_arquivo = f'pgbf.01.{data_formatada}{hora_da_rodada}.{lead}.avrg.grib.grb2'
            diretorio = Path(output, nome_arquivo)

            with open(diretorio, "wb") as arquivo_:
                arquivo_.write(resp)
                print(f"{arquivo} [ok]")

        else :

            sys.exit('Erro 404. Após verificado a disponibilidade do arquivo, ainda houve erro no download')
    
    return 'arquivos baixados'
