# Dmatrix
Dmatrix assingment

Initial understanding:
Task 1: Verify if the vendor is correct for a given product.
What exactly mean by verifying the correct vendor, is it that the given vendor website exists or not? or the PRODNAME exists in the given vendor website?

earlier assumption is fairly easy to achieve by fetching the status code of the vendor website (and it will be very fast). For the later assumption we can fetch raw HTML content of homepage and check if the PRODNAME name exists in those contents (most time consuming part).

Task 2: Last Vendor
I'm assuming that, if the given vendor VENDOR_WEBSITE is redirecting to some other URL/domain then I can consider the given VENDOR_WEBSITE is the last vendor and the redirect URL/domain is the new vendor. Is my assumption right?

Task 3: Is the parent category appropriate?
Read parent category of each PRODNAME from catalog and see if it is there in given Cat-SubCategory list.

Task 4: Is the sub-category appropriate?
Read SubCategory of each PRODNAME from catalog and see if it is there in Cat-SubCategory list.

Task 5: Validate Category-SubCategory combinations
Read Parent-Category:Sub-Category of each PRODNAME from catalog and see if it is there in given Cat-SubCategory list and relation hierarchy present.

High-level approach:
1. Collect the data for Parent and Sub-categories.
2. Create 3 Dictionary objects to store parent categories, Sub-categories and their relation.
3. Read test data into iterator object.
4. Using multi-processing to process test data in parallel.
	4.1. Now checking for the product vendor (VENDOR_WEBSITE), if it is the correct vendor otherwise picking the current vendor and tracking the previous vendor (LAST_VENDOR).
	4.2. Verifying the parent category of each PRODNAME and its relation with Sub-category.
	4.3 Verifying the sub-category of each PRODNAME and its relation with Parent category.
	4.4 Verifying the Parent-Sub-Category combos.
5. Collecting the data from each process and writing it to new result file.

How to analyze results:
Final result sheet can found under 'reports' folder of project, however the path is configurable through myconfig.py. While analyzing results sheet, please be informed that 1=True and 0=False, using 1 & 0 instead of string saves a lot memory.

Configurable parameters:
Please note that I've provided flexibility for some parameters, like file locations and thread counts. Please refer myconfig.py under 'config' folder in the project folder.
List of configurable parameters:
1. file_path (path to input file like '../testdata/QCSampleProblem.xlsx')
2. sheet1 (name of Catalog sheet with in an excel file)
3. sheet2 (name of 'Cat-SubCat' sheet with in an excel file)
4. reports_location (path to save final results like '../reports/')
5. thread_count (number of threads to achieve multiprocessing like 8,12,16 & 24 etc.)

Instructions to run project:
1. Clone the repo using https://github.com/vivek1723/Dmatrix.git
2. Configure the python interpreter if it asks for.
3. Install dependencies using pip install -r requirements.txt
4. Run test.py to run the test, it will send logs to console.

Note: Please note that I've not implied exception handling as of now.

Performance:
I've tested 2k data rows using a Quadcore CPU with 4GB RAM on 15 mbps broadband internet connection and following is performance result I observed:
1. Threads: 2, CPU usage: very low, Total time: ~18 mins 21 seconds
2. Threads: 10, CPU usage: Low, Total time: ~6 mins 37 seconds
3. Threads: 16, CPU usage: Low-Medium, Total time: ~4 mins 17 seconds
4. Threads: 24, CPU usage: Medium-High , Total time: ~2 mins 7 seconds

The 'Total time' is affected by network latency, Ram and CPU.