#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input
from textual.containers import ScrollableContainer, Vertical
from textual import on
import subprocess

class TermuxMenu(App):
    """Menu Termux Simplificado com Funções Essenciais"""

    CSS = """
    Screen {
        align: center middle;
        background: #121212;
    }
    #main {
        width: 90%;
        height: 90%;
        padding: 1;
        overflow-y: auto;
    }
    .btn {
        width: 100%;
        margin: 1 0;
        background: #252525;
    }
    #output {
        margin: 1 0;
        padding: 1;
        background: #1e1e1e;
    }
    #enter_button { display: none; }
    """

    welcome_msg = "Termux Premium - Digite um comando ou selecione uma opção"

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="main"):
            with Vertical():
                yield Static("TERMUX PRO", id="title")
                yield Button("Terminal", id="terminal", classes="btn")
                yield Button("Atualizar Pacotes", id="update", classes="btn")
                yield Button("Limpar Tela", id="clear", classes="btn")
                yield Button("Listar Janelas", id="windows", classes="btn")
                yield Button("Configurações", id="config", classes="btn")
                yield Static(self.welcome_msg, id="output")
                yield Input(placeholder="Comando...", id="input")
                yield Button("Encerrar Sessões", id="enter_button", classes="btn")
                yield Button("Sair", id="exit", classes="btn")

    def on_mount(self):
        self.query_one("#input").focus()

    # Funções principais
    @on(Button.Pressed, "#terminal")
    def show_terminal(self):
        self.query_one("#enter_button").styles.display = "block"
        self.query_one("#output").update("Terminal ativo - Digite comandos")

    @on(Button.Pressed, "#update")
    def update_packages(self):
        self.run_cmd("pkg update && pkg upgrade -y", "Pacotes atualizados!")

    @on(Button.Pressed, "#clear")
    def clear_output(self):
        self.query_one("#output").update(self.welcome_msg)

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        self.run_cmd("termux-window -l", "Janelas:")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        self.run_cmd("nano $HOME/.termux/termux.properties", "Editando config...")

    @on(Button.Pressed, "#enter_button")
    def kill_sessions(self):
        self.run_cmd("pkill -9 bash", "Sessões encerradas!")
        self.query_one("#enter_button").styles.display = "none"

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        self.exit()

    def run_cmd(self, cmd, success_msg):
        try:
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            output = result.stdout or success_msg
            self.query_one("#output").update(output)
        except Exception as e:
            self.query_one("#output").update(f"Erro: {str(e)}")

if __name__ == "__main__":
    TermuxMenu().run()
