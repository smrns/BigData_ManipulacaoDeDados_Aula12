import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

try:
    print('Obtendo os dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    print('Dados carregados com sucesso!')

    # Agrupando por município para obter o total de roubos de veículos
    df_roubo_municipio = df_ocorrencias.groupby('munic')['roubo_veiculo'].sum().reset_index()
    array_roubo_veiculo = df_roubo_municipio['roubo_veiculo'].to_numpy()

except Exception as e:
    print(f'Erro ao obter/processar os dados: {e}')
    exit()

try:
    # Medidas Básicas e de Posição
    media_roubo_veiculo = df_roubo_municipio['roubo_veiculo'].mean()
    mediana_roubo_veiculo = df_roubo_municipio['roubo_veiculo'].median()
    distancia = abs(media_roubo_veiculo - mediana_roubo_veiculo)
    minimo = df_roubo_municipio['roubo_veiculo'].min()
    maximo = df_roubo_municipio['roubo_veiculo'].max()
    amplitude = maximo - minimo

    # Quartis e Limites (Outliers)
    q1 = df_roubo_municipio['roubo_veiculo'].quantile(0.25)
    q3 = df_roubo_municipio['roubo_veiculo'].quantile(0.75)
    iqr = q3 - q1
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)
    
    if limite_inferior < 0: 
        limite_inferior = 0

    
    assimetria = df_roubo_municipio['roubo_veiculo'].skew()
    curtose = df_roubo_municipio['roubo_veiculo'].kurt() 
    variancia = df_roubo_municipio['roubo_veiculo'].var()
    desvio_padrao = df_roubo_municipio['roubo_veiculo'].std()
    coef_variacao = (desvio_padrao / media_roubo_veiculo) * 100
    
    distancia_media_variancia = (abs(media_roubo_veiculo - desvio_padrao) / media_roubo_veiculo) * 100

  
    print('\n' + '='*50)
    print('ANÁLISE ESTATÍSTICA COMPLETA')
    print('='*50)
    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Variância: {variancia:.2f}')
    print(f'Desvio Padrão: {desvio_padrao:.2f}')
    print(f'Assimetria (Pandas): {assimetria:.2f}')
    print(f'Curtose (Pandas): {curtose:.2f}')

except Exception as e:
    print(f'Erro ao calcular as informações estatísticas: {e}')
    exit()

try:
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))


    plt.subplot(2, 2, 1)
    
    df_top10_maiores = df_roubo_municipio.sort_values(by='roubo_veiculo', ascending=False).head(10)
    df_top10_maiores = df_top10_maiores.sort_values(by='roubo_veiculo', ascending=True)
    
    plt.barh(df_top10_maiores['munic'], df_top10_maiores['roubo_veiculo'], color='#1f77b4')

   
    deslocamento = max(df_top10_maiores['roubo_veiculo']) * 0.01
    for i, valor in enumerate(df_top10_maiores['roubo_veiculo']):
        plt.text(
            valor + deslocamento, 
            i, 
            f'{valor:,}',
            ha='left', 
            va='center',
            fontsize=9,
            fontweight='bold'
        )

    plt.title('Cidades com Maiores Casos de Roubos', fontsize=12, fontweight='bold')
    plt.xlabel('Total de Roubos')

    plt.subplot(2, 2, 2) 

    plt.hist(array_roubo_veiculo, bins=30, color='#aec7e8', edgecolor='black', alpha=0.7)
    plt.axvline(media_roubo_veiculo, color='green', linewidth=2, linestyle='--', label=f'Média ({media_roubo_veiculo:.1f})')
    plt.axvline(mediana_roubo_veiculo, color='orange', linewidth=2, linestyle='-', label=f'Mediana ({mediana_roubo_veiculo:.1f})')

    plt.title('Histograma de Roubos por Município', fontsize=12, fontweight='bold')
    plt.xlabel('Quantidade de Roubos')
    plt.ylabel('Frequência (Nº de Municípios)')
    plt.legend()

    
    contagens, limites = np.histogram(array_roubo_veiculo, bins=30)
    print('\nFaixas do Histograma:')
    for i in range(len(contagens)):
        if contagens[i] > 0:
            print(f'Faixa {i+1}: {limites[i]:.0f} até {limites[i+1]:.0f} roubos => {contagens[i]} municípios')

    plt.subplot(2, 2, 3)
    
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True, showfliers=False,
                patch_artist=True, boxprops=dict(facecolor='#c7e9b4'))
    plt.title('Boxplot dos Roubos por Municípios (Sem Outliers)', fontsize=12, fontweight='bold')
    plt.xlabel('Total de Roubos')
    plt.yticks([]) 
  
    plt.subplot(2, 2, 4) 
    
    plt.text(0.05, 0.90, f'Média: {media_roubo_veiculo:.2f}', fontsize=10)
    plt.text(0.05, 0.80, f'Mediana: {mediana_roubo_veiculo:.2f}', fontsize=10)
    plt.text(0.05, 0.70, f'Distância Média/Med: {distancia:.2f}', fontsize=10)
    plt.text(0.05, 0.60, f'Menor Valor: {minimo}', fontsize=10)
    plt.text(0.05, 0.50, f'Limite Inferior: {limite_inferior:.2f}', fontsize=10)
    plt.text(0.05, 0.40, f'Q1 (25%): {q1:.2f}', fontsize=10)
    plt.text(0.05, 0.30, f'Q3 (75%): {q3:.2f}', fontsize=10)
    plt.text(0.05, 0.20, f'Limite Superior: {limite_superior:.2f}', fontsize=10)
    plt.text(0.05, 0.10, f'Maior Valor: {maximo}', fontsize=10)
    plt.text(0.05, 0.00, f'Amplitude Total: {amplitude}', fontsize=10)

    plt.text(0.55, 0.90, f'Assimetria: {assimetria:.2f}', fontsize=10, fontweight='bold')
    plt.text(0.55, 0.80, f'Curtose: {curtose:.2f}', fontsize=10, fontweight='bold')
    plt.text(0.55, 0.70, f'Variância: {variancia:.2f}', fontsize=10, fontweight='bold')
    plt.text(0.55, 0.60, f'Dist. Média/Desvio: {distancia_media_variancia:.2f} %', fontsize=10)
    plt.text(0.55, 0.50, f'Desvio Padrão: {desvio_padrao:.2f}', fontsize=10, fontweight='bold')
    plt.text(0.55, 0.40, f'Coef. de Variação: {coef_variacao:.2f} %', fontsize=10, fontweight='bold')

    plt.title('Resumo Estatístico Final', fontsize=12, fontweight='bold', color='darkred')
    plt.axis('off') 

    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f'Erro ao renderizar os gráficos: {e}')
    exit()