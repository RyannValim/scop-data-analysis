from typing import List
import numpy as np
import pandas as pd

def analisar_padroes_clusters(
    df_dados: pd.DataFrame,
    rotulos_clusters: np.ndarray,
    nome_coluna_classe: str = "classe",
    n_top_kmers: int = 3
) -> None:
    df_temp = df_dados.copy()
    df_temp["cluster"] = rotulos_clusters

    colunas_kmers: List[str] = [
        c for c in df_temp.columns
        if c not in [nome_coluna_classe, "cluster"]
    ]

    total_instancias = df_temp.shape[0]

    print("\n===== Análise de Padrões por Cluster =====")
    for id_cluster, grupo in df_temp.groupby("cluster"):
        num_instancias = grupo.shape[0]
        proporcao = (num_instancias / total_instancias) * 100.0

        medias_kmers = grupo[colunas_kmers].mean().sort_values(ascending=False)
        kmers_representativos = list(medias_kmers.head(n_top_kmers).index)

        serie_classes = grupo[nome_coluna_classe].value_counts()
        classe_predominante = serie_classes.idxmax()
        freq_classe_pred = serie_classes.max()

        print(f"\nCluster {id_cluster}:")
        print(f"  - Número de instâncias: {num_instancias} ({proporcao:.2f}%)")
        print(f"  - k-mers mais representativos: {', '.join(kmers_representativos)}")
        print(f"  - Classe real predominante: {classe_predominante} (freq = {freq_classe_pred})")