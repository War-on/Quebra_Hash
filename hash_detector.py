import re
import hashlib

def detectar_tipo_hash(hash_str):
    """
    Detecta o tipo de hash baseado no comprimento, formato e prefixo da string.
    Suporta: MD5, SHA1, SHA224, SHA256, SHA384, SHA512, bcrypt, scrypt, Argon2.
    """
    hash_str = hash_str.strip()
    hash_str_lower = hash_str.lower()
    tamanhos = {
        32: "MD5",
        40: "SHA1",
        56: "SHA224",
        64: "SHA256",
        96: "SHA384",
        128: "SHA512"
    }
    # Detectar bcrypt
    if hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
        return "BCRYPT"
    # Detectar scrypt (padrão do passlib)
    if hash_str.startswith("$scrypt$"):
        return "SCRYPT"
    # Detectar Argon2 (padrão do argon2-cffi)
    if hash_str.startswith("$argon2i$") or hash_str.startswith("$argon2d$") or hash_str.startswith("$argon2id$"):
        return "ARGON2"
    # Verifica se é hexadecimal
    if all(c in "0123456789abcdef" for c in hash_str_lower):
        tipo = tamanhos.get(len(hash_str_lower))
        if tipo:
            return tipo
        else:
            return "Hash desconhecida ou não suportada"
            exit()
    return "Formato inválido de hash"
    exit()

# Exemplo de uso:
if __name__ == "__main__":
    hash_input = input("Digite o hash para detectar o tipo: ").strip()
    resultado = detectar_tipo_hash(hash_input)
    print(f"Tipo detectado: {resultado}")
    
