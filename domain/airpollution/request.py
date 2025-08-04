import requests

# Shared headers for both requests
COMMON_HEADERS = {
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://sim.csb.gov.tr",
    "Referer": "https://sim.csb.gov.tr/STN/STN_Report/StationDataDownloadNew",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "Cookie": "ASP.NET_SessionId=ignnpsgo0fq0zscy0amics2h; language=TR; __RequestVerificationToken=jqztNcB8tqXzQeWyJxEPhJt_Dh_VMvx91CynQCng7sf4I4UZ2RMu0Jg78STzhjRve4sI6mXSOjnwUnAJT7FdH-7grAp0Doc43U_rp30U6xw1; _ga_L0C9ETY97G=GS2.1.s1753803798$o5$g0$t1753803798$j60$l0$h0; _gid=GA1.3.737895938.1754223772; _ga=GA1.1.1580766359.1746798827; _ga_3FH8CLTTJ7=GS2.1.s1754223772$o4$g1$t1754224498$j58$l0$h0"
}

def fetch_station_data():
    url = "https://sim.csb.gov.tr/STN/STN_Report/StationDataDownloadNewData"
    headers = {
        **COMMON_HEADERS,
        "Accept": "*/*",
    }
    data = {
        "__RequestVerificationToken": "bs2QsnIBFgNzO4uRac1D46SfEunVsuTnT8wYzvxOrTlrn1LWlLCi7wiKgf5eJsrdq3Xx9ZdIb0ixvRvnsZu0ze8ynGq4xka0SOn9SAZsA9o1",
        "StationIds": ["00b1dcdb-702d-459b-8399-30548d8164ec", "862bd2b3-3434-4a69-8b7a-1b9dccdec63c"],
        "Parameters": ["CO", "NO"],
        "DataPeriods": "8",
        "StartDateTime": "02.08.2025 15:34",
        "EndDateTime": "03.08.2025 15:37"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetch_constants():
    url = "https://sim.csb.gov.tr/STN/STN_Report/StationDataDownloadNewDefaults"
    headers = {
        **COMMON_HEADERS,
        "Accept": "application/json, text/javascript, */*; q=0.01",
    }
    data = {
        "StationId": "",
        "StationType_Title": "Hava Kalitesi",
        "GroupKey": "00000000-0000-0000-0000-000000000000",
        "StationIds": "",
        "NearestStationIds": "",
        "Parameters": "",
        "StartDateTime": "2025-07-04T15:00:00",
        "EndDateTime": "2025-08-03T15:00:00",
        "DataPeriods": "8",
        "StationType": "1",
        "FixtureId": "",
        "BasinId": "",
        "StationCompanyId": "",
        "StationGroupId": "",
        "CityId": "",
        "StationSubType": "",
        "AreaType": "",
        "SourceType": "",
        "DeviceType": "",
        "SubType_Title": "Tip Seçiniz...",
        "DataBank": "true"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    try:
        print("Fetching station data...")
        station_data = fetch_station_data()
        print("Station Data:", station_data)

        print("\nFetching constants...")
        constants = fetch_constants()
        print("Constants:", constants)
    except Exception as e:
        print(f"Error: {e}")
