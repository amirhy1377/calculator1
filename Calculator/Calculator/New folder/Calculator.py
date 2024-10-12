import tkinter as tk
from tkinter import ttk, messagebox
import requests
from sympy import sympify, symbols, Matrix, solve

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ماشین حساب پیشرفته")
        self.root.geometry("1000x800")  # افزایش ابعاد پنجره اصلی

        self.equation = tk.StringVar()

        # ایجاد نوار تب‌ها
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # ایجاد تب‌ها
        self.base_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.base_frame, text="ماشین حساب")

        self.scientific_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.scientific_frame, text="ماشین حساب علمی")

        # نمایشگر معادله
        self.display = tk.Text(self.base_frame, height=4, width=60, font=("Arial", 20))  # افزایش اندازه نمایشگر
        self.display.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # ایجاد قاب برای دکمه‌ها و اسکرول بار
        self.button_canvas = tk.Canvas(self.base_frame)
        self.button_canvas.grid(row=1, column=0, columnspan=5, sticky="nsew")

        self.button_frame = ttk.Frame(self.button_canvas)
        self.button_frame.bind(
            "<Configure>",
            lambda e: self.button_canvas.configure(scrollregion=self.button_canvas.bbox("all"))
        )

        self.button_canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

        self.vsb = tk.Scrollbar(self.base_frame, orient="vertical", command=self.button_canvas.yview)
        self.vsb.grid(row=1, column=6, sticky="ns")
        self.button_canvas.configure(yscrollcommand=self.vsb.set)

        # اتصال رویداد اسکرول با ماوس به متد جدید
        self.button_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

        # ایجاد دکمه‌ها
        self.create_base_buttons()
        self.create_scientific_buttons()

    def create_base_buttons(self):
        button_texts = [
            "7", "8", "9", "/", "C",
            "4", "5", "6", "*", "(",
            "1", "2", "3", "-", ")",
            "0", ".", "=", "+", "sin",
            "cos", "tan", "cot", "log",
            "exp", "sqrt", "x", "y", "z",
            "Exit", "حل معادله", "رسم نمودار",
            "مشتق", "انتگرال", "ماتریس", "حل معادله ماتریسی",
            "دانلود داده"
        ]

        row_val = 0
        col_val = 0
        for text in button_texts:
            button = tk.Button(self.button_frame, text=text, padx=30, pady=30, font=("Arial", 18),  # افزایش اندازه دکمه‌ها
                               command=lambda txt=text: self.button_click(txt))
            button.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # تنظیم وزن ستون‌ها و ردیف‌ها برای پر کردن فضا
        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(row_val + 1):
            self.button_frame.grid_rowconfigure(i, weight=1)

    def create_scientific_buttons(self):
        scientific_buttons = [
            "log2", "log10", "pow", "mod",
            "سین", "آزمایش", "دلخواه1", "دلخواه2", "دلخواه3"
        ]

        row_val = 0
        col_val = 0
        for text in scientific_buttons:
            button = tk.Button(self.scientific_frame, text=text, padx=30, pady=30, font=("Arial", 18),  # افزایش اندازه دکمه‌ها
                               command=lambda txt=text: self.button_click(txt))
            button.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        # تنظیم وزن ستون‌ها و ردیف‌ها برای پر کردن فضا
        for i in range(5):
            self.scientific_frame.grid_columnconfigure(i, weight=1)
        for i in range(row_val + 1):
            self.scientific_frame.grid_rowconfigure(i, weight=1)

    def on_mouse_wheel(self, event):
        self.button_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def button_click(self, button_text):
        current_equation = self.display.get("1.0", tk.END).strip()

        if button_text == "=":
            self.evaluate_expression(current_equation)
        elif button_text == "C":
            self.display.delete("1.0", tk.END)
        elif button_text == "Exit":
            self.root.quit()
        elif button_text == "حل معادله":
            self.solve_equation()
        elif button_text == "رسم نمودار":
            self.plot_graph()
        elif button_text == "مشتق":
            self.differentiate_expression()
        elif button_text == "انتگرال":
            self.integrate_expression()
        elif button_text == "ماتریس":
            self.enter_matrix()
        elif button_text == "حل معادله ماتریسی":
            self.solve_matrix_equation()
        elif button_text == "دانلود داده":
            self.download_data()
        else:
            if button_text in ["sin", "cos", "tan", "cot", "log", "exp", "sqrt"]:
                button_text += "("
            self.display.insert(tk.END, button_text)

    def evaluate_expression(self, expression):
        try:
            result = str(sympify(expression))
            self.display.delete("1.0", tk.END)
            self.display.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("خطا", f"معادله اشتباه است: {e}")
            self.display.delete("1.0", tk.END)

    def solve_equation(self):
        equation = self.display.get("1.0", tk.END).strip()
        try:
            x, y, z = symbols('x y z')
            solutions = solve(sympify(equation), (x, y, z))
            self.display_solutions(solutions)
        except Exception as e:
            messagebox.showerror("خطا", f"معادله اشتباه است یا متغیرهای x، y، z ندارد: {e}")
            self.display.delete("1.0", tk.END)

    def solve_matrix_equation(self):
        try:
            matrix_A_str = self.display.get("1.0", "2.0").strip()
            matrix_B_str = self.display.get("2.0", "3.0").strip()

            matrix_A = Matrix(sympify(matrix_A_str))
            matrix_B = Matrix(sympify(matrix_B_str))

            if matrix_A.shape[1] != matrix_B.shape[0]:
                raise ValueError("تعداد ستون‌های ماتریس A باید برابر با تعداد سطرهای ماتریس B باشد.")

            solutions = matrix_A.inv() * matrix_B

            self.display.delete("1.0", tk.END)
            self.display.insert(tk.END, f"X =\n{solutions}")
        except Exception as e:
            messagebox.showerror("خطا", f"معادلات ماتریسی وارد شده اشتباه است یا سازگار نیستند: {e}")
            self.display.delete("1.0", tk.END)

    def plot_graph(self):
        pass  # کد رسم نمودار

    def differentiate_expression(self):
        pass  # کد مشتق

    def integrate_expression(self):
        pass  # کد انتگرال

    def enter_matrix(self):
        matrix_window = tk.Toplevel(self.root)
        matrix_window.title("ورود ماتریس")

        tk.Label(matrix_window, text="تعداد سطرها:").grid(row=0, column=0)
        tk.Label(matrix_window, text="تعداد ستون‌ها:").grid(row=1, column=0)

        rows_entry = tk.Entry(matrix_window)
        cols_entry = tk.Entry(matrix_window)
        rows_entry.grid(row=0, column=1)
        cols_entry.grid(row=1, column=1)

        def create_matrix_entries():
            try:
                rows = int(rows_entry.get())
                cols = int(cols_entry.get())
            except ValueError:
                messagebox.showerror("خطا", "تعداد سطرها و ستون‌ها باید عددی باشد.")
                return

            for widget in matrix_window.winfo_children():
                if isinstance(widget, tk.Entry):
                    widget.destroy()

            self.matrix_entries = []
            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    entry = tk.Entry(matrix_window, width=5)
                    entry.grid(row=i+2, column=j)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)

            def save_matrix():
                matrix = []
                for row in self.matrix_entries:
                    row_values = []
                    for entry in row:
                        try:
                            value = float(entry.get())
                            row_values.append(value)
                        except ValueError:
                            messagebox.showerror("خطا", "لطفاً مقادیر معتبر وارد کنید.")
                            return
                    matrix.append(row_values)

                matrix_str = str(Matrix(matrix))
                self.display.delete("1.0", tk.END)
                self.display.insert(tk.END, matrix_str)
                matrix_window.destroy()

            save_button = tk.Button(matrix_window, text="ذخیره", command=save_matrix)
            save_button.grid(row=rows+2, column=0, columnspan=cols)

        create_matrix_button = tk.Button(matrix_window, text="ایجاد ماتریس", command=create_matrix_entries)
        create_matrix_button.grid(row=2, column=0, columnspan=2)

    def download_data(self):
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        try:
            response = requests.get(url)
            data = response.json()
            rates = data["rates"]
            result = "\n".join([f"{currency}: {rate}" for currency, rate in rates.items()])
            self.display.delete("1.0", tk.END)
            self.display.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در دانلود داده‌ها: {e}")

    def display_solutions(self, solutions):
        self.display.delete("1.0", tk.END)
        if isinstance(solutions, dict):
            for variable, solution in solutions.items():
                self.display.insert(tk.END, f"{variable} = {solution}\n")
        else:
            self.display.insert(tk.END, solutions)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
