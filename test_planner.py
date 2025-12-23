"""
Test script for planner_logic.py
Run this to verify the planning algorithm works correctly
"""

from planner_logic import build_study_plan
import json


def test_basic_plan():
    """Test basic study plan generation"""
    print("=" * 60)
    print("TEST 1: Basic Study Plan")
    print("=" * 60)
    
    test_input = {
        "subjects": [
            {"name": "Math", "difficulty": "hard", "deadline": "2025-12-20"},
            {"name": "Physics", "difficulty": "medium", "deadline": "2025-12-25"},
            {"name": "Chemistry", "difficulty": "easy", "deadline": "2025-12-30"}
        ],
        "available_hours_per_day": 6,
        "study_preferences": {
            "preferred_times": ["morning", "evening"],
            "break_duration": 15
        }
    }
    
    result = build_study_plan(test_input)
    print(json.dumps(result, indent=2))
    print("\n")


def test_urgent_deadline():
    """Test with urgent deadline"""
    print("=" * 60)
    print("TEST 2: Urgent Deadline Scenario")
    print("=" * 60)
    
    test_input = {
        "subjects": [
            {"name": "Final Exam", "difficulty": "hard", "deadline": "2025-12-15"},
            {"name": "Project", "difficulty": "medium", "deadline": "2026-01-10"}
        ],
        "available_hours_per_day": 8,
        "study_preferences": {
            "preferred_times": ["afternoon"],
            "break_duration": 10
        }
    }
    
    result = build_study_plan(test_input)
    print(json.dumps(result, indent=2))
    print("\n")


def test_many_subjects():
    """Test with many subjects"""
    print("=" * 60)
    print("TEST 3: Multiple Subjects")
    print("=" * 60)
    
    test_input = {
        "subjects": [
            {"name": "Calculus", "difficulty": "hard", "deadline": "2025-12-22"},
            {"name": "Linear Algebra", "difficulty": "hard", "deadline": "2025-12-23"},
            {"name": "Programming", "difficulty": "medium", "deadline": "2025-12-24"},
            {"name": "History", "difficulty": "easy", "deadline": "2025-12-26"},
            {"name": "Literature", "difficulty": "easy", "deadline": "2025-12-28"}
        ],
        "available_hours_per_day": 10,
        "study_preferences": {
            "preferred_times": ["morning", "afternoon", "evening"],
            "break_duration": 20
        }
    }
    
    result = build_study_plan(test_input)
    
    # Print summary
    print(f"Success: {result['success']}")
    print(f"Total Subjects: {result['metadata']['total_subjects']}")
    print(f"\nStudy Load Distribution:")
    for subject, details in result['study_load'].items():
        print(f"  {subject}: {details['hours_per_day']}h/day (Priority: {details['priority_score']})")
    print("\n")


def test_edge_case_minimal_time():
    """Test with minimal study time"""
    print("=" * 60)
    print("TEST 4: Edge Case - Minimal Time Available")
    print("=" * 60)
    
    test_input = {
        "subjects": [
            {"name": "Quick Review", "difficulty": "easy", "deadline": "2025-12-18"}
        ],
        "available_hours_per_day": 2,
        "study_preferences": {
            "preferred_times": ["evening"],
            "break_duration": 5
        }
    }
    
    result = build_study_plan(test_input)
    print(json.dumps(result, indent=2))
    print("\n")


def run_all_tests():
    """Run all test cases"""
    print("\n")
    print("🧪 RUNNING ALL TESTS FOR PLANNER LOGIC")
    print("=" * 60)
    print("\n")
    
    test_basic_plan()
    test_urgent_deadline()
    test_many_subjects()
    test_edge_case_minimal_time()
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
