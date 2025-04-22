#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input
from textual.containers import Center, Vertical
from textual import on
import subprocess
import os

class TermuxProMenu(App):
    """Menu Termux Premium com Funções Reais"""

    CSS = """
    Screen {
        align: center middle;
        background: #121212;
    }

    #main {
        width: 80%;
        border: double #333;
        padding: 2;
        background: #1e1e1e;
    }

    #title {
        text-align: center;
        color: #00ff9d;
        text-style: bold;
        margin-bottom: 2;
    }

    #output {
        margin-top: 2;
        min-height: 4;
        border: solid #333;
        padding: 1;
    }

    .btn {
        width: 100%;
        height: 3;
        margin: 1 0;
        background: #252525;
        color: white;
    }

    .btn:hover {
        background: #333;
    }
    """

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="main"):
                yield Static("RUSC521 TERMINAL", id="title")
                yield Button("TERMINAL", id="terminal", classes="btn")
                yield Button("ATUALIZAR PACOTES", id="update", classes="btn")
                yield Button("LIMPAR TELA", id="clear", classes="btn")
                yield Button("LISTAR JANELAS", id="windows", classes="btn")
                yield Button("EDITAR CONFIG", id="config", classes="btn")
                yield Button("FECHAR TODAS SESSÕES", id="close_sessions", classes="btn")
                yield Button("SAIR", id="exit", classes="btn")
                yield Static("", id="output")
                yield Input(placeholder="Digite algo...", id="user_input")
                yield Button("ENTER", id="enter_button", classes="btn")
                yield Button("ALTERAR FRASE", id="alter_phrase", classes="btn")

    @on(Button.Pressed, "#terminal")
    def open_terminal(self):
        """Abre novo terminal"""
        self.notify("Use Ctrl+C para voltar ao menu")
        self.query_one("#output", Static).update("Terminal ativo...")

    @on(Button.Pressed, "#update")
    def update_packages(self):
        """Atualiza pacotes"""
        self.run_command("pkg update && pkg upgrade -y", "Sistema atualizado!")

    @on(Button.Pressed, "#clear")
    def clear_screen(self):
        """Limpa a tela e exibe a mensagem padrão"""
        self.query_one("#output", Static).update("Welcome to Termux!\nDocs: https://termux.dev/docs\nDonate: https://termux.dev/donate\nCommunity: https://termux.dev/community\n\nWorking with packages:\n - Search:  pkg search <query>\n - Install: pkg install <package>\n - Upgrade: pkg upgrade\n\nSubscribing to additional repositories:\n - Root: pkg install root-repo\n - X11: pkg install x11-repo\n\nFor fixing any repository issues, try 'termux-change-repo' command.\n\nReport issues at https://termux.dev/issues")

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        """Lista janelas abertas"""
        self.run_command("termux-window -l", "Janelas listadas")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        """Edita configuração"""
        self.run_command("nano ~/.termux/termux.properties", "Editando config...")

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        """Sai do aplicativo"""
        self.exit()

    @on(Button.Pressed, "#close_sessions")
    def close_sessions(self):
        """Fecha todas as sessões"""
        self.query_one("#output", Static).update("Fechando todas as sessões... Pressione 'Enter' para continuar.")
        self.query_one("#enter_button", Button).show()

    @on(Button.Pressed, "#enter_button")
    def press_enter(self):
        """Simula pressionamento de 'Enter' para continuar o processo"""
        # Fecha todas as sessões com o comando kill
        self.run_command("ps -ef | grep 'bash' | grep -v 'grep' | awk '{print $2}' | xargs kill -9", "Todas as sessões foram fechadas!")

        # Atualiza o texto para indicar que as sessões foram fechadas
        self.query_one("#output", Static).update("Todas as sessões foram fechadas. Pressione 'Enter' para continuar.")

        # Esconde o botão de "Enter" após a ação
        self.query_one("#enter_button", Button).hide()

    @on(Button.Pressed, "#alter_phrase")
    def alter_phrase(self):
        """Altera a frase padrão"""
        input_text = self.query_one("#user_input", Input).value
        if input_text:
            self.query_one("#output", Static).update(input_text)
        else:
            self.query_one("#output", Static).update("Por favor, insira um texto válido para alterar.")

    def run_command(self, command: str, success_msg: str = ""):
        """Executa comandos no terminal"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            output = result.stdout or success_msg
            self.query_one("#output", Static).update(output)
        except subprocess.CalledProcessError as e:
            self.query_one("#output", Static).update(f"Erro: {e.stderr or 'Falha ao executar'}")
        except Exception as e:
            self.query_one("#output", Static).update(f"Erro inesperado: {str(e)}")

if __name__ == "__main__":
    TermuxProMenu().run()
    
