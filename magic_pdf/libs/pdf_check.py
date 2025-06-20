import fitz
import numpy as np
from loguru import logger
import re
from io import BytesIO
from pdfminer.high_level import extract_text


def calculate_sample_count(total_page: int):
    select_page_cnt = min(10, total_page)
    return select_page_cnt


def extract_pages(src_pdf_bytes: bytes) -> fitz.Document:
    pdf_docs = fitz.open("pdf", src_pdf_bytes)
    total_page = len(pdf_docs)
    if total_page == 0:

        logger.warning("PDF is empty, return empty document")
        return fitz.Document()
    select_page_cnt = calculate_sample_count(total_page)

    page_num = np.random.choice(total_page, select_page_cnt, replace=False)
    sample_docs = fitz.Document()
    try:
        for index in page_num:
            sample_docs.insert_pdf(pdf_docs, from_page=int(index), to_page=int(index))
    except Exception as e:
        logger.exception(e)
    return sample_docs


def detect_invalid_chars(src_pdf_bytes: bytes) -> bool:
    sample_docs = extract_pages(src_pdf_bytes)
    sample_pdf_bytes = sample_docs.tobytes()
    sample_pdf_file_like_object = BytesIO(sample_pdf_bytes)
    text = extract_text(sample_pdf_file_like_object)
    text = text.replace("\n", "")
    # logger.info(text)
    cid_pattern = re.compile(r'\(cid:\d+\)')
    matches = cid_pattern.findall(text)
    cid_count = len(matches)
    cid_len = sum(len(match) for match in matches)
    text_len = len(text)
    if text_len == 0:
        cid_chars_radio = 0
    else:
        cid_chars_radio = cid_count/(cid_count + text_len - cid_len)
    logger.info(f"cid_count: {cid_count}, text_len: {text_len}, cid_chars_radio: {cid_chars_radio}")
    if cid_chars_radio > 0.05:
        return False
    else:
        return True


def count_replacement_characters(text: str) -> int:
    return text.count('\ufffd')


def detect_invalid_chars_by_pymupdf(src_pdf_bytes: bytes) -> bool:
    sample_docs = extract_pages(src_pdf_bytes)
    doc_text = ""
    for page in sample_docs:
        page_text = page.get_text('text', flags=fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_MEDIABOX_CLIP)
        doc_text += page_text
    text_len = len(doc_text)
    uffd_count = count_replacement_characters(doc_text)
    if text_len == 0:
        uffd_chars_radio = 0
    else:
        uffd_chars_radio = uffd_count / text_len
    logger.info(f"uffd_count: {uffd_count}, text_len: {text_len}, uffd_chars_radio: {uffd_chars_radio}")
    if uffd_chars_radio > 0.01:
        return False
    else:
        return True