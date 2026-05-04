import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("600x500")

        # Файл для сохранения избранных пользователей
        self.favorites_file = "favorites.json"
        self.load_favorites()

        self.setup_ui()

    def setup_ui(self):
        # Поле ввода для поиска
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(search_frame, text="Поиск пользователя GitHub:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_users())

        search_button = ttk.Button(search_frame, text="Найти", command=self.search_users)
        search_button.pack(side="left")

        # Список результатов поиска
        results_frame = ttk.LabelFrame(self.root, text="Результаты поиска")
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.results_tree = ttk.Treeview(results_frame, columns=("Login", "Name", "URL"), show="headings", height=10)
        self.results_tree.heading("Login", text="Логин")
        self.results_tree.heading("Name", text="Имя")
        self.results_tree.heading("URL", text="Профиль")
        self.results_tree.column("Login", width=150)
        self.results_tree.column("Name", width=200)
        self.results_tree.column("URL", width=250)
        self.results_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Кнопка добавления в избранное
        add_favorite_button = ttk.Button(results_frame, text="Добавить в избранное",
                                         command=self.add_to_favorites)
        add_favorite_button.pack(pady=5)

        # Список избранных пользователей
        favorites_frame = ttk.LabelFrame(self.root, text="Избранное")
        favorites_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.favorites_tree = ttk.Treeview(favorites_frame, columns=("Login", "Name", "URL"),
                                          show="headings", height=5)
        self.favorites_tree.heading("Login", text="Логин")
        self.favorites_tree.heading("Name", text="Имя")
        self.favorites_tree.heading("URL", text="Профиль")
        self.favorites_tree.column("Login", width=150)
        self.favorites_tree.column("Name", width=200)
        self.favorites_tree.column("URL", width=250)
        self.favorites_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Обновление списка избранного
        self.update_favorites_list()

    def search_users(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым!")
            return

        try:
            response = requests.get(f"https://api.github.com/search/users?q={query}")
            if response.status_code == 200:
                data = response.json()
                self.display_search_results(data["items"])
            else:
                messagebox.showerror("Ошибка", f"Ошибка API: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def display_search_results(self, users):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for user in users[:10]:  # Показываем первые 10 результатов
            self.results_tree.insert("", "end", values=(
                user["login"],
                user.get("name", "Не указано"),
                user["html_url"]
            ))

    def add_to_favorites(self):
        selected = self.results_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пользователя из списка!")
            return

        values = self.results_tree.item(selected[0])["values"]
        user_data = {
            "login": values[0],
            "name": values[1],
            "url": values[2]
        }

        if user_data not in self.favorites:
            self.favorites.append(user_data)
            self.save_favorites()
            self.update_favorites_list()
            messagebox.showinfo("Успех", "Пользователь добавлен в избранное!")
        else:
            messagebox.showinfo("Информация", "Этот пользователь уже в избранном!")

    def load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r", encoding="utf-8") as f:
                self.favorites = json.load(f)
        else:
            self.favorites = []

    def save_favorites(self):
        with open(self.favorites_file, "w", encoding="utf-8") as f:
            json.dump(self.favorites, f, ensure_ascii=False, indent=2)

    def update_favorites_list(self):
        for item in self.favorites_tree.get_children():
            self.favorites_tree.delete(item)

        for user in self.favorites:
            self.favorites_tree.insert("", "end", values=(
                user["login"], user["name"], user["url"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()
