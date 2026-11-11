"""Модуль графического интерфейса пользователя для Лабораторной работы № 5."""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict


class TextEchoTab(ttk.Frame):
    """Задание 2 (Средняя): Текстовое поле и кнопка вывода сообщения."""

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=15)
        self._build_widgets()

    def _build_widgets(self) -> None:
        ttk.Label(
            self,
            text="Введите произвольный текст:",
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W, pady=(5, 2))

        self.user_input = ttk.Entry(self, width=42)
        self.user_input.pack(fill=tk.X, pady=6)

        self.display_label = ttk.Label(
            self,
            text="Результат появится здесь",
            font=("Segoe UI", 11, "italic"),
            foreground="#1e3d59"
        )
        self.display_label.pack(pady=12)

        action_btn = ttk.Button(
            self,
            text="Отобразить введённое",
            command=self._update_text
        )
        action_btn.pack(pady=4)

    def _update_text(self) -> None:
        content = self.user_input.get().strip()
        if content:
            self.display_label.config(text=f"Вы напечатали: {content}")
        else:
            self.display_label.config(text="Предупреждение: строка пуста!")


class CitySelectorTab(ttk.Frame):
    """Задание 4 (Средняя): Список Listbox и обработка выбора элемента."""

    ITEMS = ["Москва", "Томск", "Санкт-Петербург", "Новосибирск", "Казань"]

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=15)
        self._build_widgets()

    def _build_widgets(self) -> None:
        self.summary_lbl = ttk.Label(
            self,
            text="Выберите город из списка ниже:",
            font=("Segoe UI", 10)
        )
        self.summary_lbl.pack(pady=(0, 8))

        self.listbox = tk.Listbox(
            self,
            height=6,
            selectmode=tk.SINGLE,
            font=("Segoe UI", 10)
        )
        for city in self.ITEMS:
            self.listbox.insert(tk.END, city)
        self.listbox.pack(fill=tk.X, pady=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_item_picked)

    def _on_item_picked(self, _event: tk.Event) -> None:
        selection = self.listbox.curselection()
        if selection:
            chosen = self.listbox.get(selection[0])
            self.summary_lbl.config(text=f"Текущий выбор: {chosen}")


class DrawingCanvasTab(ttk.Frame):
    """Задание 2 (Повышенная): Рисование графических примитивов мышью."""

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=10)
        self.prev_x = None
        self.prev_y = None
        self._build_widgets()

    def _build_widgets(self) -> None:
        ctrl_bar = ttk.Frame(self)
        ctrl_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(
            ctrl_bar,
            text="Зажмите ЛКМ на холсте для рисования",
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT)

        clear_btn = ttk.Button(
            ctrl_bar,
            text="Очистить холст",
            command=self._clear_board
        )
        clear_btn.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(
            self,
            bg="#ffffff",
            highlightthickness=1,
            highlightbackground="#cccccc"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self._start_point)
        self.canvas.bind("<B1-Motion>", self._draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self._stop_stroke)

    def _start_point(self, event: tk.Event) -> None:
        self.prev_x = event.x
        self.prev_y = event.y

    def _draw_stroke(self, event: tk.Event) -> None:
        if self.prev_x is not None and self.prev_y is not None:
            self.canvas.create_line(
                self.prev_x,
                self.prev_y,
                event.x,
                event.y,
                width=3,
                fill="#17252a",
                capstyle=tk.ROUND,
                smooth=True
            )
        self.prev_x = event.x
        self.prev_y = event.y

    def _stop_stroke(self, _event: tk.Event) -> None:
        self.prev_x = None
        self.prev_y = None

    def _clear_board(self) -> None:
        self.canvas.delete("all")


class CurrencyExchangeTab(ttk.Frame):
    """Задание 6 (Повышенная): Конвертер валют."""

    EXCHANGE_TABLE: Dict[str, float] = {
        "RUB": 1.0,
        "USD": 91.20,
        "EUR": 98.40,
        "CNY": 12.60,
    }

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent, padding=15)
        self._build_widgets()

    def _build_widgets(self) -> None:
        row1 = ttk.Frame(self)
        row1.pack(fill=tk.X, pady=4)
        ttk.Label(row1, text="Сумма для конвертации:", width=22).pack(side=tk.LEFT)
        self.amount_box = ttk.Entry(row1)
        self.amount_box.insert(0, "1000")
        self.amount_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        row2 = ttk.Frame(self)
        row2.pack(fill=tk.X, pady=4)
        ttk.Label(row2, text="Исходная валюта:", width=22).pack(side=tk.LEFT)
        currency_keys = list(self.EXCHANGE_TABLE.keys())
        self.from_box = ttk.Combobox(row2, values=currency_keys, state="readonly")
        self.from_box.set("RUB")
        self.from_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        row3 = ttk.Frame(self)
        row3.pack(fill=tk.X, pady=4)
        ttk.Label(row3, text="Целевая валюта:", width=22).pack(side=tk.LEFT)
        self.to_box = ttk.Combobox(row3, values=currency_keys, state="readonly")
        self.to_box.set("USD")
        self.to_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.status_display = ttk.Label(
            self,
            text="Итог: ожидание расчёта",
            font=("Segoe UI", 11, "bold"),
            foreground="#2b7a78"
        )
        self.status_display.pack(pady=14)

        calc_button = ttk.Button(
            self,
            text="Выполнить расчёт",
            command=self._convert_currency
        )
        calc_button.pack()

    def _convert_currency(self) -> None:
        try:
            value = float(self.amount_box.get().replace(",", "."))
            if value < 0:
                raise ValueError
            base_amount = value * self.EXCHANGE_TABLE[self.from_box.get()]
            converted = base_amount / self.EXCHANGE_TABLE[self.to_box.get()]
            self.status_display.config(
                text=f"Итог: {converted:.2f} {self.to_box.get()}"
            )
        except ValueError:
            self.status_display.config(
                text="Ошибка: введите положительное число!"
            )


class MainApplication(tk.Tk):
    """Главное окно приложения с панелью меню и системой вкладок."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Лабораторная работа № 5 — GUI")
        self.geometry("540x440")
        self.minsize(480, 360)

        self._create_main_menu()
        self._create_tab_system()

    def _create_main_menu(self) -> None:
        """Задание 7 (Средняя): Окно с главным меню File -> Exit."""
        app_menu = tk.Menu(self)

        file_section = tk.Menu(app_menu, tearoff=0)
        file_section.add_command(label="Выход", command=self.destroy)
        app_menu.add_cascade(label="Файл", menu=file_section)

        help_section = tk.Menu(app_menu, tearoff=0)
        help_section.add_command(
            label="О программе",
            command=lambda: messagebox.showinfo(
                "Инфо", "Лабораторная работа № 5 (Вариант 2)"
            )
        )
        app_menu.add_cascade(label="Справка", menu=help_section)

        self.config(menu=app_menu)

    def _create_tab_system(self) -> None:
        """Инициализация вкладок ttk.Notebook."""
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH, padx=8, pady=8)

        notebook.add(TextEchoTab(notebook), text="Эхо-поле")
        notebook.add(CitySelectorTab(notebook), text="Список городов")
        notebook.add(DrawingCanvasTab(notebook), text="Рисование")
        notebook.add(CurrencyExchangeTab(notebook), text="Конвертер валют")


def main() -> None:
    """Точка запуска приложения."""
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()