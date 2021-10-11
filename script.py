#Kousalya Lakshmanan - Adobe Case Study - Data Engineer Role - Hit Level Data
#AWS Lambda, S3

#Importing the necessary packages
import sys
from datetime import datetime
from io import StringIO

import boto3
from decouple import config
import numpy as np
import pandas as pd

#getting current date
now = datetime.today().strftime("%Y-%m-%d")

#naming the file with the current date
file_name = f"{now}_SearchKeywordPerformance.tab"
bucket_name = config("bucket_name")

#access keys - IAM role - Kousalya
aws_access_key_id = config("aws_access_key_id")
aws_secret_access_key = config("aws_secret_access_key")

#in-memory file like object fro parsing
csv_buffer = StringIO()

s3 = boto3.client(
    "s3", 
    aws_access_key_id=aws_access_key_id, 
    aws_secret_access_key=aws_secret_access_key
)



class KeywordRevenueFinder:
#Takes the filename as argument    
    def revenue_finder(self, file):
        try:
            #reads the TSV file
            data = pd.read_csv(file, sep='\t')
            
            #considering the revenue value, splitting and considering the 3rd value from the eg format
            data[["revenue"]] = data.product_list.str.split(';', expand=True)[3]
            
            #Total Revenue: Revenue is considered only when the purchase event is set to 1     
            #1:Purchase

            data["revenue"] = np.where(
                data["event_list"] != 1, 
                data["revenue"].replace(r"^\s*$", 0, regex=True),
                data["revenue"]
                )
            
            #search engine domain is extracted from the referrer column
            data['referrer'] = data["referrer"].str.extract("http[s]?://([A-Za-z_0-9.-]+).*")
            search_engines = data['referrer']
            keywords = data["pagename"]
            revenue = data["revenue"]
            
            #creating a dataframe from the extracted column values
            df = pd.DataFrame(columns=["Search Engine Domain", "Search Keyword", "Revenue"])
            df["Search Engine Domain"] = search_engines
            df["Search Keyword"] = keywords
            df["Revenue"] = revenue

            #replacing NaN values with zeros
            df["Revenue"] = df.Revenue.fillna(0).astype(int)
            
            #Sorting the Revenue in decending order
            df = df.sort_values(by=["Revenue"], ascending=False)
            
            df.to_csv(csv_buffer, sep='\t')
            
            #sending the file to s3 bucket
            response = s3.put_object(
                Bucket=bucket_name, 
                Body=csv_buffer.getvalue(), 
                Key=file_name,
                ACL="public-read"
            )
            print("Data Converted Successfully and uploaded to S3")

            #printing the final output
            print(df)

            #summary of the data
            print(df.describe())

            print(pd.crosstab(df["Search Keyword"], df["Revenue"]))
            return response
        except Exception as error:
            print(error)


finder = KeywordRevenueFinder()
finder.revenue_finder(sys.argv[1])
