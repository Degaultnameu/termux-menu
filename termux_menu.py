#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input
from textual.containers import ScrollableContainer, Vertical
from textual import on
import subprocess

class TermuxProMenu(App):
    """Menu Termux Premium com Scroll Suave"""

    CSS = """
    Screen {
        align: center middle;
        background: #121212;
        overflow: hidden;
    }

    #scroll_container {
        width: 80%;
        height: 90%;
        border: double #333;
        background: #1e1e1e;
        scrollbar-color: #555 #1e1e1e;
    }

    #title {
        text-align: center;
        color: #00ff9d;
        text-style: bold;
        margin-bottom: 2;
    }

    #output {
        margin: 2 0;
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
        margin-bottom: 1;
    }

    #enter_button {
        display: none;  /* Oculta o botão inicialmente */
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
"""

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="scroll_container"):
            with Vertical():
                yield Static("TERMUX PRO MENU", id="title")
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
        self.query_one("#user_input", Input).focus()

    @on(Button.Pressed, "#terminal")
    def terminal_pressed(self):
        self.query_one("#enter_button").styles.display = "block"  # Mostra o botão
        self.query_one("#output", Static).update("Terminal ativo. Pressione o botão abaixo para encerrar sessões.")

    @on(Button.Pressed, "#enter_button")
    def kill_sessions(self):
        self.run_command("pkill -9 bash", "Todas as sessões bash foram encerradas!")
        self.query_one("#enter_button").styles.display = "none"  # Oculta novamente

    @on(Button.Pressed, "#update")
    def update_packages(self):
        self.run_command("pkg update && pkg upgrade -y", "Pacotes atualizados!")

    @on(Button.Pressed, "#clear")
    def clear_screen(self):
        self.query_one("#output", Static).update(self.frase_padrao)

    @on(Button.Pressed, "#alter_phrase")
    def change_phrase(self):
        new_text = self.query_one("#user_input", Input).value
        if new_text:
            self.frase_padrao = new_text
            self.query_one("#output", Static).update(new_text)

    def run_command(self, command, success_msg):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout if result.stdout else success_msg
            self.query_one("#output", Static).update(output)
        except Exception as e:
            self.query_one("#output", Static).update(f"Erro: {str(e)}")

if __name__ == "__main__":
    TermuxProMenu().run()
