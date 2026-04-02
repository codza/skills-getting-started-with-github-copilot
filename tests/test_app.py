from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    """Test that root redirects to static index"""
    # Arrange
    # (No special setup needed)
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_get_activities():
    """Test fetching all activities"""
    # Arrange
    # (No special setup needed)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    # Verify structure
    chess = data["Chess Club"]
    assert "description" in chess
    assert "schedule" in chess
    assert "max_participants" in chess
    assert "participants" in chess
    assert isinstance(chess["participants"], list)

def test_signup_success():
    """Test successful signup"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Tennis Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    
    # Additional verification
    response2 = client.get("/activities")
    data = response2.json()
    assert email in data[activity]["participants"]

def test_signup_duplicate():
    """Test signing up for the same activity twice"""
    # Arrange
    email = "dupstudent@mergington.edu"
    activity = "Swimming Team"
    client.post(f"/activities/{activity}/signup?email={email}")  # First signup
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_activity_not_found():
    """Test signup for non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    activity = "NonExistent"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_delete_success():
    """Test successful deletion"""
    # Arrange
    email = "deleteme@mergington.edu"
    activity = "Music Club"
    client.post(f"/activities/{activity}/signup?email={email}")  # Signup first
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "Removed" in result["message"]
    
    # Additional verification
    response2 = client.get("/activities")
    data = response2.json()
    assert email not in data[activity]["participants"]

def test_delete_not_signed_up():
    """Test deleting a student not signed up"""
    # Arrange
    email = "notsigned@mergington.edu"
    activity = "Art Club"
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "not signed up" in result["detail"]

def test_delete_activity_not_found():
    """Test delete from non-existent activity"""
    # Arrange
    email = "test@mergington.edu"
    activity = "NonExistent"
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]