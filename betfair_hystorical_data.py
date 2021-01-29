import pandas as pd
import json
from bz2 import BZ2File
import os
import openpyxl
import copy
print("Program is running! Close the excel file if open, otherwise the program will crash :D")




main_directory = os.getcwd()
excel_file_name = "all_data.xlsx"

def get_bz2_data(file_name, date, current_df):
    """This function returns a dataframe with the market information from a file, this means that it will only gather information from one event only"""
    cols = ["Event_Name", "Date", "pt", "mc__marketDefinition__inPlay", "mc__marketDefinition__runners__id", "mc__marketDefinition__runners__name", "mc__marketDefinition__runners__id2", "mc__marketDefinition__runners__name2", "mc__rc__ltp", "mc__rc__id"]
#     print(f"Getting data from {file_name} played on {date}")
    ### This block reads the file and creates the empty list for the data
    with BZ2File(file_name, "r") as file:
        lines = file.readlines()
    os.chdir(main_directory)
    
    data = []
    
    first_line = True
    ### This is the main block that tries to update the market definition (event name and others) if there is one, as well as the lpc
    for line in lines:
        linedata = []
        # This loads the market changes of each individual line
        content = json.loads(line)
        market_changes = content.get("mc")[0]
        # Getting the pt
        pt = content.get("pt")
        ### This block tries to get the information of the event from the marketDefinition, if possible. The event name is updated only once. 
        try:
            #This tries to get the marketDefinition, if it isn't there then it jumps out of the try
            market_definition = market_changes.get('marketDefinition')
            # Getting the event name, it is updated only once since the name shouldn't change.
            if first_line == True:
                event_name = market_definition.get("eventName")
                first_line == False
            
            
            # Getting mc__marketDefinition__inPlay
            inPlay = market_definition.get("inPlay")
                       
            # Getting mc__marketDefinition__runners__id and mc__marketDefinition__runners__name for both teams
            runners_id1 = market_definition.get("runners")[0].get("id")
            runners_name1 = market_definition.get("runners")[0].get("name")
                  
            runners_id2 = market_definition.get("runners")[1].get("id")
            runners_name2 = market_definition.get("runners")[1].get("name")
            
            
        except:
             pass
#             print("There was no Market Definition, getting the runner changes")
        
        ### This updates linedata with the latest data, if the data was not updated it will use the last data        
        linedata.append(event_name)
        linedata.append(date)
        linedata.append(pt)
        linedata.append(inPlay)
        linedata.append(runners_id1)
        linedata.append(runners_name1)
        linedata.append(runners_id2)
        linedata.append(runners_name2)
        # These two instructions add two items at the end for the ltp and id to replace.
        linedata.append("")
        linedata.append("")
        
        ### This block tries to get the information of the event from the marketDefinition, if possible. If both teams changed, it will create one line for each team price change (This has to be done in the end)
        try:
            runners_change = market_changes.get("rc")
            ltp = runners_change[0].get("ltp")    
            run_id = runners_change[0].get("id")
            linedata[-2] = ltp
            linedata[-1] = run_id
            
            #If there is more than one price change we add it as two lines.
            if len(runners_change) == 2:
                # A copy needs to be done since we will be editing the object in the next lines. If copy isn't used, linedata2 will be overwritten, since linedata2 = linedata doesn't create a new object, they are both the same object.
                linedata2 = copy.copy(linedata)
                data.append(linedata2)
                ltp2 = runners_change[1].get("ltp")    
                run_id2 = runners_change[1].get("id")
                linedata[-2] = ltp2
                linedata[-1] = run_id2
                
        except:
            pass
#             print("There was no runner changes")
        
        
        data.append(linedata)
        
    #This adds the resulting dataframe to the existing one so that the spreadsheet has a million rows!!!!111one
    result_df = pd.DataFrame(data, columns=cols)
    try:
        current_df = current_df.append(result_df)
        return current_df
    except:
        return result_df




def sort_list(list_):
    """This method sorts the list as if the items were integers and not strings"""
    for i in range(len(list_)):
        list_[i] = int(list_[i])
    list_.sort()
    for i in range(len(list_)):
        list_[i] = str(list_[i])
    return list_


def loop_through_all_dirs():
    """This function makes sure that the get_bz2_function gets called for each file on each directory"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    data_directory = os.getcwd() + "\\Data"
    os.chdir(data_directory)
    dataframe = None
    
    for year in os.listdir():
        print("Getting data for the year", year)
        
        for month in range(12):
            os.chdir(f"{data_directory}\\{year}")
            if months[month] in os.listdir():
                month_name = months[month]
                os.chdir(f"{data_directory}\\{year}\\{month_name}")
                print("Getting data for", months[month])
                
                for day in sort_list(os.listdir()):
                    os.chdir(f"{data_directory}\\{year}\\{month_name}\\{day}")
                    
                    for event in os.listdir():
                        os.chdir(f"{data_directory}\\{year}\\{month_name}\\{day}\\{event}")
                        
                        for market in os.listdir():
                            os.chdir(f"{data_directory}\\{year}\\{month_name}\\{day}\\{event}")
                            actual_month = month+1
                            try:
                                dataframe = get_bz2_data(market, f"{day}/{actual_month}/{year}", dataframe)
                            except:
                                print(f"There has been an error on file {market}, folder {year}\\{month_name}\\{day}\\{event}. It is possible that this event was cancelled.")
                            
                            
    print("Saving file, this could take minutes if the Data folder contains many different years...")
    dataframe.to_excel(excel_file_name, index=False)







### This is the main block
    
loop_through_all_dirs()
print("Program ended successfully!")