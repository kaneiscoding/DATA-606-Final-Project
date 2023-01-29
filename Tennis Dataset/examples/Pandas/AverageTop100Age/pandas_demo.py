import glob
import matplotlib.pyplot as plt
import datetime, sys

pd.options.display.mpl_style = 'default'

# Function to parse the date format 
def parse(t):
    string_ = str(t)
    try:
        # Returns date in the format of (year, month, day)
        return datetime.date(int(string_[:4]), int(string_[4:6]), int(string_[6:]))
    except:
        # If there is an error, return a default date of (1900,1,1)
	    print("Error", len(string_))
        return datetime.date(1900,1,1)
    
# Function to read all the files in the directory
def readAllFiles(dirname):
    # Find all the files in the directory that match the pattern
    allFiles = glob.glob(dirname + "/atp_rankings_" + "*.csv")
    # Create an empty dataframe
    ranks = pd.DataFrame()
    list_ = list()
    # Iterate through the list of files
    for filen in allFiles:
	    print(filen)
        # Read the csv file and parse the dates
        df = pd.read_csv(filen,
                         index_col=None,
                         header=None,
                         parse_dates=[0],
                         date_parser=lambda t:parse(t))
        list_.append(df)
    # Concatenate the dataframe
    ranks = pd.concat(list_)
    return ranks

# Function to read the players data
def readPlayers(dirname):
    print("Reading Players")
    # Read the csv file and parse the dates
    return pd.read_csv(dirname+"/atp_players.csv",
                       index_col=None,
                       header=None,
                       parse_dates=[4],
                       date_parser=lambda t:parse(t))

# Read the ranks data
ranks = readAllFiles(sys.argv[1])
# Filter the ranks data to only include ranks less than 100
ranks = ranks[(ranks[1]<100)]
print ranks
# Read the players data
players = readPlayers (sys.argv[1])
# Merge the ranks and players data
plRanks = ranks.merge(players,right_on=0,left_on=2)
# Create a new column "B" which is the difference in date between the rank date and the birthdate
plRanks["B"] = plRanks["0_x"] - plRanks[4]
# Convert the difference to years
plRanks["B"] = plRanks["B"].astype(int) / (365243600*1000000000.0)

# Group the data by rank date
agg = plRanks[["0_x","B"]].groupby("0_x")

# Calculate the mean age of the top 100 players for each rank date
agg.mean().to_csv("top100ages.csv")