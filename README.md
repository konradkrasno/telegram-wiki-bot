# telegram-wiki-bot

An idea of this application is to create a bot that can answer the user's questions. The bot takes knowledge from Polish 
Wikipedia. The application based on Telegram Bot API and uses machine learning models to give answers.

## About application

As I mentioned above the application based on Telegram Bot API. It takes message from users and process it to give the 
answer. The authors of this application try to simulate the conversation with bot. To achieve this they created states 
for bot logic such as: "question", "greeting" or giving "feedback". Using this states bot can recognise whether user ask the 
question or make greeting. Bot also can ask for feedback whether the answer was correct. The logic allow to extend this and 
create new states in the future.\
When user ask the question and bot status is "question" bot logic starts looking for the answer.

The process of finding answer consist from:
* finding the most suitable article
* finding some of the most relevant paragraphs
* using machine learning model for choose the phrase with the answer

## Dependencies

The application uses django to handle with Telegram Bot API.
It also uses elasticsearch for keeping and finding Wikipedia's articles.
To save questions, answers and user's feedback about the aswers the application uses Postgres database.
To finding the answers the application uses deeppavlov or simpletransformers models.

All depencencies:
* telegram
* elasticsearch
* ngrok
* django
* deeppavlov
* simpletransformers
* postgress

## Example how it works

To converse with WikiBot we have to have Telegram account. After login to Telegram account we have to find the WikiBot.
The start of conversation looks like this:

![starting_message](https://user-images.githubusercontent.com/55924004/93598011-53018d80-f9bc-11ea-9510-3c4d32c1956d.PNG)

After this message we can ask the question.

Examples of questions and correct answer:

![good_answer](https://user-images.githubusercontent.com/55924004/93597971-411fea80-f9bc-11ea-981f-3df07ccc3acf.PNG)

![good_answer_2](https://user-images.githubusercontent.com/55924004/93597976-41b88100-f9bc-11ea-8985-150aef3e4ea6.jpg)

![good_answer_3](https://user-images.githubusercontent.com/55924004/93597977-42511780-f9bc-11ea-8657-fc7fa8763524.jpg)

Of course bot don't know everything. An example of incorrect answer:

![bad_answer](https://user-images.githubusercontent.com/55924004/93597970-3feebd80-f9bc-11ea-90fc-20f50cfe40a4.jpg)

We have to remember to provide feedback whether the answer was correct or not.
