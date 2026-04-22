import streamlit as st
import json
import os

# --- DICȚIONAR CU DESCRIERI DIN PDF (TERASĂ) ---
DESCRIERI_PDF_TERASA = {
    "CFU": "Unitate de bază FIXĂ, geam dublu sau triplu (noua generație). Izolare termică excelentă și reducere a zgomotului ploii.",
    "CVU": "Unitate de bază ELECTRICĂ, geam dublu sau triplu. Include senzor de ploaie și ventilare automată.",
    "CXU": "NOUA GENERAȚIE - FEREASTRĂ PENTRU ACCES PE ACOPERIȘ. Se deschide până la 60° pentru ieșire ușoară. Geam dublu/triplu.",
    "CXP": "Fereastră pentru acces pe acoperiș terasă (clasică). Deschidere manuală 60°. Necesită cupolă ISD.",
    "CFP": "Unitate de bază FIXĂ (clasică). Soluție standard recomandată cu protecție tip cupolă.",
    "CVP": "Unitate de bază ELECTRICĂ (clasică). Include senzor de ploaie. Recomandată cu protecție tip cupolă.",
    "CSP": "Fereastră pentru evacuarea fumului (desfumare) pentru acoperiș terasă.",
    "ISU 1093": "Protecție din sticlă PLATĂ. Design minimalist, sticlă securizată la exterior (pante 2° - 15°).",
    "ISU 2093": "Protecție din sticlă CURBATĂ (CurveTech). Drenaj perfect al apei, chiar și la 0°. Sticlă securizată.",
    "ISD 0000": "Cupolă din acril transparent. O soluție clasică, robustă și durabilă.",
    "ISD 0010": "Cupolă din acril opac. Oferă o lumină difuză și intimitate excelentă.",
    "ISD 0100": "Cupolă din policarbonat transparent. Rezistență extremă la impact și grindină.",
    "ISD 0110": "Cupolă din policarbonat opac. Lumină difuză, rezistență maximă la șocuri.",
    "DSU": "Rulou opac cu acționare SOLARĂ. Blochează lumina și oferă izolare termică pe timpul verii.",
    "MSU": "Rulou parasolar cu acționare SOLARĂ. Reduce căldura păstrând transparența."
}

def determina_categoria(nume_model):
    m = nume_model.upper()
    if any(x in m for x in ["CFU", "CVU", "CVP", "CFP", "CSP", "CXU", "CXP"]):
        return "baza"
    elif "ISU" in m or "ISD" in m:
        return "protectie"
    elif "DSU" in m or "MSU" in m or "FMG" in m or "FMK" in m:
        return "rulou"
    else:
        return "altul"

def get_sort_weight(nume_model):
    m = nume_model.upper()
    if "CFU" in m or "CFP" in m: return 1 
    if "CVU" in m or "CVP" in m: return 2 
    if "CXU" in m or "CXP" in m: return 3 
    if "CSP" in m: return 4 
    return 5

def eticheta_baza(nume_model):
    m = nume_model.upper()
    if "CFU" in m or "CFP" in m: return f"⬜ FIXĂ | {nume_model}"
    if "CVU" in m or "CVP" in m: return f"⚡ ELECTRICĂ | {nume_model}"
    if "CXU" in m or "CXP" in m: return f"🚪 IEȘIRE TERASĂ | {nume_model}"
    if "CSP" in m: return f"🔥 DESFUMARE | {nume_model}"
    return nume_model

def get_sort_weight_protectie(nume_model):
    m = nume_model.upper()
    if "ISU 2093" in m: return 1
    if "ISU 1093" in m: return 2
    if "ISD" in m: return 3
    return 4

def eticheta_protectie(nume_model):
    m = nume_model.upper()
    if "ISU 2093" in m: return f"🌊 STICLĂ CURBATĂ | {nume_model}"
    if "ISU 1093" in m: return f"📏 STICLĂ PLATĂ | {nume_model}"
    if "ISD" in m: return f"🔮 CUPOLĂ | {nume_model}"
    return nume_model

def obtine_descriere(model_nume, descriere_default):
    for cheie, text_pdf in DESCRIERI_PDF_TERASA.items():
        if cheie in model_nume:
            return text_pdf
    return descriere_default

def main():
    st.title("Configurator VELUX: Acoperiș Terasă")
    st.markdown("Pachet obligatoriu: **Unitate de Bază + Unitate Superioară (Protecție)**")

    file_path = os.path.join("VELUX_APPS", "2_Terasa.json")
    if not os.path.exists(file_path):
        st.error(f"Eroare: Nu găsesc baza de date la {file_path}. Ai rulat generatorul?")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    baze = {k: v for k, v in catalog.items() if determina_categoria(k) == "baza"}
    protectii = {k: v for k, v in catalog.items() if determina_categoria(k) == "protectie"}
    rulouri = {k: v for k, v in catalog.items() if determina_categoria(k) == "rulou"}
    
    st.subheader("1. Alege Unitatea de Bază")
    
    lista_baze_ordonate = sorted(list(baze.keys()), key=lambda x: (get_sort_weight(x), x))
    model_baza = st.selectbox(
        "Tip Fereastră (Fixă / Electrică / Ieșire):", 
        options=lista_baze_ordonate,
        format_func=eticheta_baza
    )
    
    dimensiuni_baza = sorted(list(baze[model_baza]["variante"].keys()))
    dimensiune_aleasa = st.selectbox("Dimensiune Fereastră (ex. 100100):", dimensiuni_baza)
    
    pret_baza = baze[model_baza]["variante"][dimensiune_aleasa]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        if baze[model_baza]["imagine"] and str(baze[model_baza]["imagine"]) != 'nan':
            st.image(baze[model_baza]["imagine"], use_container_width=True)
    with c2:
        text_descriere_baza = obtine_descriere(model_baza, baze[model_baza]['descriere'])
        st.info(f"**Detalii Bază:**\n\n{text_descriere_baza}")
        st.success(f"Preț unitate bază: **{pret_baza:,.2f} MDL**")

    st.markdown("---")
    
    st.subheader("2. Alege Protecția Superioară (Obligatoriu)")
    st.caption("Pentru ca sistemul să fie complet, trebuie să adaugi sticla exterioară sau cupola.")
    
    # Aici e magia! Sistemul caută DOAR protecțiile care se fabrică pe dimensiunea aleasă
    protectii_compatibile = [k for k, v in protectii.items() if dimensiune_aleasa in v["variante"]]
    
    if protectii_compatibile:
        lista_prot_ordonate = sorted(protectii_compatibile, key=lambda x: (get_sort_weight_protectie(x), x))
        model_protectie = st.selectbox("Tip Protecție (Curbată / Plată / Cupolă):", lista_prot_ordonate, format_func=eticheta_protectie)
        
        # Extrage prețul corect pentru dimensiunea sticlei!
        pret_protectie = protectii[model_protectie]["variante"][dimensiune_aleasa]
        
        c3, c4 = st.columns([1, 2])
        with c3:
             if protectii[model_protectie]["imagine"] and str(protectii[model_protectie]["imagine"]) != 'nan':
                 st.image(protectii[model_protectie]["imagine"], use_container_width=True)
        with c4:
            desc_prot = obtine_descriere(model_protectie, protectii[model_protectie]['descriere'])
            st.info(f"**Detalii Protecție:**\n\n{desc_prot}")
            st.success(f"Preț protecție ({dimensiune_aleasa}): **{pret_protectie:,.2f} MDL**")
    else:
        st.warning(f"Nu s-au găsit protecții compatibile pentru dimensiunea {dimensiune_aleasa}.")
        pret_protectie = 0

    st.markdown("---")
    
    st.subheader("3. Rulou Solar (Opțional)")
    rulouri_compatibile = [k for k, v in rulouri.items() if dimensiune_aleasa in v["variante"]]
    rulouri_compatibile.insert(0, "Fără rulou") 
    
    model_rulou = st.selectbox("Alege Rulou de Terasă:", rulouri_compatibile)
    pret_rulou = 0
    if model_rulou != "Fără rulou":
        pret_rulou = rulouri[model_rulou]["variante"][dimensiune_aleasa]
        desc_rulou = obtine_descriere(model_rulou, rulouri[model_rulou]['descriere'])
        st.caption(desc_rulou)
        st.success(f"Preț rulou ({dimensiune_aleasa}): **{pret_rulou:,.2f} MDL**")

    st.markdown("---")
    
    total_mdl = pret_baza + pret_protectie + pret_rulou
    st.metric(label=f"PREȚ TOTAL PACHET TERASĂ ({dimensiune_aleasa})", value=f"{total_mdl:,.2f} MDL")

if __name__ == "__main__":
    main()