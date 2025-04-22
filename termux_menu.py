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
                yield Button("SAIR", id="exit", classes="btn")
                yield Static("", id="output")
                yield Input(placeholder="Digite algo...", id="user_input")
                yield Button("ENCERRAR TODAS SESSÕES", id="enter_button", classes="btn")
                yield Button("ALTERAR FRASE", id="alter_phrase", classes="btn")
                yield Button("SALVAR COMO MOTD", id="save_motd", classes="btn")

    @on(Button.Pressed, "#terminal")
    def open_terminal(self):
        self.notify("Use Ctrl+C para voltar ao menu")
        self.query_one("#output", Static).update("Terminal ativo...")

    @on(Button.Pressed, "#update")
    def update_packages(self):
        self.run_command("pkg update && pkg upgrade -y", "Sistema atualizado!")

    @on(Button.Pressed, "#clear")
    def clear_screen(self):
        self.query_one("#output", Static).update(
            "Welcome to Termux!\nDocs: https://termux.dev/docs\nDonate: https://termux.dev/donate\nCommunity: https://termux.dev/community\n\n"
            "Working with packages:\n - Search:  pkg search <query>\n - Install: pkg install <package>\n - Upgrade: pkg upgrade\n\n"
            "Subscribing to additional repositories:\n - Root: pkg install root-repo\n - X11: pkg install x11-repo\n\n"
            "For fixing any repository issues, try 'termux-change-repo' command.\n\nReport issues at https://termux.dev/issues"
        )

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
        self.query_one("#output", Static).update("Todas as sessões foram fechadas. Pressione 'Enter' para continuar.")

    @on(Button.Pressed, "#alter_phrase")
    def alter_phrase(self):
        input_text = self.query_one("#user_input", Input).value
        if input_text:
            self.query_one("#output", Static).update(input_text)
        else:
            self.query_one("#output", Static).update("Por favor, insira um texto válido para alterar.")

    @on(Button.Pressed, "#save_motd")
    def save_motd(self):
        text = self.query_one("#user_input", Input).value
        if text:
            os.makedirs(os.path.expanduser("~/.termux"), exist_ok=True)
            motd_path = os.path.expanduser("~/.termux/motd")
            with open(motd_path, "w") as f:
                f.write(text + "\n")

            # Garante que o Termux mostre o motd
            properties_path = os.path.expanduser("~/.termux/termux.properties")
            with open(properties_path, "w") as prop:
                prop.write("hide-motd=false\n")

            subprocess.run("termux-reload-settings", shell=True)
            self.query_one("#output", Static).update("MOTD salvo com sucesso!")
        else:
            self.query_one("#output", Static).update("Digite algo para salvar como MOTD.")

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
    
