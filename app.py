import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================
st.set_page_config(page_title="App Geotecnia", page_icon="🌍", layout="wide")
st.title("Aplicación Interactiva de Geotecnia (Parte 1)")
st.markdown("""
Bienvenidos a este entorno interactivo de aprendizaje diseñado para ingenieros civiles y geotécnicos. 
Basado en el referente pedagógico del **Prof. Felipe Ochoa-Cornejo** (U. de Chile).
""")

# Crear las 8 pestañas para los módulos
tabs = st.tabs([
    "1. USCS", "2. Fases", "3. Compactación", "4. Tensiones", 
    "5. Flujo", "6. Terreno", "7. Consolidación", "8. Corte & Mohr"
])

# ==========================================
# MÓDULO 1: CLASIFICACIÓN USCS
# ==========================================
with tabs[0]:
    st.header("1. Clasificación de Suelos (USCS)")
    col1, col2 = st.columns(2)
    with col1:
        pasa_200 = st.slider('% Pasa #200:', 0.0, 100.0, 13.0, key='m1_p200')
        pasa_4 = st.slider('% Pasa #4:', 0.0, 100.0, 62.0, key='m1_p4')
    with col2:
        ll = st.slider('Límite Líquido (LL):', 0.0, 100.0, 35.0, key='m1_ll')
        ip = st.slider('Índice Plast. (IP):', 0.0, 100.0, 12.0, key='m1_ip')
        
    st.subheader("Resultados")
    if pasa_200 < 50:
        fraccion_arena, fraccion_grava = pasa_4 - pasa_200, 100 - pasa_4
        tipo = "S" if fraccion_arena > fraccion_grava else "G"
        if pasa_200 > 12:
            linea_a = 0.73 * (ll - 20)
            sub_tipo = "C" if ip >= linea_a else "M"
            st.success(f"**Grupo USCS:** {tipo}{sub_tipo}")
        else:
            st.warning("Requiere Cu y Cc para clasificar (W/P).")
    else:
        st.warning("Suelo fino. Requiere Carta de Plasticidad completa.")
        
    st.divider()
    opcion_q1 = st.radio("¿Qué controla la plasticidad en suelos finos?", 
                         ["La mineralogía y agua adsorbida.", "La granulometría.", "La gravedad."], key="q1", index=None)
    if st.button("Verificar M1"):
        if "mineralogía" in opcion_q1: st.success("¡Correcto!")
        else: st.error("Incorrecto.")

# ==========================================
# MÓDULO 2: RELACIONES DE FASE
# ==========================================
with tabs[1]:
    st.header("2. Relaciones de Fase (Diagrama)")
    col1, col2, col3 = st.columns(3)
    with col1: gs = st.slider('Gs (Sólidos):', 2.50, 2.85, 2.65, 0.01)
    with col2: e = st.slider('e (Vacíos):', 0.30, 1.20, 0.70, 0.05)
    with col3: sr_percent = st.slider('Sr (% Saturación):', 0.0, 100.0, 50.0, 5.0)

    sr, gamma_w = sr_percent / 100.0, 9.81
    vs, vv = 1.0, e
    vw, va = sr * e, vv - (sr * e)
    ws, ww = gs * gamma_w, vw * gamma_w
    v_total, w_total = vs + vv, ws + ww
    
    col_plot, col_res = st.columns([2, 1])
    with col_plot:
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        ax2.bar(1, va, bottom=vs+vw, color='#ced4da', edgecolor='black', label=f'Aire (Va={va:.2f})')
        ax2.bar(1, vw, bottom=vs, color='#a2d2ff', edgecolor='black', label=f'Agua (Vw={vw:.2f})')
        ax2.bar(1, vs, bottom=0, color='#b7b7a4', edgecolor='black', label=f'Sólido (Vs={vs:.2f})')
        ax2.set_xlim(0, 2); ax2.set_xticks([]); ax2.legend(loc='upper right')
        st.pyplot(fig2)
    with col_res:
        st.metric("Humedad (w)", f"{(ww/ws)*100:.1f} %")
        st.metric("Porosidad (n)", f"{(vv/v_total)*100:.1f} %")
        st.metric("Peso Esp. (γ)", f"{w_total/v_total:.2f} kN/m³")

# ==========================================
# MÓDULO 3: COMPACTACIÓN
# ==========================================
with tabs[2]:
    st.header("3. Compactación Proctor")
    col1, col2, col3 = st.columns(3)
    with col1: w_opt = st.slider('w Óptima (%):', 8.0, 18.0, 12.0, 0.5)
    with col2: gamma_max = st.slider('γd Máx (kN/m³):', 15.0, 21.0, 18.5, 0.1)
    with col3: gs_comp = st.slider('Gs del Suelo:', 2.60, 2.80, 2.68, 0.01, key='m3_gs')

    w_array = np.linspace(4, 24, 100)
    gamma_d = gamma_max - 0.08 * (w_array - w_opt)**2
    gamma_zav = (gs_comp * 9.81) / (1 + (w_array * gs_comp / 100.0))
    
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(w_array, gamma_d, 'r-', linewidth=2, label='Curva Proctor')
    ax3.plot(w_array, gamma_zav, 'b--', linewidth=2, label='Curva ZAV (Sr=100%)')
    ax3.plot(w_opt, gamma_max, 'go', label=f'Óptimo: {w_opt}% | {gamma_max} kN/m³')
    ax3.set_ylim(12, 22); ax3.set_xlabel('Humedad (%)'); ax3.set_ylabel('γd (kN/m³)'); ax3.grid(True); ax3.legend()
    st.pyplot(fig3)

# ==========================================
# MÓDULO 4: TENSIONES EFECTIVAS
# ==========================================
with tabs[3]:
    st.header("4. Tensiones Efectivas")
    col1, col2, col3 = st.columns(3)
    with col1: zw = st.slider('Nivel Freático (m):', 0.0, 12.0, 4.0, 0.5)
    with col2: g_d = st.slider('γ seco (kN/m³):', 14.0, 18.0, 16.5, 0.1)
    with col3: g_sat = st.slider('γ sat (kN/m³):', 18.0, 22.0, 19.5, 0.1)

    z_steps = np.linspace(0, 12, 100)
    sigma, u = np.where(z_steps <= zw, g_d * z_steps, g_d * zw + g_sat * (z_steps - zw)), np.where(z_steps <= zw, 0, 9.81 * (z_steps - zw))
    
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    ax4.plot(sigma, z_steps, 'k-', label='Esfuerzo Total (σ)')
    ax4.plot(u, z_steps, 'b-', label='Presión de Poros (u)')
    ax4.plot(sigma - u, z_steps, 'r-', label='Esfuerzo Efectivo (σ\')')
    ax4.axhline(zw, color='#a2d2ff', linestyle=':', label='NF')
    ax4.invert_yaxis(); ax4.grid(True); ax4.legend(); ax4.set_xlabel('Presión (kPa)'); ax4.set_ylabel('Profundidad (m)')
    st.pyplot(fig4)

# ==========================================
# MÓDULO 5: FLUJO DE AGUA
# ==========================================
with tabs[4]:
    st.header("5. Flujo de Agua (Darcy)")
    col1, col2 = st.columns(2)
    with col1: 
        k_exp = st.slider('log10(k m/s):', -8, -2, -5)
        dh = st.slider('Carga ΔH (m):', 1.0, 15.0, 5.0)
    with col2:
        nf = st.slider('Canales (Nf):', 1, 10, 4)
        nd = st.slider('Caídas (Nd):', 2, 20, 8)
        
    k = 10**k_exp
    q_sec = k * dh * (nf / nd)
    st.success(f"**Caudal unitario (q):** {q_sec:.2e} m³/s/m")
    st.info(f"**Volumen infiltrado:** {q_sec * 3600 * 1000:.2f} Litros/hora por metro lineal.")

# ==========================================
# MÓDULO 6: TERRENO (SPT & Vs30)
# ==========================================
with tabs[5]:
    st.header("6. Ensayos In Situ (SPT y Vs30)")
    c1, c2 = st.columns(2)
    with c1:
        n_mues = st.number_input('Golpes SPT (N):', value=25)
        eficiencia = st.slider('Eficiencia Martillo %:', 45.0, 90.0, 60.0)
    with c2:
        vs1 = st.slider('Vs Estrato 1 (m/s):', 150, 800, 450, step=10)
        vs2 = st.slider('Vs Estrato 2 (m/s):', 150, 800, 350, step=10)
        vs3 = st.slider('Vs Estrato 3 (m/s):', 150, 800, 250, step=10)
        
    n60 = n_mues * (eficiencia / 60.0) * 0.85 * 1.0
    vs30 = 30.0 / ((10/vs1) + (10/vs2) + (10/vs3))
    
    st.metric("N60 Corregido", f"{n60:.1f} golpes/pie")
    st.metric("Velocidad Vs30", f"{vs30:.1f} m/s")

# ==========================================
# MÓDULO 7: CONSOLIDACIÓN
# ==========================================
with tabs[6]:
    st.header("7. Consolidación de Arcillas")
    col1, col2 = st.columns(2)
    with col1:
        cc = st.slider('Índice Cc:', 0.15, 0.60, 0.35)
        e0_c = st.slider('e0 inicial:', 0.50, 1.30, 0.90)
        hc = st.slider('Espesor Hc (m):', 1.0, 10.0, 4.0)
    with col2:
        ds = st.slider('Sobrecarga Δσ (kPa):', 10.0, 100.0, 40.0)
        cv_exp = st.slider('log10(Cv m²/año):', -2, 2, 0)

    s_total = (cc * hc / (1 + e0_c)) * np.log10((50.0 + ds) / 50.0)
    tiempos = np.linspace(0.1, 30, 100)
    tv = (10**cv_exp * tiempos) / ((hc/2)**2)
    u_vals = np.where(tv < 0.283, 100 * np.sqrt(4*tv/np.pi), 100 * (1 - 10**((1.781 - tv)/0.933)))
    asentamientos = (np.clip(u_vals, 0, 99.9) / 100.0) * s_total * 100
    
    fig7, ax7 = plt.subplots(figsize=(8, 4))
    ax7.plot(tiempos, asentamientos, 'm-', linewidth=2)
    ax7.set_xlabel('Tiempo (años)'); ax7.set_ylabel('Asentamiento (cm)'); ax7.invert_yaxis(); ax7.grid(True)
    st.pyplot(fig7)
    st.metric("Asentamiento Total Esperado", f"{s_total*100:.2f} cm")

# ==========================================
# MÓDULO 8: CÍRCULO DE MOHR
# ==========================================
with tabs[7]:
    st.header("8. Círculo de Mohr y Trayectorias")
    col1, col2 = st.columns(2)
    with col1: 
        s1 = st.slider('σ1 (kPa):', 100.0, 400.0, 180.0)
        phi = st.slider("Fricción φ' (°):", 15.0, 45.0, 30.0)
    with col2: 
        s3 = st.slider('σ3 (kPa):', 10.0, 150.0, 50.0)
        c_ef = st.slider("Cohesión c' (kPa):", 0.0, 40.0, 10.0)

    if s1 < s3: st.error("σ1 debe ser mayor que σ3")
    else:
        fig8, (ax8a, ax8b) = plt.subplots(1, 2, figsize=(10, 4))
        centro, radio = (s1 + s3)/2, (s1 - s3)/2
        th = np.linspace(0, np.pi, 100)
        
        # Panel Izquierdo (Mohr)
        ax8a.plot(centro + radio * np.cos(th), radio * np.sin(th), 'b-')
        ax8a.plot(np.linspace(0, s1*1.2, 10), c_ef + np.linspace(0, s1*1.2, 10)*np.tan(np.radians(phi)), 'r--')
        ax8a.set_aspect('equal'); ax8a.grid(True); ax8a.set_title("Plano de Mohr")
        
        # Panel Derecho (MIT)
        ax8b.plot(centro, radio, 'ro', label="Estado Actual")
        ax8b.plot(np.linspace(0, s1*1.2, 10), np.linspace(0, s1*1.2, 10)*np.sin(np.radians(phi)), 'g--', label="Línea Kf")
        ax8b.grid(True); ax8b.set_title("Espacio MIT (p-q)"); ax8b.legend()
        
        st.pyplot(fig8)
