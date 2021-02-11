import requests
from bs4 import BeautifulSoup
import re
from requests import ConnectionError

class Parser:
    def __init__(self, name, url, headers):
        self.name = name
        self.url = url
        self.headers = headers
        # self.vacancies_link = []
        # self.pages = []

class Vacancies(Parser):
    NAME = "Python"
    PAGE_URL = str('https://rabota.by/search/vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=' + NAME + '&page=0')
    HEADERS = {'user-agent': 'my-app/0.0.1'}
    vacancies_link = []
    pages = []

    def __init__(self):
        super().__init__(Vacancies.NAME, Vacancies.PAGE_URL, Vacancies.HEADERS)


    def searh_num_pages(self):
        try:
            self.soup = BeautifulSoup(requests.get(Vacancies.PAGE_URL, headers=Vacancies.HEADERS).text, 'lxml')
            for i in self.soup.findAll(class_='bloko-button HH-Pager-Control', text=True):
                self.pages.append(i["href"][-1:])
        except(ConnectionError, Exception) as e:
            print ("Exception is :", e)

    def search_vacancies_link(self):
        for i in range(int(self.pages[-1]) + 1):
            url = str('https://rabota.by/search/vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=' + Vacancies.NAME + '&page=' + str(i))
            soup = BeautifulSoup(requests.get(url, headers=Vacancies.HEADERS).text, 'lxml')
            for j in soup.findAll("a", text=True):
                if "Python" in j.text:
                    self.vacancies_link.append(j["href"])

class Calculator(Vacancies):
    def __init__(self, words):
        self.words = words
        self.counter = []
        self.result = []

    def searh_words(self):
        for word in self.words:
            for i in range(int(Vacancies.pages[-1]) + 1):
                url = str('https://rabota.by/search/vacancy?L_is_autosearch=false&area=16&clusters=true&enable_snippets=true&text=' + Vacancies.NAME + '&page=' + str(i))
                soup = BeautifulSoup(requests.get(url, headers=Vacancies.HEADERS).text, 'lxml')
                self.counter.append(re.findall(word, str(soup).lower()))


    def average_number(self):
        for i in self.counter:
            for j in i:
                # if j == 'python' or j == 'linux' or j == 'flask':
                if j in self.words:
                    self.result.append(j)

        result_all = {i: self.result.count(i) for i in self.result}
        for key, value in result_all.items():
            print(str(key) + " counts " + str(value) + ', average number of occurrence' + ' = ' + str(value / len(self.result)*100) + '%')


if __name__ == '__main__':
    jobs = Vacancies()
    jobs.searh_num_pages()
    jobs.search_vacancies_link()
    print(*jobs.vacancies_link, sep='\n')
    calc = Calculator(["python", "linux", "flask"])
    calc.searh_words()
    calc.average_number()
    # print(calc.counter)
