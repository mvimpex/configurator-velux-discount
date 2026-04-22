import streamlit as st
import json
import os

# --- DICȚIONAR CU DESCRIERI DIN PDF (ACCESORII) ---
DESCRIERI_PDF_ACCESORII = {
    "ZCT": "Tijă telescopică pentru acționarea ferestrelor și rulourilor manuale montate la înălțime.",
    "ZCZ": "Tijă de operare fixă (nemodificabilă ca lungime).",
    "ZOZ": "Adaptor pentru tije (necesar pentru acționarea rulourilor manuale cu tija ZCT/ZCZ).",
    "KMG": "Motor electric pentru ferestre de mansardă cu deschidere mediană (necesită KUX 110).",
    "KUX": "Unitate de comandă electrică (obligatorie pentru alimentarea unui motor KMG sau rulou electric, dacă fereastra nu e deja electrică).",
    "KSX": "Kit de motorizare SOLARĂ pentru ferestre de mansardă. Nu necesită cabluri! Include senzor de ploaie și întrerupător.",
    "KLI": "Întrerupător de perete wireless pentru operarea produselor electrice/solare.",
    "KLF": "Interfață pentru integrarea produselor VELUX INTEGRA în alte sisteme Smart Home.",
    "ZZZ": "Kituri de mentenanță și piese de schimb (ex. filtre de aer, burete pentru bara de operare).",
    "KIX": "Sistem VELUX ACTIVE with NETATMO. Pachet de bază (Gateway, Senzor de climat interior și Întrerupător plecare). Controlează automat ferestrele și rulourile pe baza temperaturii, umidității și nivelului de CO2.",
    "KLN": "Senzor de climat interior suplimentar pentru sistemul VELUX ACTIVE. Măsoară temperatura, umiditatea și calitatea aerului (CO2) din cameră.",
    "KRM": "Întrerupător de plecare suplimentar pentru sistemul VELUX ACTIVE. Închide toate ferestrele VELUX INTEGRA la plecarea de acasă."
}

def determina_categoria(nume_model):
    m = nume_model.upper()
    if any(x in m for x in ["KMG", "KUX", "KSX", "KLF", "KLI", "KIX", "KLA", "KLN", "KRM"]):
        return "1. ⚡ Automatizare & Smart Home"
    elif any(x in m for x in ["ZCT", "ZCZ", "ZOZ"]):
        return "2. 🦯 Operare Manuală (Tije & Adaptoare)"
    else:
        return "3. 🔧 Mentenanță / Piese de schimb"

def obtine_descriere(model_nume, descriere_default):
    for cheie, text_pdf in DESCRIERI_PDF_ACCESORII.items():
        if cheie in model_nume:
            return text_pdf
    return descriere_default

def main():
    st.set_page_config(page_title="VELUX - Accesorii", page_icon="🦯")
    st.title("Configurator VELUX: Accesorii & Automatizare")
    st.markdown("Adaugă tije, motoare electrice sau elemente de mentenanță.")

    file_path = os.path.join("VELUX_APPS", "4_Accesorii.json")
    if not os.path.exists(file_path):
        st.error(f"Eroare: Nu găsesc baza de date la {file_path}. Asigură-te că ai rulat generatorul.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    # Grupăm produsele pe categorii
    produse_categorisite = {}
    for k in catalog.keys():
        cat = determina_categoria(k)
        if cat not in produse_categorisite:
            produse_categorisite[cat] = []
        produse_categorisite[cat].append(k)

    # --- PASUL 1: Alege Categoria ---
    st.subheader("1. Alege Categoria")
    lista_categorii = sorted(list(produse_categorisite.keys()))
    categoria_aleasa = st.selectbox("Tip Accesoriu:", lista_categorii)

    # --- PASUL 2: Alege Modelul ---
    st.subheader("2. Alege Modelul")
    modele_disponibile = sorted(produse_categorisite[categoria_aleasa])
    model_ales = st.selectbox("Denumire Produs:", modele_disponibile)

    produs = catalog[model_ales]
    
    # --- PASUL 3: Alege Varianta (dacă e cazul) ---
    st.subheader("3. Alege Varianta / Dimensiunea")
    st.caption("Notă: Majoritatea accesoriilor au o singură variantă (0000) sau dimensiuni bazate pe lungime (ex. 100cm).")
    
    dimensiuni_disponibile = sorted(list(produs["variante"].keys()))
    
    if dimensiuni_disponibile:
        dimensiune_aleasa = st.selectbox("Variantă:", dimensiuni_disponibile)
        pret_final = produs["variante"][dimensiune_aleasa]
    else:
        st.warning("Acest produs nu are variante înregistrate.")
        dimensiune_aleasa = "-"
        pret_final = 0

    st.markdown("---")
    
    # --- AFIȘARE DETALII ---
    c1, c2 = st.columns([1, 2])
    with c1:
        if produs["imagine"] and str(produs["imagine"]) != 'nan':
            st.image(produs["imagine"], use_container_width=True)
    with c2:
        desc_text = obtine_descriere(model_ales, produs.get('descriere', ''))
        st.info(f"**Detalii Produs:**\n\n{desc_text}")

    st.metric(label=f"PREȚ ACCESORIU", value=f"{pret_final:,.2f} MDL")

if __name__ == "__main__":
    main()