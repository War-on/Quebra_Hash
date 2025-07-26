import argparse
import sys
import time
import multiprocessing as mp
from hash_detector import detectar_tipo_hash
from paralelismo import executar_paralelismo, verificar_dependencias

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
    
    # Verifica se o formato do hash é inválido
    if detector == "Formato inválido de hash":
        print("[ERRO] Formato inválido de hash") 
        sys.exit(1)
    
    # Verifica se o hash é desconhecido ou não suportado
    if detector == "Hash desconhecida ou não suportada":
        print("[ERRO] Hash desconhecida ou não suportada")
        sys.exit(1)
    
    print(f'Usando {num_processos} processos')

    # Verifica dependências
    try:
        verificar_dependencias(detector)
    except ImportError as e:
        print(f"[ERRO] {e}")
        sys.exit(1)

    start_time = time.time()
    
    try:
        # Executa o processamento paralelo
        palavra_encontrada, total_testes = executar_paralelismo(hash_alvo, detector, wordlist, num_processos)
        
        tempo = time.time() - start_time
        
        # Exibe resultado
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
        
    except FileNotFoundError as e:
        print(f"[ERRO] {e}")
    except Exception as e:
        print(f"[ERRO] {e}")

if __name__ == '__main__':
    main()
