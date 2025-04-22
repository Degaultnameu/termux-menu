#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input
from textual.containers import Center, VerticalScroll, Vertical
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
        color: white;
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

    Input {
        background: #333;
        color: white;
        border: solid #555;
    }
    """

    frase_padrao = """Welcome to Termux!

Docs:       https://termux.dev/docs
Donate:     https://termux.dev/donate
Community:  https://termux.dev/community

Working with packages:

 - Search:  pkg search <query>
 - Install: pkg install <package>
 - Upgrade: pkg upgrade

Subscribing to additional repositories:

 - Root:    pkg install root-repo
 - X11:     pkg install x11-repo

For fixing any repository issues,
try 'termux-change-repo' command.

Report issues at https://termux.dev/issues
"""

    def compose(self) -> ComposeResult:
        with Center():
            with VerticalScroll(id="main"):
                with Vertical():
                    yield Static("RUSC521 TERMINAL", id="title")
                    yield Button("TERMINAL", id="terminal", classes="btn")
                    yield Button("ATUALIZAR PACOTES", id="update", classes="btn")
                    yield Button("LIMPAR TELA", id="clear", classes="btn")
                    yield Button("LISTAR JANELAS", id="windows", classes="btn")
                    yield Button("EDITAR CONFIG", id="config", classes="btn")
                    yield Button("SAIR", id="exit", classes="btn")
                    yield Static("", id="output")
                    yield Input(placeholder="Digite algo...", id="user_input")
                    yield Button("ENCERRAR TODAS SESSÕES", id="enter_button", classes="btn")
                    yield Button("ALTERAR FRASE", id="alter_phrase", classes="btn")

    def on_mount(self):
        self.query_one("#output", Static).update(self.frase_padrao)
        self.query_one("#enter_button", Button).show()
        self.query_one("#user_input", Input).focus()  # Mostra o teclado ao iniciar

    @on(Button.Pressed, "#terminal")
    def open_terminal(self):
        self.notify("Use Ctrl+C para voltar ao menu")
        self.query_one("#output", Static).update("Terminal ativo...")

    @on(Button.Pressed, "#update")
    def update_packages(self):
        self.run_command("pkg update && pkg upgrade -y", "Sistema atualizado!")

    @on(Button.Pressed, "#clear")
    def clear_screen(self):
        self.query_one("#output", Static).update(self.frase_padrao)

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        self.run_command("termux-window -l", "Janelas listadas")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        self.run_command("nano ~/.termux/termux.properties", "Editando config...")

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        self.exit()

    @on(Button.Pressed, "#enter_button")
    def press_enter(self):
        self.run_command("ps -ef | grep 'bash' | grep -v 'grep' | awk '{print $2}' | xargs kill -9", "Todas as sessões foram fechadas!")
        self.query_one("#output", Static).update("Sessões encerradas automaticamente.")
        self.query_one("#user_input", Input).focus()

    @on(Button.Pressed, "#alter_phrase")
    def alter_phrase(self):
        input_text = self.query_one("#user_input", Input).value
        if input_text:
            self.frase_padrao = input_text
            self.query_one("#output", Static).update(self.frase_padrao)
        else:
            self.query_one("#output", Static).update("Digite um texto válido para alterar a mensagem inicial.")

    def run_command(self, command: str, success_msg: str = ""):
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
    
