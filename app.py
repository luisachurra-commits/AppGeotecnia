import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="App Geotecnia", layout="wide")
st.title("Aplicación Interactiva de Geotecnia")

# Crear pestañas
tab1, tab2 = st.tabs(["Clasificación USCS", "Círculo de Mohr"])

# --- PESTAÑA 1: USCS ---
with tab1:
    st.header("Análisis Granulométrico y de Plasticidad")
    col1, col2 = st.columns(2)
    
    with col1:
        pasa_200 = st.slider('% Pasa #200:', 0.0, 100.0, 13.0)
        pasa_4 = st.slider('% Pasa #4:', 0.0, 100.0, 62.0)
    with col2:
        ll = st.slider('Límite Líquido (LL):', 0.0, 100.0, 35.0)
        ip = st.slider('Índice Plast. (IP):', 0.0, 100.0, 12.0)
        
    st.divider()
    st.subheader("Resultados del Análisis USCS:")
    
    if pasa_200 < 50:
        fraccion_arena = pasa_4 - pasa_200
        fraccion_grava = 100 - pasa_4
        tipo_principal = "S" if fraccion_arena > fraccion_grava else "G"
        
        if pasa_200 > 12:
            linea_a = 0.73 * (ll - 20)
            sub_tipo = "C" if ip >= linea_a else "M"
            grupo = f"{tipo_principal}{sub_tipo}"
            nombres = {"SC": "Arena arcillosa", "SM": "Arena limosa", "GC": "Grava arcillosa", "GM": "Grava limosa"}
            st.success(f"**Código del Grupo USCS:** {grupo}")
            st.info(f"**Descripción tentativa:** {nombres.get(grupo, 'Suelo grueso')}")
        else:
            st.warning("Código: Requiere coeficientes Cu y Cc para clasificar (Pobres/Bien graduados).")
    else:
        st.warning("Suelo fino. Requiere uso de la Carta de Plasticidad de Casagrande completa.")

# --- PESTAÑA 2: CÍRCULO DE MOHR ---
with tab2:
    st.header("Análisis de Esfuerzos")
    col1, col2 = st.columns(2)
    
    with col1:
        sigma1 = st.slider('Esfuerzo Principal Mayor (σ1) [kPa]:', 10.0, 300.0, 100.0)
    with col2:
        sigma3 = st.slider('Esfuerzo Principal Menor (σ3) [kPa]:', 0.0, 150.0, 40.0)
        
    if sigma1 < sigma3:
        st.error("Error: El esfuerzo principal mayor (σ1) no puede ser menor que σ3.")
    else:
        centro = (sigma1 + sigma3) / 2
        radio = (sigma1 - sigma3) / 2
        theta = np.linspace(0, np.pi, 100)
        x = centro + radio * np.cos(theta)
        y = radio * np.sin(theta)
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(x, y, 'b-', label='Círculo de Mohr')
        ax.plot([sigma3, sigma1], [0, 0], 'ro') 
        ax.fill_between(x, y, color='blue', alpha=0.1)
        
        ax.set_title('Representación del Círculo de Mohr')
        ax.set_xlabel('Esfuerzo Normal, σ (kPa)')
        ax.set_ylabel('Esfuerzo Cortante, τ (kPa)')
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        ax.axis('equal') 
        
        st.pyplot(fig)
        st.write(f"**Esfuerzo Cortante Máximo (τ_max):** {radio:.2f} kPa")
        st.write(f"**Esfuerzo Normal Promedio (Centro):** {centro:.2f} kPa")