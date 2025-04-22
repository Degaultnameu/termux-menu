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
                yield Static("PANELA TERMINAL", id="title")
                yield Button("TERMINAL", id="terminal", classes="btn")
                yield Button("ATUALIZAR PACOTES", id="update", classes="btn")
                yield Button("LIMPAR TELA", id="clear", classes="btn")
                yield Button("LISTAR JANELAS", id="windows", classes="btn")
                yield Button("EDITAR CONFIG", id="config", classes="btn")
                yield Button("SAIR", id="exit", classes="btn")
                yield Static("", id="output")

                # Adicionando o campo de entrada para editar a mensagem
                yield Input(id="new_message", placeholder="Digite a nova mensagem de boas-vindas...")
                # Adicionando o botão "Salvar Config"
                yield Button("SALVAR CONFIG", id="save_config", classes="btn")

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
        """Limpa a tela"""
        self.query_one("#output", Static).update("")

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        """Lista janelas abertas"""
        self.run_command("termux-window -l", "Janelas listadas")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        """Edita a configuração de boas-vindas"""
        # Aqui você só quer abrir o campo de input
        self.query_one("#output", Static).update("Digite a nova mensagem de boas-vindas...")

    @on(Button.Pressed, "#save_config")
    def save_config(self):
        """Captura o texto do campo de entrada e salva no motd"""
        new_message = self.query_one("#new_message", Input).value
        if new_message:
            # Salva a nova mensagem no arquivo motd
            self.save_welcome_message(new_message)
        else:
            self.query_one("#output", Static).update("Por favor, insira uma nova mensagem.")

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        """Sai do aplicativo"""
        self.exit()

    def save_welcome_message(self, message: str):
        """Salva a nova mensagem no arquivo motd"""
        try:
            motd_file = "/data/data/com.termux/files/usr/etc/motd"
            with open(motd_file, "w") as file:
                file.write(message)
            self.query_one("#output", Static).update("Mensagem de boas-vindas atualizada com sucesso!")
        except PermissionError:
            self.query_one("#output", Static).update("Erro: Permissão negada ao tentar modificar o motd.")
        except Exception as e:
            self.query_one("#output", Static).update(f"Erro ao salvar a mensagem: {str(e)}")

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
    
