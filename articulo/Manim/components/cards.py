from manim import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THEME, FONT_SERIF, FONT_SANS


class ConceptCard(VGroup):
    """
    Componente visual para cada uno de los 3 conceptos clave de la diapositiva:
    - Flecha azul brillante (➔) perfectamente alineada en columna
    - Título en negrita (ej. 'Anclaje Empírico')
    - Descripción explicativa (ej. 'Respuestas basadas en un corpus documental cerrado.')
    - Contenedor con alineación fija a la izquierda para máxima legibilidad tipográfica.
    """

    def __init__(
        self,
        title_text: str,
        desc_text: str,
        width: float = 6.2,
        height: float = 0.85,
        theme: dict = None,
        has_box: bool = True,
        title_size: int = 18,
        desc_size: int = 14,
        card_id: int = 1,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME
        self.width_val = width
        self.height_val = height
        self.has_box = has_box
        self.card_id = card_id

        # 1. Flecha estilo cian/eléctrico idéntica a la imagen (compacta y nítida)
        arrow_shaft = Line(ORIGIN, RIGHT * 0.32, stroke_width=4.0, color=self.theme["accent_blue"])
        arrow_head = ArrowTriangleFilledTip(start_angle=0, length=0.20, width=0.20, color=self.theme["accent_blue"])
        arrow_head.move_to(arrow_shaft.get_end())
        self.arrow = VGroup(arrow_shaft, arrow_head)

        # 2. Título (Negrita, color marino profundo)
        self.title = Text(
            title_text,
            font=FONT_SANS,
            weight=BOLD,
            font_size=title_size,
            color=self.theme["text_primary"],
        )

        # 3. Descripción (Texto secundario pizarra)
        self.desc = Text(
            desc_text,
            font=FONT_SANS,
            font_size=desc_size,
            color=self.theme["text_secondary"],
        )

        # Disposición interna estricta:
        # El título y la descripción están alineados exactamente a su borde izquierdo
        self.title.align_to(ORIGIN, LEFT)
        self.desc.next_to(self.title, DOWN, aligned_edge=LEFT, buff=0.10)
        self.text_group = VGroup(self.title, self.desc)

        # La flecha se ubica a la izquierda del título, centrada verticalmente con la primera línea
        self.arrow.next_to(self.title, LEFT, buff=0.20)
        self.arrow.match_y(self.title)

        content = VGroup(self.arrow, self.text_group)

        # Fondo sutil con esquinas redondeadas
        pad_x = 0.25
        card_w = max(content.width + pad_x * 2, width)
        card_h = max(content.height + 0.20, height)

        self.bg_box = RoundedRectangle(
            corner_radius=0.12,
            width=card_w,
            height=card_h,
            stroke_width=1.0 if has_box else 0,
            stroke_color=self.theme["card_border"],
            fill_color=self.theme["card_bg"],
            fill_opacity=0.85 if has_box else 0,
        )

        # ALINEAR CONTENIDO A LA IZQUIERDA DEL RECUADRO (para que todas las flechas queden en la misma columna)
        content.align_to(self.bg_box, LEFT)
        content.shift(RIGHT * pad_x)
        content.match_y(self.bg_box)

        # Borde de iluminación (para destacar cuando esté activo)
        self.highlight_border = RoundedRectangle(
            corner_radius=0.12,
            width=card_w + 0.04,
            height=card_h + 0.04,
            stroke_width=2.5,
            stroke_color=self.theme["accent_blue"],
            fill_opacity=0,
        )
        self.highlight_border.move_to(self.bg_box)
        self.highlight_border.set_opacity(0)

        # Agregar al VGroup
        self.add(self.bg_box, self.highlight_border, self.arrow, self.title, self.desc)

    def get_arrow(self):
        return self.arrow

    def get_title(self):
        return self.title

    def get_desc(self):
        return self.desc
