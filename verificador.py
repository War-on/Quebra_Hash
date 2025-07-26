import argparse
import hashlib
import sys
import time
import multiprocessing as mp
from hash_detector import detectar_tipo_hash

# Novas libs para hashes seguros
try:
    import bcrypt
except ImportError:
    bcrypt = None
try:
    from argon2 import PasswordHasher
except ImportError:
    PasswordHasher = None
try:
    import scrypt
except ImportError:
    scrypt = None

def processar_chunk(chunk_data):
    hash_alvo, detector, chunk = chunk_data
    total_testes = 0
    for palavra in chunk:
        palavra = palavra.strip()
        total_testes += 1
        # Mostra a palavra testada apenas a cada 5000 testes para não sobrecarregar
        if total_testes % 5000 == 0:
            print(f'\rTestando: \033[33m{palavra}\033[0m', end='', flush=True)
        if detector == "BCRYPT":
            if not bcrypt:
                continue
            try:
                if bcrypt.checkpw(palavra.encode(), hash_alvo.encode()):
                    return (True, palavra, total_testes)
            except Exception:
                continue
        elif detector == "SCRYPT":
            if not scrypt:
                continue
            try:
                # scrypt.hash retorna bytes, então comparar com hash alvo em bytes
                hash_bytes = scrypt.hash(palavra, salt=b"salt", N=16384, r=8, p=1)
                if hash_bytes.hex() == hash_alvo:
                    return (True, palavra, total_testes)
            except Exception:
                continue
        elif detector == "ARGON2":
            if not PasswordHasher:
                continue
            ph = PasswordHasher()
            try:
                ph.verify(hash_alvo, palavra)
                return (True, palavra, total_testes)
            except Exception:
                continue
        else:
            # Hashes clássicos
            try:
                hash_func = getattr(hashlib, detector.lower())
                hash_digest = hash_func(palavra.encode()).hexdigest()
                if hash_digest == hash_alvo:
                    return (True, palavra, total_testes)
            except Exception:
                continue
    return (False, None, total_testes)

def dividir_wordlist(wordlist_path, num_processos):
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
    parser = argparse.ArgumentParser(description='Verificador de hash seguro e realista para wordlist.')
    parser.add_argument('-H', '--hash', required=True, help='Hash alvo')
    parser.add_argument('-W', '--wordlist', required=True, help='Arquivo de wordlist')
    parser.add_argument('-P', '--processos', type=int, default=mp.cpu_count(), help='Número de processos (padrão: número de CPUs)')
    args = parser.parse_args()

    hash_alvo = args.hash
    wordlist = args.wordlist
    num_processos = args.processos

    detector = detectar_tipo_hash(hash_alvo)
    print(f'Tipo de hash detectado: {detector}')
    print(f'Usando {num_processos} processos')

    if detector == "BCRYPT" and not bcrypt:
        print("[ERRO] Instale a biblioteca 'bcrypt' para suporte a bcrypt: pip install bcrypt")
        sys.exit(1)
    if detector == "ARGON2" and not PasswordHasher:
        print("[ERRO] Instale a biblioteca 'argon2-cffi' para suporte a Argon2: pip install argon2-cffi")
        sys.exit(1)
    if detector == "SCRYPT" and not scrypt:
        print("[ERRO] Instale a biblioteca 'scrypt' para suporte a scrypt: pip install scrypt")
        sys.exit(1)

    start_time = time.time()
    try:
        chunks = dividir_wordlist(wordlist, num_processos)
        dados_processos = [(hash_alvo, detector, chunk) for chunk in chunks]
        with mp.Pool(processes=num_processos) as pool:
            resultados = pool.map(processar_chunk, dados_processos)
        total_testes = 0
        palavra_encontrada = None
        for sucesso, palavra, testes in resultados:
            total_testes += testes
            if sucesso:
                palavra_encontrada = palavra
                break
        tempo = time.time() - start_time
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
