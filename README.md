# 🚀 Guia de Instalação Passo a Passo

## 🔌 Pré-requisitos
Verifique se você tem:
- Termux atualizado
- Armazenamento permitido

## 📦 Instalação Automática (Recomendado)
Execute este comando único:

```bash
curl -sL https://raw.githubusercontent.com/Degaultnameu/termux-menu/main/install.sh | bash

🛠️ Instalação Manual
1. Clonar o repositório
bash
git clone https://github.com/Degaultnameu/termux-menu.git ~/termux-menu
2. Acessar a pasta
bash
cd ~/termux-menu
3. Dar permissão de execução
bash
chmod +x install.sh
4. Executar instalação
bash
./install.sh
5. Reiniciar o Termux
bash
exit
🚑 Solução de Problemas
Se a pasta já existir:
bash
rm -rf ~/termux-menu
Depois repita o processo de instalação.

Se faltar permissões:
bash
termux-setup-storage
Atualizar pacotes:
bash
pkg update && pkg upgrade -y
🔥 Recursos Instalados
Menu automático ao abrir o Termux

Comando rápido turbo

Design profissional

Dica: Após instalar, feche e reabra o Termux para ativar!


### ✨ Melhorias desta versão:
1. **Blocos independentes** - Cada comando pode ser copiado separadamente
2. **Símbolos visuais** - Ícones para cada seção
3. **Espaçamento inteligente** - Facilita a leitura móvel
4. **Destaques** - Comandos críticos em caixas isoladas
5. **Solução rápida** - Seções de erro separadas
