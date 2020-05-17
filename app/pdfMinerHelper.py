from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (
    LAParams,
    LTAnno,
    LTChar,
    LTTextLineHorizontal,
    LTTextLineVertical,
    LTImage,
)


def get_page_layout_for_all_pages(  filename,
                                    char_margin=1.0,
                                    line_margin=0.5,
                                    word_margin=0.1,
                                    detect_vertical=True,
                                    all_texts=True,
                                    ):
    pageObjects = []
    with open(filename, "rb") as f:
            parser = PDFParser(f)
            document = PDFDocument(parser)
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            laparams = LAParams(
                char_margin=char_margin,
                line_margin=line_margin,
                word_margin=word_margin,
                detect_vertical=detect_vertical,
                all_texts=all_texts,
            )
            rsrcmgr = PDFResourceManager()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                layout = device.get_result()
                width = layout.bbox[2]
                height = layout.bbox[3]
                pageObjects.append(layout)
    return pageObjects


def get_pdfMiner_objects(layout, ltype="char", t=None):    
    if ltype == "char":
        LTObject = LTChar
    elif ltype == "image":
        LTObject = LTImage
    elif ltype == "horizontal_text":
        LTObject = LTTextLineHorizontal
    elif ltype == "vertical_text":
        LTObject = LTTextLineVertical
    if t is None:
        t = []
    try:
        for obj in layout._objs:
            if isinstance(obj, LTObject):
                t.append(obj)
            else:
                t += get_pdfMiner_objects(obj, ltype=ltype)
    except AttributeError:
        pass
    return t
