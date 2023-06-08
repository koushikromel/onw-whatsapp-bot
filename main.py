from fastapi import FastAPI, Request
import requests, keys, pyrebase, uvicorn
from twilio.rest import Client

app = FastAPI()

account_sid = keys.account_sid
auth_token = keys.auth_token
client = Client(account_sid, auth_token)

databse = pyrebase.initialize_app(keys.config)
db = databse.database()

template_id = "YOUR_TEMPLATE_ID"

def whatsapp(reply,to , _from="whatsapp:+917708630275"):
    message = client.messages.create(
        body=reply,
        to=to,
        from_=_from
    )

def send_template_reply(to_number, template, from_number="whatsapp:+917708630275"):
    print('inside send template')
    message = client.messages.create(
        body=template,
        from_=from_number,
        to=to_number,
        template_id=template_id,
    )
    return message.sid

def reply(body, _from):
    try:
        userData = db.child(_from).get().val()
        if userData == None:

            user = False
        elif userData['name'] == False:
            whatsapp('May I rembember your name as {}\nreply with "yes" to save your name\n"no" to reenter'.format(body.capitalize()))
            db.child(_from).update({'name': body,'pending':'yes or no'})
        elif userData['pending'] =='yes or no':
            if body == "yes":
                whatsapp('saving your name as {}'.format(userData['name'].capitalize()))
                db.child(_from).update({'name': userData['name'],'pending':'none'})

            elif body == "no":
                whatsapp('ok, Please enter your name again')
                db.child(_from).update({'name': False})
            else:
                whatsapp('Please reply with yes or no')
        else:
            user  =True
    except Exception as e:
       print('errprr is ', e)
       whatsapp('Can\'t handle the current laod. surver is too busy.\nError code is 12')


    if user:
        name = userData['name'].capitalize()
        print(name)
    else:
        whatsapp('Hey,\nBefore answering that may I know what shall I call you?\nEnter your name:')
        db.child(_from).update({'name': False,'firstAskedQuestion':body})
        return


@app.post("/webhook")
async def webhook(request: Request):
    # Handle the webhook request
    data = await request.form()
    print(f"data is {data}")
    message_body = data.get("Body")
    message_from = data.get("From")
    body = message_body.lower()
    from_ = message_from.lower()
    ProfileName = data.get("ProfileName")
    print(f"body is {body} and its from {from_}")
    if body == "hello":
        print("inside iff")
        template = 'Hello {{1}}, thank you for your message.'
        send_template_reply(from_,  template)
        # whatsapp(f"Hello {ProfileName}, {{1}}", from_)
    elif body == "hello":
        print("inside elif")
        whatsapp("Hello Welcome to onwords webhook101", from_)
    elif body == "hell":
        print("inside elifff")
        whatsapp("Hell this is onwords webhook101", from_)
    else:
        print("inside else")
        whatsapp("None of the aboveee webhook101", from_)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7887, reload=True)