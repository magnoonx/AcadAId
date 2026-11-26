"""
Escena 4: Relevancia Marginal Máxima (MMR) en Espacio de Embeddings 3D
AcadAId: Marco de Inferencia Local con Generación Aumentada por Recuperación

Explica dinámicamente el algoritmo de Relevancia Marginal Máxima (MMR, Carbonell & Goldstein, 1998)
aplicado a la investigación científica y RAG académico:
1. Proyección de la Consulta de Investigación Q en el espacio tridimensional de embeddings.
2. Selección del primer documento D1 por máxima relevancia semántica.
3. El Dilema de la Similitud Estándar (k-NN): Detección y penalización del paper redundante D_red
   mediante rotación orbital 3D que evidencia la colinealidad semántica.
4. Selección guiada por MMR del paper metodológicamente complementario D2 (diversidad vectorial).
5. Selección del paper D3 (ética y soberanía) completando el Tetraedro de Cobertura Científica 3D.
6. Rotación 360° continua mostrando la superioridad de MMR frente a búsquedas por similitud pura.
"""

from manim import *
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FONT_SERIF, FONT_SANS


class PaperBadge3D(VGroup):
    """
    Tarjeta de identificación 3D flotante para documentos científicos.
    Diseñada para orientarse automáticamente hacia la cámara (billboarding).
    """

    def __init__(
        self,
        doc_id: str,
        title: str,
        category: str,
        color: str = "#00F0FF",
        score_text: str = "",
        width: float = 2.4,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # 1. Cabecera con ID y categoría
        id_label = Text(doc_id, font=FONT_SANS, weight=BOLD, font_size=11, color=color)
        cat_label = Text(category, font=FONT_SANS, font_size=8, color="#94A3B8")
        header = VGroup(id_label, cat_label).arrange(RIGHT, buff=0.15)

        # 2. Título del paper científico
        title_label = Text(
            title,
            font=FONT_SANS,
            weight=BOLD,
            font_size=10,
            color=WHITE,
        )

        elements = [header, title_label]

        # 3. Métrica / Puntuación opcional
        if score_text:
            score_lbl = Text(score_text, font=FONT_SANS, font_size=8.5, color=color)
            elements.append(score_lbl)

        content = VGroup(*elements).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        card_width = max(width, content.width + 0.35)
        card_height = content.height + 0.22

        bg_card = RoundedRectangle(
            corner_radius=0.08,
            width=card_width,
            height=card_height,
            stroke_width=1.3,
            stroke_color=color,
            fill_color="#0A1124",
            fill_opacity=0.92,
        )
        content.move_to(bg_card.get_center())

        self.bg_card = bg_card
        self.content = content
        self.color = color
        self.add(bg_card, content)


class MMR3DScene(ThreeDScene):
    """
    Animación 3D cinematográfica del algoritmo MMR en el espacio semántico.
    Demuestra cómo balancear Relevancia y Diversidad en la investigación científica.
    """

    def construct(self):
        # 1. Fondo ciberespacial científico profundo
        self.camera.background_color = "#030612"

        # 2. Orientación inicial de la cámara 3D (perspectiva isométrica elevada)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-55 * DEGREES, zoom=0.88)

        # ====================================================
        # FASE 0: INTERFAZ HUD FUTURISTA FIJA EN PANTALLA
        # ====================================================
        # Banner superior fijo
        header_box = RoundedRectangle(
            corner_radius=0.10,
            width=13.2,
            height=0.64,
            stroke_width=1.2,
            stroke_color="#1E3A8A",
            fill_color="#080F24",
            fill_opacity=0.92,
        )
        header_box.to_edge(UP, buff=0.18)

        ai_tag = Text("ACADAID // RECUPERACIÓN SEMÁNTICA", font=FONT_SANS, weight=BOLD, font_size=10, color="#38BDF8")
        title_hud = Text("RELEVANCIA MARGINAL MÁXIMA (MMR) EN ESPACIO 3D", font=FONT_SANS, weight=BOLD, font_size=13, color=WHITE)
        title_grp = VGroup(ai_tag, title_hud).arrange(RIGHT, buff=0.25)
        title_grp.move_to(header_box.get_center())

        # Indicador de estado del algoritmo
        status_dot = Dot(radius=0.06, color="#00F0FF")
        status_txt = Text("ESPACIO VECTORIAL 3D", font=FONT_SANS, weight=BOLD, font_size=9, color="#00F0FF")
        status_hud = VGroup(status_dot, status_txt).arrange(RIGHT, buff=0.10)
        status_hud.next_to(header_box.get_right(), LEFT, buff=0.35)

        param_badge = MathTex(r"\lambda = 0.50 \text{ (Balance Relevancia - Diversidad)}", font_size=15, color="#F59E0B")
        param_badge.next_to(header_box.get_left(), RIGHT, buff=0.35)

        hud_top = VGroup(header_box, title_grp, status_hud, param_badge)

        # Panel inferior izquierdo: Formulación Matemática de MMR
        math_box = RoundedRectangle(
            corner_radius=0.12,
            width=6.1,
            height=1.45,
            stroke_width=1.0,
            stroke_color="#1E293B",
            fill_color="#060C1D",
            fill_opacity=0.88,
        )
        math_box.to_corner(DL, buff=0.25)

        math_title = Text("CRITERIO MARGINAL (CARBONELL & GOLDSTEIN, 1998)", font=FONT_SANS, weight=BOLD, font_size=9, color="#94A3B8")
        math_eq = MathTex(
            r"\text{MMR} = \arg\max_{D_i \in R \setminus S} \left[ \lambda\,\text{Sim}_1(D_i, Q) - (1-\lambda)\max_{D_j \in S}\text{Sim}_2(D_i, D_j) \right]",
            font_size=14,
            color="#F8FAFC",
        )
        math_sub1 = Text("Relevancia hacia la Consulta Q", font=FONT_SANS, font_size=8.5, color="#10B981")
        math_sub2 = Text("Penalización por Redundancia con S", font=FONT_SANS, font_size=8.5, color="#F43F5E")
        math_subs = VGroup(math_sub1, math_sub2).arrange(RIGHT, buff=0.30)

        math_content = VGroup(math_title, math_eq, math_subs).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        math_content.move_to(math_box.get_center())
        hud_math = VGroup(math_box, math_content)

        # Panel inferior derecho: Telemetría de Selección Científica
        tele_box = RoundedRectangle(
            corner_radius=0.12,
            width=4.8,
            height=1.45,
            stroke_width=1.0,
            stroke_color="#1E293B",
            fill_color="#060C1D",
            fill_opacity=0.88,
        )
        tele_box.to_corner(DR, buff=0.25)

        t1 = Text("APLICACIÓN: RAG Científico (AcadAId)", font=FONT_SANS, font_size=8.5, color="#10B981")
        t2 = Text("CORPUS SELECCIONADO S: 0 / 3 Papers", font=FONT_SANS, font_size=8.5, color="#E2E8F0")
        t3 = Text("REDUNDANCIA INTER-DOCUMENTAL: 0.0%", font=FONT_SANS, font_size=8.5, color="#38BDF8")
        t4 = Text("COBERTURA EPISTÉMICA: En Evaluación...", font=FONT_SANS, font_size=8.5, color="#F59E0B")
        tele_content = VGroup(t1, t2, t3, t4).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        tele_content.move_to(tele_box.get_center())
        hud_tele = VGroup(tele_box, tele_content)

        # Registrar HUD en pantalla fija
        self.add_fixed_in_frame_mobjects(hud_top, hud_math, hud_tele)

        # ====================================================
        # FASE 1: CONSTRUCCIÓN DEL ESPACIO SEMÁNTICO 3D
        # ====================================================
        # Ejes tridimensionales de representación de embeddings
        axes = ThreeDAxes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-3.2, 3.2, 1],
            z_range=[-1.5, 2.8, 1],
            x_length=6.4,
            y_length=6.4,
            z_length=4.3,
            axis_config={
                "color": "#1E3A8A",
                "stroke_width": 1.2,
            },
        )

        # Etiquetas de los ejes semánticos (orientadas a la cámara)
        label_x = Text("Dimensión Arquitectura / Metodología", font=FONT_SANS, font_size=9, color="#38BDF8")
        label_x.move_to(np.array([3.4, 0.2, 0]))

        label_y = Text("Dimensión Rendimiento / Benchmarks", font=FONT_SANS, font_size=9, color="#34D399")
        label_y.move_to(np.array([0.2, 3.4, 0]))

        label_z = Text("Dimensión Ética & Privacidad Local", font=FONT_SANS, font_size=9, color="#A855F7")
        label_z.move_to(np.array([0.2, 0.2, 2.9]))

        axis_labels = VGroup(label_x, label_y, label_z)
        self.add_fixed_orientation_mobjects(*axis_labels)

        # Cuadrícula holográfica en el plano base (Z = -0.8)
        grid_lines = VGroup()
        for x_val in np.linspace(-3.0, 3.0, 7):
            line = Line3D(
                start=np.array([x_val, -3.0, -0.8]),
                end=np.array([x_val, 3.0, -0.8]),
                color="#0F244A",
                thickness=0.008,
            )
            grid_lines.add(line)
        for y_val in np.linspace(-3.0, 3.0, 7):
            line = Line3D(
                start=np.array([-3.0, y_val, -0.8]),
                end=np.array([3.0, y_val, -0.8]),
                color="#0F244A",
                thickness=0.008,
            )
            grid_lines.add(line)

        # Iniciar rotación lenta ambiental para sensación inmersiva 3D
        self.begin_ambient_camera_rotation(rate=0.14)

        self.play(
            Create(axes),
            FadeIn(grid_lines),
            LaggedStartMap(FadeIn, axis_labels, lag_ratio=0.2),
            run_time=1.8,
        )
        self.wait(0.5)

        # ====================================================
        # FASE 2: INYECCIÓN DE LA CONSULTA DE INVESTIGACIÓN Q
        # ====================================================
        # Punto focal central de la consulta científica del usuario
        q_pos = np.array([0.0, 0.0, 1.25])

        # Esfera radiante y aura de la Consulta Q
        q_sphere = Sphere(center=q_pos, radius=0.14, color="#F59E0B").set_opacity(0.95)
        q_ring1 = Circle(radius=0.28, color="#FBBF24", stroke_width=2.0).move_to(q_pos)
        q_ring2 = Circle(radius=0.45, color="#F59E0B", stroke_width=1.2, stroke_opacity=0.6).move_to(q_pos)
        q_aura = VGroup(q_sphere, q_ring1, q_ring2)

        # Badge identificador de la Consulta
        q_badge = PaperBadge3D(
            doc_id="CONSULTA Q",
            title='“Inferencia Local & Privacidad en RAG”',
            category="NECESIDAD DE INVESTIGACIÓN",
            color="#F59E0B",
            width=2.8,
        )
        q_badge.move_to(q_pos + UP * 0.75 + RIGHT * 0.3)
        self.add_fixed_orientation_mobjects(q_badge)

        self.play(
            FadeIn(q_aura, scale=0.5),
            FadeIn(q_badge, shift=UP * 0.2),
            run_time=1.4,
        )

        # Pulso expansivo semántico desde Q
        q_pulse = Sphere(center=q_pos, radius=0.15, color="#F59E0B").set_opacity(0.7)
        self.play(
            q_pulse.animate.scale(14.0).set_opacity(0),
            run_time=1.2,
        )
        self.remove(q_pulse)

        # ====================================================
        # FASE 3: MATERIALIZACIÓN DEL CORPUS CIENTÍFICO EN 3D
        # ====================================================
        # Definición de coordenadas 3D y metadata de los papers candidatos
        papers_info = [
            {
                "key": "d1",
                "id": "PAPER D1",
                "title": "Arquitectura RAG Local Segura",
                "cat": "ARQUITECTURA // METODOLOGÍA",
                "pos": np.array([1.65, 0.95, 1.45]),
                "color": "#10B981",
                "sim_q": 0.92,
            },
            {
                "key": "d_red",
                "id": "PAPER D_red",
                "title": "Inferencia Offline RAG Local",
                "cat": "DUPLICADO // ALTA REDUNDANCIA",
                "pos": np.array([1.95, 1.15, 1.60]),  # Muy cercano a D1 en 3D
                "color": "#F43F5E",
                "sim_q": 0.89,
            },
            {
                "key": "d2",
                "id": "PAPER D2",
                "title": "Cuantización 4-bit & Latencia",
                "cat": "RENDIMIENTO // BENCHMARKS",
                "pos": np.array([-1.75, 1.45, 0.55]),
                "color": "#00F0FF",
                "sim_q": 0.78,
            },
            {
                "key": "d3",
                "id": "PAPER D3",
                "title": "Soberanía de Datos & Citas Hermenéuticas",
                "cat": "ÉTICA & INTEGRIDAD CIENTÍFICA",
                "pos": np.array([0.35, -1.95, 1.75]),
                "color": "#A855F7",
                "sim_q": 0.75,
            },
            {
                "key": "d_irr",
                "id": "PAPER D_irr",
                "title": "Visión Artificial en Agronomía",
                "cat": "CORPUS EXTERNO // IRRELEVANTE",
                "pos": np.array([-2.40, -2.10, -0.60]),
                "color": "#475569",
                "sim_q": 0.12,
            },
        ]

        # Construir objetos 3D y badges billboarded para cada paper
        paper_nodes = {}
        paper_badges = {}
        candidate_spheres = VGroup()
        candidate_badges = VGroup()

        for p in papers_info:
            pos = p["pos"]
            col = p["color"]

            # Nodo esférico 3D con anillo
            sphere = Sphere(center=pos, radius=0.10, color=col).set_opacity(0.9)
            halo = Circle(radius=0.18, color=col, stroke_width=1.5, stroke_opacity=0.7).move_to(pos)
            node_grp = VGroup(sphere, halo)

            # Tarjeta identificadora
            score_str = f"Sim(Q): {p['sim_q']:.2f}"
            badge = PaperBadge3D(
                doc_id=p["id"],
                title=p["title"],
                category=p["cat"],
                color=col,
                score_text=score_str,
            )
            badge.move_to(pos + UP * 0.55 + RIGHT * 0.2)

            paper_nodes[p["key"]] = node_grp
            paper_badges[p["key"]] = badge
            candidate_spheres.add(node_grp)
            candidate_badges.add(badge)

        self.add_fixed_orientation_mobjects(*candidate_badges)

        self.play(
            LaggedStartMap(FadeIn, candidate_spheres, scale=0.6, lag_ratio=0.15),
            LaggedStartMap(FadeIn, candidate_badges, shift=UP * 0.2, lag_ratio=0.15),
            run_time=2.0,
        )
        self.wait(0.6)

        # Rayos de similitud preliminares conectando Q con todos los candidatos
        prelim_rays = VGroup()
        for p in papers_info:
            ray = Line3D(start=q_pos, end=p["pos"], color="#38BDF8", thickness=0.012)
            ray.set_opacity(0.35)
            prelim_rays.add(ray)

        self.play(Create(prelim_rays), run_time=1.2)
        self.wait(0.4)

        # Descartar inmediatamente el documento irrelevante D_irr
        self.play(
            FadeOut(prelim_rays[4]),
            paper_nodes["d_irr"].animate.set_opacity(0.20),
            paper_badges["d_irr"].animate.set_opacity(0.25),
            run_time=0.8,
        )

        # ====================================================
        # FASE 4: SELECCIÓN DEL PRIMER DOCUMENTO D1 (MÁXIMA SIMILITUD)
        # ====================================================
        # Actualizar telemetría HUD
        self.play(
            status_txt.animate.set_text("PASO 1: SELECCIONANDO D1").set_color("#10B981"),
            status_dot.animate.set_color("#10B981"),
            t2.animate.set_text("CORPUS SELECCIONADO S: { D1 } (1 / 3)").set_color("#10B981"),
            t4.animate.set_text("D1: Base Metodológica RAG").set_color("#10B981"),
            run_time=0.6,
        )

        # Resaltar haz de luz hacia D1
        d1_ray = Line3D(start=q_pos, end=papers_info[0]["pos"], color="#10B981", thickness=0.035)

        self.play(
            Transform(prelim_rays[0], d1_ray),
            paper_nodes["d1"].animate.scale(1.25),
            paper_badges["d1"].bg_card.animate.set_stroke("#10B981", width=2.4),
            run_time=1.0,
        )

        # Pulso de confirmación de D1 en S
        d1_pulse = Sphere(center=papers_info[0]["pos"], radius=0.12, color="#10B981").set_opacity(0.8)
        self.play(
            d1_pulse.animate.scale(4.0).set_opacity(0),
            run_time=0.8,
        )
        self.remove(d1_pulse)
        self.wait(0.6)

        # ====================================================
        # FASE 5: EL DILEMA DE k-NN Y ROTACIÓN 3D (PAPER REDUNDANTE)
        # ====================================================
        # Aquí aprovechamos la naturaleza 3D con un giro de cámara dirigido
        # Detener la rotación ambiental para un acercamiento preciso y revelador
        self.stop_ambient_camera_rotation()

        self.play(
            status_txt.animate.set_text("INSPECCIÓN 3D DE REDUNDANCIA").set_color("#F43F5E"),
            status_dot.animate.set_color("#F43F5E"),
            run_time=0.4,
        )

        # ROTACIÓN DE CÁMARA 3D: Alinearse casi en el rayo que conecta D1 y D_red
        # Permite ver con total claridad cómo D_red está justo detrás de D1
        self.move_camera(
            phi=78 * DEGREES,
            theta=-22 * DEGREES,
            zoom=1.15,
            run_time=2.2,
        )

        # Rayo rojo de redundancia inter-documental entre D1 y D_red
        redundancy_line = Line3D(
            start=papers_info[0]["pos"],
            end=papers_info[1]["pos"],
            color="#F43F5E",
            thickness=0.032,
        )

        # Etiqueta flotante 3D que evidencia la alta redundancia
        sim_inter_badge = PaperBadge3D(
            doc_id="ALERTA: REDUNDANCIA",
            title="Sim(D1, D_red) = 0.96 (Cuasi-Idénticos)",
            category="SESGO k-NN TRADICIONAL",
            color="#F43F5E",
            score_text="MMR Penaliza: 0.5(0.89) - 0.5(0.96) = -0.035",
            width=3.2,
        )
        sim_inter_badge.move_to((papers_info[0]["pos"] + papers_info[1]["pos"]) / 2 + UP * 0.75 + RIGHT * 0.4)
        self.add_fixed_orientation_mobjects(sim_inter_badge)

        self.play(
            Create(redundancy_line),
            FadeIn(sim_inter_badge, scale=0.8),
            paper_badges["d_red"].bg_card.animate.set_stroke("#F43F5E", width=2.5),
            t3.animate.set_text("REDUNDANCIA D1 - D_red: 96% (CRÍTICA)").set_color("#F43F5E"),
            run_time=1.4,
        )
        self.wait(1.0)

        # Demostración del descarte de D_red por MMR
        penalty_cross = Text("✖ DESCARTADO POR MMR", font=FONT_SANS, weight=BOLD, font_size=9, color="#F43F5E")
        penalty_cross.next_to(paper_badges["d_red"].bg_card, DOWN, buff=0.10)
        self.add_fixed_orientation_mobjects(penalty_cross)

        self.play(
            FadeIn(penalty_cross),
            paper_badges["d_red"].animate.set_opacity(0.35),
            paper_nodes["d_red"].animate.set_opacity(0.30),
            FadeOut(prelim_rays[1]),
            FadeOut(redundancy_line),
            run_time=1.2,
        )
        self.wait(0.6)

        # ====================================================
        # FASE 6: ROTACIÓN 3D Y SELECCIÓN DE DIVERSIDAD (D2)
        # ====================================================
        # Rotar la cámara ampliamente hacia el cuadrante opuesto para ver D2
        self.play(
            status_txt.animate.set_text("PASO 2: MAXIMIZANDO DIVERSIDAD (D2)").set_color("#00F0FF"),
            status_dot.animate.set_color("#00F0FF"),
            FadeOut(sim_inter_badge),
            FadeOut(penalty_cross),
            run_time=0.6,
        )

        # ROTACIÓN ORBITAL 3D HACIA EL SEGUNDO HEMISFERIO
        self.move_camera(
            phi=58 * DEGREES,
            theta=-118 * DEGREES,
            zoom=0.98,
            run_time=2.4,
        )

        # Mostrar cálculo ventajoso de MMR para D2
        d2_ray = Line3D(start=q_pos, end=papers_info[2]["pos"], color="#00F0FF", thickness=0.035)

        # Conexión de diversidad entre D1 y D2
        diversity_line_d1_d2 = Line3D(
            start=papers_info[0]["pos"],
            end=papers_info[2]["pos"],
            color="#38BDF8",
            thickness=0.018,
        )
        diversity_line_d1_d2.set_opacity(0.60)

        score_d2_badge = PaperBadge3D(
            doc_id="D2 SELECCIONADO",
            title="Alta Novedad Semántica",
            category="DIVERSIDAD VECTORIAL ÓPTIMA",
            color="#00F0FF",
            score_text="MMR Score: 0.5(0.78) - 0.5(0.22) = +0.280",
            width=3.0,
        )
        score_d2_badge.move_to(papers_info[2]["pos"] + UP * 0.75 + LEFT * 0.3)
        self.add_fixed_orientation_mobjects(score_d2_badge)

        self.play(
            Transform(prelim_rays[2], d2_ray),
            Create(diversity_line_d1_d2),
            FadeIn(score_d2_badge, shift=UP * 0.2),
            paper_nodes["d2"].animate.scale(1.25),
            paper_badges["d2"].bg_card.animate.set_stroke("#00F0FF", width=2.4),
            t2.animate.set_text("CORPUS SELECCIONADO S: { D1, D2 } (2 / 3)").set_color("#00F0FF"),
            t3.animate.set_text("REDUNDANCIA S: 22% (DIVERSIDAD ALTA)").set_color("#00F0FF"),
            t4.animate.set_text("D2: Aporta Métricas Empíricas").set_color("#00F0FF"),
            run_time=1.6,
        )

        d2_pulse = Sphere(center=papers_info[2]["pos"], radius=0.12, color="#00F0FF").set_opacity(0.8)
        self.play(
            d2_pulse.animate.scale(4.0).set_opacity(0),
            FadeOut(score_d2_badge),
            run_time=0.8,
        )
        self.remove(d2_pulse)
        self.wait(0.6)

        # ====================================================
        # FASE 7: EXPANSIÓN AL 3ER EJE - VOLUMEN DE CONOCIMIENTO (D3)
        # ====================================================
        # Rotar la cámara a un ángulo cenital elevado para abarcar las 3 dimensiones
        self.play(
            status_txt.animate.set_text("PASO 3: COBERTURA 3D TOTAL (D3)").set_color("#A855F7"),
            status_dot.animate.set_color("#A855F7"),
            run_time=0.5,
        )

        # ROTACIÓN HACIA VISTA ELEVADA PANORÁMICA
        self.move_camera(
            phi=48 * DEGREES,
            theta=38 * DEGREES,
            zoom=0.88,
            run_time=2.2,
        )

        d3_ray = Line3D(start=q_pos, end=papers_info[3]["pos"], color="#A855F7", thickness=0.035)

        # Aristas de la red tridimensional
        diversity_line_d1_d3 = Line3D(start=papers_info[0]["pos"], end=papers_info[3]["pos"], color="#818CF8", thickness=0.018).set_opacity(0.55)
        diversity_line_d2_d3 = Line3D(start=papers_info[2]["pos"], end=papers_info[3]["pos"], color="#818CF8", thickness=0.018).set_opacity(0.55)

        self.play(
            Transform(prelim_rays[3], d3_ray),
            Create(diversity_line_d1_d3),
            Create(diversity_line_d2_d3),
            paper_nodes["d3"].animate.scale(1.25),
            paper_badges["d3"].bg_card.animate.set_stroke("#A855F7", width=2.4),
            t2.animate.set_text("CORPUS SELECCIONADO S: { D1, D2, D3 } (3 / 3)").set_color("#A855F7"),
            t3.animate.set_text("DIVERSIDAD GLOBAL: 94.6% ÓPTIMA").set_color("#10B981"),
            t4.animate.set_text("D3: Soberanía Ética y Hermenéutica").set_color("#A855F7"),
            run_time=1.8,
        )

        # ====================================================
        # FASE 8: EL TETRAEDRO 3D DE COBERTURA CIENTÍFICA
        # ====================================================
        # Ahora que S={D1, D2, D3} está completo con Q, se forma el
        # tetraedro tridimensional (simplex) que abarca el volumen de conocimiento
        p_q = q_pos
        p_d1 = papers_info[0]["pos"]
        p_d2 = papers_info[2]["pos"]
        p_d3 = papers_info[3]["pos"]

        # Caras poligonales 3D translúcidas con bioluminiscencia
        face_q_d1_d2 = Polygon(p_q, p_d1, p_d2, fill_color="#00F0FF", fill_opacity=0.22, stroke_color="#00F0FF", stroke_width=1.5)
        face_q_d2_d3 = Polygon(p_q, p_d2, p_d3, fill_color="#A855F7", fill_opacity=0.22, stroke_color="#A855F7", stroke_width=1.5)
        face_q_d3_d1 = Polygon(p_q, p_d3, p_d1, fill_color="#10B981", fill_opacity=0.22, stroke_color="#10B981", stroke_width=1.5)
        face_base = Polygon(p_d1, p_d2, p_d3, fill_color="#F59E0B", fill_opacity=0.18, stroke_color="#F59E0B", stroke_width=1.5)

        polyhedron_3d = VGroup(face_q_d1_d2, face_q_d2_d3, face_q_d3_d1, face_base)

        # Badge central del volumen de conocimiento
        volume_badge = PaperBadge3D(
            doc_id="VOLUMEN DE CONOCIMIENTO MÁXIMO",
            title="Cobertura Triangulada: Metodología + Benchmarks + Ética",
            category="SÍNTESIS CIENTÍFICA HOLÍSTICA",
            color="#10B981",
            score_text="Ventana de Contexto 100% Libre de Redundancia",
            width=3.6,
        )
        volume_badge.move_to((p_q + p_d1 + p_d2 + p_d3) / 4 + UP * 1.1)
        self.add_fixed_orientation_mobjects(volume_badge)

        self.play(
            FadeIn(polyhedron_3d, scale=0.8),
            FadeIn(volume_badge, shift=UP * 0.25),
            status_txt.animate.set_text("TETRAEDRO MMR COMPLETADO").set_color("#10B981"),
            status_dot.animate.set_color("#10B981"),
            run_time=2.0,
        )
        self.wait(1.0)

        # ====================================================
        # FASE 9: ROTACIÓN ORBITAL CINEMATOGRÁFICA 360° Y CONCLUSIÓN
        # ====================================================
        # Reactivar la rotación continua de la cámara para que el espectador
        # contemple el tetraedro y la distribución tridimensional desde todos los ángulos
        self.begin_ambient_camera_rotation(rate=0.22)

        # Banner comparativo fijo en pantalla que consolida el aprendizaje
        comparative_box = RoundedRectangle(
            corner_radius=0.12,
            width=12.2,
            height=0.74,
            stroke_width=1.6,
            stroke_color="#10B981",
            fill_color="#030E1F",
            fill_opacity=0.96,
        )
        c_left = Text("Búsqueda Estándar (k-NN): 3 papers casi idénticos (Redundancia = 96%) ✖", font=FONT_SANS, font_size=9.5, color="#F87171")
        c_right = Text("MMR AcadAId: 3 pilares científicos complementarios (Diversidad = 95%) ✔", font=FONT_SANS, weight=BOLD, font_size=10, color="#10B981")
        comp_content = VGroup(c_left, c_right).arrange(DOWN, buff=0.08)
        comp_content.move_to(comparative_box.get_center())

        final_comparison = VGroup(comparative_box, comp_content)
        final_comparison.set_y(-3.25)
        self.add_fixed_in_frame_mobjects(final_comparison)

        # Pulso armónico simultáneo en los 3 pilares del tetraedro
        self.play(
            FadeIn(final_comparison, shift=UP * 0.3),
            polyhedron_3d.animate.set_stroke(width=2.5),
            paper_badges["d1"].bg_card.animate.set_stroke("#10B981", width=3.0),
            paper_badges["d2"].bg_card.animate.set_stroke("#00F0FF", width=3.0),
            paper_badges["d3"].bg_card.animate.set_stroke("#A855F7", width=3.0),
            run_time=1.8,
        )

        # Tiempo para disfrutar la rotación 360° de la escena completada
        self.wait(3.5)

        # Cierre suave
        self.stop_ambient_camera_rotation()
        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=1.2,
        )
        self.wait(0.4)


# Alias para facilitar importación o invocación directa
RelevanciaMarginalMaxima3DScene = MMR3DScene
