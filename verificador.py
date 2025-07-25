import argparse
import hashlib
import sys
import time
import multiprocessing as mp
from itertools import islice
from hash_detector import detectar_tipo_hash

def processar_chunk(chunk_data):
    """Processa um chunk de palavras em paralelo"""
    hash_alvo, detector, chunk = chunk_data
    hash_func = getattr(hashlib, detector.lower())
    
    for i, palavra in enumerate(chunk):
        palavra = palavra.strip()
        hash_digest = hash_func(palavra.encode()).hexdigest()
        
        if hash_digest == hash_alvo:
            return (True, palavra, i + 1)
    
    return (False, None, len(chunk))

def dividir_wordlist(wordlist_path, num_processos):
    """Divide a wordlist em chunks para processamento paralelo"""
    with open(wordlist_path, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    
    tamanho_chunk = len(linhas) // num_processos
    chunks = []
    
    for i in range(num_processos):
        inicio = i * tamanho_chunk
        fim = inicio + tamanho_chunk if i < num_processos - 1 else len(linhas)
        chunks.append(linhas[inicio:fim])
    
    return chunks

def main():
    parser = argparse.ArgumentParser(description='Verificador de hash paralelo para wordlist.')
    parser.add_argument('-H', '--hash', required=True, help='Hash alvo')
    parser.add_argument('-W', '--wordlist', required=True, help='Arquivo de wordlist')
    parser.add_argument('-P', '--processos', type=int, default=mp.cpu_count(), 
                       help='Número de processos (padrão: número de CPUs)')
    args = parser.parse_args()

    hash_alvo = args.hash
    wordlist = args.wordlist
    num_processos = args.processos

    detector = detectar_tipo_hash(hash_alvo)
    print(f'Tipo de hash detectado: {detector}')
    print(f'Usando {num_processos} processos')

    start_time = time.time()
    
    try:
        # Dividir wordlist em chunks
        chunks = dividir_wordlist(wordlist, num_processos)
        
        # Preparar dados para cada processo
        dados_processos = [(hash_alvo, detector, chunk) for chunk in chunks]
        
        # Executar em paralelo
        with mp.Pool(processes=num_processos) as pool:
            resultados = pool.map(processar_chunk, dados_processos)
        
        # Verificar resultados
        total_testes = 0
        palavra_encontrada = None
        
        for sucesso, palavra, testes in resultados:
            total_testes += testes
            if sucesso:
                palavra_encontrada = palavra
                break
        
        tempo = time.time() - start_time
        
        # Exibir resultado
        print('\n' + '╔' + '═'*28 + '╗')
        print(f'║{"RESULTADO":^28}║')
        print('╠' + '═'*28 + '╣')
        
        if palavra_encontrada:
            print(f'║ Valor encontrado:')
            print(f'║ \033[32m{palavra_encontrada}\033[0m')
        else:
            print(f'║    \033[31mValor NÃO encontrado\033[0m    ║')
        
        print('╠' + '═'*28 + '╣')
        print(f'║ Total de testes: {total_testes:<8}')
        print(f'║ Tempo: {tempo:.2f} segundos')
        print(f'║ Velocidade: {total_testes/tempo:.0f} hash/s')
        print('╚' + '═'*28 + '╝')
        
    except FileNotFoundError:
        print(f"Arquivo '{wordlist}' não encontrado.")

if __name__ == '__main__':
    main()
