import streamlit as st
import json
import os

# --- DICȚIONAR CU DESCRIERI DIN PDF ---
DESCRIERI_PDF = {
    "GZL 1051": "Deschidere de sus, acționare manuală, lemn de pin, finisare cu strat dublu, lac transparent, geam cu două foi de sticlă.",
    "GLU 0051": "Deschidere de sus, acționare manuală, lemn cu înveliș de poliuretan alb, fără întreținere, durabil, geam cu două foi de sticlă.",
    "GLL 1061": "Deschidere de sus, acționare manuală, lemn de pin, finisare cu strat dublu, lac transparent, geam triplu (Standard Plus).",
    "GLU 0061": "Deschidere de sus, acționare manuală, lemn cu înveliș de poliuretan alb, fără întreținere, durabil, geam triplu.",
    "GLL 1064": "Deschidere de sus, acționare manuală, lemn de pin, finisare cu strat dublu, lac transparent, geam triplu (Confort - izolare superioară).",
    "GLU 0064": "Deschidere de sus, acționare manuală, lemn cu înveliș de poliuretan alb, fără întreținere, durabil, geam triplu (Confort).",
    "GGL 3066": "Deschidere de sus, acționare manuală, lemn de pin, finisaj cu strat triplu, vopsit în alb, geam triplu (Confort Plus).",
    "GPL 3066": "Acționare manuală, articulare superioară (deschidere de jos), lemn de pin, finisaj cu strat triplu, geam triplu.",
    "GPU 0066": "Acționare manuală, deschidere de jos, lemn cu înveliș de poliuretan alb, fără întreținere, geam triplu.",
    "EDW 1000": "Pentru învelitoare ondulată (țiglă metalică, ceramică, beton), grosime de până la 120 mm.",
    "EDW 2000": "Pentru învelitoare ondulată, grosime de până la 120 mm. Pachetul include kitul de izolare termică BDX.",
    "EDS 1000": "Pentru învelitoare plată (șindrilă bituminoasă, ardezie), grosime de până la 16 mm (2 x 8 mm).",
    "EDS 2000": "Pentru învelitoare plată, grosime de până la 16 mm. Pachetul include kitul de izolare termică BDX.",
    "BDX 2000": "Kit de izolare termică. Asigură o izolare perfectă între tocul ferestrei și acoperiș. Include folia hidroizolatoare BFX.",
    "BFX 1000": "Folie hidroizolatoare plisată. Asigură o conexiune etanșă între fereastră și folia acoperișului.",
    "BBX 0000": "Barieră de vapori. Previne formarea condensului în structura acoperișului."
}

def determina_categoria(nume_model):
    if any(p in nume_model for p in ["GZL", "GLL", "GLU", "GNL", "GNU", "GGL", "GGU", "GPL", "GPU", "VFE", "VIU", "VFA", "VFB", "GDL", "GEL", "GXL", "GXU", "GVK", "VLT", "GVT"]):
        return "fereastra"
    elif any(p in nume_model for p in ["EDW", "EDT", "EDS", "EDQ", "EDB", "EDL", "EDP", "EDJ", "EDN", "EKW", "EKS", "EKL", "EKQ", "EKT"]):
        return "rama"
    elif any(p in nume_model for p in ["BDX", "BFX", "BBX"]):
        return "kit"
    elif any(p in nume_model for p in ["TWR", "TWF", "TLR", "TLF"]):
        return "tunel"
    else:
        return "altul"

def get_sort_weight(nume_model):
    m = nume_model.upper()
    if "GZL" in m or ("GLU" in m and "51" in m): return 1
    elif ("GLL" in m and "61" in m) or ("GLU" in m and "61" in m): return 2
    elif ("GLL" in m and "64" in m) or ("GLU" in m and "64" in m) or "GNL" in m or "GNU" in m: return 3
    elif "GGL" in m or "GGU" in m or "GPL" in m or "GPU" in m: return 4
    elif any(x in m for x in ["VFE", "VIU", "VFA", "VFB"]): return 5
    elif any(x in m for x in ["GDL", "GEL", "GXL", "GXU", "GVK", "VLT", "GVT"]): return 6
    elif "TWR" in m or "TWF" in m or "TLR" in m or "TLF": return 7
    return 8

# Funcție nouă pentru forțarea ramelor top-seller la începutul listei
def get_sort_weight_rama(nume_model):
    m = nume_model.upper()
    if "EDS 1000" in m: return 1
    if "EDS 2000" in m: return 2
    if "EDW 1000" in m: return 3
    if "EDW 2000" in m: return 4
    return 5

def eticheta_grup_fereastra(nume_model):
    m = nume_model.upper()
    if "GZL" in m or ("GLU" in m and "51" in m):
        return f"🟦 1. Basic | {nume_model}"
    elif ("GLL" in m and "61" in m) or ("GLU" in m and "61" in m):
        return f"🟨 2. Standard | {nume_model}"
    elif ("GLL" in m and "64" in m) or ("GLU" in m and "64" in m) or "GNL" in m or "GNU" in m:
        return f"🟧 3. Confort | {nume_model}"
    elif "GGL" in m or "GGU" in m or "GPL" in m or "GPU" in m:
        return f"🟥 4. Confort Plus | {nume_model}"
    elif any(x in m for x in ["VFE", "VIU", "VFA", "VFB"]):
        return f"🪟 5. Element Vertical | {nume_model}"
    elif any(x in m for x in ["GDL", "GEL", "GXL", "GXU", "GVK", "VLT", "GVT"]):
        return f"🚪 6. Ieșire / Balcon | {nume_model}"
    elif "TWR" in m or "TWF" in m or "TLR" in m or "TLF":
        return f"☀️ 7. Tunel Solar | {nume_model}"
    return nume_model

def obtine_descriere(model_nume, descriere_default):
    for cheie, text_pdf in DESCRIERI_PDF.items():
        if cheie in model_nume:
            return text_pdf
    return descriere_default

def main():
    st.title("Configurator VELUX: Mansardă")
    st.markdown("Configurează pachetul complet: **Fereastră + Ramă + Produse de montaj**")

    file_path = os.path.join("VELUX_APPS", "1_Mansarda.json")
    if not os.path.exists(file_path):
        st.error(f"Eroare: Nu găsesc baza de date la {file_path}.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    ferestre = {k: v for k, v in catalog.items() if determina_categoria(k) in ["fereastra", "tunel"]}
    rame = {k: v for k, v in catalog.items() if determina_categoria(k) == "rama"}
    kituri = {k: v for k, v in catalog.items() if determina_categoria(k) == "kit"}
    
    # --- PASUL 1: Fereastra ---
    st.subheader("1. Alege Fereastra")
    
    lista_modele_ordonate = sorted(list(ferestre.keys()), key=lambda x: (get_sort_weight(x), x))
    model_fereastra = st.selectbox(
        "Model Fereastră:", 
        options=lista_modele_ordonate,
        format_func=eticheta_grup_fereastra
    )
    
    dimensiuni_fereastra = sorted(list(ferestre[model_fereastra]["variante"].keys()))
    dimensiune_aleasa = st.selectbox("Dimensiune (Mărimea):", dimensiuni_fereastra)
    
    pret_fereastra = ferestre[model_fereastra]["variante"][dimensiune_aleasa]
    
    c1, c2 = st.columns([1, 2])
    with c1:
        if ferestre[model_fereastra]["imagine"] and str(ferestre[model_fereastra]["imagine"]) != 'nan':
            st.image(ferestre[model_fereastra]["imagine"], use_container_width=True)
    with c2:
        text_descriere = obtine_descriere(model_fereastra, ferestre[model_fereastra]['descriere'])
        st.info(f"**Detalii:**\n\n{text_descriere}")
        st.success(f"Preț fereastră: **{pret_fereastra:,.2f} MDL**")

    st.markdown("---")
    
    # --- PASUL 2: Rama ---
    st.subheader("2. Alege Rama de Etanșare")
    rame_compatibile = [k for k, v in rame.items() if dimensiune_aleasa in v["variante"]]
    
    if rame_compatibile:
        # Aici aplicăm noua logică de sortare pentru rame
        rame_compatibile_ordonate = sorted(rame_compatibile, key=lambda x: (get_sort_weight_rama(x), x))
        
        model_rama = st.selectbox("Tip Învelitoare (Model Ramă):", rame_compatibile_ordonate)
        pret_rama = rame[model_rama]["variante"][dimensiune_aleasa]
        
        desc_rama = obtine_descriere(model_rama, "")
        if desc_rama:
            st.caption(desc_rama)
            
        st.success(f"Preț ramă ({dimensiune_aleasa}): **{pret_rama:,.2f} MDL**")
    else:
        st.warning(f"Nu s-au găsit rame compatibile pentru dimensiunea {dimensiune_aleasa}.")
        pret_rama = 0

    st.markdown("---")
    
    # --- PASUL 3: Kit Montaj ---
    st.subheader("3. Produse de montaj (Opțional)")
    kituri_compatibile = [k for k, v in kituri.items() if dimensiune_aleasa in v["variante"]]
    kituri_compatibile.insert(0, "Fără kit") 
    
    model_kit = st.selectbox("Alege Kit de Izolare/Folie:", kituri_compatibile)
    pret_kit = 0
    if model_kit != "Fără kit":
        pret_kit = kituri[model_kit]["variante"][dimensiune_aleasa]
        
        desc_kit = obtine_descriere(model_kit, "")
        if desc_kit:
            st.caption(desc_kit)
            
        st.success(f"Preț kit ({dimensiune_aleasa}): **{pret_kit:,.2f} MDL**")

    st.markdown("---")
    
    # --- TOTAL ---
    total_mdl = pret_fereastra + pret_rama + pret_kit
    st.metric(label=f"PREȚ TOTAL PACHET ({dimensiune_aleasa})", value=f"{total_mdl:,.2f} MDL")

if __name__ == "__main__":
    main()