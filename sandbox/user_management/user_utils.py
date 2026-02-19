"""User management module with authentication utilities."""

import hashlib
import re


class User:
    """Represents a user in the system."""
    
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age
        self.is_active = True
    
    def deactivate(self):
        """Deactivate user account."""
        self.is_active = False
        return True
    
    def get_display_name(self):
        """Return formatted display name."""
        return self.username.title()


def validate_email(email):
    """Check if email format is valid."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_age(age):
    """Validate that age is reasonable."""
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 150:
        raise ValueError("Age is too high")
    return True


def hash_password(password):
    """Hash a password for secure storage."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def calculate_account_score(user, login_count, posts_count):
    """Calculate user engagement score."""
    if not user.is_active:
        return 0
    
    base_score = login_count + posts_count
    age_bonus = user.age // 10
    
    return base_score + age_bonus


def filter_active_users(users):
    """Return list of active users."""
    active = []
    for user in users:
        if user.is_active:
            active.append(user)
    return active


def find_user_by_email(users, email):
    """Find a user by their email address."""
    for user in users:
        if user.email == email:
            return user
    raise ValueError(f"User with email '{email}' not found.")