# ResourceGuardians

Goal:

We are trying to create a website or software (likely a website) with python DASH to allow inserts of data files to be then converted into graphs showing energy usage across campus. The idea is that our working algorithm will automatically extract, sort, convert, and display the final data without extra work. Right now we are working with CSV files but that can be extended by future teams if need be. Currently we are trying to display base on different energy usage due to not having enough data by location (according to client, Wilmington will have next to nothing if compared side by side with Newark). However we want to keep the locations there for future work and extensions. 

Deployment page includes 2 links, one for sorting and file input and one for graph with python dash.

Not included in final code:

1. Multiplecsv: Able to upload mutilple CSV files with their own keys using a dictionary. Each of the uploaded csvs have their own hash and can be accessed with different keys.
2. Needlemanwunsch: A customized implementation of the Needleman-Wunsch protein comparison algorithm, redesigned to correct spelling errors. It takes three parameters, an input string, a set of target strings, and a gap cost (as of now, designed around a cost of 10). It created a dynamic programming table comparing the input to each target string, and whichever of those has the greatest value is returned as the selection. As the files were observed to have inconsistent spelling when it came to data such as addresses, this algorithm should alleviate some of the discrepancies.

Next Steps:

Current website does not work with client data, graph is currently using sample data. Sorting algorithm does not return csv to be used with dash. Need to connect the 2 dots first. 

1. Make sure sorting algorithm returns a sorted csv file at the end to input into dash.
2. Check over code, change local link to udel links to work for public.
3. CLient wants a step by step how to once everything is working.
4. Making website more public and accessible.
5. Creating more unique graphs to fit client need.
6. Obtain more data(dash works well with csv files and client can provide either csv or pdf, recommend csv)

