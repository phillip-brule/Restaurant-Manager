from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from restaurantmanager import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    completed_tasks = db.relationship('Completed_Task', backref='employee', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    r_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.name}', Restaurant id:'{self.r_id}')"

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default_restaurant.jpg')
    tasks = db.relationship('Task', backref='restaurant', lazy=True)
    reports = db.relationship('Report', backref='restaurant', lazy=True)

    def __repr__(self):
        return f"Restaurant('{self.name}', id:'{self.id}')"

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    comment = db.Column(db.String(250), nullable=True)
    completed_tasks = db.relationship('Completed_Task', backref='report', lazy=True)

    def __repr__(self):
        return f"Report('{self.report_date}', id:'{self.id}')"


#strftime method to display dates with datetime object
class Completed_Task(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), primary_key=True)
    date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    rating = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"Completed Task( Task id:'{self.task_id}', User id:'{self.user_id}', Date Completed: '{self.date_completed}', Rating: '{self.rating}')"
    def task(self):
        return  Task.query.filter_by(id = self.task_id)

class Role(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    r_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
    role = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Role('{self.role}', User id:'{self.user_id}', Restuarant id:'{self.r_id}')"