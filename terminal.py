from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.widgets import Footer, Header, Static, Input

import tkinter
from tkinter import simpledialog

import socket
import threading

class Terminal(App):
    CSS_PATH = 'style/ip.tcss'
    BINDINGS = [
        ("ctrl+t", "cycle_theme", "Cycle Theme"),
        ("enter", "submit", "Send Message"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        yield Container(
            ScrollableContainer(id="txt"),
            Horizontal(
                Input(placeholder="Send message...", id="inp"),
                id="dial2"
            ),
            id="dialog"
        )

    def on_mount(self) -> None:
        self.title = "Hermes"
        self.sub_title = "Secure Chat"

        self.query_one("#inp").placeholder = "Enter host (e.g. 127.0.0.1)..."
        self.input_stage = "host"

        self.port = 47777


    def action_cycle_theme(self):
        themes = ["nord", "gruvbox", "tokyo-night", "textual-dark", "solarized-light"]
        theme_id = themes.index(str(self.theme))

        if theme_id == len(themes)-1:
            theme_id = 0
        else:
            theme_id += 1

        self.theme = str(themes[theme_id])

    @on(Input.Submitted)
    def action_submit(self):
        inp = self.query_one("#inp")
        val = inp.value.strip()

        if self.input_stage == "host":
            self.host = val
            inp.value = ""
            inp.placeholder = "Enter nickname..."
            self.input_stage = "nick"
        elif self.input_stage == "nick":
            self.nick = val
            inp.value = ""
            inp.placeholder = "Send message..."
            self.connect_socket()
            self.input_stage = "chat"
        elif self.input_stage == "chat":
            message = f"{self.nick}: {val}"
            self.client.send(message.encode('utf-8'))
            inp.value = "" 


    def connect_socket(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            thread = threading.Thread(target=self.receive, daemon=True)
            thread.start()
        except Exception as e:
            self.query_one("#inp").placeholder = f"Connection failed: {e}"

    def display_message(self, message: str):
        cont = self.query_one("#txt")
        msg_box = Static(f"{message}")
        cont.mount(msg_box)
        msg_box.scroll_visible()

    def write(self, msg):
        message = f"{self.nick}: {msg}"
        self.client.send(message.encode('utf-8'))       

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8').strip()
                if message == "REQ_NICK":
                    self.client.send(self.nick.encode('ascii'))
                else:
                    self.call_from_thread(self.display_message, message)

            except ConnectionAbortedError:
                break
            except:
                print("Error occurred in receive loop")
                self.client.close()
                break

if __name__ == "__main__":
    app = Terminal()
    app.run()
