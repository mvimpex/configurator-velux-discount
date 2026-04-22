import streamlit as st
import importlib

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(page_title="Configurator VELUX - Discount.md", layout="wide")

# --- CSS TOTAL: ALB COMPLET + TEXT NEGRU ORIUNDE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800&display=swap');

    /* 1. FUNDAL ALB PESTE TOT (Main + Sidebar + Header) */
    .stApp, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stSidebar"] > div:first-child {
        background-color: #ffffff !important;
    }

    /* 2. TEXT NEGRU PESTE TOT (Main area + Sidebar) */
    /* Targetăm toate elementele de text posibile: paragrafe, titluri, label-uri, span-uri */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, label, span, .stSelectbox, .stRadio {
        font-family: 'Nunito Sans', sans-serif !important;
        color: #000000 !important; /* Negru pur */
    }

    /* 3. REGLAJE SPECIFICE PENTRU VIZIBILITATE ÎN DREAPTA (Main Content) */
    [data-testid="stAppViewContainer"] .stMarkdown p, 
    [data-testid="stAppViewContainer"] h1, 
    [data-testid="stAppViewContainer"] h2, 
    [data-testid="stAppViewContainer"] h3, 
    [data-testid="stAppViewContainer"] label {
        color: #000000 !important;
    }

    /* 4. BUTOANE (#b44427) */
    div.stButton > button:first-child {
        background-color: #b44427 !important;
        color: #ffffff !important; /* Textul de pe butoane rămâne ALB pentru contrast */
        border-radius: 10px !important;
        border: none !important;
        font-weight: 700 !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #dd7b68 !important;
    }

    /* 5. CASETE METRICE (PRET) */
    .stMetric {
        background-color: #ffffff !important;
        border: 1px solid #eeeeee !important;
        box-shadow: 0px 8px 28px 0px #00000014 !important;
        border-left: 5px solid #b44427 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #b44427 !important;
    }
    
    /* 6. FIX PENTRU SIDEBAR CATEGORII */
    [data-testid="stSidebar"] .stRadio label {
        color: #000000 !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Logo
    logo_url = "https://discount.md/wp-content/uploads/2023/11/discount-logo.svg"
    st.sidebar.image(logo_url, use_container_width=True)
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    # Navigare
    pagina = st.sidebar.radio(
        "NAVIGARE CATALOG:",
        ["🏠 Ferestre de Mansardă", "🏢 Ferestre de Terasă", "☀️ Rulouri & Protecție", "🔧 Accesorii & Automatizări"]
    )

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color: #000000; font-size: 11px; text-align: center;'>© 2026 discount.md</p>", unsafe_allow_html=True)

    # Incarcare pagini
    try:
        if pagina == "🏠 Ferestre de Mansardă":
            import app_mansarda
            app_mansarda.main()
        elif pagina == "🏢 Ferestre de Terasă":
            import app_terasa
            app_terasa.main()
        elif pagina == "☀️ Rulouri & Protecție":
            import app_protectie
            app_protectie.main()
        elif pagina == "🔧 Accesorii & Automatizări":
            import app_accesorii
            app_accesorii.main()
    except Exception as e:
        st.error(f"Eroare: {e}")

if __name__ == "__main__":
    main()