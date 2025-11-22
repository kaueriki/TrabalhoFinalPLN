def gerar_topicos(bow, tfidf, n_top_palavras=10, n_topicos=3):
    """
    - Ordena palavras por score combinado = tfidf * freq
    - Divide as palavras em grupos (tópicos)
    """

    # Calcula score combinado
    scores = {}
    for palavra in bow:
        freq = bow[palavra]
        t = tfidf.get(palavra, 0.0)
        score = freq * t
        scores[palavra] = score

    # Ordena por score
    top_palavras = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Mantém apenas as principais
    palavras_selecionadas = [p for p, _ in top_palavras[:n_top_palavras * n_topicos]]

    # Quebra em "tópicos" simples
    topicos = []
    for i in range(n_topicos):
        inicio = i * n_top_palavras
        fim = inicio + n_top_palavras
        topicos.append(palavras_selecionadas[inicio:fim])

    return topicos
