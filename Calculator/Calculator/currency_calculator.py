import tkinter as tk
from tkinter import messagebox
import requests

class CurrencyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ماشین حساب قیمت ارز")
        self.root.geometry("400x300")

        # نمایشگر برای نمایش نرخ ارز
        self.display = tk.Text(root, height=10, width=40, font=("Arial", 14))
        self.display.pack(pady=20)

        # دکمه برای دریافت نرخ ارز
        self.get_exchange_rate_button = tk.Button(root, text="دریافت نرخ ارز", command=self.get_exchange_rate, font=("Arial", 14))
        self.get_exchange_rate_button.pack(pady=10)

    def get_exchange_rate(self):
        api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        try:
            # ارسال درخواست به API
            response = requests.get(api_url)
            response.raise_for_status()  # بررسی وضعیت پاسخ

            # دریافت داده‌ها از پاسخ API
            data = response.json()
            rates = data.get("rates", {})

            # انتخاب ارز مورد نظر (به عنوان مثال EUR)
            currency = "EUR"
            rate = rates.get(currency)
            
            if rate:
                result = f"1 USD = {rate} {currency}"
                self.display.delete("1.0", tk.END)  # پاک کردن محتوای قبلی نمایشگر
                self.display.insert(tk.END, result)  # نمایش نرخ ارز در نمایشگر
            else:
                messagebox.showerror("خطا", f"نرخ ارز برای {currency} یافت نشد.")
        except requests.RequestException as e:
            messagebox.showerror("خطا", f"خطا در دریافت نرخ ارز: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyCalculator(root)
    root.mainloop()
