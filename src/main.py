from pathlib import Path
from carregador_dados import carregar_fasta, estatisticas_basicas
from extrator_atributos import montar_matriz_binaria, normalizar, reduzir_pca
from analise import (composicao_aminoacidos, comparar_listas_ids,
                     rodar_kmeans, avaliar_silhueta, grafico_pca_clusters,
                     dashboard_exploratorio)

DATA_RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

def escolher_arquivo(pergunta="Digite o nome do arquivo que aparece acima (ex.: arquivo.txt): "):
    print(f"\nArquivos em {DATA_RAW}:")
    for p in sorted(DATA_RAW.glob("*.txt")):
        print(" -", p.name)
    nome = input(pergunta).strip()
    return str(DATA_RAW / nome)

def painel():
    cabecalhos, sequencias, classes = [], [], []
    while True:
        print("\n=== PAINEL DE EXPLORAÇÃO ===")
        print("1) Carregar base FASTA")
        print("2) Estatísticas básicas")
        print("3) Composição de aminoácidos (gráfico)")
        print("4) Comparar dois arquivos por ID")
        print("5) Clusterização (k-mer 2x2 → PCA → K-Means → Silhouette)")
        print("6) Dashboard exploratório (4 gráficos)\n")
        print("0) Sair\n")

        op = input("Escolha: ").strip()

        if op == "1":
            caminho = escolher_arquivo()
            cabecalhos, sequencias, classes = carregar_fasta(caminho)

        elif op == "2":
            if not sequencias: print("Carregue um arquivo primeiro."); continue
            estatisticas_basicas(sequencias, classes)

        elif op == "3":
            if not sequencias: print("Carregue um arquivo primeiro."); continue
            composicao_aminoacidos(sequencias)

        elif op == "4":
            a1 = escolher_arquivo("Primeiro arquivo: ")
            a2 = escolher_arquivo("Segundo arquivo: ")
            c1, s1, _ = carregar_fasta(a1)
            c2, s2, _ = carregar_fasta(a2)
            comparar_listas_ids(c1, c2)

        elif op == "5":
            if not sequencias: print("Carregue um arquivo primeiro."); continue
            print("→ Vetorizando com k-mer 2x2 (binário, presença/ausência)...")
            M = montar_matriz_binaria(sequencias, skip=2, limite_sequencias=400)
            X = normalizar(M)
            Xp, pca = reduzir_pca(X, n_componentes=300)
            print(f"PCA com {Xp.shape[1]} componentes úteis.")
            y, km = rodar_kmeans(Xp, k=5)
            sil = avaliar_silhueta(Xp, y)
            print(f"Silhouette = {sil:.4f}")
            grafico_pca_clusters(Xp, y, "Clusters K-Means (PCA)")

        elif op == "6":
            if not sequencias: print("Carregue um arquivo primeiro."); continue
            dashboard_exploratorio(sequencias, classes)

        elif op == "0":
            print("Programa encerrado."); break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    print("=== Análise de Proteínas • SCOP ===")
    painel()
