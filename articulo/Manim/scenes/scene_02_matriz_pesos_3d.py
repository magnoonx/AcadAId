"""
Escena 2: Matriz de Pesos 3D de una Red Neuronal (Tensor Cúbico de la IA)
AcadAId: Marco de Inferencia Local con Generación Aumentada por Recuperación

Simula la construcción y funcionamiento en tiempo real de una matriz de pesos 3D
(Tensor sináptico W ∈ ℝ^(3x3x3)) con símbolos algebraicos, conexiones neuronales,
propagación de activaciones y rotación orbital cinematográfica.
"""

from manim import *
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import FONT_SERIF, FONT_SANS


class MatrizPesos3DScene(ThreeDScene):
    """
    Animación 3D cinematográfica del tensor de pesos de una IA en ejecución.
    """

    def construct(self):
        # 1. Fondo de atmósfera tecnológica oscura profunda
        self.camera.background_color = "#040711"

        # 2. Configuración inicial de la cámara 3D
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES, zoom=0.92)

        # ====================================================
        # FASE 0: INTERFAZ HUD FUTURISTA FIJA EN PANTALLA
        # ====================================================
        # Banner superior fijo
        header_box = RoundedRectangle(
            corner_radius=0.10,
            width=13.0,
            height=0.62,
            stroke_width=1.2,
            stroke_color="#1E3A8A",
            fill_color="#0A1128",
            fill_opacity=0.88,
        )
        header_box.to_edge(UP, buff=0.18)

        ai_tag = Text("ACADAID // MOTOR DE INFERENCIA", font=FONT_SANS, weight=BOLD, font_size=10, color="#38BDF8")
        title_hud = Text("TENSOR DE PESOS SINÁPTICOS", font=FONT_SANS, weight=BOLD, font_size=13, color=WHITE)
        title_grp = VGroup(ai_tag, title_hud).arrange(RIGHT, buff=0.25)
        title_grp.move_to(header_box.get_center())

        # Badge de estado pulsante
        status_dot = Dot(radius=0.06, color="#10B981")
        status_txt = Text("IA COMPUTANDO", font=FONT_SANS, weight=BOLD, font_size=9, color="#10B981")
        status_hud = VGroup(status_dot, status_txt).arrange(RIGHT, buff=0.10)
        status_hud.next_to(header_box.get_right(), LEFT, buff=0.35)

        dim_badge = MathTex(r"\mathcal{W} \in \mathbb{R}^{3 \times 3 \times 3}", font_size=16, color="#38BDF8")
        dim_badge.next_to(header_box.get_left(), RIGHT, buff=0.35)

        hud_top = VGroup(header_box, title_grp, status_hud, dim_badge)

        # Panel inferior izquierdo: Formulación Matemática
        math_box = RoundedRectangle(
            corner_radius=0.12,
            width=5.4,
            height=1.25,
            stroke_width=1.0,
            stroke_color="#1E293B",
            fill_color="#080E1E",
            fill_opacity=0.85,
        )
        math_box.to_corner(DL, buff=0.30)

        math_title = Text("ACTIVACIÓN Y OPTIMIZACIÓN LOCAL", font=FONT_SANS, weight=BOLD, font_size=9, color="#94A3B8")
        math_eq1 = MathTex(r"\mathbf{a}^{(l+1)} = \sigma\left(\mathbf{W}^{(l)} \cdot \mathbf{a}^{(l)} + \mathbf{b}\right)", font_size=15, color="#F8FAFC")
        math_eq2 = MathTex(r"\Delta \mathbf{W}_{ijk} = -\eta \, \frac{\partial \mathcal{L}}{\partial \mathbf{W}_{ijk}}", font_size=14, color="#38BDF8")
        math_content = VGroup(math_title, math_eq1, math_eq2).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        math_content.move_to(math_box.get_center())
        hud_math = VGroup(math_box, math_content)

        # Panel inferior derecho: Telemetría de la IA
        tele_box = RoundedRectangle(
            corner_radius=0.12,
            width=4.6,
            height=1.25,
            stroke_width=1.0,
            stroke_color="#1E293B",
            fill_color="#080E1E",
            fill_opacity=0.85,
        )
        tele_box.to_corner(DR, buff=0.30)

        t1 = Text("ESTADO: Activo • Inferencia Offline", font=FONT_SANS, font_size=8.5, color="#10B981")
        t2 = Text("PESOS: 27 Parámetros Sinápticos", font=FONT_SANS, font_size=8.5, color="#E2E8F0")
        t3 = Text("PRECISIÓN: FP16 • Cuantización Local", font=FONT_SANS, font_size=8.5, color="#38BDF8")
        t4 = Text("LATENCIA: < 1.1 ms (Hardware Propio)", font=FONT_SANS, font_size=8.5, color="#94A3B8")
        tele_content = VGroup(t1, t2, t3, t4).arrange(DOWN, aligned_edge=LEFT, buff=0.07)
        tele_content.move_to(tele_box.get_center())
        hud_tele = VGroup(tele_box, tele_content)

        # Agregar HUD fijo en pantalla
        self.add_fixed_in_frame_mobjects(hud_top, hud_math, hud_tele)

        # Iniciar rotación continua de la cámara orbital
        self.begin_ambient_camera_rotation(rate=0.20)

        # ====================================================
        # FASE 1: CONSTRUCCIÓN DE LOS VOXELS DEL TENSOR CÚBICO
        # ====================================================
        # Grilla 3x3x3: espaciado y colores por capa de profundidad (Z)
        spacing = 1.25
        side = 0.72

        layer_colors = [
            "#8B5CF6",  # Z = -1 (Capa profunda: Violeta)
            "#2563EB",  # Z =  0 (Capa media: Azul real)
            "#00E5FF",  # Z = +1 (Capa frontal: Cian brillante)
        ]

        # Estructuras de datos para organizar los componentes del tensor
        voxels_by_layer = {0: VGroup(), 1: VGroup(), 2: VGroup()}
        labels_by_layer = {0: VGroup(), 1: VGroup(), 2: VGroup()}
        nodes_by_layer = {0: VGroup(), 1: VGroup(), 2: VGroup()}

        all_cubes = VGroup()
        all_labels = VGroup()
        grid_positions = {}

        for k in range(3):        # Z axis (-1, 0, 1) -> indices 0, 1, 2
            z_pos = (k - 1) * spacing
            col = layer_colors[k]

            for j in range(3):    # Y axis (-1, 0, 1)
                y_pos = (1 - j) * spacing  # Invertir para que j=0 sea arriba

                for i in range(3): # X axis (-1, 0, 1)
                    x_pos = (i - 1) * spacing
                    pos = np.array([x_pos, y_pos, z_pos])
                    grid_positions[(i, j, k)] = pos

                    # 1. Cubo voxel translúcido
                    cube = Cube(
                        side_length=side,
                        fill_color=col,
                        fill_opacity=0.18,
                        stroke_color=col,
                        stroke_width=1.4,
                    )
                    cube.move_to(pos)

                    # 2. Nodo central brillante
                    node_dot = Dot3D(point=pos, radius=0.05, color=WHITE)

                    # 3. Símbolo algebraico (w_{ijk})
                    # Índices 1-indexados para la notación matemática estándar
                    lbl = MathTex(
                        f"w_{{{i+1}{j+1}{k+1}}}",
                        font_size=15,
                        color=WHITE,
                    )
                    lbl.move_to(pos)

                    voxels_by_layer[k].add(cube)
                    nodes_by_layer[k].add(node_dot)
                    labels_by_layer[k].add(lbl)

                    all_cubes.add(cube)
                    all_labels.add(lbl)

        # Asegurar que todas las etiquetas miren a la cámara durante la rotación
        self.add_fixed_orientation_mobjects(*all_labels)

        # 4. Sinapsis / Conexiones intercelulares
        synapses_x = VGroup()
        synapses_y = VGroup()
        synapses_z = VGroup()

        for (i, j, k), pos in grid_positions.items():
            if i < 2:
                next_pos = grid_positions[(i + 1, j, k)]
                line = Line3D(pos, next_pos, thickness=0.015, color="#38BDF8")
                line.set_opacity(0.40)
                synapses_x.add(line)
            if j < 2:
                next_pos = grid_positions[(i, j + 1, k)]
                line = Line3D(pos, next_pos, thickness=0.015, color="#38BDF8")
                line.set_opacity(0.40)
                synapses_y.add(line)
            if k < 2:
                next_pos = grid_positions[(i, j, k + 1)]
                line = Line3D(pos, next_pos, thickness=0.015, color="#818CF8")
                line.set_opacity(0.40)
                synapses_z.add(line)

        all_synapses = VGroup(synapses_x, synapses_y, synapses_z)

        # ====================================================
        # FASE 2: GÉNESIS DIMENSIONAL (1D -> 2D -> 3D)
        # ====================================================
        # 1. Nace el vector central 1D en la capa media (k=1, j=1)
        vector_1d_cubes = VGroup(voxels_by_layer[1][3], voxels_by_layer[1][4], voxels_by_layer[1][5])
        vector_1d_labels = VGroup(labels_by_layer[1][3], labels_by_layer[1][4], labels_by_layer[1][5])
        vector_1d_nodes = VGroup(nodes_by_layer[1][3], nodes_by_layer[1][4], nodes_by_layer[1][5])

        self.play(
            LaggedStartMap(FadeIn, vector_1d_cubes, scale=0.5, lag_ratio=0.2),
            LaggedStartMap(FadeIn, vector_1d_nodes, lag_ratio=0.2),
            LaggedStartMap(Write, vector_1d_labels, lag_ratio=0.2),
            run_time=1.2,
        )
        self.wait(0.6)

        # 2. Expansión a Matriz 2D (se completa la capa media k=1 de 9 elementos)
        remaining_2d_cubes = VGroup(*[voxels_by_layer[1][idx] for idx in [0, 1, 2, 6, 7, 8]])
        remaining_2d_labels = VGroup(*[labels_by_layer[1][idx] for idx in [0, 1, 2, 6, 7, 8]])
        remaining_2d_nodes = VGroup(*[nodes_by_layer[1][idx] for idx in [0, 1, 2, 6, 7, 8]])

        # Sinapsis del plano central
        synapses_mid_plane = VGroup(
            *[s for s in synapses_x if np.isclose(s.get_center()[2], 0, atol=0.2)],
            *[s for s in synapses_y if np.isclose(s.get_center()[2], 0, atol=0.2)],
        )

        self.play(
            FadeIn(remaining_2d_cubes, scale=0.7),
            FadeIn(remaining_2d_nodes),
            Write(remaining_2d_labels),
            Create(synapses_mid_plane),
            run_time=1.4,
        )
        self.wait(0.8)

        # 3. Expansión a Tensor Cúbico 3D (Capa Frontal k=2 y Capa Posterior k=0)
        remaining_3d_cubes = VGroup(voxels_by_layer[0], voxels_by_layer[2])
        remaining_3d_labels = VGroup(labels_by_layer[0], labels_by_layer[2])
        remaining_3d_nodes = VGroup(nodes_by_layer[0], nodes_by_layer[2])

        remaining_synapses = VGroup(
            *[s for s in all_synapses if s not in synapses_mid_plane]
        )

        # Cubo contenedor exterior envolvente
        bounding_cage = Cube(
            side_length=spacing * 2 + side + 0.15,
            fill_opacity=0.03,
            fill_color="#38BDF8",
            stroke_color="#38BDF8",
            stroke_width=1.8,
        )

        self.play(
            FadeIn(remaining_3d_cubes, scale=0.8),
            FadeIn(remaining_3d_nodes),
            Write(remaining_3d_labels),
            Create(remaining_synapses),
            FadeIn(bounding_cage),
            run_time=1.8,
        )
        self.wait(1.0)

        # ====================================================
        # FASE 3: PULSOS DE PROPAGACIÓN SINÁPTICA DE LA IA
        # ====================================================
        # Cambio suave de perspectiva de la cámara para apreciar la profundidad
        self.move_camera(phi=62 * DEGREES, theta=25 * DEGREES, run_time=1.6)

        # Simular una ráfaga de activación que viaja a través del tensor (Z: -1 -> 0 -> +1)
        # Los voxels se iluminan secuencialmente con gradiente dorado/esmeralda
        highlight_color_1 = "#F59E0B"  # Ámbar de excitación
        highlight_color_2 = "#10B981"  # Verde de activación

        for layer_idx in [0, 1, 2]:
            cubes_in_layer = voxels_by_layer[layer_idx]
            original_color = layer_colors[layer_idx]

            self.play(
                cubes_in_layer.animate.set_fill(highlight_color_1, opacity=0.45).set_stroke(highlight_color_1, width=2.5),
                run_time=0.45,
            )
            self.play(
                cubes_in_layer.animate.set_fill(highlight_color_2, opacity=0.28).set_stroke(original_color, width=1.5),
                run_time=0.45,
            )

        self.wait(0.8)

        # ====================================================
        # FASE 4: VISTA EXPLOTADA (INSPECCIÓN DE CAPAS INTERNAS)
        # ====================================================
        # Para que el espectador 'observe a la IA trabajar por dentro',
        # las 3 capas del tensor se separan a lo largo del eje Z
        shift_dist = 1.10

        front_layer_group = VGroup(voxels_by_layer[2], nodes_by_layer[2], labels_by_layer[2])
        back_layer_group = VGroup(voxels_by_layer[0], nodes_by_layer[0], labels_by_layer[0])
        mid_layer_group = VGroup(voxels_by_layer[1], nodes_by_layer[1], labels_by_layer[1])

        # Ocultar temporalmente las sinapsis Z y la jaula para una vista limpia de las capas
        self.play(
            FadeOut(synapses_z),
            FadeOut(bounding_cage),
            front_layer_group.animate.shift(OUT * shift_dist),
            back_layer_group.animate.shift(IN * shift_dist),
            run_time=1.5,
        )

        # Resaltar el peso central oculto w_222 en el núcleo de la IA
        core_cube = voxels_by_layer[1][4]
        core_label = labels_by_layer[1][4]

        pulse_box = Cube(side_length=side + 0.1, stroke_color="#00E5FF", stroke_width=3.0, fill_opacity=0)
        pulse_box.move_to(core_cube.get_center())

        self.play(
            core_cube.animate.set_fill("#00E5FF", opacity=0.55).set_stroke("#00E5FF", width=3.0),
            FadeIn(pulse_box, scale=0.8),
            run_time=0.8,
        )
        self.play(
            FadeOut(pulse_box, scale=1.4),
            core_cube.animate.set_fill(layer_colors[1], opacity=0.18).set_stroke(layer_colors[1], width=1.4),
            run_time=0.8,
        )
        self.wait(1.0)

        # Reconvergencia de las capas en el tensor sólido unificado
        self.play(
            front_layer_group.animate.shift(IN * shift_dist),
            back_layer_group.animate.shift(OUT * shift_dist),
            FadeIn(synapses_z),
            FadeIn(bounding_cage),
            run_time=1.5,
        )
        self.wait(0.8)

        # ====================================================
        # FASE 5: CLÍMAX Y CONVERGENCIA DEL TENSOR
        # ====================================================
        # La cámara regresa a una vista orbital amplia majestuosa
        self.move_camera(phi=68 * DEGREES, theta=-45 * DEGREES, zoom=0.90, run_time=1.8)

        # Pulso armónico simultáneo en todos los 27 voxels
        self.play(
            all_cubes.animate.set_stroke("#00E5FF", width=2.2),
            bounding_cage.animate.set_stroke("#00E5FF", width=2.8).set_fill("#00E5FF", opacity=0.06),
            status_txt.animate.set_color("#00E5FF"),
            status_dot.animate.set_color("#00E5FF"),
            run_time=1.2,
        )
        self.wait(2.5)

        # Cierre suave
        self.stop_ambient_camera_rotation()
        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=1.2,
        )
        self.wait(0.5)
