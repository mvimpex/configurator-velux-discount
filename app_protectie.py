import streamlit as st
import json
import os

# --- DICȚIONAR CU DESCRIERI DIN PDF (RULOURI) ---
DESCRIERI_PDF_PROTECTIE = {
    "MHL": "Rulou exterior parasolar MANUAL. Reduce căldura cu până la 76%, lăsând lumina să intre și păstrând vizibilitatea spre exterior.",
    "MSL": "Rulou exterior parasolar cu acționare SOLARĂ. Se instalează ușor, fără cabluri, pe orice fereastră VELUX. Include telecomandă.",
    "MML": "Rulou exterior parasolar ELECTRIC. Recomandat pentru ferestrele electrice VELUX INTEGRA.",
    "SSL": "Roletă exterioară cu acționare SOLARĂ. Oferă protecție termică maximă, întuneric total și izolare fonică (ploaie/grindină). Nu necesită cabluri.",
    "SML": "Roletă exterioară ELECTRICĂ. Protecție supremă pe tot parcursul anului.",
    "SSS": "Rulou exterior opac SOLAR (Soft). Material textil extrem de rezistent. Blochează eficient căldura și lumina.",
    "DKL": "Rulou interior opac MANUAL. Design elegant, blochează complet lumina – ideal pentru dormitoare. Se montează rapid (Pick&Click!).",
    "DML": "Rulou interior opac ELECTRIC. Perfect pentru ferestre la înălțime.",
    "DSL": "Rulou interior opac SOLAR. Se controlează din telecomandă, instalare fără fire.",
    "DFD": "Rulou Duo (Opac DKL + Pliseu FHL). 2-în-1: Întuneric total noaptea și lumină difuză ziua.",
    "RFL": "Rulou interior semitransparent MANUAL. Atenuează razele soarelui și decorează camera.",
    "FHL": "Rulou plisat MANUAL. Flexibil, nu este fixat nici sus, nici jos (se poate poziționa oriunde pe geam).",
    "ZIL": "Plasă contra insectelor. Se montează pe finisajul peretelui (pe conturul ferestrei), permițând deschiderea geamului pentru aerisire."
}

def determina_categoria(nume_model):
    m = nume_model.upper()
    if any(x in m for x in ["MHL", "MSL", "MML", "SSL", "SML", "SSS", "SMH"]):
        return "☀️ 1. Protecție Exterioară (Contra Căldurii)"
    elif any(x in m for x in ["DKL", "DML", "DSL", "DFD", "RFL", "RML", "RSL", "FHL", "FML", "FSL", "FHC", "PAL", "PML"]):
        return "🪟 2. Rulouri Interioare (Controlul Luminii)"
    elif "ZIL" in m:
        return "🦟 3. Plasă contra insectelor"
    else:
        return "🔧 4. Alte Rulouri / Accesorii"

def obtine_descriere(model_nume, descriere_default):
    for cheie, text_pdf in DESCRIERI_PDF_PROTECTIE.items():
        if cheie in model_nume:
            return text_pdf
    return descriere_default

def main():
    st.set_page_config(page_title="VELUX - Rulouri", page_icon="☀️")
    st.title("Configurator VELUX: Rulouri & Protecție Solară")
    st.markdown("Selectează categoria, modelul și dimensiunea geamului.")

    file_path = os.path.join("VELUX_APPS", "3_Protectie.json")
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
    st.subheader("1. Alege Tipul Protecției")
    lista_categorii = sorted(list(produse_categorisite.keys()))
    categoria_aleasa = st.selectbox("Unde se montează?", lista_categorii)

    # --- PASUL 2: Alege Modelul ---
    st.subheader("2. Alege Modelul")
    modele_disponibile = sorted(produse_categorisite[categoria_aleasa])
    model_ales = st.selectbox("Model Rulou:", modele_disponibile)

    produs = catalog[model_ales]
    
    # --- PASUL 3: Alege Dimensiunea ---
    st.subheader("3. Alege Dimensiunea")
    st.caption("⚠️ **Atenție:** Codul dimensiunii ruloului (ex. MK06) trebuie să fie EXACT același cu codul ferestrei pe care se montează!")
    dimensiuni_disponibile = sorted(list(produs["variante"].keys()))
    
    if dimensiuni_disponibile:
        dimensiune_aleasa = st.selectbox("Cod Dimensiune Fereastră:", dimensiuni_disponibile)
        pret_final = produs["variante"][dimensiune_aleasa]
    else:
        st.warning("Acest produs nu are dimensiuni standard înregistrate.")
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
        st.success(f"Preț unitar: **{pret_final:,.2f} MDL**")

    st.metric(label=f"TOTAL RULOU ({dimensiune_aleasa})", value=f"{pret_final:,.2f} MDL")

if __name__ == "__main__":
    main()