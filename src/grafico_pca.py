import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plotar_pca_clusters(X_pca: np.ndarray, rotulos_clusters):
    if X_pca.shape[1] < 2:
        raise ValueError(
            "O PCA fornecido possui menos de 2 componentes. "
            "Não é possível gerar o gráfico 2D."
        )

    plt.figure(figsize=(10, 7))

    sns.scatterplot(
        x=X_pca[:, 0],
        y=X_pca[:, 1],
        hue=rotulos_clusters,
        palette="tab10",
        s=18,
        legend="full"
    )

    plt.title("Projeção PCA (2D) colorida por cluster")
    plt.xlabel("Componente Principal 1")
    plt.ylabel("Componente Principal 2")
    plt.legend(title="Cluster", fontsize=10)
    plt.tight_layout()
    plt.show()