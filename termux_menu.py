#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static
from textual.containers import Vertical
from textual import on
from textual.reactive import reactive
import subprocess

class TermuxVIP(App):
    CSS = """
    Screen {
        align: center middle;
        background: #1e1e1e;  /* Cor de fundo mais suave */
    }

    #header {
        background: #007acc;  /* Azul mais suave */
        color: white;
        text-align: center;
        height: 3;
        padding: 1 0;
        border-radius: 5px;  /* Bordas arredondadas */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);  /* Sombra */
    }

    .btn {
        width: 80%;
        max-width: 30;
        margin: 1 0;
        content-align: center middle;
        border: solid #4caf50;  /* Verde mais suave */
        background: #2e7d32;  /* Fundo do botão */
        color: white;  /* Cor do texto */
        border-radius: 5px;  /* Bordas arredondadas */
        transition: background 0.3s;  /* Transição suave */
    }

    .btn:hover {
        background: #388e3c;  /* Cor do botão ao passar o mouse */
    }
    """

    is_loading = reactive(False)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("TERMUXVIP", id="header")
            yield Button("ALTERAR TERMUX", id="alterar", classes="btn")
            yield Button("VERIFICAR JANELAS", id="verificar", classes="btn")
            yield Button("ATUALIZAR E PACOTES INSTALADOS", id="atualizar", classes="btn")

    @on(Button.Pressed, "#alterar")
    def alterar_termux(self):
        self.run_cmd("nano $HOME/.termux/termux.properties", "Abrindo configuração do Termux...")

    @on(Button.Pressed, "#verificar")
    def verificar_janelas(self):
        self.run_cmd("termux-window -l", "Listando janelas abertas...")

    @on(Button.Pressed, "#atualizar")
    def atualizar_pacotes(self):
        self.run_cmd("pkg update && pkg upgrade -y", "Atualizando pacotes...")

    async def run_cmd(self, cmd, mensagem):
        self.is_loading = True
        try:
            result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
            output = result.stdout if result.returncode == 0 else result.stderr
            self.console.bell()
            self.notify(mensagem + "\n" + output)
        except Exception as e:
            self.notify(f"Erro: {str(e)}")
        finally:
            self.is_loading = False

if __name__ == "__main__":
    TermuxVIP().run()
