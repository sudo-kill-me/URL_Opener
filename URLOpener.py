from selenium import webdriver
from twilio.rest import Client
from flask import Flask, request


app = Flask(__name__)

twilioAccountSID = "_place_your_twilio_acct_sid_here_"
twilioAuthToken = "_place_your_twilio_auth_token_here_"
ngrokAuthToken = "_place_your_ngrok_auth_token_here_"
firefoxDriverPath = "_place_path_to_resource_here"
client = Client(twilioAccountSID, twilioAuthToken)


def parseURL(sender, text):
    option = str(text[0])
    urlData = str(text[2:])
    openURL(sender, option, urlData)


def openURL(sender, option, urlData):
    if option == '1':
        fullURL = 'https://www.' + urlData + '.com'
    elif option == '2' or option == ' ':
        fullURL = urlData
    else:
        client.messages.create(to=sender,
                               from_='19193733967',
                               body="Error!\nOptions:\n1 <website> - websites should be a popular \".com\" site,"
                                    " such as \"google\".\n\n2 <full url> - this should be the full url that includes "
                                    "the \"https://\" and information following site name.")

    driver = webdriver.Firefox(executable_path=firefoxDriverPath)
    driver.get(fullURL)


@app.route('/sms', methods=['POST'])
def sms():
    sender = request.form['From']
    messageBody = request.form['Body']
    parseURL(sender, messageBody)


if __name__ == '__main__':
    app.run()