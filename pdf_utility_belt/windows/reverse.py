from pathlib import PurePath

import PySimpleGUI as sg
from loguru import logger
from pikepdf import Pdf, PdfError

from pdf_utility_belt.helpers.utility import are_pdf_files_valid


def reverse_pdf_order_window():
    layout = [
        [sg.InputText(key="-INPUT-"), sg.Button("Select")],
        [sg.Button("Reverse PDF", key="-REVERSE-")]
    ]
    window = sg.Window("Reverse PDF", layout=layout, size=(430, 90))
    pdf_file = ""
    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSED:
                break
            case "Select":
                pdf_file = sg.popup_get_file("Input valid PDF file")
                logger.debug(f"PDF filename supplied {pdf_file}")
                if pdf_file and not are_pdf_files_valid([pdf_file]):
                    logger.debug(f"PDF file not valid")
                    sg.popup_error("Please input only valid PDF file")
                    continue
                window["-INPUT-"].update(pdf_file)
            case "-REVERSE-":
                if not pdf_file:
                    sg.popup_error("Please input a pdf file")
                    continue
                try:
                    pdf = Pdf.open(pdf_file)
                    if pdf.is_encrypted:
                        password = sg.popup_get_text("Password for the file")
                        pdf = Pdf.open(pdf_file, password=password)
                    pdf.pages.reverse()
                    path = PurePath(pdf_file)
                    output_file = path.parent.joinpath(path.stem + "-reversed" + path.suffix)
                    pdf.save(str(output_file))
                    logger.debug(f"{output_file} saved")
                    sg.popup(f"PDF file reversed. Saved at {output_file}")
                except PdfError:
                    sg.popup_error("Something went wrong. Please check input file.")
                pdf_file = ""
                window["-INPUT-"].update("")
    window.close()
