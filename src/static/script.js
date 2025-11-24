let pieChart = null;
let barCharts = [];

function atualizarStatus(msg) {
    document.getElementById("status").innerText = msg;
}

async function postData(url) {
    const resp = await fetch(url, { method: "POST" });
    return resp.json();
}

document.getElementById("btn-lda").onclick = async () => {
    atualizarStatus("Processando com LDA (coletando, processando e gerando tópicos)...");
    const data = await postData("/process");

    if (data.status === "ok") {
        atualizarStatus("Tópicos LDA gerados com sucesso!");
        document.getElementById("summary-content").innerText =
            "Pipeline LDA concluído: coleta, pré-processamento e modelagem.";
        
        exibirTopicos(data.topicos);
        plotarGraficos(data.chart_data);
    } else {
        atualizarStatus("Erro ao processar com LDA: " + data.mensagem);
    }
};

document.getElementById("btn-transformers").onclick = async () => {
    atualizarStatus("Processando com Transformers (coletando, processando e gerando tópicos)...");
    const data = await postData("/processtransformers");

    if (data.status === "ok") {
        atualizarStatus("Tópicos Transformers gerados com sucesso!");
        document.getElementById("summary-content").innerText =
            "Pipeline Transformers concluído: coleta, pré-processamento e modelagem.";
        
        exibirTopicos(data.topicos);
        plotarGraficos(data.chart_data);
    } else {
        atualizarStatus("Erro ao processar com Transformers: " + data.mensagem);
    }
};

function exibirTopicos(topicos) {
    let texto = "";
    topicos.forEach((topico, i) => {
        texto += `Tópico ${i + 1}:\n`;
        topico.forEach(([palavra, score]) => {
            texto += `  - ${palavra}: ${score.toFixed(4)}\n`;
        });
        texto += "\n";
    });
    document.getElementById("insights-text").innerText = texto;
}

function plotarGraficos(chartData) {
    // Limpa gráficos anteriores
    if (pieChart) pieChart.destroy();
    barCharts.forEach(chart => chart.destroy());
    barCharts = [];

    // Gráfico de pizza - distribuição de tópicos
    const pieCtx = document.getElementById("chartPie");
    if (pieCtx && chartData.pie_chart) {
        pieChart = new Chart(pieCtx, {
            type: "pie",
            data: {
                labels: chartData.pie_chart.labels,
                datasets: [{
                    data: chartData.pie_chart.data,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Distribuição de Tópicos'
                    }
                }
            }
        });
    }

    // Gráficos de barras - palavras por tópico
    const barContainer = document.getElementById("barChartsContainer");
    barContainer.innerHTML = ""; // Limpa container

    chartData.bar_charts.forEach((topico, i) => {
        const div = document.createElement("div");
        div.className = "chart-card";
        
        const h3 = document.createElement("h3");
        h3.textContent = topico.topic;
        div.appendChild(h3);
        
        const canvas = document.createElement("canvas");
        canvas.id = `chartBar${i}`;
        div.appendChild(canvas);
        
        barContainer.appendChild(div);
        
        const chart = new Chart(canvas, {
            type: "bar",
            data: {
                labels: topico.words,
                datasets: [{
                    label: "Score",
                    data: topico.scores,
                    backgroundColor: '#36A2EB'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        barCharts.push(chart);
    });
}
