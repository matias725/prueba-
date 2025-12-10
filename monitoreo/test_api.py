"""
Script de prueba para la API REST de EcoEnergy
Ejecutar: python test_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"🔹 {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)

def test_api():
    print("\n🚀 Iniciando pruebas de la API REST de EcoEnergy\n")
    
    # 1. Info del proyecto
    print_response(
        "1. Información del Proyecto",
        requests.get(f"{BASE_URL}/info/")
    )
    
    # 2. Listar organizaciones
    print_response(
        "2. Listar Organizaciones",
        requests.get(f"{BASE_URL}/organizaciones/")
    )
    
    # 3. Listar zonas
    print_response(
        "3. Listar Zonas",
        requests.get(f"{BASE_URL}/zonas/")
    )
    
    # 4. Listar dispositivos
    print_response(
        "4. Listar Dispositivos",
        requests.get(f"{BASE_URL}/dispositivos/")
    )
    
    # 5. Dispositivos por categoría
    print_response(
        "5. Dispositivos por Categoría",
        requests.get(f"{BASE_URL}/dispositivos/por_categoria/")
    )
    
    # 6. Listar mediciones
    print_response(
        "6. Listar Mediciones",
        requests.get(f"{BASE_URL}/mediciones/")
    )
    
    # 7. Estadísticas generales de mediciones
    print_response(
        "7. Estadísticas Generales de Mediciones",
        requests.get(f"{BASE_URL}/mediciones/estadisticas_generales/")
    )
    
    # 8. Listar alertas
    print_response(
        "8. Listar Alertas",
        requests.get(f"{BASE_URL}/alertas/")
    )
    
    # 9. Alertas por gravedad
    print_response(
        "9. Alertas por Gravedad",
        requests.get(f"{BASE_URL}/alertas/por_gravedad/")
    )
    
    # 10. Alertas críticas
    print_response(
        "10. Alertas Críticas",
        requests.get(f"{BASE_URL}/alertas/criticas/")
    )
    
    print("\n✅ Pruebas completadas\n")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: No se pudo conectar al servidor.")
        print("Asegúrate de que el servidor Django esté corriendo:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
