#!/usr/bin/env python3
"""
Exemplo prático de como usar o endpoint de upload de imagens de anúncios
"""
import requests
import json
import os
from io import BytesIO
from PIL import Image

# Configurações
BASE_URL = "http://localhost:8000/api/v1"

def create_sample_image(width=800, height=600, color=(255, 0, 0), text="SAMPLE"):
    """Cria uma imagem de exemplo"""
    img = Image.new('RGB', (width, height), color)
    return img

def image_to_bytes(image, format='JPEG'):
    """Converte imagem PIL para bytes"""
    buf = BytesIO()
    image.save(buf, format=format)
    buf.seek(0)
    return buf.getvalue()

def test_upload_anuncio_with_images():
    """Testa o upload de anúncio com imagens"""
    print("🚀 Testando upload de anúncio com imagens...\n")
    
    try:
        # Primeiro, vamos criar dados de teste necessários
        print("📝 Criando dados de teste...")
        
        # Cria um usuário
        user_data = {
            "nome": "João Silva",
            "cpf": "12345678901",
            "email": "joao@teste.com",
            "senha": "senha123"
        }
        
        user_response = requests.post(f"{BASE_URL}/usuarios/create", json=user_data)
        if user_response.status_code != 200:
            print(f"❌ Erro ao criar usuário: {user_response.status_code}")
            return False
        
        usuario_id = user_response.json()["id"]
        print(f"✅ Usuário criado com ID: {usuario_id}")
        
        # Cria um funcionário
        func_data = {
            "usuario_id": usuario_id,
            "rendimento_mensal": 3000.0
        }
        
        func_response = requests.post(f"{BASE_URL}/funcionarios/create", json=func_data)
        if func_response.status_code != 200:
            print(f"❌ Erro ao criar funcionário: {func_response.status_code}")
            return False
        
        funcionario_id = func_response.json()["id"]
        print(f"✅ Funcionário criado com ID: {funcionario_id}")
        
        # Cria um carro
        carro_data = {
            "modelo": "Civic",
            "marca": "Honda",
            "ano": 2020,
            "cor": "Preto",
            "tipo_combustivel": "Gasolina",
            "preco": 85000.0,
            "revisado": True,
            "disponivel": True,
            "tipo_direcao": "Hidráulica",
            "tracao": "Dianteira",
            "consumo_cidade": 12.5,
            "airbag": True,
            "ar_condicionado": True
        }
        
        carro_response = requests.post(f"{BASE_URL}/carros/create", json=carro_data)
        if carro_response.status_code != 200:
            print(f"❌ Erro ao criar carro: {carro_response.status_code}")
            return False
        
        carro_id = carro_response.json()["id"]
        print(f"✅ Carro criado com ID: {carro_id}")
        
        # Cria imagens de exemplo
        print("🖼️  Criando imagens de exemplo...")
        image1 = create_sample_image(800, 600, (255, 0, 0), "FRENTE")
        image2 = create_sample_image(800, 600, (0, 255, 0), "LATERAL")
        image3 = create_sample_image(800, 600, (0, 0, 255), "TRASEIRA")
        
        # Converte para bytes
        image1_bytes = image_to_bytes(image1)
        image2_bytes = image_to_bytes(image2)
        image3_bytes = image_to_bytes(image3)
        
        # Prepara os dados para upload
        files = {
            'imagem1': ('frente.jpg', image1_bytes, 'image/jpeg'),
            'imagem2': ('lateral.jpg', image2_bytes, 'image/jpeg'),
            'imagem3': ('traseira.jpg', image3_bytes, 'image/jpeg')
        }
        
        data = {
            'funcionario_id': funcionario_id,
            'carro_id': carro_id,
            'data_publicacao': '2024-01-15'
        }
        
        # Faz o upload
        print("📤 Fazendo upload do anúncio com imagens...")
        response = requests.post(f"{BASE_URL}/anuncios/create-with-images", data=data, files=files)
        
        if response.status_code == 200:
            anuncio = response.json()
            print("✅ Anúncio criado com sucesso!")
            print(f"   ID: {anuncio['id']}")
            print(f"   Funcionário: {anuncio['funcionario_id']}")
            print(f"   Carro: {anuncio['carro_id']}")
            print(f"   Data: {anuncio['data_publicacao']}")
            print(f"   Imagem 1: {anuncio['imagem1_url']}")
            print(f"   Imagem 2: {anuncio['imagem2_url']}")
            print(f"   Imagem 3: {anuncio['imagem3_url']}")
            
            # Verifica se as imagens estão acessíveis
            print("\n🔍 Verificando se as imagens estão acessíveis...")
            for i, url in enumerate([anuncio['imagem1_url'], anuncio['imagem2_url'], anuncio['imagem3_url']], 1):
                if url:
                    img_response = requests.get(url)
                    if img_response.status_code == 200:
                        print(f"   ✅ Imagem {i}: Acessível ({len(img_response.content)} bytes)")
                    else:
                        print(f"   ❌ Imagem {i}: Erro {img_response.status_code}")
                else:
                    print(f"   ⚠️  Imagem {i}: Não enviada")
            
            return True
        else:
            print(f"❌ Erro ao criar anúncio: {response.status_code}")
            print(f"   Detalhes: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        return False

if __name__ == "__main__":
    # Instala PIL se necessário
    try:
        from PIL import Image
    except ImportError:
        print("📦 Instalando Pillow...")
        os.system("pip install Pillow")
        from PIL import Image
    
    success = test_upload_anuncio_with_images()
    
    if success:
        print("\n🎉 Teste concluído com sucesso!")
        print("\n📋 Próximos passos:")
        print("   1. Acesse o MinIO em http://localhost:9001")
        print("   2. Faça login com: minio_admin / minio_admin123")
        print("   3. Verifique o bucket 'autocampos-images'")
        print("   4. Integre com o frontend para upload de imagens")
    else:
        print("\n❌ Teste falhou. Verifique os logs do backend.")
