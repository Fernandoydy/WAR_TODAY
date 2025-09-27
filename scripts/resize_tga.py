#!/usr/bin/env python3
"""
Script para redimensionar arquivos .tga
Cria duas pastas com diferentes tamanhos:
- small: 10x7 pixels
- medium: 41x26 pixels
"""

import os
import sys
from pathlib import Path
from PIL import Image

def create_directories(base_path):
    """Cria os diretórios 'small' e 'medium' se não existirem."""
    small_dir = base_path / "small"
    medium_dir = base_path / "medium"
    
    small_dir.mkdir(exist_ok=True)
    medium_dir.mkdir(exist_ok=True)
    
    return small_dir, medium_dir

def process_tga_files(source_dir):
    """
    Processa todos os arquivos .tga no diretório especificado.
    
    Args:
        source_dir: Caminho para o diretório contendo os arquivos .tga
    """
    # Converter para Path object
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"Erro: O diretório '{source_dir}' não existe.")
        return False
    
    if not source_path.is_dir():
        print(f"Erro: '{source_dir}' não é um diretório.")
        return False
    
    # Criar diretórios de saída
    small_dir, medium_dir = create_directories(source_path)
    
    # Buscar arquivos .tga (case-insensitive)
    tga_files = list(source_path.glob("*.tga")) + list(source_path.glob("*.TGA"))
    
    if not tga_files:
        print(f"Nenhum arquivo .tga encontrado em '{source_dir}'")
        return False
    
    print(f"Encontrados {len(tga_files)} arquivos .tga para processar...")
    
    # Dimensões de saída
    SMALL_SIZE = (10, 7)
    MEDIUM_SIZE = (41, 26)
    
    processed_count = 0
    error_count = 0
    
    for tga_file in tga_files:
        try:
            print(f"Processando: {tga_file.name}")
            
            # Abrir a imagem
            with Image.open(tga_file) as img:
                # Informações da imagem original
                print(f"  Dimensões originais: {img.size[0]}x{img.size[1]}")
                
                # Criar versão small (10x7)
                img_small = img.resize(SMALL_SIZE, Image.Resampling.LANCZOS)
                small_path = small_dir / tga_file.name
                img_small.save(small_path, "TGA")
                print(f"  ✓ Versão small salva: {small_path.name}")
                
                # Criar versão medium (41x26)
                img_medium = img.resize(MEDIUM_SIZE, Image.Resampling.LANCZOS)
                medium_path = medium_dir / tga_file.name
                img_medium.save(medium_path, "TGA")
                print(f"  ✓ Versão medium salva: {medium_path.name}")
                
                processed_count += 1
                
        except Exception as e:
            print(f"  ✗ Erro ao processar {tga_file.name}: {str(e)}")
            error_count += 1
            continue
    
    # Resumo do processamento
    print("\n" + "="*50)
    print("RESUMO DO PROCESSAMENTO:")
    print(f"  Total de arquivos processados: {processed_count}")
    print(f"  Total de erros: {error_count}")
    print(f"  Arquivos salvos em:")
    print(f"    - {small_dir} (10x7 pixels)")
    print(f"    - {medium_dir} (41x26 pixels)")
    print("="*50)
    
    return True

def main():
    """Função principal do script."""
    print("="*50)
    print("REDIMENSIONADOR DE ARQUIVOS TGA")
    print("="*50)
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        source_directory = sys.argv[1]
    else:
        # Se não foi fornecido argumento, usar diretório atual
        source_directory = input("Digite o caminho da pasta com os arquivos .tga (ou Enter para usar pasta atual): ").strip()
        if not source_directory:
            source_directory = "."
    
    # Processar os arquivos
    success = process_tga_files(source_directory)
    
    if success:
        print("\nProcessamento concluído com sucesso!")
    else:
        print("\nProcessamento falhou ou não encontrou arquivos.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcessamento interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")
        sys.exit(1)