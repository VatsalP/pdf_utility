import PySimpleGUI as sg
from loguru import logger

from pdf_utility_belt.helpers.utility import are_pdf_files_valid, merge_pdf


def pdf_merge_window():
    layout = [
        [sg.Button("PDF file to merge to", key="-PDF_FILE-", size=(20, 1)),
         sg.InputText(key="-PDF_FILE_VAL-", size=(27, 1))],
        [sg.Button("Select PDF Files", key="-Select-", size=(20, 1)),
         sg.Multiline(size=(25, 10), key="-FILES_MERGE-")],
        [sg.Text("Optional Password:", font="bold", size=(18, 1)),
         sg.InputText(default_text="", key="-PASS-", size=(27, 1))],
        [sg.Button("Merge", size=(50, 1))]
    ]
    merge_window = sg.Window("Merge PDFs", layout=layout, size=(400, 280))
    valid = False
    to_merge_file = ""
    files_to_merge = []
    while True:
        event, values = merge_window.read()
        logger.debug(f"{event} {values}")
        match event:
            case sg.WIN_CLOSED:
                break
            case "-PDF_FILE-":
                to_merge_file = sg.popup_get_file("PDF Merge File", save_as=True)
                merge_window["-PDF_FILE_VAL-"].update(to_merge_file)
                logger.debug(f"Merge file {to_merge_file}")
            case "-Select-":
                file_names = sg.popup_get_file("PDF Files to merge", multiple_files=True)
                file_names = file_names.split(";")
                logger.debug(f"Files to merge: {file_names}")
                valid, files = are_pdf_files_valid(file_names)
                if not valid:
                    logger.debug(f"Invalid files {files}")
                    sg.popup_error(
                        "Pass Only Valid Pdf Files\nInvalid PDF files:\n"
                        "\n".join(files),
                        title="Invalid PDF files"
                    )
                    continue
                merge_window["-FILES_MERGE-"].update("Selected\n" + "\n".join(file_names))
                files_to_merge = files
            case "Merge":
                if valid and to_merge_file:
                    merge_pdf(files_to_merge, to_merge_file, password=values["-PASS-"])
                    sg.popup(f"PDF files merged to {to_merge_file}")
                    valid, to_merge_file, files_to_merge = False, "", []
                    merge_window["-FILES_MERGE-"].update("")
                    merge_window["-PDF_FILE_VAL-"].update("")
                else:
                    sg.popup_auto_close("PDF files and Merge files have to be selected")
            case _:
                pass

    merge_window.close()
