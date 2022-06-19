import PySimpleGUI as sg
from loguru import logger
from pkg_resources import resource_string

from pdf_utility_belt.helpers.utility import center
from pdf_utility_belt.windows.merge import pdf_merge_window
from pdf_utility_belt.windows.reverse import reverse_pdf_order_window

sg.set_options(icon=resource_string("pdf_utility_belt.res.images", "screwdriver-wrench-solid.png"))


def main_window():
    layout = [
        [*center(sg.Button("Merge PDF", key=f"merge")), *center(sg.Button("Reverse PDF", key=f"reverse"))]
    ]
    frame = sg.Frame("Utility Belt", layout=layout, title_location=sg.TITLE_LOCATION_BOTTOM_RIGHT, size=(400, 180))
    window = sg.Window(
        "PDF Utility Belt - a gui for your pdf needs", layout=[[frame]],
        size=(400, 180)
    )
    logger.info("Starting main window")
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
