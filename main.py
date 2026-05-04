import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

class RandomQuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x600")

        # Предопределённые цитаты
        self.quotes = [
            {"text": "Жизнь — это то, что происходит с тобой, пока ты строишь другие планы.",
             "author": "Джон Леннон", "topic": "Философия"},
            {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.",
             "author": "Уинстон Черчилль", "topic": "Мотивация"},
            {"text": "Знание — сила.",
             "author": "Фрэнсис Бэкон", "topic": "Наука"},
            {"text": "Будь изменением, которое ты хочешь видеть в мире.",
             "author": "Махатма Ганди", "topic": "Саморазвитие"}
        ]

        # Файл для сохранения истории
        self.history_file = "quote_history.json"
        self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Кнопка генерации цитаты
        generate_frame = ttk.Frame(self.root)
        generate_frame.pack(pady=10, padx=20, fill="x")

        generate_btn = ttk.Button(generate_frame, text="Сгенерировать цитату",
                               command=self.generate_quote)
        generate_btn.pack()

        # Отображение текущей цитаты
        quote_frame = ttk.LabelFrame(self.root, text="Случайная цитата")
        quote_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.quote_text = tk.Text(quote_frame, height=5, wrap="word")
        self.quote_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Фильтры
        filter_frame = ttk.LabelFrame(self.root, text="Фильтры")
        filter_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5, pady=5)
        self.author_filter = ttk.Entry(filter_frame, width=20)
        self.author_filter.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5, pady=5)
        self.topic_filter = ttk.Entry(filter_frame, width=20)
        self.topic_filter.grid(row=0, column=3, padx=5, pady=5)

        filter_btn = ttk.Button(filter_frame, text="Применить фильтр",
                           command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=5, pady=5)

        reset_btn = ttk.Button(filter_frame, text="Сбросить фильтры",
                         command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5, pady=5)

        # История цитат
        history_frame = ttk.LabelFrame(self.root, text="История цитат")
        history_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("Текст", "Автор", "Тема")
        self.history_tree = ttk.Treeview(history_frame, columns=columns,
                                  show="headings", height=8)

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)

        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_history_list()

    def generate_quote(self):
        if not self.quotes:
            messagebox.showerror("Ошибка", "Нет доступных цитат!")
            return

        quote = random.choice(self.quotes)
        self.current_quote = quote

        # Очистка и отображение новой цитаты
        self.quote_text.delete(1.0, tk.END)
        display_text = f"{quote['text']}\n\n— {quote['author']} ({quote['topic']})"
        self.quote_text.insert(1.0, display_text)

        # Добавление в историю
        if quote not in self.history:
            self.history.append(quote)
            self.save_history()
            self.update_history_list()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)
        else:
            self.history = []

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def update_history_list(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        filtered_history = self.apply_filters_to_history()
        for quote in filtered_history:
            self.history_tree.insert("", "end", values=(
                quote["text"], quote["author"], quote["topic"]
            ))

    def apply_filter(self):
        self.update_history_list()

    def reset_filter(self):
        self.author_filter.delete(0, tk.END)
        self.topic_filter.delete(0, tk.END)
        self.update_history_list()

    def apply_filters_to_history(self):
        author_filter = self.author_filter.get().strip().lower()
        topic_filter = self.topic_filter.get().strip().lower()

        filtered = self.history
        if author_filter:
            filtered = [q for q in filtered if author_filter in q["author"].lower()]
        if topic_filter:
            filtered = [q for q in filtered if topic_filter in q["topic"].lower()]

        return filtered

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomQuoteGenerator(root)
    root.mainloop()
