import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd


def consulta_cnpj(cnpj):
    link = "https://economicasnet.ibge.gov.br/UploadPesquisa/ResultadoPesquisaEmpresa?cnpj=" + cnpj
    x = requests.get(link)
    soup = BeautifulSoup(x.text,'html.parser')
    soup_result = soup.findAll("div", class_="panel-body")

    result = soup_result[0].findAll('p')[0].text

    lista = []

    if result == 'Abaixo os dados retornados da pesquisa pela Raiz do CNPJ':

        empresa = soup_result[0].findAll('p')[1].text
        pesquisa = soup_result[0].findAll('p')[2].text
        modelo = soup_result[0].findAll('p')[3].text
        lista.append(True)
        lista.append(empresa)
        lista.append(pesquisa)
        lista.append(modelo)
        return lista

    if result == 'Esta empresa não consta nas pesquisas econômicas deste ano!':
        lista.append(False)
        return lista


df = pd.read_csv('empresas.csv', delimiter=";", encoding='utf-8', dtype={'CNPJ': str})

for index, row in df.iterrows():
    razao_social = row['razao_social']
    cnpj = row['CNPJ']
    empresa_p = row['Empresa']
    pesquisa_p = row['Pesquisa']
    modelo_p = row['Modelo']

    if len(cnpj) == 14:
        consulta = consulta_cnpj(cnpj[:8])
        if consulta[0] == True:
            df.at[index, 'Empresa'] = consulta[1]
            df.at[index, 'Pesquisa'] = consulta[2]
            df.at[index, 'Modelo'] = consulta[3]
            print(razao_social, cnpj, empresa_p, pesquisa_p, modelo_p)
            df.to_csv('empresas.csv', sep=';', encoding='utf-8', index=False)
        else:
            pass
