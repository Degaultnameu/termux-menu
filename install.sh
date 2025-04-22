#!/bin/bash
# termux-menu/install.sh

# Cores para mensagens
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}[*] Instalando Termux Menu...${NC}"

# Instala dependências
echo -e "${GREEN}[*] Instalando Python e Git...${NC}"
pkg update -y && pkg install -y python git

echo -e "${GREEN}[*] Instalando biblioteca Textual...${NC}"
pip install textual --upgrade

# Clona o repositório (se não estiver instalando manualmente)
if [ ! -d ~/termux-menu ]; then
    echo -e "${GREEN}[*] Baixando termux-menu...${NC}"
    git clone https://github.com/Degaultnameu/termux-menu.git ~/termux-menu
fi

# Configura o .bashrc (apenas se não estiver configurado)
if ! grep -q "termux-menu" ~/.bashrc; then
    echo -e "${GREEN}[*] Configurando auto-start...${NC}"
    cat ~/termux-menu/.bashrc_snippet >> ~/.bashrc
fi

echo -e "${GREEN}[+] Instalação concluída!${NC}"
echo -e "${RED}⚠️ Feche e reabra o Termux para ativar o menu.${NC}"
