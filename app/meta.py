import pandas as pd
from datetime import datetime
from azure.storage.fileshare import ShareFileClient
import os

# 0 Group A: Qatar, Ecuador, Senegal, Netherlands.
# 1 Group B: England, Iran, USA, Wales.
# 2 Group C: Argentina, Saudi Arabia, Mexico, Poland.
# 3 Group D: France, Australia, Denmark, Tunisia.
# 4 Group E: Spain, Costa Rica, Germany, Japan.
# 5 Group F: Belgium, Canada, Morocco, Croatia.
# 6 Group G: Brazil, Serbia, Switzerland, Cameroon.
# 7 Group H: Portugal, Ghana, Uruguay, Korea Republic.

WIN_POINTS = 2
DRAW_POINTS = 1
groups = [
            {"groupid": 0, "groupname": "Group A", "primarycolor": "#3a1349", "secondarycolor": ""},
            {"groupid": 1, "groupname": "Group B", "primarycolor": "#51b8a5", "secondarycolor": ""},
            {"groupid": 2, "groupname": "Group C", "primarycolor": "#d91b49", "secondarycolor": ""},
            {"groupid": 3, "groupname": "Group D", "primarycolor": "#f2b22a", "secondarycolor": ""},
            {"groupid": 4, "groupname": "Group E", "primarycolor": "#7b1d33", "secondarycolor": ""},
            {"groupid": 5, "groupname": "Group F", "primarycolor": "#009a4a", "secondarycolor": ""},
            {"groupid": 6, "groupname": "Group G", "primarycolor": "#225a9a", "secondarycolor": ""},
            {"groupid": 7, "groupname": "Group H", "primarycolor": "#e67aa5", "secondarycolor": ""}
         ]

# countries = [
#                 {"countryid" : 0, "countryname": "Qatar", "tla": "QAT", "groupid": 0},
#                 {"countryid" : 1, "countryname": "Ecuador", "tla": "ECU", "groupid": 0},
#                 {"countryid" : 2, "countryname": "Senegal", "tla": "SEN", "groupid": 0},
#                 {"countryid" : 3, "countryname": "Netherlands", "tla": "NED", "groupid": 0},
                
#                 {"countryid" : 4, "countryname": "England", "tla": "ENG", "groupid": 1},
#                 {"countryid" : 5, "countryname": "Iran", "tla": "IRN", "groupid": 1},
#                 {"countryid" : 6, "countryname": "United States of America", "tla": "USA", "groupid": 1},
#                 {"countryid" : 7, "countryname": "Wales", "tla": "WAL", "groupid": 1},
                
#                 {"countryid" : 8, "countryname": "Argentina", "tla": "ARG", "groupid": 2},
#                 {"countryid" : 9, "countryname": "Saudi Arabia", "tla": "KSA", "groupid": 2},
#                 {"countryid" : 10, "countryname": "Mexico", "tla": "MEX", "groupid": 2},
#                 {"countryid" : 11, "countryname": "Poland", "tla": "POL", "groupid": 2},
                
#                 {"countryid" : 12, "countryname": "France", "tla": "FRA", "groupid": 3},
#                 {"countryid" : 13, "countryname": "Australia", "tla": "AUS", "groupid": 3},
#                 {"countryid" : 14, "countryname": "Denmark", "tla": "DEN", "groupid": 3},
#                 {"countryid" : 15, "countryname": "Tunisia", "tla": "TUN", "groupid": 3},

#                 {"countryid" : 16, "countryname": "Spain", "tla": "ESP", "groupid": 4},
#                 {"countryid" : 17, "countryname": "Costa Rica", "tla": "CRC", "groupid": 4},
#                 {"countryid" : 18, "countryname": "Germany", "tla": "GER", "groupid": 4},
#                 {"countryid" : 19, "countryname": "Japan", "tla": "JPN", "groupid": 4},
                
#                 {"countryid" : 20, "countryname": "Belgium", "tla": "BEL", "groupid": 5},
#                 {"countryid" : 21, "countryname": "Canada", "tla": "CAN", "groupid": 5},
#                 {"countryid" : 22, "countryname": "Morocco", "tla": "MAR", "groupid": 5},
#                 {"countryid" : 23, "countryname": "Croatia", "tla": "CRO", "groupid": 5},
                
#                 {"countryid" : 24, "countryname": "Brazil", "tla": "BRA", "groupid": 6},
#                 {"countryid" : 25, "countryname": "Serbia", "tla": "SRB", "groupid": 6},
#                 {"countryid" : 26, "countryname": "Switzerland", "tla": "SUI", "groupid": 6},
#                 {"countryid" : 27, "countryname": "Cameroon", "tla": "CMR", "groupid": 6},

#                 {"countryid" : 28, "countryname": "Portugal", "tla": "POR", "groupid": 7},
#                 {"countryid" : 29, "countryname": "Ghana", "tla": "GHA", "groupid": 7},
#                 {"countryid" : 30, "countryname": "Uruguay", "tla": "URU", "groupid": 7},
#                 {"countryid" : 31, "countryname": "Korea Repulic", "tla": "KOR", "groupid": 7}
                
#             ]

countries = [
                {"countryid" : 0, "countryname": "Qatar", "tla": "QAT", "flag": "🇶🇦", "groupid": 0},
                {"countryid" : 1, "countryname": "Ecuador", "tla": "ECU", "flag": "🇪🇨", "groupid": 0},
                {"countryid" : 2, "countryname": "Senegal", "tla": "SEN", "flag": "🇸🇳", "groupid": 0},
                {"countryid" : 3, "countryname": "Netherlands", "tla": "NED", "flag": "🇳🇱", "groupid": 0},
                
                {"countryid" : 4, "countryname": "England", "tla": "ENG", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "groupid": 1},
                {"countryid" : 5, "countryname": "Iran", "tla": "IRN", "flag": "🇮🇷", "groupid": 1},
                {"countryid" : 6, "countryname": "United States of America", "tla": "USA", "flag": "🇺🇸", "groupid": 1},
                {"countryid" : 7, "countryname": "Wales", "tla": "WAL", "flag": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "groupid": 1},
                
                {"countryid" : 8, "countryname": "Argentina", "tla": "ARG", "flag": "🇦🇷", "groupid": 2},
                {"countryid" : 9, "countryname": "Saudi Arabia", "tla": "KSA", "flag": "🇸🇦", "groupid": 2},
                {"countryid" : 10, "countryname": "Mexico", "tla": "MEX", "flag": "🇲🇽", "groupid": 2},
                {"countryid" : 11, "countryname": "Poland", "tla": "POL", "flag": "🇵🇱", "groupid": 2},
                
                {"countryid" : 12, "countryname": "France", "tla": "FRA", "flag": "🇫🇷", "groupid": 3},
                {"countryid" : 13, "countryname": "Australia", "tla": "AUS", "flag": "🇦🇺", "groupid": 3},
                {"countryid" : 14, "countryname": "Denmark", "tla": "DEN", "flag": "🇩🇰", "groupid": 3},
                {"countryid" : 15, "countryname": "Tunisia", "tla": "TUN", "flag": "🇹🇳", "groupid": 3},

                {"countryid" : 16, "countryname": "Spain", "tla": "ESP", "flag": "🇪🇸", "groupid": 4},
                {"countryid" : 17, "countryname": "Costa Rica", "tla": "CRC", "flag": "🇨🇷", "groupid": 4},
                {"countryid" : 18, "countryname": "Germany", "tla": "GER", "flag": "🇩🇪", "groupid": 4},
                {"countryid" : 19, "countryname": "Japan", "tla": "JPN", "flag": "🇯🇵", "groupid": 4},
                
                {"countryid" : 20, "countryname": "Belgium", "tla": "BEL", "flag": "🇧🇪", "groupid": 5},
                {"countryid" : 21, "countryname": "Canada", "tla": "CAN", "flag": "🇨🇦", "groupid": 5},
                {"countryid" : 22, "countryname": "Morocco", "tla": "MAR", "flag": "🇲🇦", "groupid": 5},
                {"countryid" : 23, "countryname": "Croatia", "tla": "CRO", "flag": "🇭🇷", "groupid": 5},
                
                {"countryid" : 24, "countryname": "Brazil", "tla": "BRA", "flag": "🇧🇷", "groupid": 6},
                {"countryid" : 25, "countryname": "Serbia", "tla": "SRB", "flag": "🇷🇸", "groupid": 6},
                {"countryid" : 26, "countryname": "Switzerland", "tla": "SUI", "flag": "🇨🇭", "groupid": 6},
                {"countryid" : 27, "countryname": "Cameroon", "tla": "CMR", "flag": "🇨🇲", "groupid": 6},

                {"countryid" : 28, "countryname": "Portugal", "tla": "POR", "flag": "🇵🇹", "groupid": 7},
                {"countryid" : 29, "countryname": "Ghana", "tla": "GHA", "flag": "🇬🇭", "groupid": 7},
                {"countryid" : 30, "countryname": "Uruguay", "tla": "URU", "flag": "🇺🇾", "groupid": 7},
                {"countryid" : 31, "countryname": "Korea Repulic", "tla": "KOR", "flag": "🇰🇷", "groupid": 7}
                
            ]

venues = [
            {"venueid": 0, "venuename": "Al Bayat Stadium", "location": "", "lat": "", "lon" : ""},
            {"venueid": 1, "venuename": "Khalifa International Stadium", "location": "", "lat": "", "lon" : ""},
            {"venueid": 2, "venuename": "Al Thumama Stadium", "location": "", "lat": "", "lon" : ""},
            {"venueid": 3, "venuename": "Ahmad Bin Ali Stadium", "location": "", "lat": "", "lon" : ""},
            {"venueid": 4, "venuename": "Lusail Stadium", "location": "", "lat": "", "lon" : ""},
            {"venueid": 5, "venuename": "Stadium 974", "location": "", "lat": "", "lon" : ""},
            {"venueid": 6, "venuename": "Education City Stadium", "location": "", "lat": "", "lon" : ""},
            {"venueid": 7, "venuename": "Al Janoub Stadium", "location": "", "lat": "", "lon" : ""}
         ]

matchtype = [
                {"matchtypeid": 0, "matchtypename": "Group Matches"},
                {"matchtypeid": 1, "matchtypename": "Round of 16"},
                {"matchtypeid": 2, "matchtypename": "Quarter Finals"},
                {"matchtypeid": 3, "matchtypename": "Semi Finals"},
                {"matchtypeid": 4, "matchtypename": "3rd Place"},
                {"matchtypeid": 5, "matchtypename": "Finals"},
            ]

itinerary = [
                # {"itineraryid": 0, "date": "20221120", "venueid": 0, "matchtypeid" : 0, "country1id": 0, "country2id": 1, "countries": [0, 1]},
                {"itineraryid": 0, "date": "20221119", "venueid": 0, "matchtypeid" : 0, "country1id": 0, "country2id": 1, "countries": [0, 1]},
                
                {"itineraryid": 1, "date": "20221121", "venueid": 2, "matchtypeid" : 0, "country1id": 2, "country2id": 3, "countries": [2, 3]},
                # {"itineraryid": 1, "date": "20221118", "venueid": 2, "matchtypeid" : 0, "country1id": 2, "country2id": 3, "countries": [2, 3]},
                {"itineraryid": 2, "date": "20221121", "venueid": 1, "matchtypeid" : 0, "country1id": 4, "country2id": 5, "countries": [4, 5]},
                {"itineraryid": 3, "date": "20221121", "venueid": 3, "matchtypeid" : 0, "country1id": 6, "country2id": 7, "countries": [6, 7]},
                
                {"itineraryid": 4, "date": "20221122", "venueid": 7, "matchtypeid" : 0, "country1id": 12, "country2id": 13, "countries": [12, 13]},
                {"itineraryid": 5, "date": "20221122", "venueid": 6, "matchtypeid" : 0, "country1id": 14, "country2id": 15, "countries": [15, 15]},
                {"itineraryid": 6, "date": "20221122", "venueid": 5, "matchtypeid" : 0, "country1id": 10, "country2id": 11, "countries": [10, 11]},
                {"itineraryid": 7, "date": "20221122", "venueid": 4, "matchtypeid" : 0, "country1id": 8, "country2id": 9, "countries": [8, 9]},
                
                {"itineraryid": 8, "date": "20221123", "venueid": 3, "matchtypeid" : 0, "country1id": 20, "country2id": 21, "countries": [20, 21]},
                {"itineraryid": 9, "date": "20221123", "venueid": 2, "matchtypeid" : 0, "country1id": 16, "country2id": 17, "countries": [16, 17]},
                {"itineraryid": 10, "date": "20221123", "venueid": 1, "matchtypeid" : 0, "country1id": 18, "country2id": 19, "countries": [18, 19]},
                {"itineraryid": 11, "date": "20221123", "venueid": 0, "matchtypeid" : 0, "country1id": 22, "country2id": 23, "countries": [22, 23]},
                
                {"itineraryid": 12, "date": "20221124", "venueid": 7, "matchtypeid" : 0, "country1id": 26, "country2id": 27, "countries": [26, 27]},
                {"itineraryid": 13, "date": "20221124", "venueid": 6, "matchtypeid" : 0, "country1id": 30, "country2id": 31, "countries": [30, 31]},
                {"itineraryid": 14, "date": "20221124", "venueid": 5, "matchtypeid" : 0, "country1id": 28, "country2id": 29, "countries": [28, 29]},
                {"itineraryid": 15, "date": "20221124", "venueid": 4, "matchtypeid" : 0, "country1id": 24, "country2id": 25, "countries": [24, 25]},

                {"itineraryid": 16, "date": "20221125", "venueid": 3, "matchtypeid" : 0, "country1id": 7, "country2id": 5, "countries": [7, 5]},
                {"itineraryid": 17, "date": "20221125", "venueid": 2, "matchtypeid" : 0, "country1id": 0, "country2id": 2, "countries": [0, 2]},
                {"itineraryid": 18, "date": "20221125", "venueid": 1, "matchtypeid" : 0, "country1id": 3, "country2id": 2, "countries": [3, 2]},
                {"itineraryid": 19, "date": "20221125", "venueid": 0, "matchtypeid" : 0, "country1id": 4, "country2id": 6, "countries": [4, 6]},

                {"itineraryid": 20, "date": "20221126", "venueid": 7, "matchtypeid" : 0, "country1id": 15, "country2id": 13, "countries": [15, 13]},
                {"itineraryid": 21, "date": "20221126", "venueid": 6, "matchtypeid" : 0, "country1id": 11, "country2id": 9, "countries": [11, 9]},
                {"itineraryid": 22, "date": "20221126", "venueid": 5, "matchtypeid" : 0, "country1id": 12, "country2id": 14, "countries": [12, 14]},
                {"itineraryid": 23, "date": "20221126", "venueid": 4, "matchtypeid" : 0, "country1id": 8, "country2id": 10, "countries": [8, 10]},

                {"itineraryid": 24, "date": "20221127", "venueid": 3, "matchtypeid" : 0, "country1id": 19, "country2id": 17, "countries": [19, 17]},
                {"itineraryid": 25, "date": "20221127", "venueid": 2, "matchtypeid" : 0, "country1id": 20, "country2id": 22, "countries": [20, 22]},
                {"itineraryid": 26, "date": "20221127", "venueid": 1, "matchtypeid" : 0, "country1id": 23, "country2id": 21, "countries": [23, 21]},
                {"itineraryid": 27, "date": "20221127", "venueid": 0, "matchtypeid" : 0, "country1id": 16, "country2id": 18, "countries": [16, 18]},

                {"itineraryid": 28, "date": "20221128", "venueid": 7, "matchtypeid" : 0, "country1id": 27, "country2id": 25, "countries": [27, 25]},
                {"itineraryid": 29, "date": "20221128", "venueid": 6, "matchtypeid" : 0, "country1id": 31, "country2id": 29, "countries": [31, 29]},
                {"itineraryid": 30, "date": "20221128", "venueid": 5, "matchtypeid" : 0, "country1id": 24, "country2id": 26, "countries": [24, 26]},
                {"itineraryid": 31, "date": "20221128", "venueid": 4, "matchtypeid" : 0, "country1id": 28, "country2id": 30, "countries": [28, 30]},

                {"itineraryid": 32, "date": "20221129", "venueid": 3, "matchtypeid" : 0, "country1id": 7, "country2id": 4, "countries": [7, 4]},
                {"itineraryid": 33, "date": "20221129", "venueid": 2, "matchtypeid" : 0, "country1id": 5, "country2id": 6, "countries": [5, 6]},
                {"itineraryid": 34, "date": "20221129", "venueid": 1, "matchtypeid" : 0, "country1id": 1, "country2id": 2, "countries": [1, 2]},
                {"itineraryid": 35, "date": "20221129", "venueid": 0, "matchtypeid" : 0, "country1id": 3, "country2id": 0, "countries": [3, 0]},

                {"itineraryid": 36, "date": "20221130", "venueid": 7, "matchtypeid" : 0, "country1id": 13, "country2id": 14, "countries": [13, 14]},
                {"itineraryid": 37, "date": "20221130", "venueid": 6, "matchtypeid" : 0, "country1id": 15, "country2id": 12, "countries": [15, 12]},
                {"itineraryid": 38, "date": "20221130", "venueid": 5, "matchtypeid" : 0, "country1id": 11, "country2id": 8, "countries": [11, 8]},
                {"itineraryid": 39, "date": "20221130", "venueid": 4, "matchtypeid" : 0, "country1id": 9, "country2id": 10, "countries": [9, 10]},

                {"itineraryid": 40, "date": "20221201", "venueid": 3, "matchtypeid" : 0, "country1id": 23, "country2id": 20, "countries": [23, 20]},
                {"itineraryid": 41, "date": "20221201", "venueid": 2, "matchtypeid" : 0, "country1id": 21, "country2id": 22, "countries": [21, 22]},
                {"itineraryid": 42, "date": "20221201", "venueid": 1, "matchtypeid" : 0, "country1id": 19, "country2id": 16, "countries": [19, 16]},
                {"itineraryid": 43, "date": "20221201", "venueid": 0, "matchtypeid" : 0, "country1id": 17, "country2id": 18, "countries": [17, 18]},

                {"itineraryid": 44, "date": "20221202", "venueid": 7, "matchtypeid" : 0, "country1id": 29, "country2id": 30, "countries": [29, 30]},
                {"itineraryid": 45, "date": "20221202", "venueid": 6, "matchtypeid" : 0, "country1id": 31, "country2id": 28, "countries": [31, 28]},
                {"itineraryid": 46, "date": "20221202", "venueid": 5, "matchtypeid" : 0, "country1id": 25, "country2id": 26, "countries": [25, 26]},
                {"itineraryid": 47, "date": "20221202", "venueid": 4, "matchtypeid" : 0, "country1id": 27, "country2id": 24, "countries": [27, 24]}

            ]

def _getResults() -> pd.DataFrame:
    connection_string = os.getenv('azure_conn_str')
    file_client = ShareFileClient.from_connection_string(conn_str=connection_string, share_name="fifa", file_path="results.csv")
    with open("./data/results.csv", "wb") as file_handle:
        data = file_client.download_file()
        data.readinto(file_handle)

    return pd.read_csv("./data/results.csv")

def _setResults(results_df: pd.DataFrame):
    results_df.to_csv("./data/results.csv", index=False)
    connection_string = os.getenv('azure_conn_str')
    file_client = ShareFileClient.from_connection_string(conn_str=connection_string, share_name="fifa", file_path="results.csv")
    with open("./data/results.csv", "rb") as source_file:
        file_client.upload_file(source_file)

def _prepareBaseData() -> pd.DataFrame:
    groups_df = pd.DataFrame(data=groups)
    countries_df = pd.DataFrame(data=countries)
    venues_df = pd.DataFrame(data=venues)
    matchtype_df = pd.DataFrame(data=matchtype)
    itinerary_df = pd.DataFrame(data=itinerary)
    results_df = _getResults()
    
    fifa_df = itinerary_df.join(venues_df.set_index('venueid'), 
                                on='venueid').join(matchtype_df.set_index('matchtypeid'), 
                                                   on='matchtypeid').join(countries_df.set_index('countryid'), lsuffix='_c1',
                                                                          on='country1id').join(countries_df.set_index('countryid'), rsuffix='_c2',
                                                                                                on='country2id').join(groups_df.set_index('groupid'),
                                                                                                                     on='groupid').join(results_df.set_index('itineraryid'),
                                                                                                                                        on='itineraryid')

    fifa_df = fifa_df.fillna(-1)
    fifa_df['fdate'] = fifa_df.apply(lambda row: datetime.strptime(row['date'], '%Y%m%d').strftime('%d-%b-%y'), axis=1)

    fifa_df['tense'] = fifa_df.apply(lambda row: (datetime.strptime(row['date'], '%Y%m%d') - datetime.utcnow()).days + 1, axis=1)
    fifa_df['tenseid'] = fifa_df.apply(lambda row: -1 if (row['tense']<0) else 0 if (row['tense']==0) else 1, axis=1 )
    # print(fifa_df[['fdate', 'tense', 'tenseid']])
    return fifa_df

def GetItinerary(groupId: int = -1) -> dict:
    base_df = _prepareBaseData()
    if groupId != -1:
        return base_df[base_df['groupid'] == groupId].to_dict("records")
    else:
        return base_df.to_dict("records")

def GetGroups() -> dict:
    return groups

def UpdateScore(request) -> dict:
    print("request: ", request["data"])
    results_df = _getResults()
    record_df = results_df.loc[results_df["itineraryid"] == request["data"]["i"]]
    if (record_df.empty):
        new_result = [{"itineraryid": request["data"]["i"], "g1": request["data"]["g1"],"g2": request["data"]["g2"]}]
        new_result_df = pd.DataFrame(data=new_result)
        results_df = pd.concat([results_df, new_result_df], ignore_index=True)
    else:
        results_df.loc[results_df["itineraryid"] == request["data"]["i"], ["g1", "g2"]] = request["data"]["g1"], request["data"]["g2"]
    # results_df.to_csv("./data/results.csv", index=False)
    _setResults(results_df)
    return GetItinerary() 

def GetPoints(groupId: int = -1) -> dict:
    results_df = _getResults()
    base_df = _prepareBaseData()
    scored_games_df = base_df.query('g1 >= 0 & g2 >= 0')
    scored_games_df = scored_games_df.reset_index()
    points_columns = ["groupid", "groupname", "primarycolor", "secondarycolor", "countryid", "countryname", "tla", "flag", "played", "won", "lost", "draw", "points"]
    # points_data = [{"groupid": 0, 
    #                 "groupname": 'Group A', 
    #                 "primarycolor": 'red', 
    #                 "secondarycolor": 'blue', 
    #                 "countryid": 0, 
    #                 "countryname": 'Qatar', 
    #                 "tla": 'QTR', 
    #                 "flag": '', 
    #                 "played": 1, 
    #                 "won": 1, 
    #                 "lost": 0, 
    #                 "draw": 0, 
    #                 "points": 2}]
    
    # points_df = pd.DataFrame(data=points_data, columns=points_columns)
    points_df = pd.DataFrame(columns=points_columns)
    # print(points_df)
    for index, row in scored_games_df.iterrows():
        countries = [
            {
                "countryid": row['country1id'],
                "countryname": row['countryname'],
                "tla": row['tla'],
                "flag": row['flag'],
                "won" : 1 if row['g1'] > row['g2'] else 0,
                "lost" : 1 if row['g2'] > row['g1'] else 0,
                "draw" : 1 if row['g1'] == row['g2'] else 0,
                "points" : WIN_POINTS if (row['g1'] > row['g2']) == 1 else DRAW_POINTS if (row['g1'] == row['g2']) == 1 else 0
            },
            {
                "countryid": row['country2id'],
                "countryname": row['countryname_c2'],
                "tla": row['tla_c2'],
                "flag": row['flag_c2'],
                "won" : 1 if row['g2'] > row['g1'] else 0,
                "lost" : 1 if row['g1'] > row['g2'] else 0,
                "draw" : 1 if row['g1'] == row['g2'] else 0,
                "points" : WIN_POINTS if (row['g2'] > row['g1']) == 1 else DRAW_POINTS if (row['g1'] == row['g2']) == 1 else 0
            }
        ]
        # won = 1 if row['g1'] > row['g2'] else 0
        # lost = 1 if row['g2'] > row['g1'] else 0
        # draw = 1 if row['g1'] == row['g2'] else 0
        # points = WIN_POINTS if won == 1 else DRAW_POINTS if draw == 1 else 0

        
        for country in countries:
            if ((points_df.loc[
                           # (points_df['groupid'] == row['groupid']) & 
                           (points_df['countryid'] == country['countryid'])]).empty):
                new_points = [
                    {
                        "groupid": row['groupid'],
                        "groupname": row['groupname'],
                        "primarycolor": row['primarycolor'],
                        "secondarycolor": row['secondarycolor'],
                        "countryid": country['countryid'],
                        "countryname": country['countryname'],
                        "tla": country['tla'],
                        "flag": country['flag'],
                        "played": 1,
                        "won": country['won'],
                        "lost": country['lost'],
                        "draw": country['draw'],
                        "points": country['points']
                    }]
                new_points_df = pd.DataFrame(data=new_points)
                points_df = pd.concat([points_df, new_points_df], ignore_index=False)
            else:
                # print('update')
                points_df['played']  = points_df.apply(lambda p: p['played']+1 if p['countryid'] == country['countryid'] else p['played'], axis =1)
                points_df['won']  = points_df.apply(lambda p: p['played']+country['won'] if p['countryid'] == country['countryid'] else p['played'], axis =1)
                points_df['lost']  = points_df.apply(lambda p: p['lost']+country['lost'] if p['countryid'] == country['countryid'] else p['played'], axis =1)
                points_df['draw']  = points_df.apply(lambda p: p['draw']+country['draw'] if p['countryid'] == country['countryid'] else p['played'], axis =1)
                points_df['points']  = points_df.apply(lambda p: p['played']+country['points'] if p['countryid'] == country['countryid'] else p['played'], axis =1)


    # print(points_df)

    if groupId != -1:
        return points_df[points_df['groupid'] == groupId].to_dict("records")
    else:
        return points_df.to_dict("records")

