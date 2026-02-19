"""Tests for user_utils module."""

import unittest
from user_utils import (
    User, validate_email, validate_age, hash_password,
    calculate_account_score, filter_active_users, find_user_by_email
)


class TestUser(unittest.TestCase):
    
    def test_deactivate_returns_true(self):
        """Deactivate should return True on success."""
        user = User("john", "john@example.com", 25)
        result = user.deactivate()
        self.assertTrue(result)
        self.assertFalse(user.is_active)
    
    def test_get_display_name(self):
        """Display name should be title case."""
        user = User("john doe", "john@example.com", 25)
        self.assertEqual(user.get_display_name(), "John Doe")


class TestValidateEmail(unittest.TestCase):
    
    def test_valid_email(self):
        self.assertTrue(validate_email("test@example.com"))
    
    def test_valid_email_with_numbers(self):
        """Should accept numbers in email local part."""
        self.assertTrue(validate_email("test123@example.com"))
    
    def test_invalid_email(self):
        self.assertFalse(validate_email("invalid-email"))


class TestValidateAge(unittest.TestCase):
    
    def test_valid_age(self):
        self.assertTrue(validate_age(25))
    
    def test_negative_age_raises_value_error(self):
        """Negative age should raise ValueError, not TypeError."""
        with self.assertRaises(ValueError):
            validate_age(-5)
    
    def test_too_high_age_raises_value_error(self):
        """Age over 150 should raise ValueError."""
        with self.assertRaises(ValueError):
            validate_age(200)


class TestHashPassword(unittest.TestCase):
    
    def test_hash_password_valid(self):
        """Should return a hash string for valid password."""
        result = hash_password("securepassword123")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)  # SHA256 produces 64 hex chars
    
    def test_short_password_raises(self):
        with self.assertRaises(ValueError):
            hash_password("short")


class TestCalculateAccountScore(unittest.TestCase):
    
    def test_active_user_score(self):
        """Score = login_count + posts_count + (age // 10)."""
        user = User("john", "john@example.com", 25)
        score = calculate_account_score(user, login_count=10, posts_count=5)
        self.assertEqual(score, 17)  # 10 + 5 + 2 = 17
    
    def test_inactive_user_score_zero(self):
        user = User("john", "john@example.com", 25)
        user.deactivate()
        score = calculate_account_score(user, login_count=10, posts_count=5)
        self.assertEqual(score, 0)


class TestFilterActiveUsers(unittest.TestCase):
    
    def test_filter_returns_user_objects(self):
        """Should return User objects, not usernames."""
        user1 = User("alice", "alice@example.com", 30)
        user2 = User("bob", "bob@example.com", 25)
        user2.is_active = False
        
        result = filter_active_users([user1, user2])
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], User)
        self.assertEqual(result[0].username, "alice")


class TestFindUserByEmail(unittest.TestCase):
    
    def test_find_existing_user(self):
        user1 = User("alice", "alice@example.com", 30)
        user2 = User("bob", "bob@example.com", 25)
        
        result = find_user_by_email([user1, user2], "bob@example.com")
        self.assertEqual(result.username, "bob")
    
    def test_user_not_found_raises(self):
        """Should raise ValueError when user not found."""
        user1 = User("alice", "alice@example.com", 30)
        
        with self.assertRaises(ValueError):
            find_user_by_email([user1], "notfound@example.com")


if __name__ == "__main__":
    unittest.main()
