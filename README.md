# scop-data-analysis
Atividade de análise de dados para a disciplina de Tópicos Especiais em Software.

Realizar análise de dados utilizando as técnicas discutidas em sala sobre não-supervisionado utilizando clusters. Utilize as IAs generativas para auxiliar na criação do código.

#Passos:
  -Entrar no site https://scop.berkeley.edu/astral/ver=2.08 e baixar a versão do banco de dados de sequências de proteínas, a base é de texto puro com header seguido de sequência.  Cada classe é definida pelos primeiros elementos do header;
  -Extrair os atributos de sequência segundo o que fizemos em sala, um kmer de 2X2, onde 2 são os pares de aminoácidos, e X é um skip. Fazer uma janela móvel deste kmer que extraia ausência e presença de todos os elementos das sequências e a transforme em uma matrix binária com todas as combinações possíveis;
  -Projetar a matriz geradas em uma base de PCA utilizando os 300 componentes principais;
  -Realizar a escolha do algoritmo de cluster rodando todos os algoritmos do sci-kit no python, calculando as métricas internas e as correlacionando com a métrica externa F1-Score;
  -Variar os parâmetros para obter a melhor métrica interna e sugerir a melhor configuração de clusters.

#Avaliação:
  -Fazer um vídeo apresentando como chegou à conclusão do melhor algoritmo;
  -A consistência da metodologia utilizada para a escolha não subjetiva do método é o fator de avaliação;
  -Entregar o projeto via GitHub ou em .zip no blackboard.
