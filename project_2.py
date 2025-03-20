from bs4 import BeautifulSoup
import re
import os
import csv
import unittest

# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"

An example of that within the function would be:
    open("filename", "r", encoding="utf-8-sig")

There are a few special characters present from Airbnb that aren't defined in standard UTF-8 (which is what Python runs by default). This is beyond the scope of what you have learned so far in this class, so we have provided this for you just in case it happens to you. Good luck!
"""

def load_listing_results(html_file): 
    """
    INPUT: A string containing the path of the html file
    RETURN: A list of tuples
    """
    listing_results = []
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html,"html.parser")
    listings = soup.find_all("div", class_="t1jojoys dir dir-ltr")
    for listing in listings:
        title = listing.text
        id_ref = listing.get("id")
        id_num = re.search(r"title_(\d+)",id_ref)#looks for patten that matches 
        id_str = id_num.group(1)
        listing_results.append((title, id_str)) 
        # print(listing_results)
    return listing_results
def get_listing_details(listing_id): 
    """
    INPUT: A string containing the listing id
    RETURN: A tuple
    """
    file = f"html_files/listing_{listing_id}.html"
    with open(file, "r", encoding="utf-8")as f: #reads in the files into the html
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")

        pul = soup.find("ul", class_="fhhmddr dir dir-ltr")#
        pli = pul.find("li", class_="f19phm7j dir dir-ltr")#Looks for the list
        policy_tag = pli.find("span", class_="ll4r2nl dir dir-ltr")
        p_str = policy_tag.text.replace("\ufeff", "").strip()#takes off \ufeff and any whiespace

        h_div = soup.find("div", class_="_dm2bj1")# locates where in the html file the class in in 
        h_tag = h_div.find("span", class_= "_1mhorg9")
        if h_tag:
            h_str = h_tag.text
        else:
            h_str ="regular"

        nameh_div = soup.find("div", class_="tehcqxo dir dir-ltr")

        nameh_tag = nameh_div.find("h2", {'class': "hnwb2pb dir dir-ltr"})

        title_h = nameh_tag.text
        obj_h = re.search(r"Hosted by (.+)", title_h)
        str_h = obj_h.group(1)

        pla_tag = soup.find("div", class_="_tqmy57")
        pla_txt = pla_tag.text
        if "private" in pla_txt:#setting type of room
            plac_str = "Private Room"
        elif "share" in pla_txt:
            plac_str = "Shared Room"
        else:
            plac_str = "Entire Room"

        rev_div = soup.find("div", class_="_dm2bj1")
        rev_span = rev_div.find("span", class_="_s65ijh7")
        if rev_span:
            rev_tag = rev_span.find("button", class_="l1j9v1wn bbkw4bl c1rxa9od dir dir-ltr")
            rev_txt = rev_tag.text
            rev_obj = re.search(r"\d+", rev_txt)# finds the number of reviews using regex pattern
            rev_str = rev_obj.group(0)
            rev_int = int(rev_str)
        else:
            rev_int = 0 #defualt to 0 if none is found

        r_div = soup.find("div", class_="_1jo4hgw")
        r_tag = r_div.find("span", class_="_tyxjp1")
        r_txt = r_tag.text
        r_obj = re.search(r"\d+", r_txt)
        r_str = r_obj.group(0)
        r_int = int(r_str)
        return((p_str, h_str, str_h, plac_str, rev_int, r_int))

def create_listing_database(html_file): 
    """
    INPUT: A string containing the path of the html file
    RETURN: A list of tuples
    """
    listing_info = []
    load_lists = load_listing_results(html_file)
    for listing in load_lists:
        list_id = listing[1]#listing id
        list_detials = get_listing_details(list_id)#returns another tuple
        listing_info.append((listing + list_detials))#combinding listing and list deatials
    return listing_info 


def output_csv(data, filename): 
    """
    INPUT: A list of tuples and a string containing the filename
    RETURN: None
    """
    sort_data = list(sorted(data, key = lambda num_review: num_review[6], reverse=True))#sorts based on number of reviews by index, in descending order, then puts them into a sorted list
    header = (("Listing Title", "Listing ID", "Policy Number", "Host Level","Host Name(s)", "Place Type", "Review Number", "Nightly Rate"))
    with open(filename, 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(sort_data)

def validate_policy_numbers(data):
    """
    INPUT: A list of tuples
    RETURN: A list of tuples
    """
    invalid_p = []
    form1 = r"20[\d+]{2}-00[\d+]{4}STR"
    form2 = r"STR-000[\d+]{4}"
    for listing in data:
        policy = listing[2]
        if policy == "pending" or policy == "exempt":
            continue
        elif re.search(form1, policy) or re.search(form2, policy):
            pass
        else:
            invalid_p.append((listing[4], listing[1], policy))
        return(invalid_p)

# EXTRA CREDIT 
def google_scholar_searcher(query): 
    """
    INPUT: query (str)
    Return: a list of titles on the first page (list)
    * see PDF instructions for more details
    """
    pass


# TODO: Don't forget to write your test cases! 
class TestCases(unittest.TestCase):
    def setUp(self):
        self.listings = load_listing_results("html_files/search_results.html")

    def test_load_listing_results(self):

        # check that the number of listings extracted is correct (18 listings)
        self.assertEqual(len(self.listings), 18)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(self.listings), list)

        # check that each item in the list is a tuple
        for item in self.listings:
            self.assertEqual(self.listings[0], ('Loft in Mission District', '1944564'))
        # check that the first title and listing id tuple is correct (open the search results html and find it)
            self.assertEqual(self.listings[-1], ('Guest suite in Mission District', '467507'))
        # check that the last title and listing id tuple is correct (open the search results html and find it)

    def test_get_listing_details(self):
        html_list = ["467507",
                     "1550913",
                     "1944564",
                     "4614763",
                     "6092596"]
        
        # call get_listing_details for i in html_list:
        listing_information = [get_listing_details(id) for id in html_list]

        # check that the number of listing information is correct
        self.assertEqual(len(listing_information), 5)
        for info in listing_information:
            # check that each item in the list is a tuple
            self.assertEqual(type(info), tuple)
            # check that each tuple has 6 elements
            self.assertEqual(len(info), 6)
            # check that the first four elements in the tuple are strings
            self.assertEqual(type(info[0]), str)
            self.assertEqual(type(info[1]), str)
            self.assertEqual(type(info[2]), str)
            self.assertEqual(type(info[3]), str)
            # check that the rest two elements in the tuple are integers
            self.assertEqual(type(info[4]), int)
            self.assertEqual(type(info[5]), int)

        # check that the first listing in the html_list has the correct policy number
        self.assertEqual(listing_information[0][0], 'STR-0005349')
        # check that the last listing in the html_list has the correct place type
        self.assertEqual(listing_information[-1][3], 'Entire Room')
        # check that the third listing has the correct cost
        self.assertEqual(listing_information[2][-1], 181)

    def test_create_listing_database(self):
        detailed_data = create_listing_database("html_files/search_results.html")

        # check that we have the right number of listings (18)
        self.assertEqual(len(detailed_data), 18)

        for item in detailed_data:
            # assert each item in the list of listings is a tuple
            self.assertEqual(type(item), tuple)
            # check that each tuple has a length of 8

        # check that the first tuple is made up of the following:
        # ('Loft in Mission District', '1944564', '2022-004088STR', 'Superhost', 'Brian', 'Entire Room', 422, 181)
        self.assertEqual(detailed_data[0], ('Loft in Mission District', '1944564', '2022-004088STR', 'Superhost', 'Brian', 'Entire Room', 422, 181))
        # check that the last tuple is made up of the following:
        # ('Guest suite in Mission District', '467507', 'STR-0005349', 'Superhost', 'Jennifer', 'Entire Room', 324, 165)
        self.assertEqual(detailed_data[-1], ('Guest suite in Mission District', '467507', 'STR-0005349', 'Superhost', 'Jennifer', 'Entire Room', 324, 165))
    def test_output_csv(self):
        # call create_listing_database on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_listing_database("html_files/search_results.html")

        # call output_csv() on the variable you saved
        output_csv(detailed_data, "test.csv")

        # read in the csv that you wrote
        csv_lines = []
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for i in csv_reader:
                csv_lines.append(i)

        # check that there are 19 lines in the csv
        self.assertEqual(len(csv_lines), 19)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Listing Title', 'Listing ID', 'Policy Number', 'Host Level', 'Host Name(s)', 'Place Type', 'Review Number', 'Nightly Rate'])
        # check that the next row is the correct information about Guest suite in San Francisco
        self.assertEqual(csv_lines[1], ['Guest suite in San Francisco', '6092596', 'STR-0000337', 'Superhost', 'Marc', 'Entire Room', '713', '164'])
        # check that the row after the above row is the correct infomration about Private room in Mission District
        self.assertEqual(csv_lines[2], ['Private room in Mission District', '16204265', '1081184', 'Superhost', 'Koncha', 'Shared Room', '520', '127'])

    def test_validate_policy_numbers(self):
        # call create_listing_database on "html_files/search_results.html"
        # and save the result to a variable
        detailed_data = create_listing_database("html_files/search_results.html")

        # call validate_policy_numbers on the variable created above and save the result as a variable
        invalid_listings = validate_policy_numbers(detailed_data)

        # check that the return value is a list
        self.assertEqual(type(invalid_listings), list)

        # check that the elements in the list are tuples
        # and that there are exactly three element in each tuple
        for item in invalid_listings:
            self.assertEqual(type(item), tuple)
def main (): 
    detailed_data = create_listing_database("html_files/search_results.html")
    output_csv(detailed_data, "airbnb_dataset.csv")

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)