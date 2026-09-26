const API_KEY_STORAGE = "api_key";

function getApiKey() {
    return localStorage.getItem(API_KEY_STORAGE) || "";
}

function setApiKey(key) {
    localStorage.setItem(API_KEY_STORAGE, key);
}

function clearApiKey() {
    localStorage.removeItem(API_KEY_STORAGE);
}

async function apiFetch(path, options = {}) {
    return fetch(path, {
        ...options,
        headers: {
            ...(options.headers || {}),
            "X-API-Key": getApiKey(),
        },
    });
}

async function validateKey(key) {
    const res = await fetch("/api/metrics", {
        headers: { "X-API-Key": key },
    });
    if (res.ok) return "ok";
    if (res.status === 401) return "invalid";
    return "error";
}

function initAuth(onAuthenticated) {
    const overlay = document.getElementById("auth-overlay");
    const form = document.getElementById("auth-form");
    const input = document.getElementById("auth-key");
    const errorEl = document.getElementById("auth-error");

    const showOverlay = (message = "") => {
        errorEl.textContent = message;
        overlay.classList.remove("hidden");
    };

    const enter = () => {
        overlay.classList.add("hidden");
        onAuthenticated();
    };

    const stored = getApiKey();
    if (stored) {
        validateKey(stored)
            .then((result) => {
                if (result === "ok") {
                    enter();
                } else if (result === "invalid") {
                    clearApiKey();
                    showOverlay("API key inválida");
                } else {
                    showOverlay("Error del servidor");
                }
            })
            .catch(() => showOverlay("Sin conexión con el servidor"));
    } else {
        showOverlay();
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const key = input.value.trim();
        if (!key) return;

        try {
            const result = await validateKey(key);
            if (result === "ok") {
                setApiKey(key);
                enter();
            } else if (result === "invalid") {
                errorEl.textContent = "API key inválida";
            } else {
                errorEl.textContent = "Error del servidor";
            }
        } catch {
            errorEl.textContent = "Sin conexión con el servidor";
        }
    });
}
