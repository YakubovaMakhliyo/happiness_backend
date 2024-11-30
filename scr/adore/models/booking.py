from django.db.models import *


class Comment(Model):
    text = TextField()
    user = ForeignKey('user.User', CASCADE, related_name='comments')
    restaurant = ForeignKey('Restaurant', CASCADE, related_name='comments')
    created_at = DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        db_table = "comment"

    def __str__(self):
        return f"{self.text} {self.user} {self.restaurant}"


class Time(Model):
    morning_time = CharField(max_length=255)
    afternoon_time = CharField(max_length=255)
    evening_time = CharField(max_length=255)
    restaurant = ForeignKey('Restaurant', CASCADE, related_name='time')

    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Times"
        db_table = "time"

    def __str__(self):
        return f"Morning: {self.morning_time} Afternoon: {self.afternoon_time} Evening: {self.evening_time}"


class Booking(Model):
    class StatusChoices(TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    date = DateField()
    morning = BooleanField(default=False)
    afternoon = BooleanField(default=False)
    evening = BooleanField(default=False)
    status = CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    user = ForeignKey('user.User', CASCADE, related_name='booking')
    restaurant = ForeignKey('Restaurant', CASCADE, related_name='booking')

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        db_table = "booking"

    def __str__(self):
        return f"{self.user} {self.restaurant} {self.date}"


class FAQModel(Model):
    question = TextField()
    answer = TextField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "TOP savol "
        verbose_name_plural = "TOP savollar "
        db_table = 'faq'
