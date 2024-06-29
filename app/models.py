from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    PasswordHash = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Role = db.Column(db.String(50), nullable=False)
    ParentID = db.Column(db.Integer, db.ForeignKey('Parents.ParentID'), nullable=True)
    CreatedAt = db.Column(db.DateTime, default=db.func.current_timestamp())

class Parent(db.Model):
    __tablename__ = 'Parents'
    ParentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    users = relationship('User', backref='parent', lazy=True)

class Player(db.Model):
    __tablename__ = 'Players'
    PlayerID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    DateOfBirth = db.Column(db.Date, nullable=False)
    TeamID = db.Column(db.Integer, db.ForeignKey('Teams.TeamID'))
    ParentID = db.Column(db.Integer, db.ForeignKey('Parents.ParentID'))
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))

class Coach(db.Model):
    __tablename__ = 'Coaches'
    CoachID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    ContactNumber = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    TeamID = db.Column(db.Integer, db.ForeignKey('Teams.TeamID'))

class Team(db.Model):
    __tablename__ = 'Teams'
    TeamID = db.Column(db.Integer, primary_key=True)
    TeamName = db.Column(db.String(100), nullable=False)
    CoachName = db.Column(db.String(100))
    CoachContact = db.Column(db.String(15))
    Division = db.Column(db.String(50))

class Fee(db.Model):
    __tablename__ = 'Fees'
    FeeID = db.Column(db.Integer, primary_key=True)
    PlayerID = db.Column(db.Integer, db.ForeignKey('Players.PlayerID'))
    Amount = db.Column(db.Numeric(10, 2), nullable=False)
    DueDate = db.Column(db.Date, nullable=False)
    PaidDate = db.Column(db.Date)
    PaymentStatus = db.Column(db.String(50))

class Schedule(db.Model):
    __tablename__ = 'Scheduling'
    ScheduleID = db.Column(db.Integer, primary_key=True)
    TeamID = db.Column(db.Integer, db.ForeignKey('Teams.TeamID'))
    EventType = db.Column(db.String(50), nullable=False)
    EventDate = db.Column(db.Date, nullable=False)
    StartTime = db.Column(db.Time, nullable=False)
    EndTime = db.Column(db.Time, nullable=False)
    Location = db.Column(db.String(255), nullable=False)

class Communication(db.Model):
    __tablename__ = 'Communication'
    MessageID = db.Column(db.Integer, primary_key=True)
    SenderID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    ReceiverID = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    MessageText = db.Column(db.Text)
    SentDate = db.Column(db.DateTime, default=db.func.current_timestamp())
