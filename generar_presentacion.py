import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide
    
    # Palette colors
    COLOR_PRIMARY = RGBColor(27, 94, 32)      # Deep Forest Green
    COLOR_ACCENT = RGBColor(230, 81, 0)       # Citrus Orange
    COLOR_BG_LIGHT = RGBColor(245, 247, 245)  # Very light soft gray-green
    COLOR_WHITE = RGBColor(255, 255, 255)
    COLOR_TEXT_DARK = RGBColor(33, 33, 33)    # Charcoal
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139)# Slate gray
    COLOR_CARD_BG = RGBColor(255, 255, 255)
    COLOR_CARD_BORDER = RGBColor(200, 230, 201)

    def add_header(slide, title_text, category_text="PILLCO CITRUS S.A.C. | ESTUDIO DE VIABILIDAD"):
        # Top banner background
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = COLOR_PRIMARY
        header_shape.line.fill.background()
        
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = RGBColor(255, 204, 128)
        
        # Title text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE
        
        # Orange bottom accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_ACCENT
        line.line.fill.background()

    def add_footer(slide, slide_num):
        # Footer text
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10), Inches(0.3))
        tf_foot = footer_box.text_frame
        p_foot = tf_foot.paragraphs[0]
        p_foot.text = "Planta de Lavavajilla Biodegradable a partir de Cáscaras de Cítricos | UNHEVAL - Huánuco"
        p_foot.font.size = Pt(10)
        p_foot.font.color.rgb = COLOR_TEXT_MUTED
        
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.0), Inches(0.3))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{slide_num} / 15"
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = COLOR_PRIMARY

    # =========================================================================
    # SLIDE 1: PORTADA
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_PRIMARY
    bg1.line.fill.background()
    
    # Orange side strip
    strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.4), Inches(7.5))
    strip.fill.solid()
    strip.fill.fore_color.rgb = COLOR_ACCENT
    strip.line.fill.background()
    
    t_box1 = s1.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(11.0), Inches(5.8))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "UNIVERSIDAD NACIONAL HERMILIO VALDIZÁN\nFACULTAD DE INGENIERÍA INDUSTRIAL, DE SISTEMAS Y MECATRÓNICA"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 204, 128)
    p.space_after = Pt(20)
    
    p = tf1.add_paragraph()
    p.text = "ESTUDIO DE VIABILIDAD A NIVEL DE PERFIL:"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(8)
    
    p = tf1.add_paragraph()
    p.text = "Planta de Lavavajilla Líquido Biodegradable a partir de Extractos de Cáscaras de Naranja y Limón"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 235, 59)
    p.space_after = Pt(15)
    
    p = tf1.add_paragraph()
    p.text = "PROYECTO: PILLCO CITRUS S.A.C. | CIUDAD DE HUÁNUCO"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_after = Pt(35)
    
    p = tf1.add_paragraph()
    p.text = "• Docente: Dr. Fermín Montesinos Chávez\n• Asignatura: Formulación y Evaluación de Proyectos\n• Integrantes: Bueno Vela, Ayleem Naelly | Espinoza Cárdenas, Alexandra\n• Fecha: 28 de Octubre de 2026"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(230, 238, 232)

    # =========================================================================
    # SLIDE 2: INTRODUCCIÓN Y DATOS GENERALES
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Datos Generales y Justificación del Proyecto")
    add_footer(s2, 2)
    
    # 3 Cards Layout
    cards_data = [
        ("ENTIDAD Y MARCA", "Pillco Citrus S.A.C.\nMarca: Pillco Citrus", 
         "• Combina la identidad territorial del histórico valle de Pillco (Huánuco) con los cítricos locales.\n• Enfoque de Economía Circular: Aprovecha residuos agroalimentarios (cáscaras de naranja y limón).\n• Nuevo bien y proceso productivo a escala piloto."),
        ("LOCALIZACIÓN ESTRATÉGICA", "Ciudad de Huánuco\n(Huánuco, Pillco Marca, Amarilis)",
         "• Materia prima disponible: Huánuco cuenta con más de 1,014 ha de cítricos (875 ha naranja, 139 ha mandarina).\n• Proximidad al mercado objetivo urbano y reducción de fletes logísticos.\n• Conectividad para distribución directa a bodegas."),
        ("ESCALA Y CAPACIDAD PILOTO", "Dimensionamiento Técnico\nCapacidad Máxima: 120,000 bot/año",
         "• Tanque mezclador de 200 L por lote (400 botellas de 500 mL por lote).\n• 1 lote/día, 25 días/mes = 10,000 botellas/mes.\n• Valida formulación, costos y mercado antes de comprometer mayores inversiones.")
    ]
    
    for i, (head, subhead, body) in enumerate(cards_data):
        left = Inches(0.8 + i * 4.0)
        shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(3.7), Inches(5.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(241, 248, 242)
        shape.line.color.rgb = COLOR_CARD_BORDER
        shape.line.width = Pt(1.5)
        
        tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.3), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = head
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.space_after = Pt(8)
        
        p = tf.add_paragraph()
        p.text = subhead
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        p.space_after = Pt(12)
        
        p = tf.add_paragraph()
        p.text = body
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 3: DIFERENCIACIÓN E INNOVACIÓN TECNOLÓGICA
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Propuesta de Valor, Innovación y Competencia")
    add_footer(s3, 3)
    
    # Left Card: Differentiation
    c1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.1))
    c1.fill.solid()
    c1.fill.fore_color.rgb = RGBColor(255, 255, 255)
    c1.line.color.rgb = COLOR_PRIMARY
    c1.line.width = Pt(1.5)
    
    tb1 = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "ATRIBUTOS DIFERENCIALES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "• Poder Desengrasante Natural: Basado en limoneno extraído de cáscaras cítricas y tensioactivos biodegradables.\n• Sostenibilidad & Economía Circular: Reutiliza residuos de pollerías, juguerías y mercados locales.\n• Identidad Territorial: Marca huanuqueña que conecta con el orgullo regional y la ecología.\n• Calidad Controlada: Estandarización de lotes, pH neutro para la piel y viscosidad óptima.\n• Presentación: Botella ergonómica de 500 mL con dispensador push-pull."
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right Card: Comparative Table
    c2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(241, 248, 242)
    c2.line.color.rgb = COLOR_CARD_BORDER
    c2.line.width = Pt(1.5)
    
    tb2 = s3.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "BENCHMARKING DE COMPETIDORES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(10)
    
    p = tf2.add_paragraph()
    p.text = "1. Marcas Industriales Masivas (Ayudín, Sapolio, Cif):\n   - Precios: S/ 6.50 a S/ 8.50 (500 mL).\n   - Químicos sintéticos, fragancias artificiales.\n   - Ayudín concentra el 47.5% de recordación local.\n\n2. Marcas Económicas (Boreal, Home Care, EKOS):\n   - Precios: S/ 3.90 a S/ 4.50.\n   - Bajo poder desengrasante, sin enfoque ecológico.\n\n3. Alternativa Artesanal Informal:\n   - Sin registro sanitario ni control de calidad lote a lote.\n\n=> Pillco Citrus se posiciona a S/ 5.90 al público (precio medio justo y ecológico)."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 4: ESTUDIO DE MERCADO - RESULTADOS DE ENCUESTA
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Validación de Mercado: Hallazgos Clave de la Encuesta")
    add_footer(s4, 4)
    
    kpis = [
        ("82.5 %", "INTENCIÓN DE COMPRA", "Comprarían el lavavajilla cítrico producido en Huánuco (52.5% Seguro sí, 30% Probablemente)."),
        ("67.5 %", "VALORACIÓN ECOLÓGICA", "Consideran Importante o Muy Importante que sea natural y biodegradable (Puntaje: 3.95 / 5)."),
        ("35.0 %", "PENETRACIÓN LÍQUIDO", "Usan formato líquido actualmente (42 de 120 hogares). 65% usa pasta (mercado a convertir)."),
        ("47.5 %", "DISPOSICIÓN A PAGAR", "Dispuestos a pagar S/ 5.50 a más por la botella de 500 mL, validando el precio PVP de S/ 5.90.")
    ]
    
    for i, (num, title, desc) in enumerate(kpis):
        x = Inches(0.8 + (i % 2) * 6.0)
        y = Inches(1.6 + (i // 2) * 2.6)
        
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.35))
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_WHITE
        card.line.color.rgb = COLOR_PRIMARY
        card.line.width = Pt(1.5)
        
        tb = s4.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), Inches(5.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.space_after = Pt(4)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 5: CÁLCULO DE LA DEMANDA POTENCIAL (CON CAPTURA)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Cuantificación de la Demanda Potencial (Paso a Paso)")
    add_footer(s5, 5)
    
    # Left: Explanation & Formulas
    tb = s5.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(4.5), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MEMORIA DE CÁLCULO:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "1. Población Objetivo Urbana:\n   217,834 habitantes (Prov. Huánuco, INEI).\n\n2. Total de Hogares Urbanos:\n   217,834 ÷ 4.5 personas/hogar = 48,408 hogares.\n\n3. Mercado Efectivo Líquido:\n   48,408 × 35.0% = 16,943 hogares que usan formato líquido.\n\n4. Consumo Promedio Mensual:\n   1.43 botellas de 500 mL / mes por hogar.\n\n5. Demanda Potencial Anual:\n   16,943 × 1.43 × 12 = 290,742 botellas/año."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right: Insert Captured Image of Table
    img_path = "graficos_calculos/tabla_demanda.png"
    if os.path.exists(img_path):
        s5.shapes.add_picture(img_path, Inches(5.5), Inches(1.8), Inches(7.0))

    # =========================================================================
    # SLIDE 6: ESTRATEGIA DE MARKETING (4P)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Estrategia Comercial (Marketing Mix - 4P)")
    add_footer(s6, 6)
    
    mix_data = [
        ("PRODUCTO", "Lavavajilla Líquido 500 mL", 
         "• Alto poder desengrasante natural (limoneno).\n• Fragancia cítrica fresca sin químicos irritantes.\n• Biodegradable y suave con las manos.\n• Envase reciclable con sistema de recarga proyectado."),
        ("PRECIO", "Estrategia de Penetración",
         "• Precio Venta al Canal: S/ 4.90 por botella.\n• Precio Venta al Público: S/ 5.90 por botella.\n• Margen atractivo para bodega: S/ 1.00 (20.4%).\n• Competitivo frente a Sapolio (S/ 6.50) y Cif (S/ 7.50)."),
        ("PLAZA", "Distribución Directa Local",
         "• Canal principal: Bodegas y minimarkets urbanos.\n• Reparto propio semanal en moto-furgón / flete local.\n• Mercados de abastos de Huánuco y Amarilis.\n• Expansión: Supermercados y restaurantes desde Año 2."),
        ("PROMOCIÓN", "Marketing Verde y Cercanía",
         "• Alianzas de economía circular con juguerías y pollerías.\n• Degustaciones de aroma y pruebas en ferias locales.\n• Contenido educativo en redes sobre sostenibilidad.\n• Material POP llamativo para puntos de venta bodegueros.")
    ]
    
    for i, (p_name, p_sub, p_desc) in enumerate(mix_data):
        left = Inches(0.8 + i * 3.0)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.6), Inches(2.75), Inches(5.1))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(245, 247, 245)
        card.line.color.rgb = COLOR_PRIMARY
        card.line.width = Pt(1.5)
        
        tb = s6.shapes.add_textbox(left + Inches(0.15), Inches(1.8), Inches(2.45), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = p_name
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        p.space_after = Pt(4)
        
        p = tf.add_paragraph()
        p.text = p_sub
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 7: INGENIERÍA Y PROCESO PRODUCTIVO
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Ingeniería del Proyecto: Proceso Productivo y Planta")
    add_footer(s7, 7)
    
    # Process sequence boxes
    steps = [
        "1. Recepción y Selección\n(Cáscaras cítricas)",
        "2. Lavado y\nDesinfección",
        "3. Trituración y\nMaceración",
        "4. Extracción Aceite\n(Limoneno y filtrado)",
        "5. Mezcla y Aditivos\n(Tensioactivos y agua)",
        "6. Control Calidad\n(pH neutro, viscosidad)",
        "7. Envasado y\nEtiquetado (500 mL)",
        "8. Almacén y\nDistribución Comercial"
    ]
    
    for i, step in enumerate(steps):
        row = i // 4
        col = i % 4
        left = Inches(0.8 + col * 2.95)
        top = Inches(1.6 + row * 1.6)
        
        box = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.7), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = COLOR_PRIMARY if i in [3, 4, 5] else RGBColor(232, 245, 233)
        box.line.color.rgb = COLOR_PRIMARY
        box.line.width = Pt(1)
        
        tb = s7.shapes.add_textbox(left + Inches(0.1), top + Inches(0.15), Inches(2.5), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = step
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE if i in [3, 4, 5] else COLOR_PRIMARY
        
    # Bottom Note Box
    bot_card = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.6))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = RGBColor(255, 248, 225)
    bot_card.line.color.rgb = RGBColor(255, 179, 0)
    bot_card.line.width = Pt(1)
    
    tb_b = s7.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(11.3), Inches(1.4))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p = tf_b.paragraphs[0]
    p.text = "REQUERIMIENTOS TÉCNICOS Y REGULATORIOS CLAVE:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(4)
    p = tf_b.add_paragraph()
    p.text = "• Local: 60 m² con zonificación compatible, piso lavable, energía monofásica/trifásica y suministro continuo de agua.\n• Equipamiento: Tanque de acero inox 200 L con agitador, equipo extractor de aceites, molino, llenadora y medidor de pH.\n• Seguridad & Calidad: Manipulación de limoneno (irritante/inflamable) bajo EPP y ventilación. Trámite de autorización sanitaria ante DIGESA."
    p.font.size = Pt(10)
    p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 8: INVERSIÓN TOTAL DEL PROYECTO (CON CAPTURA)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Presupuesto de Inversión Total (S/ 66,000)")
    add_footer(s8, 8)
    
    # Left: Explanation & Breakdown
    tb = s8.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DESGLOSE DE LA INVERSIÓN:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "• Inversión Tangible: S/ 30,000 (45.5%)\n  Tanque 200L, extractor, triturador, llenadora, mobiliario y acondicionamiento.\n\n• Inversión Intangible: S/ 8,000 (12.1%)\n  Constitución S.A.C., registro INDECOPI, trámites DIGESA y diseño de marca.\n\n• Capital de Trabajo: S/ 28,000 (42.4%)\n  Cubre 1.93 meses de operación y garantiza pagar la cuota del préstamo del Año 1.\n\n=> FÓRMULA:\nInv. Total = 30,000 + 8,000 + 28,000 = S/ 66,000"
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right: Insert Captured Image of Investment Table
    img_path = "graficos_calculos/tabla_inversion.png"
    if os.path.exists(img_path):
        s8.shapes.add_picture(img_path, Inches(5.3), Inches(1.5), Inches(7.3))

    # =========================================================================
    # SLIDE 9: FINANCIAMIENTO Y CRONOGRAMA DE DEUDA (CON CAPTURA)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. Estructura de Financiamiento y Servicio de Deuda")
    add_footer(s9, 9)
    
    # Left: Details
    tb = s9.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ESTRUCTURA Y CONDICIONES:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "• Capital Propio: S/ 39,600 (60%)\n  Aportado en partes iguales por las 2 socias. Costo de Oportunidad (COK) = 20.0%.\n\n• Deuda Financiera: S/ 26,400 (40%)\n  Préstamo a 3 años, TEA = 24.0% anual.\n\n• Cuota Anual Constante (Francés):\n  Cuota = 26,400 × 0.24 / [1 - (1.24)^-3]\n  Cuota = S/ 13,325 al año.\n\n• Costo Promedio Capital (WACC):\n  WACC = 0.60(20%) + 0.40(24%)(1-0.10)\n  WACC = 20.64% anual."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right: Insert Captured Image
    img_path = "graficos_calculos/tabla_prestamo.png"
    if os.path.exists(img_path):
        s9.shapes.add_picture(img_path, Inches(5.3), Inches(2.0), Inches(7.3))

    # =========================================================================
    # SLIDE 10: PROYECCIÓN DE COSTOS Y ECONOMÍAS DE ESCALA (CON CAPTURA)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Proyección de Costos Operativos y Economías de Escala")
    add_footer(s10, 10)
    
    # Left: Explanation
    tb = s10.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(4.2), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ANÁLISIS DE COSTOS:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "• Costo Variable Unitario (Año 1):\n  S/ 2.30 por botella (Tensioactivos S/ 0.90, Envase/tapa S/ 0.70, Insumos S/ 0.70).\n\n• Costos Fijos Anuales (Año 1):\n  S/ 98,640 (Planilla 3 personas S/ 66,240, Alquiler local S/ 14,400, Servicios/mkt).\n\n• Reducción de Costo Unitario:\n  Baja de S/ 5.29 (Año 1) a S/ 4.13 (Año 5) al diluir costos fijos.\n  En Año 1 hay pérdida operativa; desde Año 2 el precio supera al costo."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right: Insert Captured Image
    img_path = "graficos_calculos/tabla_costos.png"
    if os.path.exists(img_path):
        s10.shapes.add_picture(img_path, Inches(5.2), Inches(1.8), Inches(7.4))

    # =========================================================================
    # SLIDE 11: ESTADO DE RESULTADOS PROYECTADO (CON CAPTURA)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10. Estado de Resultados Proyectado a 5 Años")
    add_footer(s11, 11)
    
    # Left: Text highlights
    tb = s11.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(4.2), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PUNTOS CLAVE DEL EJERCICIO:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "• Año 1 (Fase de Inserción):\n  Ingresos: S/ 161,391 (32,937 botellas).\n  Pérdida neta: -S/ 23,940 debido a ventas por debajo del equilibrio. Financiada con capital de trabajo.\n\n• Año 2 al 5 (Crecimiento sostenido):\n  Año 2 genera utilidad neta de S/ 3,705.\n  Año 5 alcanza utilidad neta de S/ 64,204 con margen neto del 18.6%.\n\n• Régimen Tributario MYPE:\n  Tasa de Impuesto a la Renta de 10% (utilidad menor a 15 UIT = S/ 82,500)."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right: Insert Captured Image
    img_path = "graficos_calculos/tabla_estado_resultados.png"
    if os.path.exists(img_path):
        s11.shapes.add_picture(img_path, Inches(5.2), Inches(1.4), Inches(7.4))

    # =========================================================================
    # SLIDE 12: FLUJO DE CAJA ECONÓMICO Y FINANCIERO (CON CAPTURA)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "11. Flujo de Caja Económico y Financiero")
    add_footer(s12, 12)
    
    # Left: Explanations
    tb = s12.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ESTRUCTURA DE LIQUIDEZ:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "• Flujo de Caja Económico (FCE):\n  Evalúa la rentabilidad pura del proyecto sin deuda. En Año 0 egresan S/ 66,000.\n\n• Flujo de Caja Financiero (FCF):\n  Evalúa la rentabilidad del accionista. En Año 0 el aporte es de S/ 39,600.\n  Deduce el servicio de la deuda (Años 1-3).\n\n• Valor Residual (Año 5):\n  S/ 43,000 (Valor libros activos S/ 15,000 + Recuperación Capital Trabajo S/ 28,000)."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right: Insert Captured Image
    img_path = "graficos_calculos/tabla_flujos_caja.png"
    if os.path.exists(img_path):
        s12.shapes.add_picture(img_path, Inches(5.3), Inches(1.8), Inches(7.3))

    # =========================================================================
    # SLIDE 13: EVALUACIÓN ECONÓMICA Y FINANCIERA (VAN, TIR, B/C) (CON CAPTURA)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "12. Indicadores de Rentabilidad y Decisión de Inversión")
    add_footer(s13, 13)
    
    # Top/Left: Insert Table Image
    img_path = "graficos_calculos/tabla_indicadores.png"
    if os.path.exists(img_path):
        s13.shapes.add_picture(img_path, Inches(0.8), Inches(1.6), Inches(7.5))
        
    # Right Card: Viability Conclusion
    c = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.6), Inches(4.0), Inches(5.0))
    c.fill.solid()
    c.fill.fore_color.rgb = RGBColor(232, 245, 233)
    c.line.color.rgb = COLOR_PRIMARY
    c.line.width = Pt(1.5)
    
    tb = s13.shapes.add_textbox(Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DICTAMEN FINANCIERO"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf.add_paragraph()
    p.text = "✓ VIABILIDAD ECONÓMICA:\n  VAN = S/ 22,110 > 0\n  TIR = 28.8% > WACC (20.64%)\n  B/C = 1.34 (Retorna S/ 1.34 por cada sol)\n\n✓ VIABILIDAD FINANCIERA:\n  VAN Financiero = S/ 23,013 > 0\n  TIR Financiera = 29.9% > COK (20.0%)\n  B/C Financiero = 1.58\n\n✓ RECUPERACIÓN:\n  Capital recuperado en 3.5 años."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 14: PUNTO DE EQUILIBRIO Y SENSIBILIDAD (CON CAPTURA)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "13. Punto de Equilibrio y Análisis de Sensibilidad")
    add_footer(s14, 14)
    
    # Left: Graph Equilibrio
    img1 = "graficos_calculos/grafico_equilibrio.png"
    if os.path.exists(img1):
        s14.shapes.add_picture(img1, Inches(0.6), Inches(1.5), Inches(6.0))
        
    # Right: Graph Sensibilidad
    img2 = "graficos_calculos/grafico_sensibilidad.png"
    if os.path.exists(img2):
        s14.shapes.add_picture(img2, Inches(6.8), Inches(1.5), Inches(5.9))
        
    # Bottom Note
    tb_sens = s14.shapes.add_textbox(Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.8))
    tf_s = tb_sens.text_frame
    tf_s.word_wrap = True
    p = tf_s.paragraphs[0]
    p.text = "• Equilibrio Operativo: 37,938 botellas/año. En Año 1 (32,937 bot.) no se cubre; en Año 2 (42,982 bot.) se supera con holgura.\n• Sensibilidad Crítica: El proyecto es altamente sensible al precio (límite -3.4%) y al volumen (límite -6.3%). Se debe blindar el canal de distribución."
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_DARK

    # =========================================================================
    # SLIDE 15: CONCLUSIONES Y RECOMENDACIONES
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "14. Conclusiones y Recomendaciones Estratégicas")
    add_footer(s15, 15)
    
    # Left Box: Conclusiones
    c_c = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.1))
    c_c.fill.solid()
    c_c.fill.fore_color.rgb = RGBColor(241, 248, 242)
    c_c.line.color.rgb = COLOR_PRIMARY
    c_c.line.width = Pt(1.5)
    
    tb_c = s15.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "CONCLUSIONES PRINCIPALES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    
    p = tf_c.add_paragraph()
    p.text = "1. Proyecto Viable a Nivel de Perfil: Rentabilidad respaldada por VAN de S/ 22,110 y TIR de 28.8% superando holgadamente el WACC.\n\n2. Gran Oportunidad Ecológica y Territorial: 82.5% de aceptación y aprovechamiento de 8 ton de cáscaras cítricas locales bajo economía circular.\n\n3. Resiliencia Operativa: Inversión de S/ 66,000 con capital de trabajo dimensionado para blindar las pérdidas del primer año hasta alcanzar equilibrio en el Año 2."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK
    
    # Right Box: Recomendaciones
    c_r = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.1))
    c_r.fill.solid()
    c_r.fill.fore_color.rgb = RGBColor(255, 248, 225)
    c_r.line.color.rgb = COLOR_ACCENT
    c_r.line.width = Pt(1.5)
    
    tb_r = s15.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "RECOMENDACIONES PARA PREFACTIBILIDAD"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(10)
    
    p = tf_r.add_paragraph()
    p.text = "1. Asegurar Preventas con Bodegas: Cerrar acuerdos de colocación para mitigar el riesgo por sensibilidad de precio y volumen.\n\n2. Cotizaciones Formales: Reemplazar supuestos de maquinaria y adecuación de local (S/ 30,000) por cotizaciones de proveedores.\n\n3. Trámite Regulatorio: Consultar con DIGESA los requisitos para notificación sanitaria obligatoria en higiene doméstica.\n\n4. Validación de Laboratorio: Ensayos de estabilidad, vida útil y capacidad desengrasante comparativa frente a Ayudín."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_TEXT_DARK

    output_filename = "Presentacion_Viabilidad_Pillco_Citrus.pptx"
    prs.save(output_filename)
    print(f"Presentación guardada exitosamente como '{output_filename}' con 15 diapositivas.")

if __name__ == "__main__":
    create_deck()
