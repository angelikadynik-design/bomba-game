import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


DATA_FILE = Path(__file__).resolve().with_name("notes.json")


def safe_json_load(path):
    """Load notes safely even when the file is missing or empty."""
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = file.read().strip()
            if not data:
                return []
            loaded = json.loads(data)
            if isinstance(loaded, list):
                return loaded
            return []
    except (json.JSONDecodeError, OSError):
        return []


class MageDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mage's Diary")
        self.root.geometry("820x520")
        self.root.minsize(700, 420)

        self.notes = safe_json_load(DATA_FILE)
        self.selected_note_index = 0

        main_frame = tk.Frame(root, padx=12, pady=12, bg="#efe5d7")
        main_frame.pack(fill="both", expand=True)

        self.left_panel = tk.Frame(main_frame, bg="#e9dcc6", padx=8, pady=8)
        self.left_panel.pack(side="left", fill="y")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.apply_filter)
        search_label = tk.Label(self.left_panel, text="Filter by tag:", bg="#e9dcc6", font=("Arial", 11, "bold"))
        search_label.pack(anchor="w", pady=(0, 5))
        self.search_entry = tk.Entry(self.left_panel, textvariable=self.search_var)
        self.search_entry.pack(fill="x", pady=(0, 8))

        self.notes_listbox = tk.Listbox(self.left_panel, width=26, height=18, font=("Arial", 11))
        self.notes_listbox.pack(fill="both", expand=True)
        self.notes_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        button_frame = tk.Frame(self.left_panel, bg="#e9dcc6")
        button_frame.pack(fill="x", pady=(8, 0))

        self.new_button = tk.Button(button_frame, text="New note", command=self.new_note)
        self.new_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_note, fg="white", bg="#b84545")
        self.delete_button.pack(side="left", expand=True, fill="x")

        self.right_panel = tk.Frame(main_frame, bg="#f8f3eb", padx=10, pady=10)
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.title_label = tk.Label(self.right_panel, text="Title", font=("Arial", 11, "bold"), bg="#f8f3eb")
        self.title_label.pack(anchor="w")
        self.title_entry = tk.Entry(self.right_panel, font=("Arial", 12))
        self.title_entry.pack(fill="x", pady=(0, 8))

        self.tags_label = tk.Label(self.right_panel, text="Tags (comma separated)", font=("Arial", 11, "bold"), bg="#f8f3eb")
        self.tags_label.pack(anchor="w")
        self.tags_entry = tk.Entry(self.right_panel, font=("Arial", 12))
        self.tags_entry.pack(fill="x", pady=(0, 8))

        self.content_label = tk.Label(self.right_panel, text="Spell text", font=("Arial", 11, "bold"), bg="#f8f3eb")
        self.content_label.pack(anchor="w")
        self.content_text = tk.Text(self.right_panel, height=14, wrap="word", font=("Arial", 11))
        self.content_text.pack(fill="both", expand=True)

        self.save_button = tk.Button(self.right_panel, text="Save note", command=self.save_note, bg="#4e78c9", fg="white")
        self.save_button.pack(pady=(10, 0), fill="x")

        self.load_notes_into_list()
        if self.notes:
            self.notes_listbox.selection_set(0)
            self.display_selected_note(0)
        else:
            self.new_note()

    def normalize_tags(self, tag_text):
        if not tag_text:
            return []
        tags = [tag.strip().lower() for tag in tag_text.split(",")]
        return [tag for tag in tags if tag]

    def note_title(self, note):
        return note.get("title", "Untitled note")

    def note_tags_text(self, note):
        tags = note.get("tags", [])
        if not tags:
            return "(no tags)"
        return ", ".join(tags)

    def filter_matches(self, note):
        query = self.search_var.get().strip().lower()
        if not query:
            return True
        tags = note.get("tags", [])
        for tag in tags:
            if query in tag.lower():
                return True
        return False

    def load_notes_into_list(self):
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes:
            if self.filter_matches(note):
                self.notes_listbox.insert(tk.END, f"{self.note_title(note)} [{self.note_tags_text(note)}]")

    def apply_filter(self, *args):
        self.load_notes_into_list()
        if self.notes:
            self.selected_note_index = 0
            if self.notes_listbox.size() > 0:
                self.notes_listbox.selection_set(0)
                self.display_selected_note(0)

    def on_note_select(self, event):
        selected = self.notes_listbox.curselection()
        if not selected:
            return
        index = selected[0]
        self.display_selected_note(index)

    def display_selected_note(self, list_index):
        visible_notes = [
            note for note in self.notes if self.filter_matches(note)
        ]
        if list_index >= len(visible_notes):
            return

        note = visible_notes[list_index]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note.get("title", "Untitled note"))

        self.tags_entry.delete(0, tk.END)
        self.tags_entry.insert(0, ", ".join(note.get("tags", [])))

        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", note.get("content", ""))

    def get_selected_note(self):
        selected = self.notes_listbox.curselection()
        if not selected:
            return None

        visible_notes = [
            note for note in self.notes if self.filter_matches(note)
        ]
        if not visible_notes:
            return None

        list_index = selected[0]
        if list_index >= len(visible_notes):
            return None
        return visible_notes[list_index]

    def save_note(self):
        note = self.get_selected_note()
        if note is None:
            messagebox.showwarning("No note selected", "Please select a note to save.")
            return

        note["title"] = self.title_entry.get().strip() or "Untitled note"
        note["tags"] = self.normalize_tags(self.tags_entry.get())
        note["content"] = self.content_text.get("1.0", "end-1c")
        self.persist_notes()
        self.load_notes_into_list()

    def new_note(self):
        new_note_data = {
            "title": f"New note {len(self.notes) + 1}",
            "tags": ["new"],
            "content": "Write your spell here...",
        }
        self.notes.append(new_note_data)
        self.persist_notes()
        self.load_notes_into_list()
        self.notes_listbox.selection_clear(0, tk.END)
        self.notes_listbox.selection_set(self.notes_listbox.size() - 1)
        self.display_selected_note(self.notes_listbox.size() - 1)

    def delete_note(self):
        note = self.get_selected_note()
        if note is None:
            messagebox.showwarning("No note selected", "Please select a note to delete.")
            return

        confirmed = messagebox.askyesno("Delete note", f"Delete '{note.get('title', 'this note')}'?")
        if not confirmed:
            return

        self.notes.remove(note)
        self.persist_notes()
        self.load_notes_into_list()
        if self.notes:
            self.notes_listbox.selection_set(0)
            self.display_selected_note(0)
        else:
            self.title_entry.delete(0, tk.END)
            self.tags_entry.delete(0, tk.END)
            self.content_text.delete("1.0", tk.END)

    def persist_notes(self):
        try:
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(self.notes, file, indent=2, ensure_ascii=False)
        except OSError:
            messagebox.showerror("File error", "Could not save notes.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MageDiaryApp(root)
    root.mainloop()

