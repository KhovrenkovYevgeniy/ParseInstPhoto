import os
import instaloader
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm

def download_photos(username, folder):
    # Создаем экземпляр класса Instaloader
    L = instaloader.Instaloader()

    # Входим в Instagram (при необходимости)
    # L.login(username, password)  # Замените username и password на свои учетные данные

    try:
        # Получаем профиль Instagram по имени пользователя
        profile = instaloader.Profile.from_username(L.context, username)

        # Создаем папку с именем "ParsePhotho_<username>", если ее еще нет
        folder_path = os.path.join(folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Загружаем фото и видео в указанную папку
        posts = profile.get_posts()
        with tqdm(total=profile.mediacount, desc="Загрузка фото и видео", unit="медиа") as pbar:
            for post in posts:
                if not post.is_video and not isinstance(post, instaloader.PostSidecarNode):
                    L.download_post(post, target=folder_path)
                    pbar.update(1)

        print("Загрузка фото и видео завершена!")

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Профиль с именем пользователя '{username}' не существует.")

    # Завершаем сеанс (при необходимости)
    # L.close()

def on_download():
    username = entry_username.get()
    folder = f"ParsePhotho_{username}"
    download_photos(username, folder)

# Создаем графический интерфейс
root = tk.Tk()
root.title("Загрузка фото и видео с Instagram")

# Определяем размеры окна и центрируем его на экране
window_width = 400
window_height = 300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Поле ввода для имени пользователя
label_username = ttk.Label(frame, text="Имя пользователя:")
label_username.pack(anchor=tk.W)

entry_username = ttk.Entry(frame)
entry_username.pack(fill=tk.X)

# Кнопка для начала загрузки фото и видео
btn_download = ttk.Button(frame, text="Загрузить фото и видео", command=on_download)
btn_download.pack(side=tk.BOTTOM, pady=5)

root.mainloop()
