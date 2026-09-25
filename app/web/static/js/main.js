async function updateDashboard() {
    try {
        const res = await fetch("/api/metrics");
        if (!res.ok) return;
        const data = await res.json();

        // CPU
        if (data.cpu) {
            if (data.cpu.usage !== null && data.cpu.usage !== undefined) {
                const cpuUsageEl = document.getElementById("cpu-usage");
                if (cpuUsageEl) {
                    cpuUsageEl.textContent = `${Math.round(data.cpu.usage)} %`;
                }
            }
            if (data.cpu.temperature !== null && data.cpu.temperature !== undefined) {
                const cpuTempEl = document.getElementById("cpu-temp");
                if (cpuTempEl) {
                    cpuTempEl.textContent = `${Math.round(data.cpu.temperature)} °C`;
                }
            }
        }

        // RAM
        if (data.memory) {
            const ramInfoEl = document.getElementById("ram-info");
            if (ramInfoEl) {
                const used = data.memory.used;
                const total = Math.round(data.memory.total);
                const pct = Math.round(data.memory.percentage);
                ramInfoEl.textContent = `${used} / ${total} GB (${pct}%)`;
            }
        }

        // GPU (if supported in future responses)
        if (data.gpu) {
            if (data.gpu.name) {
                const gpuNameEl = document.getElementById("gpu-name");
                if (gpuNameEl) gpuNameEl.textContent = data.gpu.name;
            }
            if (data.gpu.temperature !== null && data.gpu.temperature !== undefined) {
                const gpuTempEl = document.getElementById("gpu-temp");
                if (gpuTempEl) gpuTempEl.textContent = `${Math.round(data.gpu.temperature)} °C`;
            }
            if (data.gpu.usage !== null && data.gpu.usage !== undefined) {
                const gpuUsageEl = document.getElementById("gpu-usage");
                if (gpuUsageEl) gpuUsageEl.textContent = `${Math.round(data.gpu.usage)} %`;
            }
        }

        // Motherboard
        if (data.motherboard &&
            data.motherboard.temperature !== null &&
            data.motherboard.temperature !== undefined) {
            const moboTempEl = document.getElementById("mobo-temp");
            if (moboTempEl) moboTempEl.textContent = `${Math.round(data.motherboard.temperature)} °C`;
        }
    } catch (err) {
        console.error("Error fetching metrics:", err);
    }
}

// Button actions
document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("click", async () => {
        const action = btn.dataset.action;
        console.log("Action clicked:", action);

        // Map system vs media actions for future backend handlers
        const isSystem = ["reiniciar", "apagar", "suspender", "bloquear"].includes(action);
        const endpoint = isSystem ? `/api/system/${action}` : `/api/media/${action}`;

        try {
            await fetch(endpoint, { method: "POST" });
        } catch (e) {
            // Endpoints might not be implemented yet in backend
        }
    });
});

updateDashboard();
setInterval(updateDashboard, 2000);
