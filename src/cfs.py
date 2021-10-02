import requests
import pendulum
import sys
import os
from pathlib import Path
from cdo import Cdo

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
    contador = 0
    while True:
        for horario_de_rodada in ['18','12','06','00']:
            
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
        contador += 1
        data = data.subtract(days=contador)


def baixa_mensal(data_string:str=None, hoje: bool=False, output:str='') -> str:
    """Baixa arquivo de previsão mensal do modelo CFSv2 gerado com discretização mensal.
    Caso a data requisitada não esteja disponível, pega a anterior.

    Args:
        data_string (str, optional): [DD-MM-YYYY] data requerida dos dados. Defaults to None.
        hoje (bool, optional): Habilita ou não a data atual. Defaults to False.
        output (str, optional): Pasta de destino. Defaults to ''- pasta do script.

    Returns:
        str: Nome do arquivo netcdf4.
    """
    cdo = Cdo()
    
    data_requerida = pendulum.now('America/Sao_Paulo') if hoje else pendulum.from_format(data_string, 'DD-MM-YYYY')
    
    url_base = 'https://ftp.cpc.ncep.noaa.gov/International/nmme/binary_monthly/'
    arquivo = f'{data_requerida.format("MMM")}IC_cfsv2_precip_anom_stdanom'
    
    for terminacao in ('ctl','dat'):
    
        url=f'{url_base}/{arquivo}.{terminacao}'

        resp=requests.get(url)

        if resp.status_code == 200:

            resp=requests.get(url).content
            nome_arquivo = f'{arquivo}.{terminacao}'
            diretorio = Path(output, nome_arquivo)

            with open(diretorio, "wb") as arquivo_:
                arquivo_.write(resp)
                print(f"{nome_arquivo} [ok]")

        else :
            print('Erro 404. Após verificado a disponibilidade do arquivo, ainda houve erro no download')
            print('Será baixado o dado do mês anterior')
            mes_anterior = data_requerida.subtract(months=1).format('DD-MM-YYYY')
            baixa_mensal(data_string=mes_anterior)
            
    filename_nc = cdo.import_binary(input=f'{output}/{arquivo}.ctl', output=f'{output}/{arquivo}.nc', options='-f nc4')
    print(f"{filename_nc} [ok]")

    return filename_nc


def baixa_mensal_com_membros(data_string:str=None,hoje:bool=False,output:str=os.getcwd()) -> str:
    """Baixa 7 leads da previsão mensal com atualização horária do modelo cfs.

    Args:
        data_string (str, optional): Data requerida. Defaults to None.
        hoje (bool, optional): Utiliza a data atual de São Paulo na execução. Defaults to False.
        output (str, optional): Pasta de saída para os downloads. Defaults to os.getcwd().

    Returns:
        str: mensagem de sucesso.
    """
    armazenador_nomes_lead_e_membros = {'lead_1':[],
        'lead_2':[],
        'lead_3':[],
        'lead_4':[],
        'lead_5':[],
        'lead_6':[],
        'lead_7':[]
        }
    data_requerida = pendulum.now('America/Sao_Paulo') if hoje else pendulum.from_format(data_string, 'DD-MM-YYYY')
    
    url_base = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cfs'

    data, hora_da_rodada = busca_ultimo_dado_disponivel(data_requerida, url_base)
    print('Iniciando downloads ...')

    membros = 0
    while membros < 6: # Baixa os arquivos disponíveis até ter 6 membros baixados
        data_formatada = data.subtract(days=membros).format('YYYYMMDD') # cada membro é a mesma rodada de dias diferentes
        
        for previsao in [1,2,3,4,5,6,7]:
            lead = data.add(months=previsao).format("YYYYMM")
            arquivo = f'cfs.{data_formatada}/{hora_da_rodada}/monthly_grib_01/flxf.01.{data_formatada}{hora_da_rodada}.{lead}.avrg.grib.grb2'

            url=f'{url_base}/{arquivo}'
            resp=requests.get(url)
        
            if resp.status_code == 200:
                resp=requests.get(url).content
                nome_arquivo = f'pgbf.01.{data_formatada}{hora_da_rodada}.{lead}.avrg.grib.grb2'
                armazenador_nomes_lead_e_membros[f'lead_{previsao}'].append(nome_arquivo) #armazena nome do arquivo
                diretorio = Path(output, nome_arquivo)

                with open(diretorio, "wb") as arquivo_:
                    arquivo_.write(resp)
                    print(f"{arquivo} [ok]")

            else :
                sys.exit('Erro 404. Após verificado a disponibilidade do arquivo, ainda houve erro no download!\n'
                'Cheque se todos os leads já se encontram disponíveis na página requisitada:'
                f'{url}'
                '>>>> Caso os dados não estejam disponíveis ainda, recomendamos que usei a data_string referente a ontem.')
        membros += 1
    
    return armazenador_nomes_lead_e_membros


