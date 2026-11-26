from manim import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THEME, FONT_SERIF, FONT_SANS


class SlideBanner(VGroup):
    """
    Banner superior de la presentación (basado en la imagen 1):
    'AcadAId: Marco RAG Local para la Investigación Académica'
    Ajustado exactamente al ancho del marco de la cámara para no desbordar.
    """

    def __init__(
        self,
        title_text: str = "AcadAId: Marco RAG Local para la Investigación Académica",
        width: float = None,
        height: float = 0.60,
        theme: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME
        w = width if width is not None else config.frame_width

        self.bg = Rectangle(
            width=w,
            height=height,
            stroke_width=0,
            fill_color=self.theme["banner_bg"],
            fill_opacity=1.0,
        )

        self.text = Text(
            title_text,
            font=FONT_SERIF,
            font_size=16,
            weight=BOLD,
            color=self.theme["banner_text"],
        )
        self.text.move_to(self.bg)

        # Línea de acento inferior en azul brillante
        self.accent_line = Line(
            self.bg.get_corner(DL),
            self.bg.get_corner(DR),
            stroke_width=2.5,
            color=self.theme["accent_blue"],
        )

        self.add(self.bg, self.text, self.accent_line)


class StatusBadge(VGroup):
    """
    Badge o píldora para estados clave (Validado, Bloqueado, Fiel).
    """

    def __init__(
        self,
        text: str,
        color: str,
        font_size: int = 10,
        theme: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME

        label = Text(text, font=FONT_SANS, font_size=font_size, weight=SEMIBOLD, color=color)

        bg = RoundedRectangle(
            corner_radius=0.12,
            width=label.width + 0.30,
            height=label.height + 0.18,
            stroke_width=1.4,
            stroke_color=color,
            fill_color=self.theme["card_bg"],
            fill_opacity=0.92,
        )
        bg.move_to(label)

        self.add(bg, label)


class InternetBlockShield(VGroup):
    """
    Componente visual que ilustra la prevención de extrapolación:
    Una nube/red exterior de 'Internet Abierto' con un escudo de bloqueo.
    """

    def __init__(
        self,
        width: float = 5.0,
        height: float = 2.3,
        theme: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME

        # Contenedor de la nube externa
        cloud_box = RoundedRectangle(
            corner_radius=0.20,
            width=width,
            height=height,
            stroke_width=1.6,
            stroke_color=self.theme["card_border"],
            fill_color=self.theme["internet_cloud"],
            fill_opacity=0.45,
        )

        cloud_label = Text(
            "INTERNET / FUENTES GENÉRICAS",
            font=FONT_SANS,
            font_size=9.5,
            weight=BOLD,
            color=self.theme["text_secondary"],
        )
        cloud_label.next_to(cloud_box.get_top(), DOWN, buff=0.12)

        # Muestra de alucinaciones / datos no verificados
        item1 = Text("• Respuestas no fundamentadas", font=FONT_SANS, font_size=8.5, color=self.theme["danger_red"])
        item2 = Text("• Alucinaciones de modelos comerciales", font=FONT_SANS, font_size=8.5, color=self.theme["danger_red"])
        item3 = Text("• Datos sesgados de la web abierta", font=FONT_SANS, font_size=8.5, color=self.theme["danger_red"])

        list_items = VGroup(item1, item2, item3).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        list_items.move_to(cloud_box.get_center() + DOWN * 0.08)

        # Sello de Bloqueo
        shield_bg = Circle(
            radius=0.32,
            stroke_width=2.2,
            stroke_color=self.theme["danger_red"],
            fill_color=self.theme["card_bg"],
            fill_opacity=1.0,
        )
        slash_line = Line(
            shield_bg.get_corner(UL) * 0.65,
            shield_bg.get_corner(DR) * 0.65,
            stroke_width=2.5,
            color=self.theme["danger_red"],
        )
        slash_line.move_to(shield_bg)

        block_text = Text("✕", font=FONT_SANS, font_size=16, weight=BOLD, color=self.theme["danger_red"])
        block_text.move_to(shield_bg)

        self.shield = VGroup(shield_bg, block_text)
        self.shield.next_to(cloud_box.get_left(), RIGHT, buff=0.15)

        self.add(cloud_box, cloud_label, list_items, self.shield)
