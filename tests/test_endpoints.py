"""
API endpoint tests for the Mergington High School Activities API.
Tests are structured using the AAA (Arrange-Act-Assert) pattern for clarity.
"""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""

    def test_get_all_activities_success(self, client, fresh_activities):
        """
        Test that GET /activities returns all activities with correct structure.

        Arrange: Initialize client with fresh activities
        Act: Make GET request to /activities
        Assert: Verify status 200, response contains all 9 activities, and structure is correct
        """
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert activities["Chess Club"]["max_participants"] == 12
        assert len(activities["Chess Club"]["participants"]) == 2


class TestSignupEndpoint:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_happy_path(self, client, fresh_activities):
        """
        Test successful signup for a student to an activity.

        Arrange: Fresh state with Chess Club having 2 participants
        Act: POST signup for new email to Chess Club
        Assert: Verify 200 status, email is added to participants list, count increased
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
        assert new_email in fresh_activities[activity_name]["participants"]
        assert len(fresh_activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_duplicate_email_returns_error(self, client, fresh_activities):
        """
        Test that duplicate signup attempt is rejected.

        Arrange: Fresh state with Chess Club participants
        Act: POST same email twice to same activity
        Assert: First signup succeeds (200), second fails (400)
        """
        # Arrange
        activity_name = "Chess Club"
        email = "duplicate@mergington.edu"

        # Act & Assert - First signup should succeed
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200

        # Act & Assert - Second signup should fail
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]

    def test_signup_invalid_activity_returns_404(self, client, fresh_activities):
        """
        Test that signup to non-existent activity returns 404.

        Arrange: Fresh state
        Act: POST signup to non-existent activity
        Assert: Verify 404 status and "Activity not found" message
        """
        # Arrange
        invalid_activity = "Underwater Basket Weaving"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_encodes_special_characters_in_activity_name(self, client, fresh_activities):
        """
        Test that signup handles URL encoding correctly for activity names with spaces.

        Arrange: Fresh state with "Basketball Team" activity
        Act: POST signup with URL-encoded activity name
        Assert: Verify 200 status and student added successfully
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "baller@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in fresh_activities[activity_name]["participants"]


class TestUnregisterEndpoint:
    """Test suite for the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_happy_path(self, client, fresh_activities):
        """
        Test successful unregister of a student from an activity.

        Arrange: Fresh state with Chess Club having michael@mergington.edu
        Act: DELETE unregister that email from Chess Club
        Assert: Verify 200 status, email removed from participants, count decreased
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in fresh_activities[activity_name]["participants"]
        assert len(fresh_activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_not_registered_returns_error(self, client, fresh_activities):
        """
        Test that unregistering a non-participant returns 400 error.

        Arrange: Fresh state
        Act: DELETE unregister email not in activity
        Assert: Verify 400 status and "not registered" message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_invalid_activity_returns_404(self, client, fresh_activities):
        """
        Test that unregister from non-existent activity returns 404.

        Arrange: Fresh state
        Act: DELETE unregister from non-existent activity
        Assert: Verify 404 status and "Activity not found" message
        """
        # Arrange
        invalid_activity = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{invalid_activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestStateConsistency:
    """Test suite for verifying state consistency across signup and unregister operations."""

    def test_signup_then_unregister_state_consistency(self, client, fresh_activities):
        """
        Test that signup followed by unregister maintains state consistency.

        Arrange: Fresh state, track initial participant count
        Act: Signup new student, then unregister them
        Assert: Final state matches initial state
        """
        # Arrange
        activity_name = "Programming Class"
        email = "tempstudent@mergington.edu"
        initial_count = len(fresh_activities[activity_name]["participants"])

        # Act - Signup
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert - Signup successful
        assert response1.status_code == 200
        assert len(fresh_activities[activity_name]["participants"]) == initial_count + 1

        # Act - Unregister
        response2 = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert - Unregister successful and state restored
        assert response2.status_code == 200
        assert len(fresh_activities[activity_name]["participants"]) == initial_count
        assert email not in fresh_activities[activity_name]["participants"]

    def test_multiple_signups_participant_count_accuracy(self, client, fresh_activities):
        """
        Test that multiple signups correctly increment participant count.

        Arrange: Fresh state
        Act: Signup 3 different students to same activity
        Assert: Verify participant count increased by exactly 3
        """
        # Arrange
        activity_name = "Art Studio"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        initial_count = len(fresh_activities[activity_name]["participants"])

        # Act & Assert
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert final count
        assert len(fresh_activities[activity_name]["participants"]) == initial_count + len(emails)
        for email in emails:
            assert email in fresh_activities[activity_name]["participants"]
