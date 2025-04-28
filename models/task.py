from extensions import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    done = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="tasks")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done, "user_id": self.user_id, "user": self.user.email if self.user else None}