from color_utils import are_complementary

def calculate_style_score(top_path, bottom_path, weather="normal"):
    """Calcule un score 0-100 basé sur des règles de style"""
    try:
        score = 50  # Score de base

        # 1. Harmonisation des couleurs
        from color_utils import get_dominant_color
        top_color = get_dominant_color(top_path)
        bottom_color = get_dominant_color(bottom_path)
        
        if are_complementary(top_color, bottom_color):
            score += 25
        elif top_color == bottom_color:
            score -= 10

        # 2. Adéquation météo (ex: veste quand il pleut)
        if "jacket" in top_path.lower() and weather == "rain":
            score += 15

        # 3. Équilibre des silhouettes
        if "oversized" in top_path.lower() and "slim" in bottom_path.lower():
            score += 10

        return max(0, min(100, score))  # Borné entre 0 et 100
    
    except Exception as e:
        raise RuntimeError(f"Erreur de calcul du score : {str(e)}")