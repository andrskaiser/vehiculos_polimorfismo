import streamlit as st


CSS = r"""
<style>
:root {
    --accent: #16a7b8;
    --accent-dark: #0d7f8c;
    --peach: #f3b092;
    --surface: #ffffff;
    --border: #dde3e7;
    --muted: #6d7780;
}
.stApp { background: #f3f5f6; }
.block-container { padding-top: 0.9rem; max-width: 1500px; }
header[data-testid="stHeader"] { background: transparent; }
.app-header {
    display: flex;
    align-items: center;
    gap: 14px;
    background: white;
    border-bottom: 1px solid var(--border);
    padding: 13px 18px;
    margin: -8px -8px 10px -8px;
}
.app-mark {
    width: 38px;
    height: 38px;
    border-radius: 9px;
    background: var(--accent);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
}
.app-title { font-size: 1.20rem; font-weight: 700; color: #334047; }
.app-subtitle { font-size: .82rem; color: var(--muted); }
[data-testid="stRadio"] > div { gap: 0.25rem; }
[data-testid="stRadio"] label {
    background: white;
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 8px 15px;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: #ffe5d9;
    border-color: var(--peach);
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border-color: var(--border) !important;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
}
.section-title { font-size: 1.08rem; font-weight: 700; color: #34424a; margin-bottom: 2px; }
.section-help { font-size: .82rem; color: var(--muted); margin-bottom: 10px; }
.metric-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 13px 15px;
    min-height: 92px;
}
.metric-label { color: var(--muted); font-size: .78rem; }
.metric-value { color: #27343a; font-size: 1.45rem; font-weight: 750; margin-top: 4px; }
.metric-detail { color: var(--muted); font-size: .74rem; margin-top: 3px; }
.small-note {
    color: var(--muted);
    background: #f8fafb;
    border-left: 3px solid var(--accent);
    padding: 8px 10px;
    font-size: .82rem;
}
.stButton > button[kind="primary"] { background: var(--accent); border-color: var(--accent); }
.stButton > button[kind="primary"]:hover { background: var(--accent-dark); border-color: var(--accent-dark); }
</style>
"""


def aplicar_estilos():
    st.markdown(CSS, unsafe_allow_html=True)
