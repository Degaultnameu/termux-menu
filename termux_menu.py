#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input
from textual.containers import Center, Vertical
from textual import on
import subprocess
import os
import signal

class TermuxProMenu(App):
    """Menu Termux Premium com Funções Reais"""

    CONFIG_FILE = os.path.expanduser("~/.termux/welcome_message.txt")
    DEFAULT_MESSAGE = """Welcome to Termux!

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
                yield Input(placeholder="Digite o texto para substituir...", id="custom_text")
                yield Button("SALVAR FRASE", id="save_phrase", classes="btn")
                yield Button("RESTAURAR FRASE ORIGINAL", id="reset_phrase", classes="btn")
                yield Button("ENCERRAR TODAS AS SESSÕES", id="kill_sessions", classes="btn")
                yield Button("SAIR", id="exit", classes="btn")
                yield Static("", id="output")

    @on(Button.Pressed, "#terminal")
    def open_terminal(self):
        self.notify("Use Ctrl+C para voltar ao menu")
        self.query_one("#output", Static).update("Terminal ativo...")

    @on(Button.Pressed, "#update")
    def update_packages(self):
        self.run_command("pkg update && pkg upgrade -y", "Sistema atualizado!")

    @on(Button.Pressed, "#clear")
    def clear_screen(self):
        self.query_one("#output", Static).update("")
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE) as f:
                frase = f.read()
        else:
            frase = self.DEFAULT_MESSAGE
        print(frase)

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        self.run_command("termux-window -l", "Janelas listadas")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        self.run_command(f"nano {self.CONFIG_FILE}", "Editando config...")

    @on(Button.Pressed, "#save_phrase")
    def save_phrase(self):
        input_text = self.query_one("#custom_text", Input).value
        if input_text.strip():
            os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
            with open(self.CONFIG_FILE, "w") as f:
                f.write(input_text.strip())
            self.query_one("#output", Static).update("Frase personalizada salva!")

    @on(Button.Pressed, "#reset_phrase")
    def reset_phrase(self):
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        with open(self.CONFIG_FILE, "w") as f:
            f.write(self.DEFAULT_MESSAGE)
        self.query_one("#output", Static).update("Frase restaurada para o padrão.")

    @on(Button.Pressed, "#kill_sessions")
    def kill_sessions(self):
        try:
            output = subprocess.check_output("ps aux | grep bash", shell=True, text=True)
            lines = output.splitlines()
            killed = 0
            for line in lines:
                if "/usr/bin/bash" in line:
                    parts = line.split()
                    pid = int(parts[1])
                    if pid != os.getpid():  # não mata a própria sessão
                        os.kill(pid, signal.SIGKILL)
                        killed += 1
            self.query_one("#output", Static).update(f"{killed} sessões encerradas.")
        except Exception as e:
            self.query_one("#output", Static).update(f"Erro ao encerrar sessões: {e}")

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        self.exit()

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
