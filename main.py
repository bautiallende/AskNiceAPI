import requests
from requests import Session
from pprint import pprint as pp
import pandas as pd



"""
We will see a series of variables that it is possible to modify with the indicated parameters.

Parameters for the Responses table: 
"""

# sort_direction: (Optional) This can have 2 alternatives "desc" (decending) or "asc" (ascending).
sort_d = True
sort_direction = 'desc'

# pagesize: (Required) page size (Default is 50,000 per request; maximum is 50,000 per request)
pagesize = 50

# pagenumber: (Required) Current page starting at 1, being the first page.
pagenumber = 1

# since_time: (Required) Pass in a unix timestamp to set the 'after date' from which up to which you want to get all responses for
since_time = 0

# format: (Optional) Leave blank or set to "json" to get data in json format "csv" to get data in csv format
format_status = True
format = 'json'

# filter: (Optional) Leave blank or "answered" for all survey responses "raw" for all surveys sent, this includes surveys sent and have not been responded to. "published" for only customer testimonials
filter_status = False
filter = ''

# sort_by: (Optional) Leave blank or "sent" to sort by survey sent date "responded" to sort by survey response date
sort_status = False
sort_by = 'responded'

#end_time: (Optional) Leave blank to default the date to now or pass in a unix timestamp to set the 'before date' up to which you want to get all responses for.
end_time_status = False
end_time = 0


# I create a dictionary for the variables
dic_p = {}
if sort_d == True:
    dic_p['sort_direction'] = sort_direction
dic_p['pagesize'] = pagesize
dic_p['pagenumber'] = pagenumber
dic_p['since_time'] = since_time
if format_status == True:
    dic_p['format'] =  format

if filter_status == True:
    dic_p['filter'] = filter
if sort_status == True:
    dic_p['sort_by'] = sort_by
if end_time_status == True:
    dic_p['end_time'] = end_time
print(f'The dictionary with the parameters will look like this: {dic_p}')



class ASK:
    # Documentacion:
    # https://asknicely.asknice.ly/help/apidocs/auth
    def __init__(self, token):
        self.apiurl = "https://DEMO.asknice.ly/api" # Change the url to the one associated with AskNice
        # CI create the headers to enter the token
        self.headers = {'X-apikey': token}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getResponses(self):
        extencion = ''

        # I scroll through the dic to get the parameters and add them to the extension
        len_dic = len(dic_p)
        for key, values in dic_p.items():
            if len_dic > 1:
                extencion += str(values) + '/'
            elif len_dic == 1:
                extencion += str(values)
            len_dic -= 1

        # Url extension where you will get the info from
        url = self.apiurl + '/v1/responses/' + extencion
        print(f'The Url will look like this {url}')
        r = self.session.get(url)
        print(f'The server response number is: {r}')

        try:
            if dic_p["format"] == 'json':
                # We store important information communicated to us by the server
                total_pages = r.json()['totalpages']
                page_number = r.json()['pagenumber']
                page_size = r.json()['pagesize']

                # For more important data, please remove the # below
                #print(f"The data returned by the server is: {r.json()}")

                data = r.json()['data']
                # We transform the data into a DF for easier manipulation and then select the columns we are interested in.
                df = pd.DataFrame(data)
                df = df[["account_id_c", "email", "answer", "topic_c", "comment", "csat_question_csat_c", "sent", "opened", "responded", "lastemailed", "account_status_c", "theme"]]
                # Save the DF in the file Responses.csv
                df.to_csv("Responses.csv")
                print(f"The CSV was saved successfully! The total number of pages on the website is: {total_pages}, e page we are analyzing at the moment is: {page_number}, and the page size is {page_size}")

            elif dic_p["format"] == 'csv':
                print(f'The information it brings in the form of a csv is: {r}')

        except:
            print("An error occurred")
            pass

        return print("Process completed!")

ask = ASK(#TOKEN)
pp(ask.getResponses())