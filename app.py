from flask import Flask, render_template, url_for, request, jsonify
import requests, stripe, os


app = Flask(__name__)
app.config['STRIPE_PK'] = os.getenv("STRIPE_PK")
app.config['STRIPE_SK'] = os.getenv("STRIPE_SK")
stripe.api_key = app.config['STRIPE_SK']


def subscribe(user_email, email_list, api_key):
	return requests.post(
        "https://api.mailgun.net/v3/lists/"+email_list+"/members",
        auth=('api', api_key),
        data={'subscribed': True,
              'address': user_email,})

@app.route("/",methods=["GET","POST"]) 
def index():
	img_url = url_for('static', filename='images/iphone-mockup.png')

	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		mode = 'payment',
		success_url = 'https://example.com/success',
		cancel_url = 'https://example.com/cancel',
		line_items=[{'price':'price_1I9xueJaVOFHXZDzV46F934h',
					'quantity':1,
		}]
		)

	if request.method == "POST":
		user_email = request.form.get('email') 
		# user_email is your alias found in mailing lists


		response = subscribe(user_email,
			'my_list@sandboxc67e2c0ba1e64bdbb055e64d41135bb4.mailgun.org',
			os.getenv("MAILGUN_SK")) # < Private mailgun apikey

	return render_template("index.html", 
		checkout_id=session['id'],
		checkout_pk=app.config['STRIPE_PK'],
		img_url = img_url)

if __name__== '__main__':
	app.run(debug=True)   
