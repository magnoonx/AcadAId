"""
Escena 3: Animación 3D del Entrenamiento y Generación de un LLM
AcadAId: Marco de Inferencia Local con Generación Aumentada por Recuperación

Simula cómo un Modelo de Lenguaje (LLM) procesa texto:
1. Ingestión de palabras, subpalabras y sílabas mediante BPE Tokenizer.
2. Proyección al espacio de Embeddings vectoriales.
3. Cómputo de Auto-Atención en el tensor 3D de pesos.
4. Generación autorregresiva de respuestas científicas fundamentadas token por token.
"""

from manim import *
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FONT_SERIF, FONT_SANS


class TokenBadge3D(VGroup):
    """
    Cápsula 3D flotante para sílabas, subpalabras o tokens.
    Mantiene orientación fija hacia la cámara para máxima legibilidad.
    """

    def __init__(
        self,
        text: str,
        token_id: str = "#000",
        color: str = "#00F0FF",
        bg_color: str = "#0A192F",
        font_size: int = 14,
        **kwargs,
    ):
        super().__init__(**kwargs)

        label = Text(text, font=FONT_SANS, weight=BOLD, font_size=font_size, color=WHITE)
        id_lbl = Text(token_id, font=FONT_SANS, font_size=font_size * 0.65, color=color)

        content = VGroup(label, id_lbl).arrange(DOWN, buff=0.06)

        pill = RoundedRectangle(
            corner_radius=0.10,
            width=max(content.width + 0.32, 1.10),
            height=content.height + 0.18,
            stroke_width=1.4,
            stroke_color=color,
            fill_color=bg_color,
            fill_opacity=0.92,
        )
        content.move_to(pill.get_center())

        self.pill = pill
        self.content = content
        self.color = color
        self.add(pill, content)


class LLMTraining3DScene(ThreeDScene):
    """
    Animación 3D cinematográfica del flujo completo de un LLM:
    Alimentación por palabras/sílabas -> Tensor de Pesos -> Auto-Atención -> Generación.
    """

    def construct(self):
        # 1. Fondo espacial cibernético
        self.camera.background_color = "#030611"

        # 2. Orientación inicial de la cámara 3D
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.90)

        # ====================================================
        # FASE 0: INTERFAZ HUD FUTURISTA FIJA EN PANTALLA
        # ====================================================
        header_box = RoundedRectangle(
            corner_radius=0.10,
            width=13.2,
            height=0.64,
            stroke_width=1.2,
            stroke_color="#1E3A8A",
            fill_color="#080F24",
            fill_opacity=0.90,
        )
        header_box.to_edge(UP, buff=0.18)

        ai_tag = Text("ACADAID // MOTOR LLM LOCAL", font=FONT_SANS, weight=BOLD, font_size=10, color="#38BDF8")
        title_hud = Text("PROCESAMIENTO DE TOKENS Y AUTO-ATENCIÓN", font=FONT_SANS, weight=BOLD, font_size=13, color=WHITE)
        header_group = VGroup(ai_tag, title_hud).arrange(RIGHT, buff=0.25)
        header_group.move_to(header_box.get_center())

        mode_dot = Dot(radius=0.06, color="#F59E0B")
        mode_txt = Text("INGESTIÓN & ENTRENAMIENTO", font=FONT_SANS, weight=BOLD, font_size=9, color="#F59E0B")
        mode_hud = VGroup(mode_dot, mode_txt).arrange(RIGHT, buff=0.10)
        mode_hud.next_to(header_box.get_right(), LEFT, buff=0.35)

        arch_badge = MathTex(r"\text{Transformer } \mathcal{M}_\theta", font_size=16, color="#38BDF8")
        arch_badge.next_to(header_box.get_left(), RIGHT, buff=0.35)

        hud_top = VGroup(header_box, header_group, mode_hud, arch_badge)

        # Panel inferior izquierdo: Matemáticas del LLM
        math_box = RoundedRectangle(
            corner_radius=0.12,
            width=5.8,
            height=1.35,
            stroke_width=1.0,
            stroke_color="#1E293B",
            fill_color="#060C1D",
            fill_opacity=0.88,
        )
        math_box.to_corner(DL, buff=0.28)

        math_title = Text("MECANISMO DE AUTO-ATENCIÓN & PREDICCIÓN", font=FONT_SANS, weight=BOLD, font_size=9, color="#94A3B8")
        eq_att = MathTex(r"\text{Attn}(\mathbf{Q},\mathbf{K},\mathbf{V}) = \text{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}", font_size=14, color="#F8FAFC")
        eq_prob = MathTex(r"P(w_{t+1} \mid w_{\le t}) = \text{Softmax}(\mathbf{W}_{\text{head}} \cdot \mathbf{h}_t)", font_size=14, color="#00F0FF")
        math_content = VGroup(math_title, eq_att, eq_prob).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        math_content.move_to(math_box.get_center())
        hud_math = VGroup(math_box, math_content)

        # Panel inferior derecho: Telemetría de Tokens
        tele_box = RoundedRectangle(
            corner_radius=0.12,
            width=4.8,
            height=1.35,
            stroke_width=1.0,
            stroke_color="#1E293B",
            fill_color="#060C1D",
            fill_opacity=0.88,
        )
        tele_box.to_corner(DR, buff=0.28)

        t1 = Text("TOKENIZADOR: BPE Subwords", font=FONT_SANS, font_size=8.5, color="#10B981")
        t2 = Text("VOCABULARIO: 32,000 Tokens", font=FONT_SANS, font_size=8.5, color="#E2E8F0")
        t3 = Text("VENTANA DE CONTEXTO: 8,192 Tokens", font=FONT_SANS, font_size=8.5, color="#38BDF8")
        t4 = Text("INFERENCIA: 100% Local / Sin APIs", font=FONT_SANS, font_size=8.5, color="#F59E0B")
        tele_content = VGroup(t1, t2, t3, t4).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        tele_content.move_to(tele_box.get_center())
        hud_tele = VGroup(tele_box, tele_content)

        self.add_fixed_in_frame_mobjects(hud_top, hud_math, hud_tele)

        # Iniciar rotación continua orbital de la cámara
        self.begin_ambient_camera_rotation(rate=0.18)

        # ====================================================
        # FASE 1: CONSTRUCCIÓN DEL NÚCLEO TENSOR 3D (EL CEREBRO DEL LLM)
        # ====================================================
        # Matriz cúbica 3x3x3 central que procesa los embeddings
        spacing = 1.15
        side = 0.65
        colors_by_layer = ["#8B5CF6", "#2563EB", "#00F0FF"]

        tensor_cubes = VGroup()
        tensor_nodes = VGroup()
        tensor_labels = VGroup()
        grid_points = {}

        for k in range(3):
            z_val = (k - 1) * spacing
            col = colors_by_layer[k]

            for j in range(3):
                y_val = (1 - j) * spacing

                for i in range(3):
                    x_val = (i - 1) * spacing
                    pt = np.array([x_val, y_val, z_val])
                    grid_points[(i, j, k)] = pt

                    voxel = Cube(
                        side_length=side,
                        fill_color=col,
                        fill_opacity=0.16,
                        stroke_color=col,
                        stroke_width=1.3,
                    )
                    voxel.move_to(pt)

                    node = Dot3D(point=pt, radius=0.045, color=WHITE)

                    lbl = MathTex(f"w_{{{i+1}{j+1}{k+1}}}", font_size=13, color=WHITE)
                    lbl.move_to(pt)

                    tensor_cubes.add(voxel)
                    tensor_nodes.add(node)
                    tensor_labels.add(lbl)

        self.add_fixed_orientation_mobjects(*tensor_labels)

        # Conexiones sinápticas internas entre los voxels
        synaptic_lines = VGroup()
        for (i, j, k), p1 in grid_points.items():
            for ni, nj, nk in [(i+1, j, k), (i, j+1, k), (i, j, k+1)]:
                if (ni, nj, nk) in grid_points:
                    p2 = grid_points[(ni, nj, nk)]
                    line = Line3D(p1, p2, thickness=0.012, color="#38BDF8")
                    line.set_opacity(0.35)
                    synaptic_lines.add(line)

        # Contenedor cuántico exterior
        outer_matrix_box = Cube(
            side_length=spacing * 2 + side + 0.15,
            fill_opacity=0.03,
            fill_color="#00F0FF",
            stroke_color="#00F0FF",
            stroke_width=1.6,
        )

        core_group = VGroup(tensor_cubes, tensor_nodes, synaptic_lines, outer_matrix_box)

        self.play(
            FadeIn(core_group, scale=0.8),
            LaggedStartMap(FadeIn, tensor_labels, lag_ratio=0.05),
            run_time=1.6,
        )
        self.wait(0.6)

        # ====================================================
        # FASE 2: INGESTIÓN DE PALABRAS Y SÍLABAS (TOKENIZACIÓN BPE)
        # ====================================================
        # Definición de tokens / sílabas académicas que alimentan al modelo
        tokens_data = [
            ("In-", "#1014", "#00F0FF", np.array([-4.8, -1.8, 1.4])),
            ("-fe-", "#2341", "#38BDF8", np.array([-4.0, 1.8, -1.2])),
            ("-ren-", "#5102", "#818CF8", np.array([-3.5, -2.0, -1.5])),
            ("-cia", "#0982", "#A855F7", np.array([-4.5, 1.5, 1.5])),
            ("con-", "#4421", "#F59E0B", np.array([-5.0, 0.0, 0.5])),
            ("-tex-", "#7819", "#FBBF24", np.array([-3.8, -1.4, 1.8])),
            ("-to", "#1120", "#34D399", np.array([-4.2, 2.0, -0.8])),
            ("AId", "#9901", "#10B981", np.array([-3.2, -0.5, -2.0])),
        ]

        token_badges = []
        for text, tid, col, start_pos in tokens_data:
            badge = TokenBadge3D(text=text, token_id=tid, color=col)
            badge.move_to(start_pos)
            token_badges.append(badge)

        self.add_fixed_orientation_mobjects(*token_badges)

        # Etiqueta indicadora del flujo de entrada
        input_stream_tag = Text(
            "FLUJO DE ENTRADA: PALABRAS Y SÍLABAS (BPE)",
            font=FONT_SANS,
            weight=BOLD,
            font_size=11,
            color="#38BDF8",
        )
        input_stream_tag.move_to(np.array([-4.2, 2.6, 0.5]))
        self.add_fixed_orientation_mobjects(input_stream_tag)

        # Aparecen los tokens flotando en el espacio 3D
        self.play(
            FadeIn(input_stream_tag, shift=RIGHT * 0.3),
            LaggedStartMap(FadeIn, VGroup(*token_badges), shift=RIGHT * 0.4, lag_ratio=0.15),
            run_time=1.4,
        )
        self.wait(0.5)

        # Ráfaga de alimentación: Las sílabas convergen una a una hacia el centro del cubo 3D
        # Al absorberse, cada token genera un flash de embedding en el tensor
        absorb_anims = []
        flash_spheres = []

        for badge in token_badges:
            # Trayectoria hacia el núcleo
            absorb_anims.append(badge.animate.move_to(ORIGIN).scale(0.3).set_opacity(0))

        self.play(
            LaggedStart(*absorb_anims, lag_ratio=0.18),
            run_time=2.4,
        )

        # Destello de absorción del tensor (todos los tokens absorbidos y convertidos en embeddings)
        flash_sphere = Sphere(radius=0.4, color="#00F0FF").set_opacity(0.8)
        flash_sphere.move_to(ORIGIN)

        self.play(
            FadeOut(input_stream_tag),
            FadeIn(flash_sphere, scale=0.3),
            outer_matrix_box.animate.set_stroke("#F59E0B", width=3.2),
            tensor_cubes.animate.set_fill("#38BDF8", opacity=0.35),
            run_time=0.6,
        )
        self.play(
            FadeOut(flash_sphere, scale=2.5),
            outer_matrix_box.animate.set_stroke("#00F0FF", width=1.6),
            tensor_cubes.animate.set_fill("#2563EB", opacity=0.16),
            run_time=0.8,
        )

        # ====================================================
        # FASE 3: PROPAGACIÓN DE AUTO-ATENCIÓN & ENTRENAMIENTO
        # ====================================================
        # Actualizar telemetría de HUD a 'Cálculo de Auto-Atención'
        self.play(
            mode_txt.animate.set_text("CALCULANDO AUTO-ATENCIÓN").set_color("#00F0FF"),
            mode_dot.animate.set_color("#00F0FF"),
            run_time=0.5,
        )

        # Manim mueve la cámara para ángulo de inspección dinámico
        self.move_camera(phi=60 * DEGREES, theta=15 * DEGREES, zoom=1.05, run_time=1.6)

        # Rayos de atención cruzada que unen pares de nodos clave dentro del tensor
        attention_rays = VGroup()
        ray_pairs = [
            (grid_points[(0, 0, 0)], grid_points[(2, 2, 2)]),
            (grid_points[(0, 2, 0)], grid_points[(2, 0, 2)]),
            (grid_points[(2, 1, 0)], grid_points[(0, 1, 2)]),
            (grid_points[(1, 0, 0)], grid_points[(1, 2, 2)]),
            (grid_points[(1, 1, 0)], grid_points[(1, 1, 2)]),
        ]

        for p1, p2 in ray_pairs:
            ray = Line3D(p1, p2, thickness=0.035, color="#F59E0B")
            attention_rays.add(ray)

        # Destellos en las líneas de atención representando matrices Q·K^T
        self.play(
            Create(attention_rays),
            outer_matrix_box.animate.set_stroke("#F59E0B", width=2.8),
            run_time=1.2,
        )

        # Pulso de actualización de pesos: ondas viajando a través de las sinapsis
        for _ in range(2):
            self.play(
                attention_rays.animate.set_color("#10B981"),
                synaptic_lines.animate.set_stroke("#10B981", width=2.0).set_opacity(0.85),
                run_time=0.45,
            )
            self.play(
                attention_rays.animate.set_color("#F59E0B"),
                synaptic_lines.animate.set_stroke("#38BDF8", width=1.0).set_opacity(0.35),
                run_time=0.45,
            )

        self.play(
            FadeOut(attention_rays),
            outer_matrix_box.animate.set_stroke("#00F0FF", width=1.6),
            run_time=0.7,
        )
        self.wait(0.5)

        # ====================================================
        # FASE 4: GENERACIÓN AUTORREGRESIVA DE RESPUESTAS TEXTUALES
        # ====================================================
        # Actualizar telemetría a 'Generación de Siguiente Token'
        self.play(
            mode_txt.animate.set_text("GENERACIÓN AUTORREGRESIVA").set_color("#10B981"),
            mode_dot.animate.set_color("#10B981"),
            run_time=0.5,
        )

        # Movimiento de cámara hacia el frente donde saldrán los tokens generados
        self.move_camera(phi=72 * DEGREES, theta=-65 * DEGREES, zoom=0.92, run_time=1.4)

        # Las palabras de la respuesta generada emergen desde el núcleo del LLM hacia la derecha
        generated_words = [
            ("Respuestas", "#00F0FF", np.array([2.8, 1.4, 1.0])),
            ("ancladas", "#38BDF8", np.array([3.4, 0.5, 0.4])),
            ("al", "#818CF8", np.array([3.8, -0.3, -0.2])),
            ("contexto", "#34D399", np.array([4.2, -1.1, -0.8])),
            ("científico", "#10B981", np.array([4.6, -1.9, -1.4])),
        ]

        out_badges = []
        emit_anims = []

        for idx, (word, col, target_pos) in enumerate(generated_words):
            out_b = TokenBadge3D(
                text=word,
                token_id=f"P = {98.2 - idx*1.3:.1f}%",
                color=col,
                bg_color="#031525",
                font_size=13,
            )
            out_b.move_to(ORIGIN)
            out_b.scale(0.2)
            out_b.set_opacity(0)
            out_badges.append(out_b)

        self.add_fixed_orientation_mobjects(*out_badges)

        # Título indicador del flujo de salida
        output_stream_tag = Text(
            "SALIDA SINTETIZADA: GENERACIÓN TOKEN A TOKEN",
            font=FONT_SANS,
            weight=BOLD,
            font_size=11,
            color="#10B981",
        )
        output_stream_tag.move_to(np.array([3.8, 2.3, 0.5]))
        self.add_fixed_orientation_mobjects(output_stream_tag)

        self.play(FadeIn(output_stream_tag, shift=LEFT * 0.25), run_time=0.6)

        # Emisión secuencial autoregresiva: Cada palabra nace del tensor y viaja al frente
        for idx, (word, col, target_pos) in enumerate(generated_words):
            badge = out_badges[idx]
            
            # Pulso en el tensor al generar cada token
            self.play(
                outer_matrix_box.animate.set_stroke(col, width=2.4),
                badge.animate.move_to(target_pos).scale(5.0).set_opacity(1.0),
                run_time=0.65,
            )
            self.play(
                outer_matrix_box.animate.set_stroke("#00F0FF", width=1.6),
                run_time=0.25,
            )

        self.wait(1.2)

        # ====================================================
        # FASE 5: SÍNTESIS FINAL Y CONVERGENCIA
        # ====================================================
        # Cámara retrocede a una vista general panorámica
        self.move_camera(phi=68 * DEGREES, theta=-45 * DEGREES, zoom=0.85, run_time=1.6)

        # Banner central de validación académica
        final_box = RoundedRectangle(
            corner_radius=0.12,
            width=11.8,
            height=0.72,
            stroke_width=1.5,
            stroke_color="#10B981",
            fill_color="#04121F",
            fill_opacity=0.95,
        )
        final_txt = Text(
            "AcadAId: LLM Local Alimentado por Corpus Científico Cerrado",
            font=FONT_SERIF,
            weight=BOLD,
            font_size=14,
            color=WHITE,
        )
        final_txt.move_to(final_box.get_center())
        final_banner = VGroup(final_box, final_txt)
        final_banner.set_y(-3.25)

        self.add_fixed_in_frame_mobjects(final_banner)

        # Pulso armónico final entre el tensor y los tokens generados
        self.play(
            FadeIn(final_banner, shift=UP * 0.3),
            tensor_cubes.animate.set_stroke("#10B981", width=2.2),
            outer_matrix_box.animate.set_stroke("#10B981", width=2.8).set_fill("#10B981", opacity=0.08),
            run_time=1.2,
        )
        self.wait(2.5)

        # Cierre suave
        self.stop_ambient_camera_rotation()
        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=1.2,
        )
        self.wait(0.4)
