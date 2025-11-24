let chartFreq = null;
let chartTfidf = null;

function atualizarStatus(msg) {
    document.getElementById("status").innerText = msg;
}

async function postData(url) {
    const resp = await fetch(url, { method: "POST" });
    return resp.json();
}

document.getElementById("btn-coletar").onclick = async () => {
    atualizarStatus("Coletando notícias...");
    const data = await postData("/coletar");

    if (data.status === "ok") {
        atualizarStatus(`Coleta concluída — ${data.total} notícias.`);
        document.getElementById("summary-content").innerText =
            `${data.total} notícias coletadas.`;

        document.getElementById("btn-processar").disabled = false;
    } else {
        atualizarStatus("Erro na coleta.");
    }
};


document.getElementById("btn-processar").onclick = async () => {
    atualizarStatus("Processando corpus...");
    const data = await postData("/processar");

    if (data.status === "ok") {
        atualizarStatus("Pré-processamento concluído.");
        document.getElementById("btn-bow").disabled = false;
    } else {
        atualizarStatus("Erro no pré-processamento.");
    }
};


document.getElementById("btn-bow").onclick = async () => {
    atualizarStatus("Calculando BOW e TF-IDF...");
    const data = await postData("/bow");

    if (data.status !== "ok") {
        atualizarStatus("Erro ao calcular BOW/TF-IDF.");
        return;
    }

    atualizarStatus("BOW e TF-IDF concluídos.");
    document.getElementById("btn-topicos").disabled = false;

    plotarGraficos(data.top_freq, data.top_tfidf);
};


document.getElementById("btn-topicos").onclick = async () => {
    atualizarStatus("Gerando tópicos...");
    const data = await postData("/topicos");

    if (data.status !== "ok") {
        atualizarStatus("Erro ao gerar tópicos.");
        return;
    }

    atualizarStatus("Tópicos gerados.");

    formatarTopicos(data.topicos);
};

function formatarTopicos(topicos) {
    const container = document.getElementById("insights-text");
    container.innerHTML = "";

    topicos.forEach((topico, index) => {
        const topicoDiv = document.createElement("div");
        topicoDiv.className = "topico-card";
        
        const titulo = document.createElement("h3");
        titulo.textContent = `Tópico ${index + 1}`;
        topicoDiv.appendChild(titulo);

        const lista = document.createElement("ol");
        topico.forEach(([palavra, peso]) => {
            const item = document.createElement("li");
            item.innerHTML = `<strong>${palavra}</strong>: ${peso.toFixed(2)}`;
            lista.appendChild(item);
        });

        topicoDiv.appendChild(lista);
        container.appendChild(topicoDiv);
    });
}

function plotarGraficos(freq, tfidf) {

    const freqLabels = freq.map(x => x[0]);
    const freqValues = freq.map(x => x[1]);

    const tfidfLabels = tfidf.map(x => x[0]);
    const tfidfValues = tfidf.map(x => x[1]);

    if (chartFreq) chartFreq.destroy();
    if (chartTfidf) chartTfidf.destroy();

    chartFreq = new Chart(document.getElementById("chartFreq"), {
        type: "bar",
        data: {
            labels: freqLabels,
            datasets: [{
                label: "Frequência",
                data: freqValues
            }]
        }
    });

    chartTfidf = new Chart(document.getElementById("chartTfidf"), {
        type: "bar",
        data: {
            labels: tfidfLabels,
            datasets: [{
                label: "TF-IDF",
                data: tfidfValues
            }]
        }
    });
}
