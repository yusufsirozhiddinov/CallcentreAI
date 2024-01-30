import telebot
import markups
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
token = "6308730048:AAGFt9M0iDtkS9pfsDnz7ov7bqjYbxtZGOo"

bot = telebot.TeleBot(token)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
client = OpenAI
client = OpenAI(
    api_key = "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"
)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="🇷🇺 Выберите язык \n 🇰🇬 Тилди танданыз")
    SolveIssue(message)


def SolveIssue(message):
    headers = {"user-agent": USER_AGENT}
    google_search = requests.get("https://www.google.com/search?q=Как заказать новый тарифный план? мегаком", headers=headers)
    if (google_search.status_code == 200):
        google_soup = BeautifulSoup(google_search.content, 'html.parser')
        results = []
        if (google_soup.find("span", class_="hgKElc")):
            bot.send_message(message.chat.id, text=google_soup.find("span", class_="hgKElc").text)
        else:
            for g in google_soup.find_all('div', class_='jGGQ5e'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    item = {
                        "title": title,
                        "link": link
                    }
                    results.append(item)
            mega_search = requests.get(results[0]["link"])
            if (mega_search.status_code == 200):
                mega_soup = BeautifulSoup(mega_search.content, "html.parser")
                print(mega_search.content)
                texts = []
                for content in mega_soup.find_all("div", class_="b-news-full__content"):
                        anchors = content.find_all('p')
                        if anchors:
                            text = anchors[0].text
                            item = {
                                "text": text
                            }
                            texts.append(item)
                            bot.send_message(message.chat.id, text=item)


bot.polling(interval=0, none_stop=True)


