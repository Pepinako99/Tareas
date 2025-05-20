import flet as ft
import os
import shutil
import subprocess

def main(page: ft.Page):
    page.title = "COPIA DE SEGURIDAD"
    page.window_width = 400
    page.window_height = 550
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#000000"

    def crear_carpetas():
        home = os.path.expanduser("~")
        proyectos = os.path.join(home, "proyectos")
        copias = os.path.join(home, "copias")
        os.makedirs(proyectos, exist_ok=True)
        os.makedirs(copias, exist_ok=True)
        return proyectos, copias

    proyectos_path, copias_path = crear_carpetas()

    dest_input = ft.TextField(
        label="Ruta destino para copia",
        width=380,
        border_color="#4a6fa5",
        focused_border_color="#166084",
        bgcolor="#333333",
        color="#ffffff",
    )

    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    day_dropdown = ft.Dropdown(
        label="Día de la semana",
        width=380,
        options=[ft.DropdownOption(d) for d in days],
        border_color="#4a6fa5",
        focused_border_color="#166084",
        filled=True,
        bgcolor="#333333",
        color="#ffffff",
        value=days[0],
    )

    hours = [str(i).zfill(2) for i in range(24)]
    hour_dropdown = ft.Dropdown(
        label="Hora",
        width=180,
        options=[ft.DropdownOption(h) for h in hours],
        border_color="#4a6fa5",
        focused_border_color="#166084",
        filled=True,
        bgcolor="#333333",
        color="#ffffff",
        value="00",
    )

    minutes = [str(i).zfill(2) for i in range(60)]
    minute_dropdown = ft.Dropdown(
        label="Minuto",
        width=180,
        options=[ft.DropdownOption(m) for m in minutes],
        border_color="#4a6fa5",
        focused_border_color="#166084",
        filled=True,
        bgcolor="#333333",
        color="#ffffff",
        value="00",
    )

    result_text = ft.Text(color="#ffffff")

    def realizar_copia(e):
        destino = dest_input.value.strip()
        if not destino:
            result_text.value = "Introduce la ruta destino."
            result_text.color = "red"
            page.update()
            return
        if not os.path.exists(destino):
            result_text.value = "La ruta destino no existe."
            result_text.color = "red"
            page.update()
            return
        try:
            destino_final = os.path.join(destino, "proyectos_backup")
            if os.path.exists(destino_final):
                shutil.rmtree(destino_final)
            shutil.copytree(proyectos_path, destino_final)
            result_text.value = f"Copia realizada para {day_dropdown.value} a las {hour_dropdown.value}:{minute_dropdown.value}."
            result_text.color = "green"
            page.update()
            # Abrir explorador en destino
            if os.name == "nt":
                subprocess.Popen(f'explorer "{destino}"')
            else:
                subprocess.Popen(["xdg-open", destino])
        except Exception as ex:
            result_text.value = f"Error: {ex}"
            result_text.color = "red"
            page.update()

    btn_copiar = ft.ElevatedButton(
        "Realizar Copia",
        on_click=realizar_copia,
        color="white",
        bgcolor="#2ecc71",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20,
        ),
    )

    page.add(
        ft.Column(
            [
                ft.Text("Copia de Seguridad", size=20, weight="bold", color="#ffffff"),                dest_input,
                ft.Row([day_dropdown], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([hour_dropdown, minute_dropdown], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                btn_copiar,
                result_text,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=15,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=30028)
