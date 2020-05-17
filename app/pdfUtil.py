from pdfMinerHelper import get_page_layout_for_all_pages,get_pdfMiner_objects
def checkIfPdfIsDigital(filePath):
    isDigital = False 
    pageObjs = get_page_layout_for_all_pages(filePath)
    for pageObj in pageObjs:
        print('processing page')
        ht_objs = get_pdfMiner_objects(pageObj,'horizontal_text')
        vt_objs = get_pdfMiner_objects(pageObj,'vertical_text')
        if len(ht_objs) != 0 or len(vt_objs) != 0:
            return True
    return isDigital


def getAllTextObj(filePath):
    textObj  = []
    pageObjs = get_page_layout_for_all_pages(filePath)
    for pageObj in pageObjs:
        ht_objs = get_pdfMiner_objects(pageObj,'horizontal_text')
        vt_objs = get_pdfMiner_objects(pageObj,'vertical_text')
        if len(ht_objs) != 0:
            for minerobj  in ht_objs:
                textObj.append(minerobj.get_text())
            for minerobj in vt_objs:
                textObj.append(minerobj.get_text())
    return textObj


