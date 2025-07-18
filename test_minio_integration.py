#!/usr/bin/env python3
"""
Script para testar a integração MinIO com endpoints de anúncios
"""
import requests
import json

# Configurações
BASE_URL = "http://localhost:8000/api/v1"
MINIO_URL = "http://localhost:9001"  # Console web do MinIO

def test_minio_connectivity():
    """Testa se o MinIO está acessível"""
    try:
        response = requests.get(f"http://localhost:9000/minio/health/live")
        print("✓ MinIO está rodando e acessível")
        return True
    except Exception as e:
        print(f"✗ Erro ao acessar MinIO: {e}")
        return False

def test_anuncios_endpoints():
    """Testa os endpoints de anúncios"""
    try:
        # Listar anúncios
        response = requests.get(f"{BASE_URL}/anuncios/get")
        if response.status_code == 200:
            print("✓ Endpoint de listagem de anúncios está funcionando")
            anuncios = response.json()
            print(f"  Encontrados {len(anuncios)} anúncios")
            return True
        else:
            print(f"✗ Erro ao listar anúncios: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Erro ao acessar endpoint de anúncios: {e}")
        return False

def print_available_endpoints():
    """Imprime os endpoints disponíveis"""
    print("\n📋 Endpoints disponíveis para upload de imagens:")
    print("  POST /api/v1/anuncios/create-with-images")
    print("  PUT  /api/v1/anuncios/update-with-images/{anuncio_id}")
    print("  GET  /api/v1/anuncios/images/{image_name}")
    print("  DELETE /api/v1/anuncios/delete/{anuncio_id}")
    
    print("\n🔧 Como usar:")
    print("  1. Para criar anúncio com imagens, use POST com multipart/form-data:")
    print("     - funcionario_id: int (obrigatório)")
    print("     - carro_id: int (opcional)")
    print("     - moto_id: int (opcional)")
    print("     - data_publicacao: string YYYY-MM-DD (opcional)")
    print("     - imagem1: arquivo (opcional)")
    print("     - imagem2: arquivo (opcional)")
    print("     - imagem3: arquivo (opcional)")
    
    print("\n🖼️  Acesso ao MinIO:")
    print(f"  Console: {MINIO_URL}")
    print("  Usuário: minio_admin")
    print("  Senha: minio_admin123")
    print("  Bucket: autocampos-images")

def main():
    print("🚀 Testando integração MinIO + Backend...\n")
    
    # Testa conectividade
    minio_ok = test_minio_connectivity()
    backend_ok = test_anuncios_endpoints()
    
    if minio_ok and backend_ok:
        print("\n✅ Integração MinIO + Backend está funcionando!")
        print_available_endpoints()
    else:
        print("\n❌ Problemas encontrados na integração")
        if not minio_ok:
            print("  - MinIO não está acessível")
        if not backend_ok:
            print("  - Backend não está respondendo corretamente")

if __name__ == "__main__":
    main()
