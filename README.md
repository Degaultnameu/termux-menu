markdown
# 📲 Guia de Instalação do Termux Menu

## Pré-requisitos
- Termux atualizado
- Conexão com internet

## 🔧 Instalação Automática (Recomendado)
```bash
curl -sL https://raw.githubusercontent.com/Degaultnameu/termux-menu/main/install.sh | bash
📚 Instalação Manual (Passo a Passo)
1. Clonar o Repositório
bash
git clone https://github.com/Degaultnameu/termux-menu.git ~/termux-menu
cd ~/termux-menu
2. Tornar o Instalador Executável
bash
chmod +x install.sh
3. Executar a Instalação
bash
./install.sh
4. Reiniciar o Termux
bash
exit
🛠 Solução de Problemas
Pasta já existe?
bash
rm -rf ~/termux-menu  # Remove a pasta existente
git clone https://github.com/Degaultnameu/termux-menu.git ~/termux-menu
Erros de permissão?
bash
termux-setup-storage
pkg update && pkg upgrade -y
🌟 Recursos Instalados
Menu automático ao iniciar

Atalho turbo para comandos rápidos

Interface profissional com Textual

▶️ Ver Demonstração <!-- Adicione link para gif/screenshot -->


### 💡 Dicas para o README:
1. **Adicione um gif** mostrando a instalação e uso (use [Kap](https://getkap.co/) ou ScreenToGif)
2. **Inclua badges** no topo:
   ```markdown
   ![GitHub stars](https://img.shields.io/github/stars/Degaultnameu/termux-menu?style=social)
   ![License](https://img.shields.io/badge/license-MIT-blue)
Seção "Contribuição":

markdown
## 🤝 Como Contribuir
1. Faça um Fork
2. Crie sua branch (`git checkout -b feature/nova-funcao`)
3. Commit suas mudanças (`git commit -m 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-funcao`)
5. Abra um Pull Request
Quer que eu gere um arquivo README.md completo para você colar no repositório? 😊

New chat
Message DeepSeek
