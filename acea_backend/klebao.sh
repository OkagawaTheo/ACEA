#!/bin/bash

USUARIO_WINDOWS="User" 

ARQUIVO="/mnt/c/Users/$USUARIO_WINDOWS/Documents/leitura.txt"

if [ ! -f "$ARQUIVO" ]; then
    echo "ERRO: O arquivo '$ARQUIVO' não existe!"
    exit 1
fi

read -p "Informe o horário para leitura (HH:MM): " HORARIO

if ! [[ "$HORARIO" =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
    echo "ERRO: Formato de horário inválido. Use HH:MM (ex: 14:30)."
    exit 1
fi

echo "Leitura agendada para $HORARIO. Aguardando..."
sleep 1

while true; do
    AGORA=$(date +%H:%M)
    
    if [[ "$AGORA" == "$HORARIO" ]]; then
        clear
        echo "==============================="
        echo "Iniciando leitura automática:"
        echo "$ARQUIVO"
        echo "==============================="
        
        cat "$ARQUIVO"
        
        echo "==============================="
        echo "Leitura concluída às $(date +%H:%M:%S)"
        
        if command -v notify-send >/dev/null 2>&1; then 
            notify-send "Leitura Automática" "Arquivo '$ARQUIVO' foi lido às $HORARIO"
        fi 
        
        break 
    fi
    
    sleep 2
done