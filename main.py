"""
main.py
-------

Arquivo principal do projeto de análise de dados SCOP.

Pipeline geral:
1. Leitura dos arquivos FASTA (SCOP) -> (classe, sequência)
2. Geração de k-mers com salto -> matriz binária de presença/ausência
3. Pré-processamento -> normalização + codificação de rótulos
4. Otimização da clusterização (KMeans) usando amostra + PCA + métricas interna/externa
5. PCA no conjunto completo + KMeans com melhores parâmetros
6. Análise dos padrões de k-mers e classes por cluster
7. Visualização 2D (PCA) colorida por cluster
"""

from pathlib import Path
from sklearn.cluster import KMeans
from src.leitura_fasta import carregar_sequencias_fasta
from src.kmers import construir_matriz_binaria_kmers
from src.preprocessamento import pre_processar_dados
from src.pca_reducao import aplicar_pca
from src.otimizar_kmers import otimizar_clusterizacao_kmeans
from src.analisar_clusters import analisar_padroes_clusters
from src.grafico_pca import plotar_pca_clusters

def selecionar_dataset() -> Path:
    pasta_raw = Path("data") / "raw"
    arquivos = sorted([f for f in pasta_raw.iterdir() if f.is_file()])

    print("Qual dataset iremos analisar?\n")

    for i, arquivo in enumerate(arquivos, start=1):
        print(f"    ({i}) {arquivo.name}")

    print()
    escolha = int(input("Escolha o dataset: "))

    if escolha < 1 or escolha > len(arquivos):
        raise ValueError("Escolha inválida!")

    return arquivos[escolha - 1]

def executar_pipeline_analise():
    print("===== Iniciando pipeline de análise SCOP =====")

    # 1) Escolha do dataset
    print("\n[1] Selecionando dataset...\n")
    caminho_dataset = selecionar_dataset()
    print(f"\nDataset escolhido: {caminho_dataset}\n")

    # 2) Leitura das sequências FASTA
    print("[2] Lendo sequências do arquivo...")
    lista_rotulo_sequencia = carregar_sequencias_fasta(str(caminho_dataset))
    print(f"Total de sequências carregadas: {len(lista_rotulo_sequencia)}")

    # 3) Geração de k-mers e construção da matriz binária
    print("\n[3] Construindo matriz binária de k-mers (aguarde)...")
    df_kmers = construir_matriz_binaria_kmers(
        lista_rotulo_sequencia,
        salto=1,
        mostrar_progresso=True
    )
    print(f"Matriz de k-mers: {df_kmers.shape[0]} linhas x {df_kmers.shape[1]} colunas")

    # 4) Pré-processamento
    print("\n[4] Pré-processando dados (normalização + label encoding)...")
    X_normalizado, y_codificado, codificador, normalizador = pre_processar_dados(
        df_kmers, nome_coluna_classe="classe"
    )
    print(f"Shape de X_normalizado: {X_normalizado.shape}")

    # 5) Otimização do KMeans
    print("\n[5] Otimizando clusterização (KMeans + PCA + métricas)...")
    df_otimizacao = otimizar_clusterizacao_kmeans(
        X_normalizado=X_normalizado,
        y_verdadeiro=y_codificado,
        n_componentes_pca=100,
        tamanho_amostra=5000,
        lista_n_clusters=[3, 5, 8],
        seed=42
    )

    if df_otimizacao.empty:
        print("\n⚠️ Nenhum parâmetro válido encontrado. Encerrando pipeline.")
        return

    melhores_parametros = df_otimizacao.iloc[0]["Parâmetros"]
    print("\n===== Melhores parâmetros =====")
    print(melhores_parametros)

    # 6) PCA completo + treinamento final do KMeans
    print("\n[6] Aplicando PCA no conjunto completo...")
    X_pca_completo, modelo_pca = aplicar_pca(
        X_normalizado,
        n_componentes=100,
        seed=42
    )
    print(f"Shape PCA completo: {X_pca_completo.shape}")

    print("[6] Treinando KMeans final...")
    kmeans_final = KMeans(**melhores_parametros)
    rotulos_clusters = kmeans_final.fit_predict(X_pca_completo)

    # 7) Análise dos clusters
    print("\n[7] Analisando clusters...")
    analisar_padroes_clusters(
        df_dados=df_kmers,
        rotulos_clusters=rotulos_clusters,
        nome_coluna_classe="classe",
        n_top_kmers=3
    )

    # 8) Visualização 2D com PCA
    print("\n[8] Plotando PCA 2D...\n")
    plotar_pca_clusters(X_pca_completo, rotulos_clusters)

    print("\n===== Pipeline concluída com sucesso! =====")

if __name__ == "__main__":
    executar_pipeline_analise()