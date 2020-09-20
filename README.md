# Requisitos

- Conversão do formato dos arquivos: Converter o arquivo CSV presente no diretório data/input/users/load.csv, para um formato colunar de alta performance de leitura de sua escolha. Justificar brevemente a escolha do formato;

Foi escolhido o formato `parquet`, pois o Apache Parquet foi projeto para oferecer um armazenamento colunar eficiente comparado com arquivos em linhas como por exemplo o `csv`, além disso o Apache Parquet foi desenvolvido com um suporte a esquemas como compactaçao, o Apache Spark compacta no formato snappy por padrão os arquivos Parquet gerados.

- Deduplicação dos dados convertidos: No conjunto de dados convertidos haverão múltiplas entradas para um mesmo registro, variando apenas os valores de alguns dos campos entre elas. Será necessário realizar um processo de deduplicação destes dados, a fim de apenas manter a última entrada de cada registro, usando como referência o id para identificação dos registros duplicados e a data de atualização (update_date) para definição do registro mais recente;

Foi desenvolvido um [script em PySpark](main.py) que faz a conversão do `csv` para `Parquet` e realiza a deduplicação.

- Conversão do tipo dos dados deduplicados: No diretório config haverá um arquivo JSON de configuração (types_mapping.json), contendo os nomes dos campos e os respectivos tipos desejados de output. Utilizando esse arquivo como input, realizar um processo de conversão dos tipos dos campos descritos, no conjunto de dados deduplicados;

No script PySpark foi desenvolvido uma conversão desacoplada, onde é possível adicionar novos campos para serem realizados a conversão, o quê foi feito com o campo `id` que estava com string, e o incluí para que fosse convertido para `integer`.

# Escalando o script

O script desenvolvido pode ser colocado para rodar em serviços em Cloud, irei focar nos serviços AWS, pois é a Cloud que eu tenho mais conhecimento e quero focar por hora.

A maneira mais robusta de escalar esse script é utilizar o `EMR`, um serviço gerenciado da AWS para execução de elástica de operações Map/Reduce, eu usaria o serviço gerenciado de cluster Spark, com os arquivos csv que fossem necessário entrar no Data Lake, colocando esses csv num bucket chamado de `raw`, onde ficariam os dados originais sem a conversão, e criaria um bucket chamado `data`, onde iam ficar os arquivos já convertidos e com as devidas regras, como por exemplo, uma deduplicaçao e salvos em Parquet comprimidos em Snappy.
