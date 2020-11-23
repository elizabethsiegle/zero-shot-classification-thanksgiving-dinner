from twilio.twiml.messaging_response import MessagingResponse
classifier = pipeline("zero-shot-classification")
topic_labels = ["politics", "family", "sports", "job", "love"]
app = Flask(__name__)
@app.route("/sms", methods=['POST'])
def sms():
    resp = MessagingResponse()
    inb_msg = request.form['Body'].lower().strip()
    obj = classifier(inb_msg, topic_labels, multi_class=True)
    keys = obj.get('labels')
    vals = obj.get('scores')
    new_dict = {keys[i]: vals[i] for i in range(len(keys))}
    key_with_max_score = max(new_dict, key=new_dict.get)
    max_score = max(new_dict.values())
    print(f'Your message {inb_msg!r} is {key_with_max_score!r}')
    if(key_with_max_score == topic_labels[0]):
        resp.message(f'We are most confident your message {inb_msg!r} corresponds to {key_with_max_score!r} with a score of {max_score!r}. Maybe talk about something else, like the weather.')
    else:
        resp.message(f'We are most confident your message {inb_msg!r} corresponds to {key_with_max_score!r} with a score of {max_score!r}. It is safe to talk say this at Thanksgiving dinner with family')
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)