const BASE_URL = "https://YOUR-RENDER-URL.onrender.com";

const API_LIVE = `${BASE_URL}/api/data`;
const API_HISTORY = `${BASE_URL}/api/history`;

const chart = new Chart(document.getElementById("powerChart"), {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Power",
            data: [],
            borderColor: "red"
        }]
    }
});


async function loadHistory() {
    const res = await fetch(API_HISTORY);
    const data = await res.json();

    chart.data.labels = data.map(d => d.time);
    chart.data.datasets[0].data = data.map(d => d.power);

    chart.update();
}


async function updateLive() {
    const res = await fetch(API_LIVE);
    const data = await res.json();

    if (data.status === "no data") return;

    document.getElementById("voltage").innerText = data.voltage;
    document.getElementById("current").innerText = data.current;
    document.getElementById("power").innerText = data.power;
    document.getElementById("prediction").innerText = data.prediction;
}


loadHistory();
setInterval(updateLive, 3000);