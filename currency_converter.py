import requests
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import time
from datetime import datetime

# Cache para armazenar taxas de câmbio e tempo de atualização
cache = {"rates": None, "last_update": None}

# Função para buscar taxas de câmbio com suporte a cache


def fetch_exchange_rates(api_key):
    global cache
    # Verificar se os dados estão no cache e ainda são válidos
    if cache["rates"] and (time.time() - cache["last_update"] < 1800):  # 30 minutos
        return cache["rates"]

    url = f"https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            cache["rates"] = data["rates"]
            cache["last_update"] = time.time()
            return data["rates"]
        else:
            messagebox.showerror(
                translations["error_title"][current_lang], translations["fetch_error"][current_lang])
            return {}
    except requests.exceptions.RequestException as e:
        messagebox.showerror(
            translations["error_title"][current_lang], f"{translations['api_error'][current_lang]}: {e}")
        return {}

# Função para realizar a conversão


def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = combo_from.get()
        to_currency = combo_to.get()

        if from_currency == to_currency:
            converted_amount = amount
        else:
            rate_from = exchange_rates[from_currency]
            rate_to = exchange_rates[to_currency]
            converted_amount = (amount / rate_from) * rate_to

        result_text = f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
        label_result.config(text=result_text)

        # Adicionar a conversão ao histórico
        listbox_history.insert(0, result_text)
    except ValueError:
        messagebox.showerror(
            translations["error_title"][current_lang], translations["value_error"][current_lang])
    except Exception as e:
        messagebox.showerror(translations["error_title"][current_lang],
                             f"{translations['conversion_error'][current_lang]}: {e}")

# Função para atualizar a lista de moedas


def update_currency_list():
    global exchange_rates
    exchange_rates = fetch_exchange_rates(api_key)
    if exchange_rates:
        currencies = list(exchange_rates.keys())
        combo_from["values"] = currencies
        combo_to["values"] = currencies
        combo_from.set("USD")
        combo_to.set("BRL")

# Função para exibir gráfico de flutuação de câmbio


def show_exchange_fluctuations():
    try:
        base_currency = combo_from.get()
        if not base_currency:
            messagebox.showwarning(
                translations["warning_title"][current_lang], translations["select_base_currency"][current_lang])
            return

        rates = fetch_exchange_rates(api_key)
        if rates:
            sorted_currencies = sorted(rates.items(), key=lambda x: x[1])[:10]
            currencies, values = zip(*sorted_currencies)

            plt.figure(figsize=(10, 6))
            plt.bar(currencies, values, color='blue')
            plt.title(translations["chart_title"]
                      [current_lang].format(base_currency))
            plt.xlabel(translations["chart_x_label"][current_lang])
            plt.ylabel(translations["chart_y_label"][current_lang])
            plt.show()
    except Exception as e:
        messagebox.showerror(translations["error_title"][current_lang],
                             f"{translations['chart_error'][current_lang]}: {e}")

# Função para mudar o idioma da interface


def change_language(lang):
    global current_lang
    current_lang = lang
    root.title(translations["app_title"][lang])
    label_amount.config(text=translations["amount_label"][lang])
    label_from.config(text=translations["from_label"][lang])
    label_to.config(text=translations["to_label"][lang])
    button_convert.config(text=translations["convert_button"][lang])
    button_update.config(text=translations["update_button"][lang])
    button_chart.config(text=translations["chart_button"][lang])
    label_result.config(text="")
    label_history.config(text=translations["history_title"][lang])


# Configuração da chave da API
api_key = "sua_api_key_aqui"  # Substitua pela sua chave da API

# Traduções para suporte a idiomas
translations = {
    "app_title": {"en": "Currency Converter", "pt": "Conversor de Moedas", "es": "Convertidor de Divisas", "fr": "Convertisseur de Devises"},
    "amount_label": {"en": "Amount:", "pt": "Valor:", "es": "Cantidad:", "fr": "Montant:"},
    "from_label": {"en": "From:", "pt": "De:", "es": "De:", "fr": "De:"},
    "to_label": {"en": "To:", "pt": "Para:", "es": "A:", "fr": "À:"},
    "convert_button": {"en": "Convert", "pt": "Converter", "es": "Convertir", "fr": "Convertir"},
    "update_button": {"en": "Update Rates", "pt": "Atualizar Taxas", "es": "Actualizar Tasas", "fr": "Mettre à Jour les Taux"},
    "chart_button": {"en": "Show Fluctuations", "pt": "Exibir Flutuações", "es": "Mostrar Fluctuaciones", "fr": "Afficher les Fluctuations"},
    "history_title": {"en": "History:", "pt": "Histórico:", "es": "Historial:", "fr": "Historique:"},
    "chart_title": {"en": "Exchange Rate Fluctuations for {}", "pt": "Flutuações de Câmbio para {}", "es": "Fluctuaciones del Tipo de Cambio para {}", "fr": "Fluctuations des Taux de Change pour {}"},
    "chart_x_label": {"en": "Currency", "pt": "Moeda", "es": "Moneda", "fr": "Devise"},
    "chart_y_label": {"en": "Exchange Rate", "pt": "Taxa de Câmbio", "es": "Tipo de Cambio", "fr": "Taux de Change"},
    "error_title": {"en": "Error", "pt": "Erro", "es": "Error", "fr": "Erreur"},
    "value_error": {"en": "Please enter a valid numeric value.", "pt": "Insira um valor numérico válido.", "es": "Introduzca un valor numérico válido.", "fr": "Veuillez entrer une valeur numérique valide."},
    "chart_error": {"en": "Unable to show chart", "pt": "Não foi possível exibir o gráfico", "es": "No se pudo mostrar el gráfico", "fr": "Impossible d'afficher le graphique"},
    "select_base_currency": {"en": "Please select a base currency.", "pt": "Por favor, selecione uma moeda base.", "es": "Por favor, seleccione una moneda base.", "fr": "Veuillez sélectionner une devise de base."},
    "fetch_error": {"en": "Failed to fetch exchange rates.", "pt": "Falha ao buscar taxas de câmbio.", "es": "Error al obtener las tasas de cambio.", "fr": "Échec de la récupération des taux de change."},
    "warning_title": {"en": "Warning", "pt": "Aviso", "es": "Advertencia", "fr": "Avertissement"},
}

# Idioma padrão
current_lang = "pt"

# Configuração da interface Tkinter
root = tk.Tk()
root.title(translations["app_title"][current_lang])

# Frame principal
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Entrada de valor
label_amount = ttk.Label(
    frame, text=translations["amount_label"][current_lang])
label_amount.grid(column=0, row=0, sticky=tk.W)
entry_amount = ttk.Entry(frame, width=20)
entry_amount.grid(column=1, row=0, sticky=tk.E)

# Seleção de moeda de origem
label_from = ttk.Label(frame, text=translations["from_label"][current_lang])
label_from.grid(column=0, row=1, sticky=tk.W)
combo_from = ttk.Combobox(frame, state="readonly", width=15)
combo_from.grid(column=1, row=1, sticky=tk.E)

# Seleção de moeda de destino
label_to = ttk.Label(frame, text=translations["to_label"][current_lang])
label_to.grid(column=0, row=2, sticky=tk.W)
combo_to = ttk.Combobox(frame, state="readonly", width=15)
combo_to.grid(column=1, row=2, sticky=tk.E)

# Botão de conversão
button_convert = ttk.Button(
    frame, text=translations["convert_button"][current_lang], command=convert_currency)
button_convert.grid(column=0, row=3, columnspan=2)

# Botão de atualização de taxas
button_update = ttk.Button(
    frame, text=translations["update_button"][current_lang], command=update_currency_list)
button_update.grid(column=0, row=4, columnspan=2)

# Botão para exibir flutuações
button_chart = ttk.Button(
    frame, text=translations["chart_button"][current_lang], command=show_exchange_fluctuations)
button_chart.grid(column=0, row=5, columnspan=2)

# Resultado da conversão
label_result = ttk.Label(frame, text="", foreground="blue")
label_result.grid(column=0, row=6, columnspan=2)

# Histórico de conversões
label_history = ttk.Label(
    frame, text=translations["history_title"][current_lang])
label_history.grid(column=0, row=7, columnspan=2)
listbox_history = tk.Listbox(frame, height=10, width=50)
listbox_history.grid(column=0, row=8, columnspan=2)

# Menu para selecionar idioma
menu = tk.Menu(root)
root.config(menu=menu)
language_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Language / Idioma / Idioma / Langue",
                 menu=language_menu)
language_menu.add_command(
    label="English", command=lambda: change_language("en"))
language_menu.add_command(
    label="Português", command=lambda: change_language("pt"))
language_menu.add_command(
    label="Español", command=lambda: change_language("es"))
language_menu.add_command(
    label="Français", command=lambda: change_language("fr"))

# Atualizar a lista de moedas ao iniciar o programa
exchange_rates = {}
update_currency_list()

# Executar a interface Tkinter
root.mainloop()
