import PySimpleGUI as sg

from pdf_utility_belt.windows.merge import pdf_merge_window
from pdf_utility_belt.windows.reverse import reverse_pdf_order_window


def main_window():
    layout = [
        [sg.Button("Merge PDF", key=f"merge"), sg.Button("Reverse PDF", key=f"reverse")]
    ]
    frame = sg.Frame("Utility Belt", layout=layout, title_location=sg.TITLE_LOCATION_BOTTOM_RIGHT, size=(320, 160))
    window = sg.Window("PDF Utility Belt - a gui for your pdf needs", layout=[[frame]], size=(320, 160), resizable=True)
    while True:
        event, _ = window.read()
        match event:
            case sg.WIN_CLOSED:
                break
            case "merge":
                pdf_merge_window()
            case "reverse":
                reverse_pdf_order_window()
            case _:
                pass
    window.close()
