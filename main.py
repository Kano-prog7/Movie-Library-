import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        self.load_movies()
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Год:").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = tk.Entry(self.root)
        self.year_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Рейтинг:").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(self.root)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("title", "genre", "year", "rating"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(self.root)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по году:").grid(row=7, column=0, padx=5, pady=5)
        self.filter_year = tk.Entry(self.root)
        self.filter_year.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=8, column=0, columnspan=2, pady=10)

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            year = int(year)
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Год — целое число. Рейтинг — от 0 до 10.")
            return

        self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
        self.save_movies()
        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for movie in self.movies:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def apply_filter(self):
        genre = self.filter_genre.get().lower()
        year = self.filter_year.get()

        filtered = self.movies

        if genre:
            filtered = [m for m in filtered if genre in m["genre"].lower()]

        if year:
            try:
                year = int(year)
                filtered = [m for m in filtered if m["year"] == year]
            except ValueError:
                messagebox.showerror("Ошибка", "Год для фильтра — целое число.")
                return

        for i in self.tree.get_children():
            self.tree.delete(i)
        for movie in filtered:
            self.tree.insert("", "end", values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def save_movies(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_movies(self):
        if os.path.exists("movies.json"):
            with open("movies.json", "r", encoding="utf-8") as f:
                self.movies = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
