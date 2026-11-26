"""
Escena: Diapositiva Animada Limpia (Marco Conceptual)
AcadAId: Marco RAG Local para la Investigación Académica

Reproduce exactamente la diapositiva con transiciones y proporciones seguras
sin ningún tipo de desborde de pantalla.
"""

from manim import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THEME, FONT_SERIF, FONT_SANS
from components.cards import ConceptCard
from components.badges import SlideBanner


class SlideLimpioScene(Scene):
    """
    Versión animada pura de la diapositiva conceptual.
    Totalmente calibrada para el marco 16:9 sin desbordes.
    """

    def construct(self):
        self.camera.background_color = THEME["bg"]

        # 1. Banner superior ajustado exactamente al ancho del marco
        banner = SlideBanner(
            title_text="AcadAId: Marco RAG Local para la Investigación Académica",
            height=0.55,
            theme=THEME,
        )
        banner.to_edge(UP, buff=0)
        self.play(FadeIn(banner, shift=DOWN * 0.3), run_time=0.8)

        # 2. Tag superior 'MARCO CONCEPTUAL'
        tag_text = Text(
            "MARCO CONCEPTUAL",
            font=FONT_SANS,
            weight=BOLD,
            font_size=13,
            color=THEME["text_tag"],
        )
        tag_text.to_corner(UL, buff=0.8)
        tag_text.set_y(2.80)
        tag_text.set_x(-5.60 + tag_text.width / 2)

        # 3. Título principal en Georgia serif
        title_rag = Text(
            "Generación\nAumentada por\nRecuperación (RAG)",
            font=FONT_SERIF,
            weight=BOLD,
            font_size=30,
            color=THEME["text_primary"],
            line_spacing=0.82,
        )
        title_rag.next_to(tag_text, DOWN, aligned_edge=LEFT, buff=0.22)

        self.play(
            FadeIn(tag_text, shift=RIGHT * 0.25),
            Write(title_rag),
            run_time=1.2,
        )
        self.wait(0.4)

        # 4. Los 3 bloques conceptuales (con alineación estricta y márgenes seguros)
        card_w = 9.2
        card_h = 0.72

        card1 = ConceptCard(
            title_text="Anclaje Empírico",
            desc_text="Respuestas basadas en un corpus documental cerrado.",
            width=card_w,
            height=card_h,
            has_box=True,
            title_size=17,
            desc_size=13.5,
            theme=THEME,
            card_id=1,
        )
        card1.next_to(title_rag, DOWN, aligned_edge=LEFT, buff=0.32)

        card2 = ConceptCard(
            title_text="Prevención de Extrapolación",
            desc_text="Elimina respuestas genéricas de internet.",
            width=card_w,
            height=card_h,
            has_box=True,
            title_size=17,
            desc_size=13.5,
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
            title_size=17,
            desc_size=13.5,
            theme=THEME,
            card_id=3,
        )
        card3.next_to(card2, DOWN, aligned_edge=LEFT, buff=0.18)

        cards = [card1, card2, card3]
        for card in cards:
            self.play(
                FadeIn(card.bg_box),
                FadeIn(card.arrow, shift=RIGHT * 0.2),
                Write(card.title),
                FadeIn(card.desc, shift=UP * 0.1),
                card.highlight_border.animate.set_opacity(0.85),
                run_time=0.9,
            )
            self.wait(0.5)
            self.play(
                card.highlight_border.animate.set_opacity(0),
                run_time=0.35,
            )

        # Resaltado final de los 3 conceptos
        self.play(
            card1.highlight_border.animate.set_opacity(0.75),
            card2.highlight_border.animate.set_opacity(0.75),
            card3.highlight_border.animate.set_opacity(0.75),
            run_time=0.8,
        )
        self.wait(2.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
