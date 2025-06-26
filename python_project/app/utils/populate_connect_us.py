from app import create_app, db
from app.models import ContactUs

app = create_app()

with app.app_context():
    email_content = ContactUs(content="samil5834@gmail.com")
    db.session.add(email_content)
    db.session.commit()

    mobile_content = ContactUs(content="+7 905 310 5247")
    db.session.add(mobile_content)
    db.session.commit()