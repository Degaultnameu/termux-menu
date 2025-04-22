#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input
from textual.containers import Center, Vertical
from textual import on
import subprocess
import os

CONFIG_FILE = "/data/data/com.termux/files/home/.termuxmotd"

TEXTO_PADRAO = """Welcome to Termux!

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

class TermuxProMenu(App):
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
                yield Button("SALVAR CONFIG", id="salvar", classes="btn")
                yield Button("RESET CONFIG", id="reset", classes="btn")
                yield Button("DELETAR SESSÕES", id="deletar_sessoes", classes="btn")
                yield Button("SAIR", id="exit", classes="btn")
                yield Input(placeholder="Digite novo texto", id="edit_input")
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
        self.query_one("#output", Static).update(self.get_motd())

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        self.run_command("termux-window -l", "Janelas listadas")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        self.query_one("#output", Static).update("Digite novo texto no campo abaixo e clique em SALVAR CONFIG.")

    @on(Button.Pressed, "#salvar")
    def salvar_config(self):
        novo_texto = self.query_one("#edit_input", Input).value
        if novo_texto.strip():
            with open(CONFIG_FILE, "w") as f:
                f.write(novo_texto)
            self.query_one("#output", Static).update("Configuração salva!")
        else:
            self.query_one("#output", Static).update("Campo vazio. Nada foi salvo.")

    @on(Button.Pressed, "#reset")
    def reset_config(self):
        with open(CONFIG_FILE, "w") as f:
            f.write(TEXTO_PADRAO)
        subprocess.run("rm -rf $PREFIX/var/cache/*", shell=True)
        self.query_one("#output", Static).update("Configuração restaurada e cache limpo!")

    @on(Button.Pressed, "#deletar_sessoes")
    def deletar_sessoes(self):
        bash_pids = subprocess.check_output("ps aux | grep bash | grep -v grep | awk '{print $2}'", shell=True, text=True).splitlines()
        for pid in bash_pids:
            subprocess.run(f"kill -9 {pid}", shell=True)
        self.query_one("#output", Static).update(f"Sessões encerradas: {', '.join(bash_pids)}")

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        self.exit()

    def run_command(self, command: str, success_msg: str = ""):
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            output = result.stdout or success_msg
            self.query_one("#output", Static).update(output)
        except subprocess.CalledProcessError as e:
            self.query_one("#output", Static).update(f"Erro: {e.stderr or 'Falha ao executar'}")
        except Exception as e:
            self.query_one("#output", Static).update(f"Erro inesperado: {str(e)}")

    def get_motd(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                return f.read()
        return TEXTO_PADRAO

if __name__ == "__main__":
    TermuxProMenu().run()
    
