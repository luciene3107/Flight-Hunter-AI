"""
Configurações da estratégia de busca do Flight Hunter AI.
"""

# Estratégias disponíveis
FAST = "fast"
BALANCED = "balanced"
FULL = "full"

# Estratégia padrão
DEFAULT_STRATEGY = FAST

# Limites por estratégia
SEARCH_LIMITS = {
    FAST: {
        "max_destinations": 5,
        "max_dates": 2,
        "max_results": 10,
        "max_requests": 10,
    },
    BALANCED: {
        "max_destinations": 10,
        "max_dates": 4,
        "max_results": 20,
        "max_requests": 40,
    },
    FULL: {
        "max_destinations": 30,
        "max_dates": 6,
        "max_results": 50,
        "max_requests": 180,
    },
}