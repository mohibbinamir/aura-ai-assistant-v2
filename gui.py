import customtkinter as ctk


class AuraGUI(ctk.CTk):
    def __init__(self, send_callback):
        super().__init__()
        self.send_callback = send_callback

        self.title("AURA AI Assistant V2.2")
        self.geometry("1400x900")
        self.minsize(1100, 750)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, height=70, corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="AURA AI Assistant",
            font=("Segoe UI", 28, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=25, pady=(18, 2), sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Local AI Assistant with Smart Actions + Chat",
            font=("Segoe UI", 13)
        )
        self.subtitle_label.grid(row=1, column=0, padx=27, pady=(0, 12), sticky="w")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Quick Actions",
            font=("Segoe UI", 20, "bold")
        )
        self.sidebar.pack_propagate(False)
        self.sidebar_title.pack(padx=20, pady=(20, 15), anchor="w")

        self._make_sidebar_button("Open GitHub", "open github")
        self._make_sidebar_button("Open YouTube", "open youtube")
        self._make_sidebar_button("Open Netflix", "open netflix")
        self._make_sidebar_button("Open Downloads", "open downloads")
        self._make_sidebar_button("Open Calculator", "open calculator")
        self._make_sidebar_button("Show Time", "what time is it")
        self._make_sidebar_button("Show Date", "what is the date")
        self._make_sidebar_button("Read Notes", "read notes")
        self._make_sidebar_button("Take Screenshot", "take screenshot")

        self.sidebar_hint = ctk.CTkLabel(
            self.sidebar,
            text="You can also type natural commands like:\n• Open YouTube and search MrBeast\n• Open GitHub please\n• What time is it",
            justify="left",
            wraplength=190,
            font=("Segoe UI", 12)
        )
        self.sidebar_hint.pack(padx=20, pady=(25, 10), anchor="w")

        # Main area
        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.grid(row=1, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.chat_frame = ctk.CTkFrame(self.main_area, corner_radius=18)
        self.chat_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(
            self.chat_frame,
            wrap="word",
            font=("Consolas", 18),
            corner_radius=14
        )
        self.chat_box.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.chat_box.insert("end", "Aura: Hello, I am Aura V2.2.\n")
        self.chat_box.configure(state="disabled")

        self.input_frame = ctk.CTkFrame(self.main_area, height=90, corner_radius=16)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Type your message here...",
            height=52,
            font=("Segoe UI", 17)
        )
        self.entry.grid(row=0, column=0, padx=(18, 10), pady=18, sticky="ew")
        self.entry.bind("<Return>", self._on_enter)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=120,
            height=52,
            font=("Segoe UI", 16, "bold"),
            command=self._send_message
        )
        self.send_button.grid(row=0, column=1, padx=(0, 18), pady=18)

    def _make_sidebar_button(self, text: str, command_text: str):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            width=190,
            height=40,
            command=lambda cmd=command_text: self._run_quick_action(cmd)
        )
        button.pack(padx=20, pady=6, anchor="w")

    def _run_quick_action(self, command_text: str):
        self.add_message("You", command_text)

        try:
            reply = self.send_callback(command_text)
        except Exception as e:
            reply = f"Quick action error: {e}"

        if reply == "__ASK_SAVE_NOTE__":
            self.add_message("Aura", "What note would you like me to save?")
            note_text = self._prompt_note()
            if note_text:
                try:
                    second_reply = self.send_callback(f"save note {note_text}")
                except Exception as e:
                    second_reply = f"Save note error: {e}"
                self.add_message("Aura", second_reply)
            return

        self.add_message("Aura", reply)

    def _on_enter(self, event):
        self._send_message()

    def _send_message(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.entry.delete(0, "end")
        self.add_message("You", user_text)

        try:
            reply = self.send_callback(user_text)
        except Exception as e:
            reply = f"Message error: {e}"

        if reply == "__ASK_SAVE_NOTE__":
            self.add_message("Aura", "What note would you like me to save?")
            note_text = self._prompt_note()
            if note_text:
                try:
                    second_reply = self.send_callback(f"save note {note_text}")
                except Exception as e:
                    second_reply = f"Save note error: {e}"
                self.add_message("Aura", second_reply)
            return

        self.add_message("Aura", reply)

    def _prompt_note(self) -> str:
        dialog = ctk.CTkInputDialog(text="Enter the note to save:", title="Save Note")
        result = dialog.get_input()
        return result.strip() if result else ""

    def add_message(self, speaker: str, text: str):
        display_text = text.replace("__SPEAK__:", "")
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{speaker}: {display_text}\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")