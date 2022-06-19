from pathlib import PurePath

import PySimpleGUI as sg
from loguru import logger
from pikepdf import PdfError

from pdf_utility_belt.helpers.utility import is_pdf_file_valid


def reverse_pdf_order_window():
    layout = [
        [sg.InputText(key="-INPUT-"), sg.Button("Select")],
        [sg.Button("Reverse PDF", key="-REVERSE-")]
    ]
    window = sg.Window("Reverse PDF", layout=layout)
    pdf_file = ""
    pdf_file_pike = None
    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSED:
                break
            case "Select":
                pdf_file = sg.popup_get_file("Input valid PDF file")
                logger.debug(f"PDF filename supplied {pdf_file}")
                if pdf_file:
                    valid, pdf_file_pike = is_pdf_file_valid(pdf_file)
                    if not valid:
                        pdf_file_pike = None
                        logger.debug(f"PDF file not valid")
                        sg.popup_error("Please input only valid PDF file")
                        continue
                window["-INPUT-"].update(pdf_file)
            case "-REVERSE-":
                if not pdf_file_pike:
                    sg.popup_error("Please input a pdf file")
                    continue
                try:
                    pdf_file_pike.pages.reverse()
                    path = PurePath(pdf_file)
                    output_file = path.parent.joinpath(path.stem + "-reversed" + path.suffix)
                    pdf_file_pike.save(str(output_file))
                    logger.debug(f"{output_file} saved")
                    sg.popup(f"PDF file reversed. Saved at {output_file}")
                except PdfError:
                    sg.popup_error("Something went wrong. Please check input file.")
                pdf_file = ""
                window["-INPUT-"].update("")
    window.close()
