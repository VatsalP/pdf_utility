import base64
from typing import List, ParamSpec

import PySimpleGUI as sg
from pikepdf import Pdf, PdfError, Encryption, PasswordError

P = ParamSpec('P')


def is_pdf_file_valid(file: str, password: str = "") -> (bool, str | Pdf):
    """
    Check if files is valid pdf

    :param file: pdf file to check
    :param password: password of the file
    :return: True and pdf object if no invalid pdf file or False and invalid file name
    """
    try:
        pdf = Pdf.open(file, password=password)
        return True, pdf
    except PasswordError:
        password = sg.PopupGetText(f"PDF file {file} needs password to open. Please input:")
        return is_pdf_file_valid(file, password=password)
    except PdfError:
        return False, file


def are_pdf_files_valid(files: List[str]) -> (bool, List[str | Pdf]):
    """
    Check if files are valid or not

    :param files: pdf files to be merged or not
    :return: True and pdf objects if no invalid pdf files or False and invalid file names
    """
    pdf_files = []
    invalid_files = []
    for file in files:
        valid, pdf = is_pdf_file_valid(file)
        if valid:
            pdf_files.append(pdf)
        else:
            invalid_files.append(file)
    return (True, pdf_files) if not invalid_files else (False, invalid_files)


def merge_pdf(files_to_merge: List[Pdf], to_merge_file: str, password: str):
    """
    Merge files to provide pdf file with optional password

    :param files_to_merge:
    :param to_merge_file:
    :param password:
    """
    encryption = None
    if password:
        encryption = Encryption(owner=password, user=password)
    pdf = Pdf.new()
    version = pdf.pdf_version
    for i, file in enumerate(files_to_merge):
        sg.one_line_progress_meter("Merging PDFs...", i + 1, len(files_to_merge), key="-PROGRESS_PDF-")
        version = max(version, file.pdf_version)
        pdf.pages.extend(file.pages)
    pdf.remove_unreferenced_resources()
    pdf.save(to_merge_file, encryption=encryption, min_version=version)
    sg.one_line_progress_meter_cancel(key="-PROGRESS_PDF-")


def center(*elements: P.args) -> list:
    """Center your elements

    :param elements: n number of sg elements or anything
    :return: list with vpush and push added to front and back
    """
    return [sg.VPush(), sg.Push(), *elements, sg.Push(), sg.VPush()]


def load_image(image_file: str) -> bytes:
    with open(image_file, 'rb') as image:
        return base64.b64encode(image.read())
