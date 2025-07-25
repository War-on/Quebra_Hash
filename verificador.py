import argparse
import hashlib
import sys
import time
from hash_detector import detectar_tipo_hash

coint = 0
# Argumentos de linha de comando
parser = argparse.ArgumentParser(description='Verificador de hash SHA256 para wordlist.')
parser.add_argument('-H', '--hash', required=True, help='Hash SHA256 alvo')
parser.add_argument('-W', '--wordlist', required=True, help='Arquivo de wordlist')
args = parser.parse_args()

hash_alvo = args.hash
wordlist = args.wordlist

detector = detectar_tipo_hash(hash_alvo)
print(f'Tipo de hash detectado: {detector}')
hash_func = getattr(hashlib, detector.lower())

start_time = time.time()
try:
    with open(wordlist, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            coint += 1
            print(f'\rTestando: \033[33m{line}\033[0m', end=' ')
            sys.stdout.flush()

            hash_digest = hash_func(line.encode()).hexdigest()

            if hash_digest == hash_alvo:
                tempo = time.time() - start_time
                print('\n' + '╔' + '═'*28 + '╗')
                print(f'║{"RESULTADO":^28}║')
                print('╠' + '═'*28 + '╣')
                print(f'║ Valor encontrado:')
                print(f'║ \033[32m{line}\033[0m')
                print('╠' + '═'*28 + '╣')
                print(f'║ Total de testes: {coint:<8}')
                print(f'║ Tempo: {tempo:.2f} segundos')
                print('╚' + '═'*28 + '╝')
                break
        else:
            tempo = time.time() - start_time
            print('\n' + '╔' + '═'*28 + '╗')
            print(f'║{"RESULTADO":^28}║')
            print('╠' + '═'*28 + '╣')
            print(f'║    \033[31mValor NÃO encontrado\033[0m    ║')
            print('╠' + '═'*28 + '╣')
            print(f'║ Total de testes: {coint:<8}')
            print(f'║ Tempo: {tempo:.2f} segundos')
            print('╚' + '═'*28 + '╝')
except FileNotFoundError:
    print(f"Arquivo '{wordlist}' não encontrado.")