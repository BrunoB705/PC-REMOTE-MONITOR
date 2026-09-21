function formatUptime(seconds) {
    const d = Math.floor(seconds / 86400);
    const h = Math.floor((seconds % 86400) / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    if (d > 0) return d + "d " + h + "h " + m + "m";
    if (h > 0) return h + "h " + m + "m";
    return m + "m";
}

function updateDashboard() {
    fetch("/api/metrics")
        .then(res => res.json())
        .then(data => {
            document.getElementById("cpu-usage").textContent = data.cpu.usage ?? "--";
            document.getElementById("cpu-temp").textContent = data.cpu.temperature ?? "N/A";
            document.getElementById("mem-used").textContent = data.memory.used;
            document.getElementById("mem-total").textContent = data.memory.total;
            document.getElementById("mem-pct").textContent = data.memory.percentage;

            const storageDiv = document.getElementById("storage-info");
            storageDiv.innerHTML = "";
            for (const [drive, info] of Object.entries(data.storage)) {
                if (info) {
                    storageDiv.innerHTML += `
                        <div class="storage-drive">
                            <p>${drive}: ${info.used} GB / ${info.total} GB (${info.percentage}%)</p>
                            <div class="storage-bar">
                                <div class="storage-fill" style="width: ${info.percentage}%"></div>
                            </div>
                        </div>`;
                }
            }

            document.getElementById("uptime").textContent = formatUptime(data.uptime);
        })
        .catch(err => console.error("Error:", err));
}

updateDashboard();
setInterval(updateDashboard, 2000);
