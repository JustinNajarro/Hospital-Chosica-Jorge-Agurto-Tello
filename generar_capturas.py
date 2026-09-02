import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("graficos_calculos", exist_ok=True)

# Configuración de estilo general
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

def save_table_image(filename, title, col_labels, cell_data, col_widths=None, highlight_rows=None, highlight_color="#E8F5E9"):
    fig, ax = plt.subplots(figsize=(10, len(cell_data) * 0.45 + 1.2), dpi=200)
    ax.axis('off')
    ax.axis('tight')
    
    # Title
    plt.title(title, fontsize=12, fontweight='bold', color='#1B5E20', pad=15, loc='left')
    
    table = ax.table(cellText=cell_data, colLabels=col_labels, colWidths=col_widths, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1, 1.5)
    
    # Style header
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#B0BEC5')
        if row == 0:
            cell.set_facecolor('#2E7D32')
            cell.get_text().set_color('white')
            cell.get_text().set_fontweight('bold')
        else:
            if highlight_rows and row in highlight_rows:
                cell.set_facecolor(highlight_color)
                cell.get_text().set_fontweight('bold')
            elif row % 2 == 1:
                cell.set_facecolor('#F1F8E9')
            else:
                cell.set_facecolor('#FFFFFF')
                
    plt.tight_layout()
    plt.savefig(f"graficos_calculos/{filename}", bbox_inches='tight', facecolor='white')
    plt.close()

# 1. Tabla Demanda Potencial
col_labels = ["Paso / Variable", "Valor", "Supuesto / Fórmula"]
cell_data = [
    ["Población urbana provincial (2017)", "217,834 hab.", "Censo INEI (City Population, 2022)"],
    ["Tamaño medio del hogar", "4.5 personas", "Encuesta, P2 (Promedio)"],
    ["Total Hogares Urbanos", "48,408", "217,834 ÷ 4.5 personas"],
    ["Hogares que usan lavavajilla líquido", "16,943 (35 %)", "Encuesta, P3 (Líquido 32.5% + Ambos 2.5%)"],
    ["Consumo mensual por hogar", "1.43 botellas/mes", "Encuesta, P5 (Botella 500 mL)"],
    ["Demanda potencial anual (Año 1)", "290,742 botellas", "16,943 × 1.43 botellas × 12 meses"]
]
save_table_image("tabla_demanda.png", "CÁLCULO DE LA DEMANDA POTENCIAL (AÑO 1)", col_labels, cell_data, [0.35, 0.22, 0.43], [6], "#C8E6C9")

# 2. Tabla Inversión Total
col_labels = ["Rubro de Inversión", "Monto (S/)", "%", "Origen y Base del Cálculo"]
cell_data = [
    ["Inversión Tangible (Equipos y Acond.)", "30,000", "45.5%", "Tanque 200L, extractor, triturador, etc."],
    ["Constitución S.A.C. y licencias", "2,500", "3.8%", "Minuta, registros y licencia municipal"],
    ["Autorización sanitaria y ensayos", "3,000", "4.5%", "Trámite DIGESA y ensayos de calidad"],
    ["Registro de marca (INDECOPI)", "600", "0.9%", "Tasa INDECOPI S/ 534.90 + gastos"],
    ["Diseño de etiqueta y lanzamiento", "1,900", "2.9%", "Diseño gráfico, primer tiraje, redes"],
    ["Subtotal Inversión Intangible", "8,000", "12.1%", "Suma de partidas intangibles"],
    ["Capital de Trabajo (Caja inicial)", "28,000", "42.4%", "Cubre déficit operativo y cuota año 1"],
    ["INVERSIÓN TOTAL DEL PROYECTO", "66,000", "100.0%", "Tangible + Intangible + Capital de Trabajo"]
]
save_table_image("tabla_inversion.png", "ESTRUCTURA DE LA INVERSIÓN TOTAL DEL PROYECTO", col_labels, cell_data, [0.38, 0.16, 0.12, 0.34], [6, 8], "#FFE0B2")

# 3. Financiamiento y Cronograma del Préstamo
col_labels = ["Año", "Saldo Inicial", "Interés (24%)", "Amortización", "Cuota Anual", "Saldo Final"]
cell_data = [
    ["Año 1", "S/ 26,400", "S/ 6,336", "S/ 6,989", "S/ 13,325", "S/ 19,411"],
    ["Año 2", "S/ 19,411", "S/ 4,659", "S/ 8,666", "S/ 13,325", "S/ 10,746"],
    ["Año 3", "S/ 10,746", "S/ 2,579", "S/ 10,746", "S/ 13,325", "S/ 0"],
    ["TOTAL", "-", "S/ 13,574", "S/ 26,400", "S/ 39,974", "-"]
]
save_table_image("tabla_prestamo.png", "CRONOGRAMA DEL PRÉSTAMO (S/ 26,400 - TEA 24% - 3 AÑOS)", col_labels, cell_data, [0.12, 0.18, 0.18, 0.18, 0.18, 0.16], [4], "#FFF9C4")

# 4. Proyección Costos Operativos y Unitarios
col_labels = ["Concepto de Costo", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
cell_data = [
    ["Ventas Proyectadas (botellas)", "32,937", "42,982", "53,322", "59,042", "64,921"],
    ["Costo Variable Unitario (S/)", "S/ 2.30", "S/ 2.35", "S/ 2.39", "S/ 2.44", "S/ 2.49"],
    ["Costos Variables Totales (S/)", "75,755", "100,836", "127,595", "144,108", "161,627"],
    ["Costos Fijos Totales (S/)", "98,640", "100,613", "102,625", "104,678", "106,771"],
    ["COSTOS OPERATIVOS TOTALES", "S/ 174,395", "S/ 201,449", "S/ 230,220", "S/ 248,786", "S/ 268,398"],
    ["COSTO TOTAL POR BOTELLA (S/)", "S/ 5.29", "S/ 4.69", "S/ 4.32", "S/ 4.21", "S/ 4.13"]
]
save_table_image("tabla_costos.png", "PROYECCIÓN DE COSTOS OPERATIVOS Y COSTO TOTAL UNITARIO", col_labels, cell_data, [0.30, 0.14, 0.14, 0.14, 0.14, 0.14], [5, 6], "#E0F2F1")

# 5. Estado de Resultados Proyectado
col_labels = ["Concepto (en Soles)", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
cell_data = [
    ["Ingresos por Ventas", "161,391", "214,824", "271,833", "307,014", "344,336"],
    ["(-) Costos Variables", "-75,755", "-100,836", "-127,595", "-144,108", "-161,627"],
    ["(-) Costos Fijos", "-98,640", "-100,613", "-102,625", "-104,678", "-106,771"],
    ["EBITDA (Resultado Operativo)", "-13,004", "13,375", "41,613", "58,228", "75,938"],
    ["(-) Depreciación y Amortización", "-4,600", "-4,600", "-4,600", "-4,600", "-4,600"],
    ["EBIT (Utilidad Operativa)", "-17,604", "8,775", "37,013", "53,628", "71,338"],
    ["(-) Intereses Préstamo", "-6,336", "-4,659", "-2,579", "0", "0"],
    ["Utilidad Antes Impuestos (UAI)", "-23,940", "4,117", "34,434", "53,628", "71,338"],
    ["(-) Impuesto Renta (10% MYPE)", "0", "-412", "-3,443", "-5,363", "-7,134"],
    ["UTILIDAD NETA", "-S/ 23,940", "S/ 3,705", "S/ 30,991", "S/ 48,265", "S/ 64,204"]
]
save_table_image("tabla_estado_resultados.png", "ESTADO DE RESULTADOS PROYECTADO A 5 AÑOS (S/)", col_labels, cell_data, [0.30, 0.14, 0.14, 0.14, 0.14, 0.14], [4, 10], "#C8E6C9")

# 6. Flujo de Caja Económico y Financiero
col_labels = ["Flujo de Caja (S/)", "Año 0", "Año 1", "Año 2", "Año 3", "Año 4", "Año 5"]
cell_data = [
    ["Inversión Total", "-66,000", "-", "-", "-", "-", "-"],
    ["EBITDA", "-", "-13,004", "13,375", "41,613", "58,228", "75,938"],
    ["(-) Impuesto sobre EBIT", "-", "0", "-878", "-3,701", "-5,363", "-7,134"],
    ["(+) Valor Residual", "-", "-", "-", "-", "-", "43,000"],
    ["FLUJO DE CAJA ECONÓMICO (FCE)", "-66,000", "-13,004", "12,498", "37,912", "52,865", "111,804"],
    ["Aporte Propio (60%)", "-39,600", "-", "-", "-", "-", "-"],
    ["Amortización Préstamo", "-", "-6,989", "-8,666", "-10,746", "0", "0"],
    ["FLUJO DE CAJA FINANCIERO (FCF)", "-39,600", "-26,328", "-361", "24,845", "52,865", "111,804"]
]
save_table_image("tabla_flujos_caja.png", "FLUJOS DE CAJA ECONÓMICO Y FINANCIERO (S/)", col_labels, cell_data, [0.28, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12], [5, 8], "#D1C4E9")

# 7. Cuadro Comparativo de Rentabilidad (VAN, TIR, B/C, Payback)
col_labels = ["Indicador Financiero", "Evaluación Económica", "Evaluación Financiera", "Criterio de Aceptación"]
cell_data = [
    ["Tasa de Descuento", "20.64 % (WACC)", "20.00 % (COK)", "Costo de capital de referencia"],
    ["Valor Actual Neto (VAN)", "S/ 22,110", "S/ 23,013", "VAN > 0 (Proyecto Rentable)"],
    ["Tasa Interna Retorno (TIR)", "28.8 %", "29.9 %", "TIR > Tasa de descuento"],
    ["Relación Beneficio / Costo (B/C)", "1.34", "1.58", "B/C > 1.0 (Devuelve S/ 1.34 x S/ 1)"],
    ["Período Recuperación (PR)", "3.5 años", "3.8 años", "Se recupera dentro del horizonte"]
]
save_table_image("tabla_indicadores.png", "RESUMEN DE INDICADORES DE RENTABILIDAD DEL PROYECTO", col_labels, cell_data, [0.28, 0.22, 0.22, 0.28], [2, 3], "#DCEDC8")

# 8. Gráfico de Punto de Equilibrio y Margen de Seguridad
fig, ax = plt.subplots(figsize=(9, 4.2), dpi=200)
years = ['Año 1', 'Año 2', 'Año 3', 'Año 4', 'Año 5']
x = np.arange(len(years))
width = 0.28

eq_op = [37938] * 5
eq_cont = [42145, 41430, 40592, 39606, 39573]
ventas = [32937, 42982, 53322, 59042, 64921]

r1 = ax.bar(x - width, eq_op, width, label='Equilibrio Operativo (37,938)', color='#90CAF9')
r2 = ax.bar(x, eq_cont, width, label='Equilibrio Contable', color='#EF9A9A')
r3 = ax.bar(x + width, ventas, width, label='Ventas Proyectadas', color='#2E7D32')

ax.set_ylabel('Botellas de 500 mL', fontsize=11, fontweight='bold', color='#333333')
ax.set_title('PUNTO DE EQUILIBRIO VS. VENTAS PROYECTADAS (BOT/AÑO)', fontsize=12, fontweight='bold', color='#1B5E20', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(years, fontsize=10, fontweight='bold')
ax.legend(frameon=True, facecolor='#FAFAFA', edgecolor='#CCCCCC')
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Value labels on top of bars
for rects in [r1, r2, r3]:
    for rect in rects:
        h = rect.get_height()
        ax.annotate(f'{int(h):,}',
                    xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=7.5, fontweight='bold')

plt.tight_layout()
plt.savefig("graficos_calculos/grafico_equilibrio.png", bbox_inches='tight', facecolor='white')
plt.close()

# 9. Análisis de Sensibilidad (Gráfico de barras de impacto en VAN)
fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=200)
escenarios = ['Base\n(S/ 22,110)', 'Ventas -15%\n(-S/ 30,807)', 'Ventas +15%\n(S/ 74,456)', 'Precio -5%\n(-S/ 10,909)']
vans = [22110, -30807, 74456, -10909]
colors = ['#1976D2', '#D32F2F', '#388E3C', '#E64A19']

bars = ax.bar(escenarios, vans, color=colors, width=0.55, edgecolor='#333333', linewidth=0.8)
ax.axhline(0, color='black', linewidth=1)
ax.set_ylabel('Valor Actual Neto Económico (S/)', fontsize=11, fontweight='bold', color='#333333')
ax.set_title('ANÁLISIS DE SENSIBILIDAD DEL VAN ECONÓMICO', fontsize=12, fontweight='bold', color='#1B5E20', pad=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    h = bar.get_height()
    va = 'bottom' if h >= 0 else 'top'
    ypos = h + (1500 if h >= 0 else -3000)
    ax.annotate(f"S/ {int(h):,}",
                xy=(bar.get_x() + bar.get_width() / 2, ypos),
                ha='center', va=va, fontsize=9.5, fontweight='bold',
                color='#D32F2F' if h < 0 else '#1B5E20')

# Threshold markers note
ax.text(0.5, -0.22, "Punto Crítico Límite: Caída máxima tolerable de Volumen = 6.3% | Caída máxima tolerable de Precio = 3.4%",
        transform=ax.transAxes, ha='center', fontsize=9, fontstyle='italic', bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF3E0', edgecolor='#FFB74D'))

plt.tight_layout()
plt.savefig("graficos_calculos/grafico_sensibilidad.png", bbox_inches='tight', facecolor='white')
plt.close()

print("Todas las capturas de cálculos han sido generadas exitosamente en graficos_calculos/")
