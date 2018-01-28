import os
from multiprocessing import Pool
import pandas as pd
from config import myconfig
from logSetup import logSetup as CL
from utils import req

# create 3 empty dicts to hold, parent categories, sub-categories and their combos
parentCats = {}
subCats = {}
parentSubCat = {}

# hold data by worker
dataDict = {}

log = CL.consoleLogger()


# noinspection PyBroadException
def worker_fetch(rowData):
    name, pType, pCat, sCat, url = rowData[1][0], rowData[1][1], rowData[1][2], rowData[1][3], rowData[1][4]
    log.info("Product Name: %s, Parent Catagory: %s, Sub-category: %s, Vendor: %s" % (name, pCat, sCat, url))
    global dataDict
    same, nUrl, prodFound, st = req.fetch(url, name, dataDict)

    global subCats
    global parentCats
    global parentSubCats

    isParentCatPresent = 1
    isSubCatPresent = 1
    isSubCatParentCatRelated = 1

    try:
        if not parentCats[pCat]:
            isParentCatPresent = 0
    except:
        pass

    try:

        if not subCats[sCat]:
            isSubCatPresent = 0
    except:
        pass

    try:
        if not parentSubCat[sCat][pCat]:
            isSubCatParentCatRelated = 0
    except:
        pass

    if nUrl:
        url, nUrl = nUrl, url

    rowVal = [name, pType, pCat, sCat, url, nUrl, prodFound, isParentCatPresent, isSubCatPresent,
              isSubCatParentCatRelated]
    return rowVal


if __name__ == "__main__":
    # parse Cat-SubCat sheet
    df = pd.ExcelFile(myconfig.file_path)
    catCombos = df.parse(myconfig.sheet2)  # Cat-SubCat sheet

    for row in catCombos.iterrows():
        c1, c2 = row[1][0], row[1][1]
        parentCats[c1] = 1
        subCats[c2] = 1
        # noinspection PyBroadException
        try:
            parentSubCat[c2][c1] = 1
        except:
            parentSubCat[c2] = {}
            parentSubCat[c2][c1] = 1

    # parse parent catalog sheet
    testCat = df.parse(myconfig.sheet1)
    # open threads=thread_count
    pool = Pool(myconfig.thread_count)
    # maps threads with
    res = pool.map(worker_fetch, testCat.iterrows(), chunksize=1)
    pool.close()
    pool.join()
    # Define the columns needed for result file , Status: 1=True and 0=False
    exCols = [
        'PRODNAME', 'PROD_TYPE', 'PARENT_CAT', 'SUB_CAT', 'VENDOR_WEBSITE', 'LAST_VENDOR',
        'PRODNAME STATUS', 'PARENT APPR', 'SUBCAT APPR', 'PARENT-SUB COMBOS',
    ]

    df = pd.DataFrame(columns=exCols)
    log.info("Preparing results")

    rowdf = [pd.DataFrame([r], columns=exCols) for r in res]
    df = pd.concat(rowdf)
    # Creates the reports directory if it doesn't exists

    os.makedirs(os.path.dirname(myconfig.reports_location), exist_ok=True)
    # Write the dataframe to final result file
    df.to_excel(myconfig.reports_location + 'results.xlsx', index=False)
    log.info("Results saved to results file")
