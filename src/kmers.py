from typing import List, Tuple
import numpy as np
import pandas as pd
from tqdm import tqdm

def gerar_kmers_com_salto(sequencia: str, salto: int = 1) -> List[str]:
    kmers: List[str] = []

    limite = len(sequencia) - (1 + salto)
    for i in range(limite):
        kmer = sequencia[i] + sequencia[i + salto + 1]
        kmers.append(kmer)

    return kmers

def construir_matriz_binaria_kmers(
    lista_rotulo_sequencia: List[Tuple[str, str]],
    salto: int = 1,
    mostrar_progresso: bool = True,
) -> pd.DataFrame:
    conjunto_todos_kmers = set()
    lista_kmers_por_sequencia: List[Tuple[str, List[str]]] = []

    iterador = lista_rotulo_sequencia
    if mostrar_progresso:
        iterador = tqdm(lista_rotulo_sequencia, desc="Gerando k-mers")

    for rotulo, sequencia in iterador:
        kmers = gerar_kmers_com_salto(sequencia, salto=salto)
        lista_kmers_por_sequencia.append((rotulo, kmers))
        conjunto_todos_kmers.update(kmers)

    lista_kmers_unicos = sorted(conjunto_todos_kmers)
    num_sequencias = len(lista_kmers_por_sequencia)
    num_kmers = len(lista_kmers_unicos)

    matriz_binaria = np.zeros((num_sequencias, num_kmers), dtype=np.uint8)

    mapa_kmer_para_indice = {k: i for i, k in enumerate(lista_kmers_unicos)}

    for indice_seq, (_, kmers) in enumerate(lista_kmers_por_sequencia):
        indices_kmers = [
            mapa_kmer_para_indice[k]
            for k in kmers
            if k in mapa_kmer_para_indice
        ]
        matriz_binaria[indice_seq, indices_kmers] = 1

    df_kmers = pd.DataFrame(matriz_binaria, columns=lista_kmers_unicos)

    df_kmers["classe"] = [rotulo for rotulo, _ in lista_kmers_por_sequencia]

    return df_kmers