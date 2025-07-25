def detectar_tipo_hash(hash_str):
    import hashlib
    """
    Detecta o tipo de hash baseado no comprimento e formato da string.
    Suporta: MD5, SHA1, SHA224, SHA256, SHA384, SHA512.
    """
    hash_str = hash_str.strip().lower()
    tamanhos = {
        32: "MD5",
        40: "SHA1",
        56: "SHA224",
        64: "SHA256",
        96: "SHA384",
        128: "SHA512"
    }
    # Verifica se é hexadecimal
    if all(c in "0123456789abcdef" for c in hash_str):
        tipo = tamanhos.get(len(hash_str))
        if tipo == "MD5":
            return tipo
        elif tipo == "SHA1":
            return tipo
        elif tipo == "SHA224":
            return tipo
        elif tipo == "SHA256":
            return tipo
        elif tipo == "SHA384":
            return tipo
        elif tipo == "SHA512":
            return tipo
        else:
            return "Hash desconhecida ou não suportada"
    else:
        return "Formato inválido de hash"

# Exemplo de uso:
if __name__ == "__main__":
    hash_input = input("Digite o hash para detectar o tipo: ").strip()
    resultado = detectar_tipo_hash(hash_input)
    print(f"Tipo detectado: {resultado}")
