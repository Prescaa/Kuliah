import requests

def test_nhtsa():
    # Parameter Test
    make = "TOYOTA"
    model = "CAMRY"
    year = 2018
    
    url = "https://api.nhtsa.gov/complaints/complaintsByVehicle"
    
    # PERBAIKAN: Ganti 'year' menjadi 'modelYear'
    params = {
        "make": make,
        "model": model,
        "modelYear": year  # <--- INI KUNCINYA
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Testing URL: {url}")
    print(f"Params: {params}")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            print(f"✅ SUKSES! Ditemukan {count} complaints untuk {model} {year}")
            # Tampilkan 1 contoh complaint biar yakin datanya real
            if count > 0 and 'results' in data:
                print(f"   Contoh: {data['results'][0].get('summary', '')[:100]}...")
        else:
            print(f"❌ Gagal: {response.text}")
            
    except Exception as e:
        print(f"❌ Error fatal: {e}")

if __name__ == "__main__":
    test_nhtsa()