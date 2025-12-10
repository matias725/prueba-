#!/usr/bin/env python3
"""
Script de prueba para SmartConnect API
Valida todos los endpoints principales
"""

import requests
import json
from typing import Optional, Dict, Any

# Configuración
BASE_URL = "http://98.88.189.220"
API_BASE = f"{BASE_URL}/api/smartconnect"

# Credenciales de prueba
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"
OPERADOR_USER = "operador"
OPERADOR_PASS = "operador123"


class SmartConnectTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        
    def login(self, username: str, password: str) -> bool:
        """Login y obtener JWT tokens"""
        url = f"{self.base_url}/login/"
        data = {"username": username, "password": password}
        
        try:
            resp = requests.post(url, json=data)
            if resp.status_code == 200:
                result = resp.json()
                self.access_token = result.get("access")
                self.refresh_token = result.get("refresh")
                print(f"✓ Login exitoso: {username}")
                print(f"  Token: {self.access_token[:20]}...")
                return True
            else:
                print(f"✗ Login fallido: {resp.status_code} - {resp.text}")
                return False
        except Exception as e:
            print(f"✗ Error en login: {e}")
            return False
    
    def _headers(self) -> Dict[str, str]:
        """Headers con autorización"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def test_info(self) -> bool:
        """Probar endpoint /info/"""
        url = f"{self.base_url}/info/"
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                print(f"\n📋 Info del API:")
                print(f"  Proyecto: {data.get('proyecto')}")
                print(f"  Versión: {data.get('version')}")
                print(f"  Descripción: {data.get('descripcion')}")
                return True
            else:
                print(f"✗ Info fallida: {resp.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error en info: {e}")
            return False
    
    def test_endpoint(self, endpoint: str, method: str = "GET", 
                     data: Optional[Dict] = None, 
                     description: str = "") -> Optional[Dict]:
        """Probar endpoint genérico"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                resp = requests.get(url, headers=self._headers())
            elif method == "POST":
                resp = requests.post(url, json=data, headers=self._headers())
            elif method == "PATCH":
                resp = requests.patch(url, json=data, headers=self._headers())
            else:
                return None
            
            if resp.status_code in [200, 201]:
                result = resp.json()
                if isinstance(result, dict) and "results" in result:
                    count = len(result["results"])
                    print(f"✓ {description}: {count} registros")
                    return result["results"]
                elif isinstance(result, list):
                    print(f"✓ {description}: {len(result)} registros")
                    return result
                else:
                    print(f"✓ {description}: éxito")
                    return result
            else:
                print(f"✗ {description}: {resp.status_code} - {resp.text[:100]}")
                return None
        except Exception as e:
            print(f"✗ Error en {description}: {e}")
            return None
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas"""
        print("=" * 60)
        print("🚀 PRUEBAS SMARTCONNECT API")
        print("=" * 60)
        
        # Test info
        self.test_info()
        
        # Login admin
        print("\n🔑 Autenticación:")
        if not self.login(ADMIN_USER, ADMIN_PASS):
            print("No se puede continuar sin autenticación")
            return
        
        # Endpoints principales
        print("\n📊 Endpoints Principales:")
        
        usuarios = self.test_endpoint(
            "/usuarios/",
            description="Usuarios"
        )
        
        roles = self.test_endpoint(
            "/roles/",
            description="Roles"
        )
        
        departamentos = self.test_endpoint(
            "/departamentos/",
            description="Departamentos"
        )
        
        sensores = self.test_endpoint(
            "/sensores/",
            description="Sensores RFID"
        )
        
        barreras = self.test_endpoint(
            "/barreras/",
            description="Barreras de Acceso"
        )
        
        eventos = self.test_endpoint(
            "/eventos/",
            description="Eventos de Acceso"
        )
        
        # Detalles de sensores
        if sensores:
            print("\n🏷️  Detalles de Sensores:")
            for sensor in sensores[:2]:
                uid = sensor.get("uid")
                estado = sensor.get("estado")
                print(f"  - UID: {uid}, Estado: {estado}")
        
        # Detalles de barreras
        if barreras:
            print("\n🚪 Detalles de Barreras:")
            for barrera in barreras[:2]:
                nombre = barrera.get("nombre")
                estado = barrera.get("estado")
                print(f"  - {nombre}: {estado}")
        
        # Test control manual de barrera (si existe)
        if barreras:
            barrera_id = barreras[0].get("id")
            print(f"\n⚙️  Control Manual de Barrera (ID: {barrera_id}):")
            result = self.test_endpoint(
                f"/barreras/{barrera_id}/control/",
                method="POST",
                data={"accion": "abrir"},
                description="Abrir barrera"
            )
            if result:
                print(f"  Estado resultado: {result.get('estado')}")
        
        # Test con operador
        print("\n\n🔑 Prueba con rol Operador:")
        if self.login(OPERADOR_USER, OPERADOR_PASS):
            self.test_endpoint(
                "/eventos/",
                description="Eventos (acceso Operador)"
            )
        
        # Resumen
        print("\n" + "=" * 60)
        print("✅ PRUEBAS COMPLETADAS")
        print("=" * 60)


def main():
    tester = SmartConnectTester(API_BASE)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
