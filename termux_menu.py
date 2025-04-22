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
                yield Button("RESETAR CONFIG", id="reset", classes="btn")
                yield Button("FECHAR TODAS SESSÕES", id="close_sessions", classes="btn")
                yield Button("SAIR", id="exit", classes="btn")
                yield Static("", id="output")
                
                # Input com foco para alterar a frase
                self.text_input = Input(placeholder="Digite a nova frase", id="text_input")
                yield self.text_input
                yield Button("ALTERAR FRASE", id="change_text", classes="btn")
                yield Static("Texto Original: Welcome to Termux!", id="original_text")

                # Botão para dar o Enter
                yield Button("Simular ENTER", id="enter_button", classes="btn", disabled=True)

                # Garantir foco no Input
                self.text_input.focus()

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
        # Resetar a mensagem personalizada
        self.query_one("#original_text", Static).update("Texto Original: Welcome to Termux!")

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        """Lista janelas abertas"""
        self.run_command("termux-window -l", "Janelas listadas")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        """Edita configuração"""
        self.run_command("nano ~/.termux/termux.properties", "Editando config...")

    @on(Button.Pressed, "#reset")
    def reset_config(self):
        """Reseta a configuração"""
        self.run_command("rm ~/.termux/termux.properties", "Configuração resetada!")

    @on(Button.Pressed, "#close_sessions")
    def close_sessions(self):
        """Fecha todas as sessões"""
        self.query_one("#output", Static).update("Por favor, pressione Enter para fechar todas as sessões.")
        self.query_one("#enter_button", Button).disabled = False  # Habilita o botão de "Enter"
    
    @on(Button.Pressed, "#enter_button")
    def press_enter(self):
        """Simula pressionamento de Enter"""
        self.run_command("exit", "Sessões encerradas!")
        self.query_one("#output", Static).update("Todas as sessões foram fechadas.")
        self.query_one("#enter_button", Button).disabled = True  # Desabilita o botão após o uso

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
                
