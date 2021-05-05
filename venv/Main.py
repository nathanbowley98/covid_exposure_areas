#programmed by NATHANAEL BOWLEY
#github: nathanbowley98


import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster
import pandas as pd

#page = urllib.request.urlopen('https://www.nshealth.ca/covid-exposures?title=&field_covid_exposure_zone_value=All&page=1')
#doc = page.read()
#content = page.content
#substring = 'even views-row-last'
#index = doc.find(substring)
geolocator = Nominatim(user_agent="Halifax NSHealth Covid19 Exposure Areas")
url_base = 'https://www.nshealth.ca/covid-exposures?title=&field_covid_exposure_zone_value=All'
url_prefix = 'https://www.nshealth.ca/covid-exposures?title=&field_covid_exposure_zone_value=All&page='
url_page = 1

def getResultPage(url, page):
    if page == -1:
        return requests.get(url)
    else:
        url = url+str(page)
        return requests.get(url)

def split(result, split_on):
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    current_page = soup.get_text()
    test = current_page.split('\n')
    return test

def hasNextPage(text, next_page_string):
    try:
        if (text.index(next_page_string) < len(text)):
            return True
    except ValueError:
        return False

def remove(array, string):
    total_of_string = array.count(string)
    #print(total_of_string)
    if (total_of_string >= 1):
        for i in range(0, total_of_string):
            array.remove(string)


def print_Locations(start_index, end_index, test):
    print("\n\n\n")
    for i in range(start_index + 1, end_index):
        print(test[i])

def get_locations(start_index, end_index, test, map):
    #print("\n\n\n")
    string = ""
    counter = 7
    current = 0
    current_location = None
    current_location_info = None
    boolean_skip_district = False
    for i in range(start_index + 1, end_index):
        if (i > start_index+ 1 + 6):
            if (current < counter):
                string += test[i] + "i = " + str(i) + "\n"
                #if we are at the location part I want to store the location now as lat long
                if (current == 2):
                    #print(test[i] + " current == 2 testing")

                    #check to see if the next place is going to be a missing central info
                    if (test[i+3] not in ("Central", "Western", "Northern", "Eastern")):
                        #then we need to adjust for that
                        boolean_skip_district = True

                    location = geolocator.geocode(test[i])
                    if location != None:
                        current_location = location
                        #print(test[i-2])
                        print("running:" + (location.latitude, location.longitude))
                    #else:

                       # print(test[i-1] + test[i] + test[i+1] + "testing")
                if (current == 6):
                    current_location_info = test[i-6] + "\n" + test[i-5] + "\n" + test[i-4] + "\n" + test[i-3] + "\n" \
                                            + test[i - 2] + "\n" + test[i-1] + "\n" + test[i] + "\n"


            else:
                if (boolean_skip_district):
                    i -= 1
                    boolean_skip_district = False

                if (current_location != None):
                    folium.Marker((current_location.latitude, current_location.longitude), popup=current_location_info).add_to(map)
                current = 0
                string += "\n" + test[i] + "i = " + str(i) + "\n"

            #for k in range(0,7):
            i +=1
            current += 1

                #string += test[start_index+1+k] + test[i] + "debugging: i = " + str(i) + "\n"
                #i +=1
    return string

#setting the center of the map.
novascotia_coords = [45.24664938443739, -63.24613206184815]

#create map
novascotia_map = folium.Map(location=novascotia_coords, zoom_start=8)

#display the map
###novascotia_map.save('novascotia_map.html')

#base cases
result = getResultPage(url_base, -1)
test = split(result, '\n')
#print("page =  1")
#remove unwanted
remove(test, '')
remove(test, ' ')

#get new array start and end indexes
start_index = test.index('- Any -CentralWesternNorthernEastern')
end_index = test.index('Pages1')

location_info = get_locations(start_index, end_index, test, novascotia_map)

#debug
#print(test)
#print_Locations(start_index, end_index, test)

#####second
result = getResultPage(url_prefix, url_page)
test = split(result, '\n')
#print("page = ", str(url_page+1))

#remove unwanted
remove(test, '')
remove(test, ' ')

#get new array start and end indexes
start_index = test.index('- Any -CentralWesternNorthernEastern')
end_index = test.index('Pages« first')

location_info = get_locations(start_index, end_index, test, novascotia_map)

#debug
#print(test)
#print_Locations(start_index, end_index, test)


#print(hasNextPage(test, 'next ›'))
#print("TESTING!!!")

while (result.status_code == 200 and hasNextPage(test, 'next ›')):

    url_page += 1


    #print("page = ", str(url_page+1))

    result = getResultPage(url_prefix, url_page)
    test = split(result, '\n')

    #remove unwanted
    remove(test, '')
    remove(test, ' ')

    #get new array start and end indexes
    start_index = test.index('- Any -CentralWesternNorthernEastern')
    end_index = test.index('Pages« first')

    #debug
    #print(test)
    #print_Locations(start_index, end_index, test)


    #maps stuff
    location_info = get_locations(start_index,end_index,test, novascotia_map)
    #print(location_info, "\n")

    novascotia_map.save('novascotia_map.html')

    #location = geolocator.geocode("175 5th Avenue NYC")
    #print(location.address)
    #print((location.latitude, location.longitude))
    #print(location.raw)

#result = requests.get('https://www.nshealth.ca/covid-exposures?title=&field_covid_exposure_zone_value=All&page=1')
#print(result.status_code)
#print(result.headers)



#test = split(result, '\n')



#total_blank = test.count('')
#print(total_blank)
#if (total_blank >= 1):
#    for i in range(0, total_blank):
 #       test.remove('')

#remove(test, '')
#remove(test, ' ')


#start_index = test.index('- Any -CentralWesternNorthernEastern')
#end_index = test.index('Pages« first')

#print(test)


#total_blank = test.count('')
#total_blank2 = test.count(' ')
#print(total_blank)
#print(total_blank2)

#print(current_page)
#print(start_index)

## todo -
# - add it to parse over each page.
# - add a legal disclaimer saying that I take no responsibility for any choices you make while using this program
    # and you agree to use it as is with any defects it may have and acknoledge it is your duty to verify if there
    # is missing locations. This program may have bugs and the creator takes no responsibility for how you decide to use
    # the program. Use at your own risk.
# - read over each part of the contents
# - place each part onto google maps using gmplot
# - push repo onto github




#print(end_index)


#print(soup.get_text())



#print(index)
#for i in doc:
 #   if
#print(urllib.request.urlopen('http://www.python.org/'))

#print(page.read())

