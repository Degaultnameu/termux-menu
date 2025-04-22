#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input, Markdown
from textual.containers import ScrollableContainer, Vertical, Horizontal
from textual import on, work
from textual.reactive import reactive
from textual.css.query import DOMQuery
import subprocess
import time
import os

class TermuxMenu(App):
    """Menu Termux Simplificado com Funções Essenciais"""

    CSS = """
    Screen {
        /* align: center middle;  Incorrect.  Use align-items and justify-content on a container. */
        background: #121212;
        layout: vertical;  /* Add this to control layout */
        align-items: center; /* Center horizontally */
        justify-content: center; /* Center vertically */
    }
    #main {
        width: 90%;
        height: 90%;
        padding: 1;
        overflow-y: auto;
    }
    .btn {
        width: 100%;
        margin-top: 1; /* Explicit margins */
        margin-bottom: 1;
        background: #252525;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 5; /* Try integer padding */
    }
    .btn:hover {
        background: #333333;
    }
    #output {
        margin-top: 1;
        margin-bottom: 1;
        padding: 1;
        background: #1e1e1e;
        color: #f0f0f0;
        border-radius: 5px;
        font-family: "monospace"; /* Add quotes */
        font-size: 9; /* Try integer font size */
    }
    #enter_button { display: none; }
    #title {
        font-size: 20; /* Try integer font size */
        text-align: center;
        margin-bottom: 1;
        color: #00aaff;
    }
    #input {
        width: 100%;
        margin-top: 1;
        margin-bottom: 1;
        padding: 5; /* Try integer padding */
        background: #252525;
        color: white;
        border: none;
        border-radius: 5px;
    }
    #footer {
        width: 100%;
        text-align: center;
        color: #888888;
        font-size: 8; /* Try integer font size */
        margin-top: 1;
    }
    #loading {
        display: none;
        text-align: center;
        color: #00aaff;
        margin-bottom: 5; /* Try integer margin */
    }
    """

    welcome_msg = "Termux Premium - Digite um comando ou selecione uma opção"
    is_loading = reactive(False)

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="main"):
            with Vertical():
                yield Static("TERMUX PRO", id="title")
                yield Static("", id="loading")  # Placeholder for loading message
                yield Button("Terminal", id="terminal", classes="btn")
                yield Button("Atualizar Pacotes", id="update", classes="btn")
                yield Button("Limpar Tela", id="clear", classes="btn")
                yield Button("Listar Janelas", id="windows", classes="btn")
                yield Button("Configurações", id="config", classes="btn")
                yield Static(self.welcome_msg, id="output")
                yield Input(placeholder="Comando...", id="input")
                yield Button("Executar Comando", id="run_command", classes="btn")
                yield Button("Encerrar Sessões", id="enter_button", classes="btn")
                yield Button("Sair", id="exit", classes="btn")
                yield Static("Criado por IA", id="footer")

    def on_mount(self):
        self.query_one("#input").focus()

    def watch_is_loading(self, is_loading: bool) -> None:
        """Show or hide the loading indicator."""
        self.query_one("#loading").styles.display = "block" if is_loading else "none"
        self.query_one("#loading").update("Carregando...") if is_loading else self.query_one("#loading").update("")

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

    @on(Button.Pressed, "#run_command")
    def run_input_command(self):
        command = self.query_one("#input").value
        self.run_cmd(command, f"Comando '{command}' executado.")
        self.query_one("#input").value = ""

    @work(exclusive=True)  # Ensures only one command runs at a time
    async def run_cmd(self, cmd, success_msg):
        self.is_loading = True
        try:
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            output = result.stdout if result.returncode == 0 else result.stderr
            if not output:
                output = success_msg
            self.query_one("#output").update(output)
        except Exception as e:
            self.query_one("#output").update(f"Erro: {str(e)}")
        finally:
            self.is_loading = False

if __name__ == "__main__":
    TermuxMenu().run()
                
