from manim import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THEME, FONT_SERIF, FONT_SANS


class LocalInferenceNode(VGroup):
    """
    Representación del Motor de Inferencia Local (LLM local privado sin conexión exterior).
    """

    def __init__(
        self,
        title: str = "MOTOR DE INFERENCIA LOCAL",
        subtitle: str = "LLM Offline / Hardware Propio",
        width: float = 4.4,
        height: float = 1.3,
        theme: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME

        self.box = RoundedRectangle(
            corner_radius=0.18,
            width=width,
            height=height,
            stroke_width=2.2,
            stroke_color=self.theme["accent_blue"],
            fill_color=self.theme["card_bg"],
            fill_opacity=0.95,
        )

        title_lbl = Text(
            title,
            font=FONT_SANS,
            weight=BOLD,
            font_size=11,
            color=self.theme["text_primary"],
        )

        sub_lbl = Text(
            subtitle,
            font=FONT_SANS,
            font_size=9,
            color=self.theme["accent_blue"],
        )

        status_dot = Dot(radius=0.07, color=self.theme["success_green"])
        status_txt = Text("100% Offline & Privado", font=FONT_SANS, font_size=8, color=self.theme["success_green"])
        status_grp = VGroup(status_dot, status_txt).arrange(RIGHT, buff=0.1)

        v_content = VGroup(title_lbl, sub_lbl, status_grp).arrange(DOWN, buff=0.1)
        v_content.move_to(self.box)

        self.add(self.box, v_content)


class HermeneuticSynthesis(VGroup):
    """
    Representación de la 'Fidelidad Hermenéutica':
    Muestra cómo los fragmentos del texto original conservan su significado,
    citación y contexto al generar la respuesta científica.
    """

    def __init__(
        self,
        width: float = 4.6,
        height: float = 2.8,
        theme: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME

        box = RoundedRectangle(
            corner_radius=0.2,
            width=width,
            height=height,
            stroke_width=2.0,
            stroke_color=self.theme["success_green"],
            fill_color=self.theme["card_bg"],
            fill_opacity=0.95,
        )

        title = Text(
            "SÍNTESIS CIENTÍFICA GROUNDED",
            font=FONT_SANS,
            weight=BOLD,
            font_size=11,
            color=self.theme["text_primary"],
        )
        title.next_to(box.get_top(), DOWN, buff=0.15)

        # Citas contextuales
        c1 = Text("Fragmento A: \"...hallazgo metodológico...\" [Doc A, p.14]", font=FONT_SANS, font_size=8.5, color=self.theme["accent_blue"])
        c2 = Text("Fragmento B: \"...validez interna observada...\" [Doc B, §3]", font=FONT_SANS, font_size=8.5, color=self.theme["accent_blue"])
        
        # Respuesta generada
        resp_box = RoundedRectangle(
            corner_radius=0.1,
            width=width * 0.88,
            height=0.95,
            stroke_width=1,
            stroke_color=self.theme["card_border"],
            fill_color=self.theme["vault_bg"],
            fill_opacity=0.7,
        )
        
        resp_label = Text("Respuesta Generada:", font=FONT_SANS, weight=SEMIBOLD, font_size=8.5, color=self.theme["text_primary"])
        resp_content = Text(
            "\"La evidencia empírica respalda la metodología sin distorsión\nde los postulados originales de los autores.\"",
            font=FONT_SERIF,
            font_size=8.5,
            color=self.theme["text_primary"],
        )
        resp_inner = VGroup(resp_label, resp_content).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        resp_inner.move_to(resp_box)
        resp_group = VGroup(resp_box, resp_inner)

        fidelity_badge = Text(
            "✓ Trazabilidad directa a las citas originales",
            font=FONT_SANS,
            font_size=8.5,
            weight=SEMIBOLD,
            color=self.theme["success_green"],
        )

        all_items = VGroup(title, c1, c2, resp_group, fidelity_badge).arrange(DOWN, buff=0.12)
        all_items.move_to(box)

        self.add(box, all_items)
