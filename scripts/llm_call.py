import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# /// script
# dependencies = [
#   "python-dotenv",
#   "google-generativeai",
# ]
# ///

def get_next_log_path(directory="help", base_name="log", extension=".md"):
    """
    Verifica no diretório especificado se já existem arquivos log1, log2, etc.,
    e retorna o próximo nome disponível dentro desse diretório.
    Cria o diretório se ele não existir.
    """
    log_dir = Path(directory)
    log_dir.mkdir(parents=True, exist_ok=True) # Garante que o diretório 'help' exista

    i = 1
    while True:
        path = log_dir / f"{base_name}{i}{extension}"
        if not path.exists():
            return path
        i += 1

def main():
    parser = argparse.ArgumentParser(
        description="Agente Engenheiro de IA - CLI Gemini Tool"
    )
    
    # Argumentos obrigatórios via CLI
    parser.add_argument("file_path", type=str, help="Caminho do arquivo a ser lido")
    parser.add_argument("user_prompt", type=str, help="O prompt/instrução para o agente")
    
    # Argumento para o caminho do .env (conforme solicitado)
    parser.add_argument(
        "--env", 
        type=str, 
        required=True, 
        help="Caminho para o arquivo .env contendo a GEMINI_API_KEY"
    )
    
    args = parser.parse_args()

    # 1. Carregar a API Key do .env especificado
    env_path = Path(args.env).expanduser().resolve()
    if not env_path.exists():
        print(f"Erro: Arquivo .env não encontrado em: {env_path}")
        return

    load_dotenv(dotenv_path=env_path)
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Erro: Variável GEMINI_API_KEY não encontrada no arquivo .env")
        return

    # 2. Configuração do Agente Gemini
    genai.configure(api_key=api_key)
    
    # Definindo o comportamento como Engenheiro de IA
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=(
            "Você é um Engenheiro de IA sênior e especialista em sistemas distribuídos e Machine Learning. "
            "Sua tarefa é analisar o conteúdo fornecido e responder de forma técnica, objetiva e otimizada."
        )
    )

    # 3. Leitura do arquivo de entrada
    input_path = Path(args.file_path).expanduser().resolve()
    if not input_path.exists():
        print(f"Erro: Arquivo de entrada não encontrado: {input_path}")
        return

    try:
        file_content = input_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # 4. Construção do Prompt e Chamada da API
    full_prompt = (
        f"CONTEÚDO DO ARQUIVO:\n---\n{file_content}\n---\n\n"
        f"INSTRUÇÃO: {args.user_prompt}"
    )
    
    print("Gerando resposta...")
    try:
        response = model.generate_content(full_prompt)
        output_text = response.text
    except Exception as e:
        print(f"Erro na API do Gemini: {e}")
        return

    # 5. Salvar Log incremental no diretório "help" com extensão ".md"
    log_file = get_next_log_path(directory="help", extension=".md")
    try:
        log_file.write_text(output_text, encoding="utf-8")
        print(f"✔ Sucesso! Resposta salva em: {log_file.absolute()}")
    except Exception as e:
        print(f"Erro ao salvar o log: {e}")

if __name__ == "__main__":
    main()