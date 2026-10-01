async function updateDashboard() {
    try {
        const res = await apiFetch("/api/metrics");
        if (res.status === 401) {
            clearApiKey();
            location.reload();
            return;
        }
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

// System actions (Fase 2): todas pasan por el modal de confirmación
const SYSTEM_ACTIONS = {
    reiniciar: "Reiniciar la PC",
    apagar: "Apagar la PC",
    suspender: "Suspender la PC",
    bloquear: "Bloquear la PC",
    apagar_pantalla: "Apagar la pantalla",
    cancelar: "Cancelar el apagado programado",
};

let pendingAction = null;
let toastTimer = null;

function showToast(message) {
    const toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.classList.remove("hidden");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.add("hidden"), 4000);
}

function openConfirm(action) {
    pendingAction = action;
    document.getElementById("confirm-text").textContent = `¿${SYSTEM_ACTIONS[action]}?`;
    document.getElementById("confirm-overlay").classList.remove("hidden");
}

function closeConfirm() {
    pendingAction = null;
    document.getElementById("confirm-overlay").classList.add("hidden");
}

async function runSystemAction(action) {
    try {
        const res = await apiFetch(`/api/system/${action}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ confirm: true }),
        });
        if (res.status === 401) {
            clearApiKey();
            location.reload();
            return;
        }
        const data = await res.json().catch(() => ({}));
        if (res.ok && data.delay && COUNTDOWN_ACTIONS[action]) {
            startCountdown(action, data.delay);
            return;
        }
        showToast(res.ok ? (data.message || "Acción enviada") : (data.detail || "No se pudo ejecutar la acción"));
    } catch (e) {
        showToast("Sin conexión con el servidor");
    }
}

async function runMediaAction(action) {
    try {
        const res = await apiFetch(`/api/media/${action}`, { method: "POST" });
        if (res.status === 401) {
            clearApiKey();
            location.reload();
            return;
        }
        const data = await res.json().catch(() => ({}));
        showToast(res.ok ? (data.message || "Acción ejecutada") : (data.detail || data.message || "No se pudo ejecutar la acción"));
    } catch (e) {
        showToast("Sin conexión con el servidor");
    }
}

// Ventana con contador para apagar/reiniciar
const COUNTDOWN_ACTIONS = {
    apagar: "Apagando la PC",
    reiniciar: "Reiniciando la PC",
};

let countdownTimer = null;

function stopCountdown() {
    clearInterval(countdownTimer);
    countdownTimer = null;
    document.getElementById("countdown-overlay").classList.add("hidden");
}

function startCountdown(action, seconds) {
    stopCountdown();
    document.getElementById("countdown-text").textContent = COUNTDOWN_ACTIONS[action];
    document.getElementById("countdown-number").textContent = seconds;
    document.getElementById("countdown-overlay").classList.remove("hidden");

    let left = seconds;
    countdownTimer = setInterval(() => {
        left -= 1;
        if (left <= 0) {
            stopCountdown();
            return;
        }
        document.getElementById("countdown-number").textContent = left;
    }, 1000);
}

document.getElementById("countdown-cancel").addEventListener("click", () => {
    stopCountdown();
    runSystemAction("cancelar");
});

document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const action = btn.dataset.action;
        if (!action) return;

        if (SYSTEM_ACTIONS[action]) {
            openConfirm(action);
            return;
        }

        // Media (Fase 3): feedback de éxito/error en el toast
        runMediaAction(action);
    });
});

document.getElementById("confirm-ok").addEventListener("click", () => {
    const action = pendingAction;
    closeConfirm();
    if (action) runSystemAction(action);
});

document.getElementById("confirm-cancel").addEventListener("click", closeConfirm);

initAuth(() => {
    updateDashboard();
    setInterval(updateDashboard, 2000);
});
