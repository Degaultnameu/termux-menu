# 🚀 Termux Menu - Menu Interativo Premium para Termux

![Termux](https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=termux&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Textual](https://img.shields.io/badge/Textual-5C4EE5?style=for-the-badge)

**O menu definitivo para turbinar seu Termux!** Uma interface elegante e funcional criada com Python + Textual, oferecendo atalhos essenciais para seu dia a dia no terminal Android.

## ✨ Recursos
✔️ **Acesso rápido** a funções essenciais do Termux  
✔️ **Interface intuitiva** com design moderno  
✔️ **Configuração automática** ao iniciar o terminal  
✔️ **Sistema de aliases** para comandos personalizados  
✔️ **Totalmente customizável** - edite conforme sua necessidade  

## 📥 Instalação Rápida
1. Clone o repositório:
```bash
git clone https://github.com/Degaultnameu/termux-menu.git
cd termux-menu
pkg install python -y
pip install textual

2. Instale as dependências:

bash
pkg install python -y
pip install textual
Execute:

bash
python3 termux_menu.py
⚙️ Configuração Avançada
Para iniciar automaticamente ao abrir o Termux, edite seu .bashrc:

echo -e '\n# Auto-start Termux Menu\nif [ -n "$PS1" ]; then\n    python3 ~/termux-menu/termux_menu.py || true\nfi' >> ~/.bashrc
source ~/.bashrc



🎨 Screenshot
Menu Preview

🤝 Contribuição
Contribuições são bem-vindas! Siga estes passos:

Faça um Fork

Crie sua branch (git checkout -b feature/incrivel)

Commit suas mudanças (git commit -m 'Adiciona feature incrível')

Push para a branch (git push origin feature/incrivel)

Abra um Pull Request

📜 Licença


### 🔍 Destaques:
1. **Badges profissionais** - Mostra as tecnologias usadas
2. **Emojis organizados** - Melhora a visualização
3. **Seções claras** - Instalação básica vs avançada
4. **Chamada para contribuição** - Padrão GitHub
5. **Espaço para screenshot** - Basta substituir o placeholder

### 💡 Dica extra:
Adicione um arquivo `screenshot.png` real do seu menu no projeto e atualize o link no README para ficar ainda mais profissional!

Quer que eu ajuste algo específico na descrição? 😊
