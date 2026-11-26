"""
Escena 1: Marco Conceptual - Generación Aumentada por Recuperación (RAG)
AcadAId: Marco de Inferencia Local con RAG para la Investigación Académica

Explica los 3 pilares del esquema:
1. Anclaje Empírico (Corpus cerrado)
2. Prevención de Extrapolación (Sin internet genérico / alucinaciones)
3. Fidelidad Hermenéutica (Síntesis fiel al contexto del autor)

Totalmente calibrada para el marco 16:9: sin desbordes ni solapamientos.
"""

from manim import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THEME, FONT_SERIF, FONT_SANS
from components.cards import ConceptCard
from components.documents import CorpusVault, AcademicDoc
from components.badges import SlideBanner, StatusBadge, InternetBlockShield
from components.network import LocalInferenceNode, HermeneuticSynthesis


class MarcoConceptualScene(Scene):
    """
    Video explicativo completo del Marco Conceptual de AcadAId.
    Presenta la diapositiva original sincronizada con diagramas animados.
    """

    def construct(self):
        # 0. Fondo
        self.camera.background_color = THEME["bg"]

        # ====================================================
        # FASE 0: BANNER DE APERTURA (Título de la Investigación)
        # ====================================================
        banner = SlideBanner(
            title_text="AcadAId: Marco RAG Local para la Investigación Académica",
            height=0.55,
            theme=THEME,
        )
        banner.to_edge(UP, buff=0)

        self.play(FadeIn(banner, shift=DOWN * 0.4), run_time=0.9)
        self.wait(0.8)

        # ====================================================
        # FASE 1: ENCABEZADO Y TÍTULO DE LA DIAPOSITIVA (Izquierda)
        # ====================================================
        left_x = -5.8

        tag_text = Text(
            "MARCO CONCEPTUAL",
            font=FONT_SANS,
            weight=BOLD,
            font_size=12,
            color=THEME["text_tag"],
        )
        tag_text.set_x(left_x + tag_text.width / 2)
        tag_text.set_y(2.80)

        title_rag = Text(
            "Generación\nAumentada por\nRecuperación (RAG)",
            font=FONT_SERIF,
            weight=BOLD,
            font_size=25,
            color=THEME["text_primary"],
            line_spacing=0.82,
        )
        title_rag.next_to(tag_text, DOWN, aligned_edge=LEFT, buff=0.20)

        self.play(
            FadeIn(tag_text, shift=RIGHT * 0.25),
            Write(title_rag),
            run_time=1.2,
        )
        self.wait(0.5)

        # ====================================================
        # FASE 2: PREPARACIÓN DE LAS 3 TARJETAS CONCEPTUALES
        # ====================================================
        card_w = 6.0
        card_h = 0.72

        card1 = ConceptCard(
            title_text="Anclaje Empírico",
            desc_text="Respuestas basadas en un corpus documental cerrado.",
            width=card_w,
            height=card_h,
            has_box=True,
            title_size=15.5,
            desc_size=12.5,
            theme=THEME,
            card_id=1,
        )
        card1.next_to(title_rag, DOWN, aligned_edge=LEFT, buff=0.30)

        card2 = ConceptCard(
            title_text="Prevención de Extrapolación",
            desc_text="Elimina respuestas genéricas de internet.",
            width=card_w,
            height=card_h,
            has_box=True,
            title_size=15.5,
            desc_size=12.5,
            theme=THEME,
            card_id=2,
        )
        card2.next_to(card1, DOWN, aligned_edge=LEFT, buff=0.18)

        card3 = ConceptCard(
            title_text="Fidelidad Hermenéutica",
            desc_text="Síntesis de textos sin perder el contexto original.",
            width=card_w,
            height=card_h,
            has_box=True,
            title_size=15.5,
            desc_size=12.5,
            theme=THEME,
            card_id=3,
        )
        card3.next_to(card2, DOWN, aligned_edge=LEFT, buff=0.18)

        # Centro del escenario visual derecho (calibrado para no colisionar)
        right_center = RIGHT * 3.5 + UP * 0.05

        # ====================================================
        # FASE 3: PILAR 1 - ANCLAJE EMPÍRICO
        # ====================================================
        self.play(
            FadeIn(card1, shift=RIGHT * 0.3),
            card1.highlight_border.animate.set_opacity(1.0),
            run_time=0.9,
        )

        vault = CorpusVault(width=5.4, height=3.2, theme=THEME)
        vault.move_to(right_center + DOWN * 0.15)

        self.play(
            FadeIn(vault.box, scale=0.92),
            FadeIn(vault.title),
            FadeIn(vault.badge),
            LaggedStartMap(FadeIn, vault.docs, shift=UP * 0.15, lag_ratio=0.18),
            run_time=1.2,
        )

        query_bubble = RoundedRectangle(
            corner_radius=0.10,
            width=4.6,
            height=0.52,
            stroke_width=1.4,
            stroke_color=THEME["accent_blue"],
            fill_color=THEME["card_bg"],
            fill_opacity=0.95,
        )
        query_text = Text(
            "Consulta: \"¿Cuál es la hipótesis y método del autor?\"",
            font=FONT_SANS,
            font_size=9.5,
            color=THEME["text_primary"],
        )
        query_text.move_to(query_bubble)
        query_grp = VGroup(query_bubble, query_text)
        query_grp.next_to(vault, UP, buff=0.20)

        self.play(FadeIn(query_grp, shift=DOWN * 0.2), run_time=0.7)

        anchor_arrows = VGroup()
        for doc in vault.docs:
            arr = DashedLine(
                query_grp.get_bottom(),
                doc.get_top(),
                stroke_width=2.2,
                color=THEME["accent_blue"],
                dash_length=0.07,
            )
            anchor_arrows.add(arr)

        status_anchor = StatusBadge(
            "✓ Recuperación estricta desde fuentes locales",
            color=THEME["success_green"],
            font_size=9.5,
            theme=THEME,
        )
        status_anchor.next_to(vault, DOWN, buff=0.15)

        self.play(
            Create(anchor_arrows),
            FadeIn(status_anchor, shift=UP * 0.15),
            run_time=1.1,
        )
        self.wait(1.4)

        self.play(
            card1.highlight_border.animate.set_opacity(0),
            FadeOut(anchor_arrows),
            FadeOut(query_grp),
            FadeOut(status_anchor),
            FadeOut(vault),
            run_time=0.7,
        )

        # ====================================================
        # FASE 4: PILAR 2 - PREVENCIÓN DE EXTRAPOLACIÓN
        # ====================================================
        self.play(
            FadeIn(card2, shift=RIGHT * 0.3),
            card2.highlight_border.animate.set_opacity(1.0),
            run_time=0.9,
        )

        shield_container = InternetBlockShield(width=5.0, height=2.2, theme=THEME)
        shield_container.move_to(right_center + UP * 0.85)

        local_node = LocalInferenceNode(
            title="MOTOR ACADAID: INFERENCIA 100% LOCAL",
            subtitle="Sin dependencias de APIs en la nube ni telemetría",
            width=5.0,
            height=1.05,
            theme=THEME,
        )
        local_node.next_to(shield_container, DOWN, buff=0.25)

        self.play(
            FadeIn(shield_container, shift=DOWN * 0.15),
            FadeIn(local_node, shift=UP * 0.15),
            run_time=1.1,
        )

        status_extrap = StatusBadge(
            "⊘ Cero Alucinaciones: Sin acceso a la web abierta",
            color=THEME["danger_red"],
            font_size=9.5,
            theme=THEME,
        )
        status_extrap.next_to(local_node, DOWN, buff=0.15)

        pulse_ring = Circle(radius=0.38, stroke_width=3.5, stroke_color=THEME["danger_red"])
        pulse_ring.move_to(shield_container.shield)

        self.play(
            FadeIn(status_extrap, shift=UP * 0.12),
            ReplacementTransform(pulse_ring, pulse_ring.copy().scale(1.5).set_stroke(opacity=0)),
            run_time=1.2,
        )
        self.wait(1.4)

        self.play(
            card2.highlight_border.animate.set_opacity(0),
            FadeOut(shield_container),
            FadeOut(status_extrap),
            FadeOut(local_node),
            run_time=0.7,
        )

        # ====================================================
        # FASE 5: PILAR 3 - FIDELIDAD HERMENÉUTICA
        # ====================================================
        self.play(
            FadeIn(card3, shift=RIGHT * 0.3),
            card3.highlight_border.animate.set_opacity(1.0),
            run_time=0.9,
        )

        herm_card = HermeneuticSynthesis(width=5.2, height=3.3, theme=THEME)
        herm_card.move_to(right_center + DOWN * 0.05)

        self.play(
            FadeIn(herm_card, scale=0.94),
            run_time=1.1,
        )

        status_fidel = StatusBadge(
            "✦ Preservación exacta de la voz y contexto del autor",
            color=THEME["accent_blue"],
            font_size=9.5,
            theme=THEME,
        )
        status_fidel.next_to(herm_card, DOWN, buff=0.15)

        self.play(
            FadeIn(status_fidel, shift=UP * 0.15),
            run_time=0.9,
        )
        self.wait(1.5)

        # ====================================================
        # FASE 6: SÍNTESIS INTEGRAL (LOS 3 PILARES UNIFICADOS)
        # ====================================================
        self.play(
            card3.highlight_border.animate.set_opacity(0),
            FadeOut(status_fidel),
            FadeOut(herm_card),
            run_time=0.7,
        )

        # Resaltar los 3 conceptos juntos
        self.play(
            card1.highlight_border.animate.set_opacity(0.85),
            card2.highlight_border.animate.set_opacity(0.85),
            card3.highlight_border.animate.set_opacity(0.85),
            run_time=0.8,
        )

        # Diagrama de arquitectura compacto a la derecha
        arch_box = RoundedRectangle(
            corner_radius=0.16,
            width=5.2,
            height=3.6,
            stroke_width=1.8,
            stroke_color=THEME["accent_blue"],
            fill_color=THEME["card_bg"],
            fill_opacity=0.95,
        )
        arch_box.move_to(right_center + DOWN * 0.10)

        arch_title = Text(
            "FLUJO DE TRABAJO ACADAID",
            font=FONT_SANS,
            weight=BOLD,
            font_size=11,
            color=THEME["text_primary"],
        )
        arch_title.next_to(arch_box.get_top(), DOWN, buff=0.15)

        step1 = StatusBadge("1. Corpus Documental Local Cerrado", color=THEME["accent_blue"], font_size=9, theme=THEME)
        down_arrow1 = Arrow(ORIGIN, DOWN * 0.35, buff=0, stroke_width=2.2, color=THEME["accent_blue"], max_tip_length_to_length_ratio=0.35)

        step2 = StatusBadge("2. Inferencia Local Offline (Sin Internet)", color=THEME["danger_red"], font_size=9, theme=THEME)
        down_arrow2 = Arrow(ORIGIN, DOWN * 0.35, buff=0, stroke_width=2.2, color=THEME["accent_blue"], max_tip_length_to_length_ratio=0.35)

        step3 = StatusBadge("3. Síntesis Académica con Citas Exactas", color=THEME["success_green"], font_size=9, theme=THEME)

        workflow_group = VGroup(
            step1,
            down_arrow1,
            step2,
            down_arrow2,
            step3,
        ).arrange(DOWN, buff=0.10)
        workflow_group.move_to(arch_box.get_center() + DOWN * 0.12)

        full_diagram = VGroup(arch_box, arch_title, workflow_group)

        self.play(
            FadeIn(full_diagram, scale=0.96),
            run_time=1.2,
        )
        self.wait(1.8)

        # ====================================================
        # FASE 7: CIERRE (CONVERGENCIA CENTRAL LIMPIA)
        # ====================================================
        # Barra de conclusión inferior que encaja perfectamente sin solapar
        conclusion_box = RoundedRectangle(
            corner_radius=0.10,
            width=11.6,
            height=0.62,
            stroke_width=1.4,
            stroke_color=THEME["accent_blue"],
            fill_color=THEME["banner_bg"],
            fill_opacity=0.96,
        )
        conclusion_text = Text(
            "AcadAId: Rigor Metodológico, Privacidad Local y Fidelidad Textual",
            font=FONT_SERIF,
            weight=BOLD,
            font_size=13.5,
            color=WHITE,
        )
        conclusion_text.move_to(conclusion_box)
        conclusion_group = VGroup(conclusion_box, conclusion_text)
        conclusion_group.set_y(-3.35)

        self.play(
            FadeIn(conclusion_group, shift=UP * 0.25),
            run_time=1.0,
        )
        self.wait(2.5)

        # Fade out suave
        self.play(
            FadeOut(Group(*self.mobjects)),
            run_time=1.0,
        )
        self.wait(0.4)
