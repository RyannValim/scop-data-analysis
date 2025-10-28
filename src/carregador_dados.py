import re
from collections import Counter

def carregar_fasta(caminho_fasta: str):
    """
    Lê um arquivo FASTA e devolve 3 listas alinhadas:
      - cabecalhos: cada linha que começa com '>'
      - sequencias: todas as linhas seguintes concatenadas até o próximo '>'
      - classes: extraídas do início do header (ex.: 'a.1.1.1' ou 'desconhecida')
    """
    cabecalhos, sequencias, classes = [], [], []

    # Expressão regular para capturar algo como 'a.1.1.1' ou 'b.2.3.4'
    padrao_classe = re.compile(r"[a-z]\.\d+(?:\.\d+){0,2}", re.IGNORECASE)

    try:
        with open(caminho_fasta, "r", encoding="utf-8", errors="ignore") as arq:
            cab_atual = None
            seq_atual = []

            for linha in arq:
                linha = linha.strip()
                if not linha:
                    continue  # ignora linhas vazias

                if linha.startswith(">"):  # novo cabeçalho encontrado
                    # salva o registro anterior (se houver)
                    if cab_atual and seq_atual:
                        sequencia = "".join(seq_atual).upper()
                        cabecalhos.append(cab_atual)
                        sequencias.append(sequencia)

                        # extrai classe do cabeçalho
                        m = padrao_classe.search(cab_atual.replace(" ", ""))
                        classes.append(m.group(0) if m else "desconhecida")

                    # prepara novo cabeçalho
                    cab_atual = linha[1:].strip()  # remove o '>'
                    seq_atual = []
                else:
                    seq_atual.append(linha.strip())

            # salva o último registro do arquivo
            if cab_atual and seq_atual:
                sequencia = "".join(seq_atual).upper()
                cabecalhos.append(cab_atual)
                sequencias.append(sequencia)
                m = padrao_classe.search(cab_atual.replace(" ", ""))
                classes.append(m.group(0) if m else "desconhecida")

        print(f"✅ {len(sequencias)} sequências carregadas de {caminho_fasta}")
        return cabecalhos, sequencias, classes

    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho_fasta}")
        return [], [], []

def estatisticas_basicas(sequencias, classes):
    """Mostra estatísticas simples das sequências e das classes."""
    if not sequencias:
        print("⚠️ Nenhuma sequência carregada.")
        return

    tamanhos = [len(s) for s in sequencias]
    print("\n=== ESTATÍSTICAS BÁSICAS ===")
    print(f"Total de sequências: {len(sequencias)}")
    print(f"Tamanho mínimo/máximo/médio: {min(tamanhos)} / {max(tamanhos)} / {sum(tamanhos)/len(tamanhos):.1f}")

    contagem = Counter(classes)
    print("\nTop 10 classes:")
    for c, q in contagem.most_common(10):
        print(f"  {c:<12} {q}")
