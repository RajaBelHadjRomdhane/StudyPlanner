"""
Study Planning Logic - Backend Person B
Handles extraction, computation, and timetable generation
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any


def extract_user_data(user_input: Dict) -> Dict:
    """
    Extract and validate user information
    
    Args:
        user_input: Raw input from frontend/backend manager
        
    Returns:
        Cleaned and structured user data
    """
    # Validate required fields
    if 'subjects' not in user_input:
        raise ValueError("Missing required field: subjects")
    
    if 'available_hours_per_day' not in user_input:
        raise ValueError("Missing required field: available_hours_per_day")
    
    # Extract and clean data
    cleaned_data = {
        'subjects': user_input['subjects'],
        'available_hours_per_day': float(user_input['available_hours_per_day']),
        'study_preferences': user_input.get('study_preferences', {})
    }
    
    # Validate subjects
    for subject in cleaned_data['subjects']:
        if 'name' not in subject or 'deadline' not in subject:
            raise ValueError(f"Subject missing required fields: {subject}")
        
        # Set default difficulty if not provided
        if 'difficulty' not in subject:
            subject['difficulty'] = 'medium'
    
    return cleaned_data


def calculate_days_until_deadline(deadline_str: str) -> int:
    """
    Calculate days remaining until deadline
    
    Args: 
        deadline_str: Date in format "YYYY-MM-DD"
        
    Returns:
        Number of days until deadline
    """
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
    today = datetime.now()
    days_left = (deadline - today).days
    
    # Return at least 1 day to avoid division by zero
    return max(days_left, 1)


def compute_study_load(subjects: List[Dict], available_hours: int) -> Dict:
    """
    Distribute study time across subjects based on: 
    - Difficulty level
    - Days until deadline
    - Total available hours
    
    Args:
        subjects: List of subject dictionaries
        available_hours: Hours available per day
        
    Returns:
        Dictionary with hours allocated per subject
    """
    # Difficulty weights
    difficulty_weights = {
        "easy": 1,
        "medium": 1.5,
        "hard": 2
    }
    
    # Calculate total weighted priority
    total_weight = 0
    subject_priorities = []
    
    for subject in subjects:
        days_left = calculate_days_until_deadline(subject['deadline'])
        difficulty = subject.get('difficulty', 'medium').lower()
        
        # Urgency factor (less days = higher priority)
        urgency_factor = 1 / max(days_left, 1)
        
        # Combined priority score
        weight = difficulty_weights[difficulty] * (1 + urgency_factor * 10)
        total_weight += weight
        
        subject_priorities.append({
            "name": subject['name'],
            "weight": weight,
            "days_left": days_left,
            "difficulty": difficulty
        })
    
    # Distribute hours proportionally
    study_load = {}
    for item in subject_priorities:
        hours_per_day = (item['weight'] / total_weight) * available_hours
        
        study_load[item['name']] = {
            "hours_per_day": round(hours_per_day, 1),
            "days_until_deadline": item['days_left'],
            "total_hours_weekly": round(hours_per_day * 7, 1),
            "difficulty": item['difficulty'],
            "priority_score": round(item['weight'], 2)
        }
    
    return study_load


def generate_timetable(study_load: Dict, preferences: Dict) -> Dict:
    """
    Create a weekly/daily timetable
    
    Args:
        study_load: Hours per subject from compute_study_load()
        preferences: User's study preferences
        
    Returns: 
        Structured timetable in JSON format
    """
    timetable = {
        "weekly_schedule": {},
        "study_sessions": []
    }
    
    # Days of the week
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Get preferred times
    preferred_times = preferences.get('preferred_times', ['morning'])
    break_duration = preferences.get('break_duration', 15)
    
    # Generate schedule for each day
    for day in days:
        daily_schedule = []
        
        for subject, allocation in study_load.items():
            # Rotate through preferred times
            time_slot = preferred_times[len(daily_schedule) % len(preferred_times)]
            
            daily_schedule.append({
                "subject": subject,
                "duration_hours": allocation['hours_per_day'],
                "time_slot": time_slot,
                "break_after_minutes": break_duration,
                "priority": allocation['priority_score']
            })
        
        # Sort by priority (highest first)
        daily_schedule.sort(key=lambda x: x['priority'], reverse=True)
        timetable['weekly_schedule'][day] = daily_schedule
    
    # Create study sessions summary
    for subject, allocation in study_load.items():
        timetable['study_sessions'].append({
            "subject": subject,
            "total_hours_weekly": allocation['total_hours_weekly'],
            "sessions_per_week": 7,
            "average_session_duration": allocation['hours_per_day']
        })
    
    return timetable


def build_study_plan(user_input: Dict) -> Dict:
    """
    Main function that orchestrates the entire planning process
    
    Args: 
        user_input: Complete user input dictionary
        
    Returns:
        Complete study plan in JSON format
    """
    try:
        # Extract data
        user_data = extract_user_data(user_input)
        
        # Compute study load
        study_load = compute_study_load(
            user_data['subjects'], 
            user_data['available_hours_per_day']
        )
        
        # Generate timetable
        timetable = generate_timetable(
            study_load, 
            user_data.get('study_preferences', {})
        )
        
        return {
            "success": True,
            "study_load": study_load,
            "timetable": timetable,
            "metadata": {
                "total_subjects": len(user_data['subjects']),
                "planning_period": "1 week",
                "total_study_hours_daily": user_data['available_hours_per_day']
            }
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to generate study plan"
        }