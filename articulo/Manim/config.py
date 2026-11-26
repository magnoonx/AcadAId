"""
Configuración global de estilos, colores y tipografías para AcadAId Manim.
Permite alternar entre tema Claro (coincidente con las diapositivas) y tema Oscuro.
"""

from manim import *

# ==========================================
# PALETA DE COLORES - TEMA CLARO (Default)
# ==========================================
LIGHT_THEME = {
    "name": "light",
    "bg": "#F5F7FA",               # Fondo grisáceo claro / off-white del slide
    "banner_bg": "#0B132B",        # Fondo oscuro para el banner superior
    "banner_text": "#FFFFFF",      # Texto blanco del banner
    "text_primary": "#0A192F",     # Azul marino profundo para títulos principales
    "text_secondary": "#475569",   # Gris pizarra para descripciones
    "text_tag": "#1E3A8A",         # Azul corporativo para 'MARCO CONCEPTUAL'
    "accent_blue": "#0088FF",      # Azul cian / eléctrico de las flechas
    "accent_blue_light": "#E0F2FE",# Fondo suave para highlights
    "card_bg": "#FFFFFF",          # Fondo de tarjetas
    "card_border": "#CBD5E1",      # Borde sutil
    "card_shadow": "#94A3B8",      # Sombra sutil
    "vault_bg": "#EBF3FB",         # Contenedor del corpus cerrado
    "vault_border": "#0284C7",     # Borde del corpus
    "doc_fill": "#FFFFFF",         # Relleno de documentos
    "doc_border": "#64748B",       # Borde de documentos
    "doc_accent": "#0284C7",       # Acento en documentos
    "internet_cloud": "#E2E8F0",   # Nube de internet
    "danger_red": "#DC2626",       # Rojo para bloqueo/prevención
    "success_green": "#059669",    # Verde de validación empírica
    "amber": "#D97706",            # Ámbar
}

# ==========================================
# PALETA DE COLORES - TEMA OSCURO
# ==========================================
DARK_THEME = {
    "name": "dark",
    "bg": "#0B1120",               # Azul oscuro profundo
    "banner_bg": "#020617",
    "banner_text": "#F8FAFC",
    "text_primary": "#F8FAFC",     # Casi blanco
    "text_secondary": "#94A3B8",   # Gris claro
    "text_tag": "#60A5FA",         # Azul brillante
    "accent_blue": "#38BDF8",      # Azul cielo eléctrico
    "accent_blue_light": "#0C4A6E",
    "card_bg": "#131E36",
    "card_border": "#1E293B",
    "card_shadow": "#020617",
    "vault_bg": "#0F213A",
    "vault_border": "#38BDF8",
    "doc_fill": "#1E293B",
    "doc_border": "#475569",
    "doc_accent": "#38BDF8",
    "internet_cloud": "#1E293B",
    "danger_red": "#F43F5E",
    "success_green": "#10B981",
    "amber": "#FBBF24",
}

# Tema por defecto (Claro, idéntico a la imagen proporcionada)
THEME = LIGHT_THEME

# ==========================================
# TIPOGRAFÍAS
# ==========================================
FONT_SERIF = "Georgia"
FONT_SANS = "Segoe UI"
