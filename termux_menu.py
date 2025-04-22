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

    #enter_button {
        width: 100%;
        height: 3;
        margin: 1 0;
        background: #006400;
        color: white;
    }

    #edit_button {
        width: 100%;
        height: 3;
        margin: 1 0;
        background: #800080;
        color: white;
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
                yield Button("FECHAR TODAS AS SESSÕES", id="close_sessions", classes="btn")
                yield Button("SAIR", id="exit", classes="btn")
                yield Static("", id="output")
                yield Input(placeholder="Digite a frase", id="edittext")
                yield Button("Alterar Frase", id="edit_button", classes="btn")
                yield Button("Pressione Enter para Confirmar", id="enter_button", classes="btn")
    
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
        """Edita configuração"""
        self.run_command("nano ~/.termux/termux.properties", "Editando config...")

    @on(Button.Pressed, "#close_sessions")
    def close_sessions(self):
        """Fecha todas as sessões ativas"""
        self.query_one("#output", Static).update("Por favor, pressione 'Enter' para confirmar...")

        # Adiciona o botão "Enter" para confirmar o fechamento
        self.query_one("#enter_button", Button).update("Pressione Enter para continuar")

    @on(Button.Pressed, "#enter_button")
    def press_enter(self):
        """Pressiona enter para encerrar as sessões"""
        # Encontrar os PIDs das sessões ativas
        pids = self.get_active_sessions()
        for pid in pids:
            self.kill_process(pid)

        # Após matar as sessões
        self.query_one("#output", Static).update(f"Sessões fechadas: {', '.join(pids)}")

    @on(Button.Pressed, "#edit_button")
    def edit_text(self):
        """Altera a frase"""
        new_text = self.query_one("#edittext", Input).value
        self.query_one("#output", Static).update(f"Texto Alterado: {new_text}")
    
    def get_active_sessions(self):
        """Obtém os PIDs das sessões ativas no Termux"""
        try:
            result = subprocess.run(
                "ps aux | grep 'bash' | awk '{print $2}'",
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            pids = result.stdout.splitlines()
            return pids
        except subprocess.CalledProcessError as e:
            self.query_one("#output", Static).update(f"Erro ao obter PIDs: {e.stderr}")
            return []

    def kill_process(self, pid):
        """Mata o processo com o PID fornecido"""
        try:
            subprocess.run(f"kill {pid}", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            self.query_one("#output", Static).update(f"Erro ao matar o processo {pid}: {e.stderr}")

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        """Sai do aplicativo"""
        self.exit()

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
        
