from manim import *
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THEME, FONT_SERIF, FONT_SANS


class AcademicDoc(VGroup):
    """
    Representación visual de un documento académico (Paper, Tesis, Artículo científico).
    """

    def __init__(
        self,
        title: str = "Paper.pdf",
        tag: str = "PDF",
        width: float = 1.3,
        height: float = 1.7,
        theme: dict = None,
        accent_color: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME
        accent = accent_color or self.theme["doc_accent"]

        # 1. Cuerpo del documento (hoja)
        self.sheet = RoundedRectangle(
            corner_radius=0.08,
            width=width,
            height=height,
            stroke_width=1.5,
            stroke_color=self.theme["doc_border"],
            fill_color=self.theme["doc_fill"],
            fill_opacity=1.0,
        )

        # 2. Barra de encabezado del documento
        header_bar = RoundedRectangle(
            corner_radius=0.04,
            width=width * 0.82,
            height=0.18,
            stroke_width=0,
            fill_color=accent,
            fill_opacity=0.9,
        )
        header_bar.next_to(self.sheet.get_top(), DOWN, buff=0.12)

        # Etiqueta de tipo (ej: PDF / ARXIV)
        tag_text = Text(tag, font=FONT_SANS, font_size=8, weight=BOLD, color=WHITE)
        tag_text.move_to(header_bar)

        # 3. Líneas de texto simuladas
        lines = VGroup()
        line_widths = [0.8, 0.75, 0.7, 0.55]
        start_y = header_bar.get_bottom() + DOWN * 0.12

        for i, lw in enumerate(line_widths):
            line = Line(
                ORIGIN,
                RIGHT * (width * lw),
                stroke_width=2.0 if i == 0 else 1.4,
                color=self.theme["text_primary"] if i == 0 else self.theme["text_secondary"],
            )
            line.set_opacity(0.7 if i == 0 else 0.4)
            line.move_to(self.sheet.get_center())
            line.set_y(start_y[1] - i * 0.16)
            lines.add(line)

        # 4. Título miniatura abajo
        doc_label = Text(
            title,
            font=FONT_SANS,
            font_size=9,
            weight=SEMIBOLD,
            color=self.theme["text_primary"],
        )
        doc_label.next_to(self.sheet, DOWN, buff=0.08)

        self.add(self.sheet, header_bar, tag_text, lines, doc_label)


class CorpusVault(VGroup):
    """
    Contenedor de seguridad del 'Corpus Documental Cerrado'.
    Representa el repositorio cerrado e inmutable de fuentes académicas verificadas.
    """

    def __init__(
        self,
        width: float = 4.8,
        height: float = 3.2,
        theme: dict = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.theme = theme or THEME

        # Caja del contenedor / bóveda
        self.box = RoundedRectangle(
            corner_radius=0.2,
            width=width,
            height=height,
            stroke_width=2.5,
            stroke_color=self.theme["vault_border"],
            fill_color=self.theme["vault_bg"],
            fill_opacity=0.6,
        )

        # Etiqueta superior de la bóveda
        header_bg = RoundedRectangle(
            corner_radius=0.1,
            width=width * 0.75,
            height=0.45,
            stroke_width=1.5,
            stroke_color=self.theme["accent_blue"],
            fill_color=self.theme["card_bg"],
            fill_opacity=0.95,
        )
        header_bg.next_to(self.box.get_top(), DOWN, buff=-0.22)

        # Texto de encabezado
        self.title = Text(
            "CORPUS DOCUMENTAL CERRADO",
            font=FONT_SANS,
            weight=BOLD,
            font_size=11,
            color=self.theme["text_tag"],
        )
        self.title.move_to(header_bg)

        # Indicador de estado cerrado / validado
        self.badge = Text(
            "🔒 Entorno Verificado (Local)",
            font=FONT_SANS,
            font_size=9,
            color=self.theme["success_green"],
        )
        self.badge.next_to(self.box.get_bottom(), UP, buff=0.15)

        # Colección de documentos internos
        self.docs = VGroup()
        doc_data = [
            ("Paper A.pdf", "TESIS", "#0284C7"),
            ("Paper B.pdf", "JOURNAL", "#059669"),
            ("Articulo C.pdf", "ARXIV", "#7C3AED"),
        ]

        spacing = width / (len(doc_data) + 1)
        for i, (doc_name, tag, color) in enumerate(doc_data):
            doc = AcademicDoc(
                title=doc_name,
                tag=tag,
                width=1.05,
                height=1.45,
                accent_color=color,
                theme=self.theme,
            )
            doc.move_to(self.box.get_center())
            doc.set_x(self.box.get_left()[0] + spacing * (i + 1))
            doc.set_y(self.box.get_center()[1] + 0.05)
            self.docs.add(doc)

        self.add(self.box, header_bg, self.title, self.badge, self.docs)
