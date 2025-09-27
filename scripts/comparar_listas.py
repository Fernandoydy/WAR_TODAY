#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparar duas listas de nomes de arquivos e editar a segunda lista
removendo os arquivos que também existem na primeira lista.
"""

import os
import sys

def ler_lista_arquivos(caminho_arquivo):
    """
    Lê um arquivo de texto e retorna um set com os nomes de arquivos.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo de texto
    
    Returns:
        set: Conjunto com os nomes dos arquivos (sem linhas vazias)
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            # Remove espaços em branco e linhas vazias
            nomes = {linha.strip() for linha in arquivo if linha.strip()}
        return nomes
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return set()
    except Exception as e:
        print(f"Erro ao ler o arquivo '{caminho_arquivo}': {e}")
        return set()

def escrever_lista_arquivos(caminho_arquivo, lista_nomes):
    """
    Escreve uma lista de nomes de arquivos em um arquivo de texto.
    
    Args:
        caminho_arquivo (str): Caminho para o arquivo de destino
        lista_nomes (set): Conjunto com os nomes dos arquivos
    """
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            for nome in sorted(lista_nomes):  # Ordena alfabeticamente
                arquivo.write(nome + '\n')
        print(f"Lista atualizada salva em '{caminho_arquivo}'")
    except Exception as e:
        print(f"Erro ao escrever o arquivo '{caminho_arquivo}': {e}")

def comparar_listas(arquivo_lista1, arquivo_lista2):
    """
    Compara duas listas de arquivos e edita a segunda lista.
    
    Args:
        arquivo_lista1 (str): Caminho para o primeiro arquivo (referência)
        arquivo_lista2 (str): Caminho para o segundo arquivo (a ser editado)
    """
    # Lê as duas listas
    print("Lendo as listas de arquivos...")
    lista1 = ler_lista_arquivos(arquivo_lista1)
    lista2 = ler_lista_arquivos(arquivo_lista2)
    
    if not lista1:
        print(f"Lista 1 está vazia ou não pôde ser lida.")
        return
    
    if not lista2:
        print(f"Lista 2 está vazia ou não pôde ser lida.")
        return
    
    # Encontra arquivos que estão apenas na lista2
    apenas_lista2 = lista2 - lista1
    arquivos_comuns = lista1.intersection(lista2)
    
    # Exibe resultados da comparação
    print(f"\n=== RESULTADO DA COMPARAÇÃO ===")
    print(f"Total de arquivos na lista 1: {len(lista1)}")
    print(f"Total de arquivos na lista 2: {len(lista2)}")
    print(f"Arquivos em comum: {len(arquivos_comuns)}")
    print(f"Arquivos apenas na lista 2: {len(apenas_lista2)}")
    
    if arquivos_comuns:
        print(f"\nArquivos que serão removidos da lista 2 (existem em ambas):")
        for arquivo in sorted(arquivos_comuns):
            print(f"  - {arquivo}")
    
    if apenas_lista2:
        print(f"\nArquivos que permanecerão na lista 2 (únicos):")
        for arquivo in sorted(apenas_lista2):
            print(f"  - {arquivo}")
    else:
        print(f"\nNenhum arquivo único encontrado na lista 2.")
    
    # Pergunta se o usuário quer salvar as alterações
    resposta = input(f"\nDeseja salvar a lista 2 atualizada? (s/n): ").lower().strip()
    if resposta in ['s', 'sim', 'y', 'yes']:
        # Cria backup da lista original
        backup_arquivo = arquivo_lista2 + '.backup'
        try:
            import shutil
            shutil.copy2(arquivo_lista2, backup_arquivo)
            print(f"Backup criado: {backup_arquivo}")
        except Exception as e:
            print(f"Aviso: Não foi possível criar backup: {e}")
        
        # Salva a lista atualizada
        escrever_lista_arquivos(arquivo_lista2, apenas_lista2)
        print(f"Lista 2 atualizada com {len(apenas_lista2)} arquivos únicos.")
    else:
        print("Operação cancelada. Nenhum arquivo foi modificado.")

def main():
    """Função principal do script."""
    print("=== COMPARADOR DE LISTAS DE ARQUIVOS ===\n")
    
    # Verifica argumentos da linha de comando
    if len(sys.argv) == 3:
        arquivo_lista1 = sys.argv[1]
        arquivo_lista2 = sys.argv[2]
    else:
        # Solicita os caminhos dos arquivos
        arquivo_lista1 = input("Digite o caminho para a lista 1 (referência): ").strip()
        arquivo_lista2 = input("Digite o caminho para a lista 2 (a ser editada): ").strip()
    
    # Verifica se os arquivos existem
    if not os.path.exists(arquivo_lista1):
        print(f"Erro: Arquivo '{arquivo_lista1}' não existe.")
        return
    
    if not os.path.exists(arquivo_lista2):
        print(f"Erro: Arquivo '{arquivo_lista2}' não existe.")
        return
    
    # Executa a comparação
    comparar_listas(arquivo_lista1, arquivo_lista2)

if __name__ == "__main__":
    main()