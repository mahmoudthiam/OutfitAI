from colorthief import ColorThief
import numpy as np

def get_dominant_color(image_path, palette_size=3):
    """Extrait la couleur dominante RGB"""
    try:
        color_thief = ColorThief(image_path)
        palette = color_thief.get_palette(color_count=palette_size)
        return palette[0]  # Retourne la couleur dominante (R, G, B)
    except Exception as e:
        raise ValueError(f"Erreur d'analyse couleur : {str(e)}")

def rgb_to_hsv(r, g, b):
    """Convertit RGB en HSV (teinte, saturation, valeur)"""
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b)/df) % 360)
    elif mx == g:
        h = (60 * ((b - r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g)/df) + 240) % 360
    return (h, mx, mn)

def are_complementary(color1, color2, threshold=120):
    """Vérifie si deux couleurs sont complémentaires"""
    hsv1 = rgb_to_hsv(*color1)
    hsv2 = rgb_to_hsv(*color2)
    hue_diff = abs(hsv1[0] - hsv2[0])
    return hue_diff > threshold