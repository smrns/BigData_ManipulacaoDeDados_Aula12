import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

try:
    print('Obtendo os dados...')

    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    print('Dados carregados com sucesso!')

    df_recuperacao = df_ocorrencias.groupby('cisp')['recuperacao_veiculos'].sum().reset_index()

except Exception as e:
    print(f'Erro ao obter os dados: {e}')
    exit()


try:

    media = df_recuperacao['recuperacao_veiculos'].mean()
    mediana = df_recuperacao['recuperacao_veiculos'].median()
    desvio_padrao = df_recuperacao['recuperacao_veiculos'].std()
    coef_variacao = (desvio_padrao / media) * 100

    print('\n' + '='*50)
    print('ANÁLISE ESTATÍSTICA PARA O SECRETÁRIO')
    print('='*50)
    print(f'Média de recuperações por DP: {media:.2f}')
    print(f'Mediana de recuperações por DP: {mediana:.2f}')
    print(f'Desvio Padrão: {desvio_padrao:.2f}')
    print(f'Coeficiente de Variação: {coef_variacao:.2f}%')

    if coef_variacao > 30:
        print('-> CONCLUSÃO: NÃO existe um padrão. Os dados são ALTAMENTE DISPERSOS.')
    else:
        print('-> CONCLUSÃO: Existe um padrão homogêneo entre as delegacias.')

    Q1 = df_recuperacao['recuperacao_veiculos'].quantile(0.25)
    Q2 = df_recuperacao['recuperacao_veiculos'].quantile(0.50)
    Q3 = df_recuperacao['recuperacao_veiculos'].quantile(0.75)
    IQR = Q3 - Q1
    limite_superior = Q3 + (1.5 * IQR)

    outliers_acima = df_recuperacao[df_recuperacao['recuperacao_veiculos'] > limite_superior].sort_values(by='recuperacao_veiculos', ascending=False)

    print('\n' + '='*60)
    print('DELEGACIAS QUE FOGEM TOTALMENTE DO PADRÃO (OUTLIERS)')
    print('='*60)
    print(f'Limite estatístico superior para ser discrepante: {limite_superior:.2f} recuperações')
    print(f'Total de delegacias que superam esse limite: {len(outliers_acima)}')
    print('='*60)
    print(outliers_acima.to_string(index=False, header=['Nº da Delegacia (CISP)', 'Total de Veículos Recuperados']))

    maiores = df_recuperacao.sort_values(by='recuperacao_veiculos', ascending=False).head(5)
    menores = df_recuperacao.sort_values(by='recuperacao_veiculos', ascending=True).head(5)

    print('\n' + '='*60)
    print('RANKING DAS EXTREMIDADES (MAIORES E MENORES)')
    print('='*60)
    print('--- AS 5 DELEGACIAS COM MAIS RECUPERAÇÕES ---')
    print(maiores.to_string(index=False, header=['CISP (DP)', 'Recuperações']))
    print('\n--- AS 5 DELEGACIAS COM MENOS RECUPERAÇÕES ---')
    print(menores.to_string(index=False, header=['CISP (DP)', 'Recuperações']))


    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Estudo Estatístico: Recuperação de Veículos por Delegacia (CISP/RJ)', fontsize=16, fontweight='bold', color='#1a1a1a')

    box_props = dict(linestyle='-', linewidth=2, color='#1f77b4', facecolor='#e1f3fd')
    flier_props = dict(marker='o', markerfacecolor='#d62728', markersize=6, linestyle='none', markeredgecolor='#d62728')
    median_props = dict(linestyle='-', linewidth=2.5, color='#ff7f0e')
    whisker_props = dict(linestyle='--', linewidth=1.5, color='#7f7f7f')
    
    ax1.boxplot(df_recuperacao['recuperacao_veiculos'], patch_artist=True,
                boxprops=box_props, flierprops=flier_props, 
                medianprops=median_props, whiskerprops=whisker_props)
    
    ax1.set_title('Distribuição e Discrepâncias Históricas\n(Pontos Vermelhos são as DPs Outliers)', fontsize=12, fontweight='bold', pad=10)
    ax1.set_ylabel('Total de Veículos Recuperados', fontsize=11)
    ax1.set_xticklabels(['Todas as Delegacias (CISPs)'])
    ax1.grid(axis='y', linestyle=':', alpha=0.6)


    top_10 = df_recuperacao.sort_values(by='recuperacao_veiculos', ascending=False).head(10)
    
    nomes_cisp = [f"CISP {int(c)}" for c in top_10['cisp']]
    
   
    cores = plt.cm.Reds(np.linspace(0.7, 0.4, 10))
    
    barras = ax2.bar(nomes_cisp, top_10['recuperacao_veiculos'], color=cores, edgecolor='#7f7f7f', linewidth=0.7)
    
    for barra in barras:
        altura = barra.get_height()
        ax2.annotate(f'{int(altura)}',
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax2.set_title('Top 10 Delegacias com Maior Volume\nde Veículos Recuperados', fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel('Unidade Policial (CISP)', fontsize=11)
    ax2.set_ylabel('Total de Veículos Recuperados', fontsize=11)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', linestyle=':', alpha=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


except Exception as e:
    print(f'Erro ao calcular as informações...: {e}')
    exit()
