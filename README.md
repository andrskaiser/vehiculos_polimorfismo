## Requisitos

- Python 3.10 o superior.
- `pip` disponible en el entorno.

## Ejecución local

### Windows PowerShell

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

### Linux o macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit mostrará una dirección local, normalmente `http://localhost:8501`.
