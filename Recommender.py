import unicodedata
import csv

movieDat = {}
raterDat = {}

#========================================
def readRaterFile():
    rater = 0
    movieID = 1
    rating = 2
    data = []   # this list will hold all the lines from the file

    #fname = 'c:/pythoncode/data/ratings_short.csv' #input('enter file name')
    fname = 'c:/pythoncode/data/ratings.csv'
    print (fname)
    fhandle = open(fname)
    x = fhandle.readline()      # skip headerline

    for line in fhandle:
        line = line.rstrip()
        wrds = line.split(",") # this is a list containing one record from the file
        movies = [wrds[1:3]]
        data.append(wrds) # each element of this list is a complete record; print this out to see what's in file
        key = wrds[0]
        if key in raterDat:
            raterDat[key].extend(movies)
        else:
            raterDat[key] = movies

#========================================
def readMovieFile():

    movieID = 0
    title = 0
    year = 1
    genre = 2
    directors = 3
    minutes = 4

    with open('c:/pythoncode/data/ratedmoviesfull.csv', newline='', encoding = 'utf-8') as csvfile:
    #with open('c:/pythoncode/data/ratedmovies_short.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        csvfile.readline()
        for row in spamreader:
            key = row[movieID]
            data = [row[1],row[2],row[4],row[5],row[6]]
            movieDat[key] = data

#========================================
def getFiltRatingAllMovies(minRaters):
    ratingDat = {}
    av = []
    avgRating = []

    for key in movieDat:
        if getByFilter(key):    # only look at movies that pass the filters
            totalRat = 0
            count = 0
            average = 0
            for ratKey in raterDat:
                ratinfo = raterDat[ratKey]
                for i in range(len(ratinfo)):
                    id = ratinfo[i][0]
                    if id == key:       # the movie is rated
                        rat = ratinfo[i][1]
                        #print("Rating for",id," by rater ", ratKey, " is ",rat)
                        totalRat = totalRat + int(rat)
                        count = count + 1
                        average = totalRat/count
            if (average > 0 and count >= minRaters):
                info = movieDat[key]    # the value of the key is the whole list of movie data
                tuple(info)             # gotta make it a tuple so it can be hashed by the sort routine
                av = [average, info]
                #print(key,av)
                avgRating.append(av)

        avgRating.sort()

    for i in range(0,len(avgRating)):
        print("{0:2.2f}\t".format(avgRating[i][0]),end='')      # print the rating with no LF
        print(', '.join(avgRating[i][1]))                       # now all the movie data
    print("\n",len(avgRating),"movies selected")

#========================================
def dFilt(movieID, dir):                # the filters: d, g, m, y -- self-explanatory I hope
    #print(movieID, dir)
    dirs = dir.split(",")
    for d in dirs:
        if d in movieDat[movieID][3]:
            return True
    return False

#========================================
def gFilt(movieID, genre):
    #print(movieID, genre)
    if genre in movieDat[movieID][2]:
        return True
    return False
#========================================
def mFilt(movieID, short, long):
    runTime =  int(movieDat[movieID][4])
    #print(movieID, short, long, runTime)
    if (runTime >= short) and (runTime <= long):
        return True
    return False
#========================================
def yFilt(movieID, year):
    #print(movieID, year, movieDat[movieID][1])
    if int(movieDat[movieID][1]) >= year:
        return True
    return False
#========================================
class Filter:
    choose = {'d': dFilt, 'g': gFilt, 'm': mFilt, 'y': yFilt}   # a dict of filters (used as a switch)
    def __init__(self, mov, fil, p1, p2 = 300):                 # constructor picks a filter and its parms
        self.movID = mov                                        # arg 'fil' will be 'd', 'g', 'y' or 'm'
        self.filType = fil                                      # so Filter will return a dFilt, gFilt, etc.
        self.parm1 = p1
        self.parm2 = p2

    def doit(self):                                             # pick a filter
        f = self.choose[self.filType]
        if self.filType == 'm':
            result = f(self.movID, self.parm1, self.parm2)      # 2 parms or 1?
        else:
            result = f(self.movID,self.parm1)                   # does movID satisfy the filter (T/F)?
        return result
#========================================
class trueFilt():                                               # need a dummy class with a .doit() that returns True
    def __init__(self):
        pass
    def doit(self):
        return True
#========================================                   #default is m=trueFilt(),y=trueFilt(),d=trueFilt(),g=trueFilt()
def allFilt(m, y, d, g):                                    # these may be a specific filter, or trueFilt
    return m.doit() and y.doit() and d.doit() and g.doit()          # if any fails, the movie isn't recommended
#========================================
def getByFilter(movieID):
    m = y = d = g = trueFilt()                              # if a filter is not used, trueFilt replaces it
    if mf:
        m = Filter(movieID,'m',*mf)                         # this method creates Filter objs which are passed to allFilt
    if  yf:                                                 # the parms of allFilt are Filters!
        y = Filter(movieID,'y',yf)
    if df:
        d = Filter(movieID,'d',df)
    if gf:
        g = Filter(movieID,'g',gf)
    return allFilt(m,y,d,g)                 # any filter not defined below (yf, mf, etc.) becomes True. Movie is True if it passes all filters
#========================================
if __name__ ==  '__main__':
    yf = mf = df = gf = None
    readMovieFile()
    readRaterFile()

    #mf = [90, 120]                                    # DEFINE THE FILTERS HERE!
    #yf = 2011                                         # m = minutes, y = year, d = director,
    df = 'Juan'                                        # g = genre
    #gf = 'Drama'

    getFiltRatingAllMovies(minRaters=1)                    # at least minRaters must have submitted ratings
