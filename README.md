# Requisitos

#### Conversão do formato dos arquivos: Converter o arquivo CSV presente no diretório data/input/users/load.csv, para um formato colunar de alta performance de leitura de sua escolha. Justificar brevemente a escolha do formato;

Foi escolhido o formato `parquet`, pois o Apache Parquet foi projeto para oferecer um armazenamento colunar eficiente comparado com arquivos em linhas como por exemplo o `csv`, além disso o Apache Parquet foi desenvolvido com um suporte a esquemas de compactaçao, o Apache Spark compacta no formato snappy por padrão os arquivos Parquet gerados.

#### Deduplicação dos dados convertidos: No conjunto de dados convertidos haverão múltiplas entradas para um mesmo registro, variando apenas os valores de alguns dos campos entre elas. Será necessário realizar um processo de deduplicação destes dados, a fim de apenas manter a última entrada de cada registro, usando como referência o id para identificação dos registros duplicados e a data de atualização (update_date) para definição do registro mais recente;

Foi desenvolvido um [script em PySpark](main.py) que faz a conversão do `csv` para `Parquet` e realiza a deduplicação.

#### Conversão do tipo dos dados deduplicados: No diretório config haverá um arquivo JSON de configuração (types_mapping.json), contendo os nomes dos campos e os respectivos tipos desejados de output. Utilizando esse arquivo como input, realizar um processo de conversão dos tipos dos campos descritos, no conjunto de dados deduplicados;

No script PySpark foi desenvolvido uma conversão desacoplada, onde é possível adicionar novos campos para serem realizados a conversão, o quê foi feito com o campo `id` que estava com string, e o incluí para que fosse convertido para `integer`.

# Execução do script.

Codigo desenvolvido em PySpark, sendo necessário a versão do Python3, as instruções abaixo foram realizadas em ambiente Linux.

#### Instalando o ambiente virtual Python
```
pip install virtualenv
```

#### Criando o ambiente virtual

```
virtualenv -p python3 venv 
```

#### Habilitando o ambiente virtual

```
source ./venv/bin/activate
```


#### Instalando os pacotes a partir do requirement file

```
pip install -r requirements.txt
```
#### Execução local do script.

```
python main.py
```

Output esperado.

```
+---+--------------------+--------------------+---------------+--------------------+---+--------------------+--------------------+
| id|                name|               email|          phone|             address|age|         create_date|         update_date|
+---+--------------------+--------------------+---------------+--------------------+---+--------------------+--------------------+
|  3|spongebob.squarep...|Spongebob Squarep...|(11) 91234-5678|124 Conch Street,...| 13|2018-05-19 04:07:...|2018-05-19 05:08:...|
|  1|david.lynch@cogni...|         David Lynch|(11) 99999-9997|Mulholland Drive,...| 72|2018-03-03 18:47:...|2018-05-23 10:13:...|
|  2|sherlock.holmes@c...|     Sherlock Holmes|(11) 94815-1623|221B Baker Street...| 34|2018-04-21 20:21:...|2018-04-21 20:21:...|
+---+--------------------+--------------------+---------------+--------------------+---+--------------------+--------------------+
```

#### Desativando o ambiente virutal

```
deactivate
```

#### Removendo o ambiente

```
rm -rf venv
```

# Escalando o script

O script desenvolvido pode ser colocado para rodar em serviços em Cloud, irei focar nos serviços AWS, pois é a Cloud que eu tenho mais conhecimento e quero focar por hora.

A maneira mais robusta de escalar esse script é utilizar o `EMR`, um serviço gerenciado da AWS para execução de elástica de operações Map/Reduce, eu usaria o serviço gerenciado de cluster Spark, com os arquivos csv que fossem necessário entrar no Data Lake, colocando esses csv num bucket chamado de `raw`, onde ficariam os dados originais sem a conversão, e criaria um bucket chamado `data`, onde iam ficar os arquivos já convertidos e com as devidas regras, como por exemplo, uma deduplicaçao e salvos em Parquet comprimidos em Snappy.
