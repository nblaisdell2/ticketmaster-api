import requests
from pprint import pprint
from enum import Enum

CLIENT_ID = "aYpew83PXZcmRTNhqGZvJqHmEyDl1Geq"
BASE_URL = "https://app.ticketmaster.com/discovery/v2/{resource}.json?apikey={apiKey}"


class SortOrder(Enum):
    ASC = 1
    DESC = 2


class SortType(Enum):
    NAME = 1
    DATE = 2
    DISTANCE = 3


def getSortValue(sortType: SortType, sortOrder: SortOrder):
    return sortType.name.lower() + "," + sortOrder.name.lower()


def getAPIResponse(resource, params={}):
    urlParams = {
        "resource": resource,
        "apiKey": CLIENT_ID,
    }
    allParams = urlParams | params

    url = BASE_URL
    for key, val in params.items():
        url += "&" + key + "=" + val

    url = url.format(**allParams)

    print('URL', url)
    return requests.get(url).json()


def getEvents(sortType: SortType, sortOrder: SortOrder):
    params = {
        "geoPoint": "drkxfub1h",
        "radius": "300",
        "startDateTime": "2023-03-31T00:00:00Z",
        # "endDateTime": "2023-03-31T00:00:00Z",
        "size": "200",
        "page": "0",
        "genreId": "KnvZfZ7vAe1",
        "sort": getSortValue(sortType, sortOrder)
    }
    res = getAPIResponse("events", params)
    return res


def getClassifications():
    res = getAPIResponse("classifications")
    classifications = res['_embedded']['classifications']

    dClass = {}
    for c in classifications:
        if 'segment' in c:
            segName = c['segment']['name']
            if segName not in dClass:
                dClass[segName] = set(())
            for g in c['segment']['_embedded']['genres']:
                gName = g['name']
                gID = g['id']
                dClass[segName].add((gName, gID))
                # for sg in g['_embedded']['subgenres']:
                #     dClass[segName].add(sg['name'])

    # pprint(dClass)
    return dClass


eventData = getEvents(SortType.DATE, SortOrder.ASC)
pprint(eventData)
