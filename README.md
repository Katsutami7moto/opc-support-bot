# opc-support-bot
Bot to help a support service of an online publishing company.

### How to prepare

- Create a DialogFlow `project` with Google Cloud:
  - [DialogFlow](https://dialogflow.cloud.google.com/#/login)
  - [How to create DialogFlow project](https://cloud.google.com/dialogflow/docs/quick/setup)

- DialogFlow project has a `Project ID`, you'll need it several times.

- [Create a DialogFlow `agent`](https://cloud.google.com/dialogflow/docs/quick/build-agent) (use that `Project ID` to connect it to Google Cloud). Don't forget to specify language that users of the bots will write with.

- Agent is like a bot, but from DialogFlow's side of things; your Telegram and VK bots will communicate with this agent.

- Create service account for your DialogFlow Google Cloud project:
https://console.cloud.google.com/iam-admin/serviceaccounts?project={project_id} - where {project_id} is the same `Project ID` from before.

- That service account will have e-mail. Use it to create a Principal here:
https://console.cloud.google.com/iam-admin/iam?project={project_id}
Give it two Roles: `Dialogflow Intent Admin` and `Dialogflow Service Agent`.

- Then go here: https://console.cloud.google.com/iam-admin/serviceaccounts?project={project_id} , click on e-mail, then on `Keys` tab and create JSON key-file. Put this file in root directory of the project (after installing it by instructions below).

### How to install

Python3 should be already installed.

Download the repository:
```commandline
git clone https://github.com/Katsutami7moto/opc-support-bot.git
cd opc-support-bot
```

Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```commandline
pip install -r requirements.txt
```

Then, configure environment variables:

1. Go to the project directory and create a file with the name `.env` (yes, it has only the extension). This file will contain environment variables that usually store data unique to each user, thus you will need to create your own.
2. Copy and paste this to `.env` file:
```dotenv
TELEGRAM_BOT_TOKEN='{telegram_token}'
GOOGLE_APPLICATION_CREDENTIALS='{credentials_json_file}'
PROJECT_ID='{project_id}'
LANGUAGE_CODE='{lang}'
VK_CLUB_TOKEN='{vk_club_token}'
```
3. Replace `{telegram_token}` with API token for the Telegram bot you have created with the help of [BotFather](https://telegram.me/BotFather). This token will look something like this: `958423683:AAEAtJ5Lde5YYfkjergber`.
4. Replace `{credentials_json_file}` with the name of JSON key-file you downloaded from the service account settings.
5. Replace `{project_id}` with `Project ID` of DialogFlow Google Cloud project.
6. Replace `{lang}` with code of your users' language, e.g. `ru`.
7. Replace `{vk_club_token}` with token of VK club you have created; token is created here: https://vk.com/{club_id}?act=tokens

### How to use

For Telegram, start chat with the bot you have created. Then run the script with this command:
```commandline
python3 tg_bot.py
```

For VK bot, execute this command:
```commandline
python3 vk_bot.py
```

To add new phrases for bots to interact with:
1. Create a JSON file with name `filename.json` that will look like this:
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    },
    "Забыл пароль": {
        "questions": [
            "Не помню пароль",
            "Не могу войти",
            "Проблемы со входом",
            "Забыл пароль",
            "Забыл логин",
            "Восстановить пароль",
            "Как восстановить пароль",
            "Неправильный логин или пароль",
            "Ошибка входа",
            "Не могу войти в аккаунт"
        ],
        "answer": "Если вы не можете войти на сайт, воспользуйтесь кнопкой «Забыли пароль?» под формой входа. Вам на почту придёт письмо с дальнейшими инструкциями. Проверьте папку «Спам», иногда письма попадают в неё."
    },
    ...
}
```
2. Execute this command:
```commandline
python3 create_intent.py --path filename.json
```
By default, this script assumes the name of the file to be `questions.json`.

### How to deploy

1. Fork this repository.
2. Sign up at [Heroku](https://id.heroku.com/login).
3. Create [an app](https://dashboard.heroku.com/new-app) at Heroku; choose `Europe` region.
4. In next points, `opc-support-bot` portion of all links should be changed to the name of Heroku app _**you**_ have created.
5. [Connect](https://dashboard.heroku.com/apps/opc-support-bot/deploy/github) forked GitHub repository.
6. Go to [Settings](https://dashboard.heroku.com/apps/opc-support-bot/settings) and set `Config Vars` from previously described environment variables, putting each name to `KEY` and value to `VALUE`, e.g. `TELEGRAM_BOT_TOKEN` to `KEY` and `{telegram_token}` (here it should be without `' '` quotation marks) to `VALUE`.
7. Setup Google Application Credentials as described [here](https://stackoverflow.com/a/56818296), but use [this buildpack](https://github.com/gerynugrh/heroku-google-application-credentials-buildpack) on step 2.
8. Go to [Deploy](https://dashboard.heroku.com/apps/opc-support-bot/deploy/github) section, scroll to bottom, to `Manual Deploy`, be sure to choose `main` branch and click `Deploy Branch` button.
9. Bot should start working and send you a `Bot is running.` message (if you have started the chat with it), but just in case check the [logs](https://dashboard.heroku.com/apps/opc-support-bot/logs) of the app. At the end it should look something like this:
```
2022-07-25T12:52:42.000000+00:00 app[api]: Build succeeded
2022-07-25T12:52:42.153483+00:00 heroku[bot.1]: Stopping all processes with SIGTERM
2022-07-25T12:52:42.338522+00:00 heroku[bot.1]: Process exited with status 143
2022-07-25T12:52:42.793206+00:00 heroku[bot.1]: Starting process with command `python3 main.py`
2022-07-25T12:52:43.389877+00:00 heroku[bot.1]: State changed from starting to up
```

### Working examples

- [Telegram](https://t.me/game_of_verbs_support_bot)
- [VK](https://vk.com/im?sel=-215562055)

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
