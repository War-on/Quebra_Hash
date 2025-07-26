import hashlib
import multiprocessing as mp

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
    """Processa um chunk de palavras em paralelo"""
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

def executar_paralelismo(hash_alvo, detector, wordlist, num_processos):
    """Executa o processamento paralelo e retorna os resultados"""
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
        
        return palavra_encontrada, total_testes
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{wordlist}' não encontrado.")
    except Exception as e:
        raise Exception(f"Erro durante processamento paralelo: {e}")

def verificar_dependencias(detector):
    """Verifica se as dependências necessárias estão instaladas"""
    if detector == "BCRYPT" and not bcrypt:
        raise ImportError("Instale a biblioteca 'bcrypt' para suporte a bcrypt: pip install bcrypt")
    if detector == "ARGON2" and not PasswordHasher:
        raise ImportError("Instale a biblioteca 'argon2-cffi' para suporte a Argon2: pip install argon2-cffi")
    if detector == "SCRYPT" and not scrypt:
        raise ImportError("Instale a biblioteca 'scrypt' para suporte a scrypt: pip install scrypt") 