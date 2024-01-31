import telebot
import markups
from openai import OpenAI
from bs4 import BeautifulSoup

import requests
token = "6308730048:AAGFt9M0iDtkS9pfsDnz7ov7bqjYbxtZGOo"
OpenAI.api_key = "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"
client = OpenAI(api_key="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")

bot = telebot.TeleBot(token)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, text="🇷🇺 Выберите язык \n🇰🇬 Тилди танданыз", reply_markup=markups.lang)
    

@bot.message_handler(content_types="text")
def message_reply(message):
    if message.text == "🇷🇺 Русский":
        bot.send_message(message.chat.id, "Напишите свой вопрос")
    elif message.text == "🇰🇬 Кыргызча":
        bot.send_message(message.chat.id, "Вопросту жазыныз")
    else:
        bot.register_next_step_handler(message, SolveIssue(message))


    
def SolveIssue(message):
    headers = {"user-agent": USER_AGENT}
    google_search = requests.get(f"https://www.google.com/search?q={message.text} мегаком", headers=headers)
    if (google_search.status_code == 200):
        google_soup = BeautifulSoup(google_search.content, 'html.parser')
        results = []
        if (google_soup.find("span", class_="hgKElc")):
            
            bot.send_message(message.chat.id, str(google_soup.find("span", class_="hgKElc").get_text()))
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
                texts = []
                print(mega_soup.contents)
                if (mega_soup.find_all("div", class_="b-news-full_content")):
                    print("b-news-full_content")
                    for content in mega_soup.find_all("div", class_="b-news-full__content"):
                        anchors = content.find_all('p')
                        if anchors:
                            text = anchors[0].text
                            item = {
                                "text": text
                            }
                            texts.append(item)
                            completion = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "user", "content": f"{item} {message}"}
                                ]
                            )
                            print(completion.choices[0].message)
                            bot.send_message(message.chat.id, text=item)
                if (mega_soup.find("div", class_="ionTabs__item")):
                    bot.send_message(message.chat.id, text=mega_soup.find("div", class_="ionTabs__item").get_text())
                    


bot.polling(interval=0, none_stop=True)


