from typing import List

import PySimpleGUI as sg
from pikepdf import Pdf, PdfError, Encryption


def are_pdf_files_valid(files: List[str]) -> (bool, List[str | Pdf]):
    """
    Check if files are valid or not

    :param files: pdf files to be merged or not
    :return: True and pdf objects if no invalid pdf files or False and invalid file names
    """
    pdf_files = []
    invalid_files = []
    for file in files:
        try:
            pdf = Pdf.open(file)
            pdf_files.append(pdf)
        except PdfError:
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
    for i, file in enumerate(files_to_merge):
        sg.one_line_progress_meter("Merging PDFs...", i + 1, len(files_to_merge), key="-PROGRESS_PDF-")
        pdf.pages.extend(file.pages)
    pdf.save(to_merge_file, encryption=encryption)
    sg.one_line_progress_meter_cancel(key="-PROGRESS_PDF-")
