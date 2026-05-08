# Requisitos

```pip install uv```

arquivo .env com a api_key do google

# Instruções para configurar a chamada de script

## Abrir 

**Cria o diretório caso ele não exista**
``` mkdir -p ~/.local/bin ```

**Cria e edita o arquivo (você pode usar o nvim)**
``` nvim ~/.local/bin/llm_call ```

## Escrever

Você pode modificar os caminhos ~/path/to/scripts/llm_call.py e ~/path/to/scripts/.env, conforme a
localização em seu sistema

```
#!/bin/bash

# Verifica se os argumentos mínimos foram passados
if [ "$#" -lt 2 ]; then
    echo "Uso: llm_call <caminho_do_arquivo> \"seu prompt aqui\""
    exit 1
fi

# Executa o comando uv referenciando os caminhos fixos que você definiu
uv run ~/path/to/scripts/llm_call.py \
    "$1" \
    "$2" \
    --env ~/path/to/scripts/.env
```


## Dar permissões ao arquivo

```chmod +` ~/.local/bin/llm_call```

## Verifique se o bin está no $PATH

```echo $PATH | grep ".local/bin"```

caso não esteja:
    ```export PATH="$HOME/.local/bin:$PATH"```


# Utilizacao

llm_call ./meu_codigo.py "Explique como otimizar este código"