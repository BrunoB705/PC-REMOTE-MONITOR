# PC Remote & Monitor

Servidor FastAPI en Windows que se controla y se monitorea desde el celular, por la Wi-Fi de tu casa. Proyecto de aprendizaje.

## Qué hace

- **Dashboard en vivo**: Uso y temperatura de CPU, GPU y motherboard, RAM, disco y uptime (actualización cada 2 s)
- **Control de sistema** desde el celular, con modal de confirmación y cuenta regresiva de 30 s (con opción de cancelar): apagar, reiniciar, suspender, bloquear, apagar pantalla
- **Acceso con API key**: todas las rutas exigen el header `X-API-Key`

## Requisitos

- Windows (la PC a controlar) con Python 3.11
- Permiso de **administrador** al levantar el servidor (sin él, las temperaturas de CPU y motherboard vienen `None`)
- El celular, en la misma red Wi-Fi
- (Opcional, para temperaturas) LibreHardwareMonitor — se instala una vez ejecutando `scripts/install_pawnio.ps1` (requiere permisos de admin)

## Instalación

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env        # crear .env y poner API_KEY dentro

scripts\get_dll.ps1           # script de descarga de los DLLs de LibreHardwareMonitor
scripts\install_pawnio.ps1    # script para instalar pawnio y poder leer las temperaturas (requiere permisos de admin)
```

## Levantar el servidor

Abrir **la terminal como administrador** antes.

```powershell
venv\Scripts\activate
uvicorn app.main:app --reload
```
 Luego:

- PC: http://localhost:8000
- Celular (misma Wi-Fi): http://TU-IP:8000 - En `ipconfig`

Poner API KEY en el acceso una única vez.

## Tests

```powershell
pytest
```

Requiere `.env` (si no, `app.core/config.py` lanza error al importar).

## Stack

Python 3.11 · FastAPI · psutil · LibreHardwareMonitor (pythonnet) · HTML/CSS/JS vanilla (sin build tools)
