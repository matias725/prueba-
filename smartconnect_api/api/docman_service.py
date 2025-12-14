"""
Servicio para integración con API Docman
"""
import requests
from django.conf import settings
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DocmanAPIClient:
    """Cliente para interactuar con la API de Docman"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'DOCMAN_API_URL', '')
        self.api_key = getattr(settings, 'DOCMAN_API_KEY', '')
        self.timeout = getattr(settings, 'DOCMAN_TIMEOUT', 30)
        
        if not self.base_url:
            logger.warning("DOCMAN_API_URL no está configurada")
    
    def _get_headers(self, additional_headers: Optional[Dict] = None) -> Dict:
        """Genera los headers para las peticiones"""
        headers = {
            'Content-Type': 'application/json',
        }
        
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Realiza una petición HTTP a la API de Docman
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint de la API (sin la base URL)
            data: Datos a enviar en el body (para POST, PUT)
            params: Parámetros de query string
        
        Returns:
            Dict con la respuesta de la API
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return {
                'success': True,
                'data': response.json() if response.content else None,
                'status_code': response.status_code
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en petición a Docman API: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }
    
    # ============ MÉTODOS PARA DOCUMENTOS ============
    
    def upload_document(
        self, 
        file_path: str, 
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Sube un documento a Docman
        
        Args:
            file_path: Ruta del archivo a subir
            metadata: Metadatos adicionales del documento
        
        Returns:
            Dict con la respuesta de la API
        """
        # TODO: Implementar según la especificación de Docman API
        endpoint = "/documents/upload"
        data = {
            'file_path': file_path,
            'metadata': metadata or {}
        }
        return self._make_request('POST', endpoint, data=data)
    
    def get_document(self, document_id: str) -> Dict[str, Any]:
        """
        Obtiene un documento de Docman
        
        Args:
            document_id: ID del documento en Docman
        
        Returns:
            Dict con la respuesta de la API
        """
        endpoint = f"/documents/{document_id}"
        return self._make_request('GET', endpoint)
    
    def list_documents(
        self, 
        filters: Optional[Dict] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Lista documentos de Docman
        
        Args:
            filters: Filtros para la búsqueda
            page: Número de página
            page_size: Tamaño de página
        
        Returns:
            Dict con la respuesta de la API
        """
        endpoint = "/documents"
        params = {
            'page': page,
            'page_size': page_size,
            **(filters or {})
        }
        return self._make_request('GET', endpoint, params=params)
    
    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Elimina un documento de Docman
        
        Args:
            document_id: ID del documento en Docman
        
        Returns:
            Dict con la respuesta de la API
        """
        endpoint = f"/documents/{document_id}"
        return self._make_request('DELETE', endpoint)
    
    def update_document_metadata(
        self, 
        document_id: str, 
        metadata: Dict
    ) -> Dict[str, Any]:
        """
        Actualiza los metadatos de un documento
        
        Args:
            document_id: ID del documento en Docman
            metadata: Nuevos metadatos
        
        Returns:
            Dict con la respuesta de la API
        """
        endpoint = f"/documents/{document_id}/metadata"
        return self._make_request('PUT', endpoint, data=metadata)
    
    # ============ MÉTODOS DE UTILIDAD ============
    
    def health_check(self) -> bool:
        """
        Verifica si la API de Docman está disponible
        
        Returns:
            True si la API responde correctamente
        """
        try:
            result = self._make_request('GET', '/health')
            return result.get('success', False)
        except Exception as e:
            logger.error(f"Error en health check de Docman: {str(e)}")
            return False


# Instancia singleton del cliente
docman_client = DocmanAPIClient()
