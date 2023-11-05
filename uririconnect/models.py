"""
Module containing Django models for the database schema.

This module defines the following models:
- Roles: Represents different roles in the system.
- Users: Represents user information, including authentication details.
- Events: Represents events with associated details and organizers.
- EventRegistrations: Represents user registrations for events.
- Resources: Represents resources with titles, descriptions, and file paths.
- Classes: Represents different classes with associated teachers.
- Messages: Represents messages sent between users.
- SecurityIncidents: Represents security incidents reported by users.
- Assignments: Represents assignments with titles, descriptions, due dates, and associated teachers and classes.
- Grades: Represents student grades for assignments.

Each model corresponds to a table in the database schema and includes appropriate fields and relationships.

Note: Some fields, such as user_password, are intended to store hashed passwords and should be handled securely in the application.
"""

from django.db import models

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email_address = models.EmailField(unique=True, null=False)
    user_password = models.CharField(max_length=255)  # Hashed password handled in the application
    phone_number = models.CharField(max_length=20, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}  {self.email_address}'

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    event_description = models.TextField(null=True)
    event_date = models.DateField(null=True)
    event_location = models.CharField(max_length=100, null=True)
    organizer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.event_description}' 

class EventRegistration(models.Model):
    event_reg_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.registration_date

class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    resource_description = models.TextField(null=True)
    file_path = models.CharField(max_length=255, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.resource_description}'

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50, null=False)
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.class_name

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(User, related_name='sender_messages', on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(User, related_name='receiver_messages', on_delete=models.CASCADE)
    message_content = models.TextField(null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message_content

class SecurityIncident(models.Model):
    security_id = models.AutoField(primary_key=True)
    reporter_id = models.ForeignKey(User, on_delete=models.CASCADE)
    incident_details = models.TextField(null=True)
    time_reported = models.DateTimeField(auto_now_add=True)
    report_status = models.CharField(max_length=20, choices=[('Reported', 'Reported'), ('Under Investigation', 'Under Investigation'), ('Resolved', 'Resolved')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.incident_details

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    assignment_description = models.TextField(null=True)
    due_date = models.DateField(null=True)
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.assignment_description}'

class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    grading_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.score
