import pandas as pd
df = pd.read_csv('/home/rafalinux/Downloads/estudopython/GSPC.csv')


#apagando a 1a coluna, DATA, pois não serve
df = df.drop('Date', axis=1)
#print(df[-2::])   #conferir as ultimas duas linhas

"""vamos lidar como se a linha 17216 fosse o dia de hoje, e a última fosse amanha, 
faremos isso para prever, logo excluiremos a ultima linha """

amanha = df[-1::] #criando a variavel que guardara a ultima linha da base df

base = df.drop(df[-1::].index, axis=0)   #guardando todos os dados exceto a ultima linha
#print(base.tail())  #ultimas 5 linhas do dataset

"""o que pretendemos prever é se o fechamento de amanha sera maior ou menor que o fechamento de hoje,
NAO PODEMOS UTILIZAR A COLUNA CLOSE COMO A VARIAVEL TARGET POIS AINDA NAO SABEMOS QUAL SERA O VALOR DELA,
MESMO TENDO O VALOR DE ABERTURA, SO TEREMOS DE FATO O FECHAMENTO NO FECHAMENTO
LOGO É NECESSARIO QUE SEJA FEITA UMA VARIAVEL TARGET COM O VALOR DA VARIAVEL CLOSE, PARA ASSIM
SER UTILIZADA, IREMOS SALVAR ESSE CONTEUDO EM OUTRA COLUNA, MAS NAO DO MESMO JEITO, E SIM COM UM 
INDICE DIFERENTE, A TARGET É A VARIAVEL PREVENDO O DIA DE AMANHA, LOGO NA LINHA 17216 O VALOR DE TARGET É
NaN POIS SO AMANHA É QUE SABEREMOS O VALOR DE FECHAMENTO """

base['target'] = base['Close'][1:len(base)].reset_index(drop=True) #[1:len(base)]  serve para não começar a salva do indice 0, e sim do indice 1
#reset_index serve para resetar os indices

"""VAMOS SEPARAR A LINHA 17216 POIS ELA NAO SERÁ POSSIVEL UTLIZAR NO TREINAMENTO E SIM A LINHA QUE QUEREMOS PREVER
UTLIZANDO A VARIAVEL TARGET"""

prev = base[-1::].drop('target', axis=1)
#print(prev)

treino = base.drop(base[-1::].index, axis=0) #retirando de novo a última linha da base
#print(treino.tail())

"""Não precisamentos saber o valor exato, só precisamos saber se irá subir ou cair o valor de target, logo aplicaremos um filtro
na base para que os valores se convertam em apenas 0 e 1"""

treino.loc[treino['target'] > treino['Close'], 'target'] = 1 #significa que teve um aumento

treino.loc[treino['target'] != 1, 'target'] = 0  #se diferente de 1 teve um abaixo
#print(treino.tail())

y = treino['target']
x = treino.drop('target', axis=1)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

from sklearn.ensemble import ExtraTreesClassifier
modelo = ExtraTreesClassifier()
modelo.fit(x_train, y_train)

resultado = modelo.score(x_test, y_test)
print('Acurácia:', resultado)


ESSE MODELO DE ML QUE DEU CERTO PARA OS VINHOS NÃO DEU CERTO COM OS DADOS DE AÇOES PORQUE TEVE UMA ACURACIA DE 50%


MELHORANDO O MODELO:


def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

import pandas as pd

prev = pd.read_csv('/home/rafalinux/Downloads/estudopython/prev.csv')
print('Fechamento anterior', prev['Close'][0])
print('Previsão anterior:', prev['target'][0])

base = pd.read_csv('/home/rafalinux/Downloads/estudopython/hoje.csv')

try:
    amanha = pd.read_csv('/home/rafalinux/Downloads/estudopython/futuro.csv')
    print('Fechamento atual:', amanha['Close'][0])
    base = base.append (amanha[:1], sort=True)
    amanha = amanha.drop(amanha[:1].index, axis=0)
    base.to_csv('/home/rafalinux/Downloads/estudopython/hoje.csv', index=False)
    amanha.to_csv ('/home/rafalinux/Downloads/estudopython/futuro.csv', index=False)
except Exception:
    print ('O fechamento ainda não ocorreu!')
    pass

base['target'] = base['Close'][1:len(base)].reset_index(drop=True) #[1:len(base)]  serve para não começar a salva do indice 0, e sim do indice 1
prev = base[-1::].drop('target', axis=1)
treino = base.drop(base[-1::].index, axis=0) #retirando de novo a última linha da base
treino.loc[treino['target'] > treino['Close'], 'target'] = 1 #significa que teve um aumento
treino.loc[treino['target'] != 1, 'target'] = 0  #se diferente de 1 teve um abaixo


y = treino['target']
x = treino.drop('target', axis=1)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)

from sklearn.ensemble import ExtraTreesClassifier
modelo = ExtraTreesClassifier()
modelo.fit(x_train, y_train)

print('Acurácia:', modelo.score(x_test, y_test))

prev['target'] = modelo.predict(prev)
print('Fechamento de ontem:', prev['Close'][0])

if prev['target'][0] == 1:
    print('VAI SUBIR!!')
else:
    print('vai cair')

prev.to_csv('/home/rafalinux/Downloads/estudopython/prev.csv', index=False)