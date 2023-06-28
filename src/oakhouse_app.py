import requests
from bs4 import BeautifulSoup
import re
import os
import sys
from datetime import datetime
import pytz

class Oakhouse:

    def __init__(self):
        pass

    """
    search each house's url for room section and stored in list of results as key:value pair
    "apartment name": rooms info soup
    """
    def get_soups(self, urls):
        results = []
        for key, value in urls.items():
            page = requests.get(value)
            soup = BeautifulSoup(page.content, "html.parser")
            apartment = soup.find(id="room")
            results.append([key, apartment])
        return results

    """search each house's rooms and returns vacancies"""
    def get_vacancies(self, urls):
        results = self.get_soups(urls)
        list_of_rooms = []
        for house in results:
            house_name = house[0]
            rooms = house[1].find_all("article", class_="p-room__caset")
            for room in rooms:
                room_number=room.find("p", class_="p-room__caset__number").text.strip()
                try:
                    bed_type=room.find("span", class_="lable", string="Semi-double bed").text
                except: continue
                room_status=re.sub(r'\s*\|\s*\n\s*\n\s*', ' ', room_number)
                if "Vacancy" in room_status and bed_type:
                    try:
                        room_info=room.find("table", class_="p-room__caset__table").text.strip().split("\n")
                        room_info = list(filter(lambda x: x.strip(), room_info))
                        room_stat_list = room_status.split()
                        room_status = ' '.join(room_stat_list)
                        list_of_rooms.append(f'{room_status} {bed_type} {room_info[8]}')
                    except: continue
                else: continue
            list_of_rooms.append(f'{"*"*20}')
        return list_of_rooms

    """output vacancies to file"""
    def get_output(self, urls):
        vacancies = self.get_vacancies(urls)
        # select cwd as filepath
        path = os.getcwd()
        filename = open(os.path.join(path, 'oakhouse_vacancies.txt'), 'w')
        sys.stdout = filename
        # get the current time in JST
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.now(jst)
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # print vacancies on output file
        print(f"Here are vacancies for {current_time}")
        for line in vacancies:
            print(line)
        filename.close()

if __name__ == '__main__':
    oakhouse = Oakhouse()

    urls = {
        "": input()
    }

    results = oakhouse.get_soups(urls)
    oakhouse.get_vacancies(urls)
    oakhouse.get_output(urls)
