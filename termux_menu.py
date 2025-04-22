#!/usr/bin/env python3
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input
from textual.containers import ScrollableContainer, Vertical
from textual import on
import subprocess
import os

class TermuxProMenu(App):
    """Menu Termux Premium Completo com Scroll Funcional"""

    CSS = """
    Screen {
        align: center middle;
        background: #121212;
        overflow: hidden;
    }

    #scrollable {
        width: 90%;
        height: 90%;
        border: double #333;
        padding: 1;
        background: #1e1e1e;
        overflow-y: scroll;
        scrollbar-color: #555 #1e1e1e;
    }

    #title {
        text-align: center;
        color: #00ff9d;
        text-style: bold;
        margin-bottom: 1;
        padding-bottom: 1;
        border-bottom: solid #333;
    }

    #output {
        margin: 1 0;
        min-height: 4;
        border: solid #333;
        padding: 1;
        color: white;
        background: #252525;
    }

    .btn {
        width: 100%;
        height: 3;
        margin: 1 0;
        background: #252525;
        color: white;
        border: none;
    }

    .btn:hover {
        background: #333;
    }

    Input {
        width: 100%;
        margin: 1 0;
        padding: 1;
        background: #333;
        color: white;
        border: solid #555;
    }

    #enter_button {
        display: none;
    }

    /* Efeitos especiais para os botões */
    .btn:focus {
        outline: 2px solid #00ff9d;
    }

    /* Barra de scroll personalizada */
    #scrollable::-webkit-scrollbar {
        width: 8px;
    }

    #scrollable::-webkit-scrollbar-thumb {
        background-color: #555;
        border-radius: 4px;
    }

    #scrollable::-webkit-scrollbar-track {
        background-color: #1e1e1e;
    }
    """

    frase_padrao = """Welcome to Termux Premium!

███╗   ██╗███████╗███╗   ███╗
████╗  ██║██╔════╝████╗ ████║
██╔██╗ ██║█████╗  ██╔████╔██║
██║╚██╗██║██╔══╝  ██║╚██╔╝██║
██║ ╚████║███████╗██║ ╚═╝ ██║
╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝

[+] Comunidade: termux.dev/community
[+] Documentação: termux.dev/docs

Comandos úteis:
• pkg update && pkg upgrade
• termux-change-repo
• termux-setup-storage
"""

    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="scrollable"):
            with Vertical():
                yield Static("TERMUX PRO MENU", id="title")
                yield Button("TERMINAL INTERATIVO", id="terminal", classes="btn")
                yield Button("ATUALIZAR SISTEMA", id="update", classes="btn")
                yield Button("LIMPAR TERMINAL", id="clear", classes="btn")
                yield Button("GERENCIAR JANELAS", id="windows", classes="btn")
                yield Button("EDITAR CONFIGURAÇÕES", id="config", classes="btn")
                yield Button("INSTALAR FERRAMENTAS", id="tools", classes="btn")
                yield Button("INFORMAÇÕES DO SISTEMA", id="sysinfo", classes="btn")
                yield Button("REDE E CONECTIVIDADE", id="network", classes="btn")
                yield Button("GERENCIAR PROCESSOS", id="process", classes="btn")
                yield Button("SAIR DO APLICATIVO", id="exit", classes="btn")
                yield Static(self.frase_padrao, id="output")
                yield Input(placeholder="Digite comandos ou mensagens...", id="user_input")
                yield Button("FECHAR TODAS SESSÕES", id="enter_button", classes="btn")
                yield Button("PERSONALIZAR MENSAGEM", id="alter_phrase", classes="btn")
                yield Button("BACKUP CONFIGURAÇÕES", id="backup", classes="btn")
                yield Button("RESTAURAR PADRÕES", id="reset", classes="btn")

    def on_mount(self):
        self.query_one("#user_input", Input).focus()
        self.query_one("#output", Static).update(self.frase_padrao)

    @on(Button.Pressed, "#terminal")
    def terminal_pressed(self):
        self.query_one("#enter_button").styles.display = "block"
        self.notify("Modo terminal ativo", timeout=3)
        self.query_one("#output", Static).update("""Terminal ativo!
Digite comandos no campo acima.
Pressione [FECHAR TODAS SESSÕES] para retornar.""")

    @on(Button.Pressed, "#enter_button")
    def kill_sessions(self):
        self.run_command("pkill -9 bash", "Sessões encerradas!")
        self.query_one("#enter_button").styles.display = "none"

    @on(Button.Pressed, "#update")
    def update_system(self):
        self.run_command("pkg update && pkg upgrade -y", "Sistema atualizado com sucesso!")

    @on(Button.Pressed, "#clear")
    def clear_terminal(self):
        self.query_one("#output", Static).update(self.frase_padrao)

    @on(Button.Pressed, "#windows")
    def list_windows(self):
        self.run_command("termux-window -l", "Janelas disponíveis:")

    @on(Button.Pressed, "#config")
    def edit_config(self):
        self.run_command("nano $HOME/.termux/termux.properties", "Editando configurações...")

    @on(Button.Pressed, "#tools")
    def install_tools(self):
        self.run_command("pkg install git python nmap", "Ferramentas básicas instaladas")

    @on(Button.Pressed, "#sysinfo")
    def system_info(self):
        self.run_command("termux-info", "Informações do sistema:")

    @on(Button.Pressed, "#network")
    def network_tools(self):
        self.run_command("ifconfig || ip a", "Configurações de rede:")

    @on(Button.Pressed, "#process")
    def show_processes(self):
        self.run_command("ps aux", "Processos em execução:")

    @on(Button.Pressed, "#backup")
    def backup_config(self):
        self.run_command("cp $HOME/.termux/termux.properties $HOME/termux_backup.properties", 
                        "Backup criado em: $HOME/termux_backup.properties")

    @on(Button.Pressed, "#reset")
    def reset_defaults(self):
        self.run_command("termux-reset", "Configurações resetadas para padrão")

    @on(Button.Pressed, "#alter_phrase")
    def change_welcome(self):
        new_msg = self.query_one("#user_input", Input).value
        if new_msg:
            self.frase_padrao = new_msg
            self.query_one("#output", Static).update(new_msg)
            self.notify("Mensagem atualizada!", timeout=2)

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        self.exit()

    def run_command(self, command, success_msg):
        try:
            result = subprocess.run(
                command,
                shell=True,
                executable="/data/data/com.termux/files/usr/bin/bash",
                capture_output=True,
                text=True
            )
            output = result.stdout if result.stdout else success_msg
            self.query_one("#output", Static).update(output)
        except Exception as e:
            self.query_one("#output", Static).update(f"Erro: {str(e)}")

if __name__ == "__main__":
    app = TermuxProMenu()
    app.run()
