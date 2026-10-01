"""
Country code to lat/lng mapping for map markers.
Source: Simplified public data.
"""

COUNTRY_COORDS = {
    'BD': (23.6850, 90.3563),    # Bangladesh
    'IN': (20.5937, 78.9629),    # India
    'US': (37.0902, -95.7129),   # United States
    'GB': (55.3781, -3.4360),    # United Kingdom
    'CA': (56.1304, -106.3468),  # Canada
    'AU': (-25.2744, 133.7751),  # Australia
    'DE': (51.1657, 10.4515),    # Germany
    'FR': (46.2276, 2.2137),     # France
    'IT': (41.8719, 12.5674),    # Italy
    'ES': (40.4637, -3.7492),    # Spain
    'NL': (52.1326, 5.2913),     # Netherlands
    'BE': (50.5039, 4.4699),     # Belgium
    'CH': (46.8182, 8.2275),     # Switzerland
    'SE': (60.1282, 18.6435),    # Sweden
    'NO': (60.4720, 8.4689),     # Norway
    'DK': (56.2639, 9.5018),     # Denmark
    'FI': (61.9241, 25.7482),    # Finland
    'PL': (51.9194, 19.1451),    # Poland
    'RU': (61.5240, 105.3188),   # Russia
    'CN': (35.8617, 104.1954),   # China
    'JP': (36.2048, 138.2529),   # Japan
    'KR': (35.9078, 127.7669),   # South Korea
    'SG': (1.3521, 103.8198),    # Singapore
    'MY': (4.2105, 101.9758),    # Malaysia
    'ID': (-0.7893, 113.9213),   # Indonesia
    'TH': (15.8700, 100.9925),   # Thailand
    'VN': (14.0583, 108.2772),   # Vietnam
    'PH': (12.8797, 121.7740),   # Philippines
    'PK': (30.3753, 69.3451),    # Pakistan
    'LK': (7.8731, 80.7718),     # Sri Lanka
    'NP': (28.3949, 84.1240),    # Nepal
    'BT': (27.5142, 90.4336),    # Bhutan
    'MM': (21.9162, 95.9560),    # Myanmar
    'AE': (23.4241, 53.8478),    # UAE
    'SA': (23.8859, 45.0792),    # Saudi Arabia
    'EG': (26.8206, 30.8025),    # Egypt
    'ZA': (-30.5595, 22.9375),   # South Africa
    'NG': (9.0820, 8.6753),      # Nigeria
    'KE': (-0.0236, 37.9062),    # Kenya
    'BR': (-14.2350, -51.9253),  # Brazil
    'AR': (-38.4161, -63.6167),  # Argentina
    'MX': (23.6345, -102.5528),  # Mexico
    'CL': (-35.6751, -71.5430),  # Chile
    'CO': (4.5709, -74.2973),    # Colombia
    'PE': (-9.1900, -75.0152),   # Peru
    'NZ': (-40.9006, 174.8860),  # New Zealand
    'TR': (38.9637, 35.2433),    # Turkey
    'IR': (32.4279, 53.6880),    # Iran
    'IQ': (33.2232, 43.6793),    # Iraq
    'IL': (31.0461, 34.8516),    # Israel
    'UA': (48.3794, 31.1656),    # Ukraine
    'RO': (45.9432, 24.9668),    # Romania
    'GR': (39.0742, 21.8243),    # Greece
    'PT': (39.3999, -8.2245),    # Portugal
    'IE': (53.1424, -7.6921),    # Ireland
    'AT': (47.5162, 14.5501),    # Austria
    'CZ': (49.8175, 15.4730),    # Czechia
    'HU': (47.1625, 19.5033),    # Hungary
    'HK': (22.3193, 114.1694),   # Hong Kong
    'TW': (23.6978, 120.9605),   # Taiwan
}


def get_coords(country_name):
    """
    Get lat/lng from country name.
    Returns (lat, lng) or None.
    """
    if not country_name:
        return None

    # Try to find country code from name
    name_to_code = {
        'bangladesh': 'BD', 'india': 'IN', 'united states': 'US', 'usa': 'US',
        'united kingdom': 'GB', 'uk': 'GB', 'canada': 'CA', 'australia': 'AU',
        'germany': 'DE', 'france': 'FR', 'italy': 'IT', 'spain': 'ES',
        'netherlands': 'NL', 'belgium': 'BE', 'switzerland': 'CH',
        'sweden': 'SE', 'norway': 'NO', 'denmark': 'DK', 'finland': 'FI',
        'poland': 'PL', 'russia': 'RU', 'china': 'CN', 'japan': 'JP',
        'south korea': 'KR', 'korea': 'KR', 'singapore': 'SG',
        'malaysia': 'MY', 'indonesia': 'ID', 'thailand': 'TH',
        'vietnam': 'VN', 'philippines': 'PH', 'pakistan': 'PK',
        'sri lanka': 'LK', 'nepal': 'NP', 'bhutan': 'BT', 'myanmar': 'MM',
        'united arab emirates': 'AE', 'uae': 'AE', 'saudi arabia': 'SA',
        'egypt': 'EG', 'south africa': 'ZA', 'nigeria': 'NG', 'kenya': 'KE',
        'brazil': 'BR', 'argentina': 'AR', 'mexico': 'MX', 'chile': 'CL',
        'colombia': 'CO', 'peru': 'PE', 'new zealand': 'NZ', 'turkey': 'TR',
        'iran': 'IR', 'iraq': 'IQ', 'israel': 'IL', 'ukraine': 'UA',
        'romania': 'RO', 'greece': 'GR', 'portugal': 'PT', 'ireland': 'IE',
        'austria': 'AT', 'czechia': 'CZ', 'czech republic': 'CZ',
        'hungary': 'HU', 'hong kong': 'HK', 'taiwan': 'TW',
    }

    code = name_to_code.get(country_name.lower().strip())
    if code and code in COUNTRY_COORDS:
        return COUNTRY_COORDS[code]

    return None