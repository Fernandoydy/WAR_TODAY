import os
from datetime import datetime

def listar_arquivos(caminho_pasta, arquivo_saida='lista_arquivos.txt', incluir_subpastas=False):
    """
    Lista todos os arquivos de uma pasta e salva em um arquivo .txt
    
    Parâmetros:
    - caminho_pasta: caminho da pasta a ser listada
    - arquivo_saida: nome do arquivo .txt de saída (padrão: 'lista_arquivos.txt')
    - incluir_subpastas: se True, inclui arquivos de subpastas (padrão: False)
    """
    
    try:
        # Verifica se a pasta existe
        if not os.path.exists(caminho_pasta):
            print(f"Erro: A pasta '{caminho_pasta}' não existe.")
            return
        
        # Lista para armazenar os arquivos encontrados
        arquivos_encontrados = []
        
        if incluir_subpastas:
            # Percorre todas as subpastas
            for pasta_atual, subpastas, arquivos in os.walk(caminho_pasta):
                for arquivo in arquivos:
                    caminho_completo = os.path.join(pasta_atual, arquivo)
                    caminho_relativo = os.path.relpath(caminho_completo, caminho_pasta)
                    arquivos_encontrados.append(caminho_relativo)
        else:
            # Lista apenas os arquivos da pasta principal
            conteudo = os.listdir(caminho_pasta)
            for item in conteudo:
                caminho_completo = os.path.join(caminho_pasta, item)
                if os.path.isfile(caminho_completo):
                    arquivos_encontrados.append(item)
        
        # Ordena a lista de arquivos
        arquivos_encontrados.sort()
        
        # Escreve no arquivo .txt
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            # Cabeçalho do arquivo
            f.write("=" * 60 + "\n")
            f.write(f"LISTA DE ARQUIVOS\n")
            f.write(f"Pasta: {os.path.abspath(caminho_pasta)}\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de arquivos: {len(arquivos_encontrados)}\n")
            f.write("=" * 60 + "\n\n")
            
            # Lista os arquivos
            if arquivos_encontrados:
                for i, arquivo in enumerate(arquivos_encontrados, 1):
                    f.write(f"{i}. {arquivo}\n")
            else:
                f.write("Nenhum arquivo encontrado na pasta.\n")
        
        print(f"✓ Lista de arquivos salva em '{arquivo_saida}'")
        print(f"✓ Total de {len(arquivos_encontrados)} arquivo(s) encontrado(s)")
        
    except PermissionError:
        print(f"Erro: Sem permissão para acessar a pasta '{caminho_pasta}'")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def listar_com_detalhes(caminho_pasta, arquivo_saida='lista_detalhada.txt'):
    """
    Lista arquivos com informações detalhadas (tamanho, data de modificação)
    """
    
    try:
        if not os.path.exists(caminho_pasta):
            print(f"Erro: A pasta '{caminho_pasta}' não existe.")
            return
        
        arquivos_info = []
        
        # Coleta informações dos arquivos
        conteudo = os.listdir(caminho_pasta)
        for item in conteudo:
            caminho_completo = os.path.join(caminho_pasta, item)
            if os.path.isfile(caminho_completo):
                stats = os.stat(caminho_completo)
                tamanho = stats.st_size
                data_mod = datetime.fromtimestamp(stats.st_mtime)
                
                arquivos_info.append({
                    'nome': item,
                    'tamanho': tamanho,
                    'data_mod': data_mod
                })
        
        # Ordena por nome
        arquivos_info.sort(key=lambda x: x['nome'])
        
        # Escreve no arquivo com formatação
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"LISTA DETALHADA DE ARQUIVOS\n")
            f.write(f"Pasta: {os.path.abspath(caminho_pasta)}\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de arquivos: {len(arquivos_info)}\n")
            f.write("=" * 80 + "\n\n")
            
            if arquivos_info:
                # Cabeçalho da tabela
                f.write(f"{'Nº':<4} {'Nome do Arquivo':<40} {'Tamanho':<15} {'Última Modificação':<20}\n")
                f.write("-" * 80 + "\n")
                
                # Lista os arquivos
                total_tamanho = 0
                for i, info in enumerate(arquivos_info, 1):
                    tamanho_formatado = formatar_tamanho(info['tamanho'])
                    data_formatada = info['data_mod'].strftime('%d/%m/%Y %H:%M')
                    
                    # Trunca nome se for muito longo
                    nome = info['nome'][:37] + "..." if len(info['nome']) > 40 else info['nome']
                    
                    f.write(f"{i:<4} {nome:<40} {tamanho_formatado:<15} {data_formatada:<20}\n")
                    total_tamanho += info['tamanho']
                
                f.write("-" * 80 + "\n")
                f.write(f"Tamanho total: {formatar_tamanho(total_tamanho)}\n")
            else:
                f.write("Nenhum arquivo encontrado na pasta.\n")
        
        print(f"✓ Lista detalhada salva em '{arquivo_saida}'")
        print(f"✓ Total de {len(arquivos_info)} arquivo(s) encontrado(s)")
        
    except Exception as e:
        print(f"Erro: {e}")

def formatar_tamanho(bytes):
    """Converte bytes para formato legível (KB, MB, GB)"""
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unidade}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

# Exemplo de uso
if __name__ == "__main__":
    # Configurações
    pasta = input("Digite o caminho da pasta (ou pressione Enter para usar a pasta atual): ").strip()
    
    if not pasta:
        pasta = "."  # Pasta atual
    
    print("\nEscolha uma opção:")
    print("1. Lista simples (apenas nomes)")
    print("2. Lista com detalhes (tamanho, data)")
    print("3. Lista incluindo subpastas")
    
    opcao = input("\nOpção (1/2/3): ").strip()
    
    if opcao == "1":
        nome_arquivo = input("Nome do arquivo de saída (Enter para 'lista_arquivos.txt'): ").strip()
        if not nome_arquivo:
            nome_arquivo = "lista_arquivos.txt"
        listar_arquivos(pasta, nome_arquivo)
        
    elif opcao == "2":
        nome_arquivo = input("Nome do arquivo de saída (Enter para 'lista_detalhada.txt'): ").strip()
        if not nome_arquivo:
            nome_arquivo = "lista_detalhada.txt"
        listar_com_detalhes(pasta, nome_arquivo)
        
    elif opcao == "3":
        nome_arquivo = input("Nome do arquivo de saída (Enter para 'lista_arquivos.txt'): ").strip()
        if not nome_arquivo:
            nome_arquivo = "lista_arquivos.txt"
        listar_arquivos(pasta, nome_arquivo, incluir_subpastas=True)
        
    else:
        print("Opção inválida!")