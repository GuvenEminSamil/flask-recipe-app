from flask import render_template
from app.models import ContactUs
from flask.views import MethodView

class ContactUsView(MethodView):
    def get(self):
        contacts = ContactUs.query.all()
        return render_template("contact_us.html", contacts=contacts)
