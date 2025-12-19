# API Configuration
API_CONFIG = {
    'nhtsa': {
        'base_url': 'https://api.nhtsa.gov',
        'timeout': 30,
        'retries': 3
    },
    'vin_decoder': {
        'base_url': 'https://vpic.nhtsa.dot.gov/api',
        'timeout': 30,
        'retries': 3
    }
}

# Mock data fallback
MOCK_DATA = {
    'complaints': {
        'Toyota': {
            'CAMRY': {2020: 45, 2021: 38, 2022: 32},
            'COROLLA': {2020: 52, 2021: 41, 2022: 35},
            'RAV4': {2020: 38, 2021: 31, 2022: 28}
        }
    }
}