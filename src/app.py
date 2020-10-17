import os
import time

from notification_sink import Notification_sink
from store.tinyDbStore import TinyDbStore


def main():
    import requests
    from bs4 import BeautifulSoup

    db = TinyDbStore(os.environ['DB_FILE'])
    sink = Notification_sink(
        os.environ['SINK_SSL_PORT'],
        os.environ['SINK_SMTP_SERVER'],
        os.environ['SINK_SENDER'],
        os.environ['SINK_RECEIVER'],
        os.environ['SINK_PASSWORD']
    )


    task_list = [
        {'tag': 'waterlevel',
         'url': 'https://www.nid.bayern.de/grundwasser/iller_lech/mammendorf-503-16184/gesamtzeitraum',
         'extractor' : lambda x: float(x.find(id='center').find(id='content_3c').find('div', class_='row').find('div', class_='col').find('p').find('strong').text.replace(',', '.')),
         'condition': lambda old, new: old % 5 != new % 5
    }, {
        'tag': 'dax',
        'url': 'https://www.comdirect.de/inf/indizes/detail/uebersicht.html?SEARCH_REDIRECT=true&ID_NOTATION=35803356',
        'extractor': lambda x: float(x.findAll("span", class_='realtime-indicator--value text-size--xxlarge text-weight--medium')[0].text.replace('.', '').replace(',', '.')),
        'condition': lambda old, new: (new - old) / old < - 0.05
    }, {
        'tag': 'kw',
        'url': 'https://www.aktuelle-kalenderwoche.org/',
        'extractor': lambda x: float(x.findAll("span", class_='cw')[0].text.replace('.', '').replace(',', '.')),
        'condition': lambda old, new: new != old
    }
    ]

    for task in task_list:
        page = requests.get(task['url'])
        soup = BeautifulSoup(page.content, 'html.parser')
        value = task['extractor'](soup)
        last_value = db.get_last(task['tag'])
        print(value, last_value)
        if last_value is not None and task['condition'](last_value, value):
            print("Sending notification: " + task['tag'])
            sink.notify(
                "Subject: "+task['tag']+" triggered \n" +
                "Tag: " + task['tag'] + "\n" +
                "Old value: " + str(last_value) + "\n" +
                "Current value: " + str(value))
        db.put(task['tag'], value)
        print(task['tag'], value)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(360)


