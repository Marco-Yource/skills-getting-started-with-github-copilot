"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Weekly chess matches and tournaments.",
        "max_participants": 20,
        "participants": []
    },
    "Robotics": {
        "description": "Build and program robots for competitions.",
        "max_participants": 15,
        "participants": []
    },
    "Drama": {
        "description": "Acting, directing, and stage production.",
        "max_participants": 25,
        "participants": []
    },
    # Sports related activities
    "Soccer Team": {
        "description": "Join the school soccer team for practice and matches.",
        "max_participants": 22,
        "participants": []
    },
    "Basketball Club": {
        "description": "Weekly basketball training and inter-school games.",
        "max_participants": 15,
        "participants": []
    },
    # Artistic activities
    "Art Club": {
        "description": "Painting, drawing, and creative workshops.",
        "max_participants": 18,
        "participants": []
    },
    "Photography": {
        "description": "Learn photography techniques and photo editing.",
        "max_participants": 12,
        "participants": []
    },
    # Intellectual activities
    "Mathletes": {
        "description": "Compete in math competitions and problem-solving sessions.",
        "max_participants": 20,
        "participants": []
    },
    "Debate Team": {
        "description": "Practice public speaking and participate in debates.",
        "max_participants": 16,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
    # Validate max participants not exceeded
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Maximum participants reached")
    # Validate email format
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid email format")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
