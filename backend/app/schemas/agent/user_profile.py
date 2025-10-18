from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class JobType(str, Enum):
    """Types of jobs that affect training availability"""

    SEDENTARY = "sedentary"  # Office work, desk job
    ACTIVE = "active"  # Physical work, on feet
    MIXED = "mixed"  # Combination of desk and physical work
    SHIFT_WORK = "shift_work"  # Irregular hours
    UNEMPLOYED = "unemployed"
    STUDENT = "student"
    RETIRED = "retired"


class InjurySeverity(str, Enum):
    """Severity levels for running injuries"""

    MINOR = "minor"  # Brief discomfort, no time off
    MODERATE = "moderate"  # Some time off, modified training
    MAJOR = "major"  # Significant time off, rehabilitation required
    CHRONIC = "chronic"  # Ongoing issue requiring management


class RunningGoal(str, Enum):
    """Main running goals"""

    GENERAL_FITNESS = "general_fitness"
    WEIGHT_LOSS = "weight_loss"
    FIRST_5K = "first_5k"
    FIRST_10K = "first_10k"
    FIRST_HALF_MARATHON = "first_half_marathon"
    FIRST_MARATHON = "first_marathon"
    IMPROVE_SPEED = "improve_speed"
    IMPROVE_ENDURANCE = "improve_endurance"
    QUALIFY_BOSTON = "qualify_boston"
    ULTRA_MARATHON = "ultra_marathon"
    TRAIL_RUNNING = "trail_running"
    COMPETITIVE_RACING = "competitive_racing"


class PersonalBest(BaseModel):
    """Personal best time for a specific distance"""

    distance_km: float = Field(..., description="Distance in kilometers", gt=0)
    time_minutes: float = Field(..., description="Time in minutes", gt=0)
    date_achieved: Optional[date] = Field(
        None, description="Date when this PB was achieved"
    )
    race_name: Optional[str] = Field(None, description="Name of the race or event")


class RunningInjury(BaseModel):
    """Information about a running injury"""

    injury_type: str = Field(
        ..., description="Type of injury (e.g., 'knee pain', 'shin splints')"
    )
    severity: InjurySeverity = Field(..., description="Severity of the injury")
    date_occurred: Optional[date] = Field(None, description="When the injury occurred")
    date_recovered: Optional[date] = Field(None, description="When fully recovered")
    description: Optional[str] = Field(
        None, description="Additional details about the injury"
    )
    still_affecting: bool = Field(
        False, description="Whether this injury still affects training"
    )


class UserProfile(BaseModel):
    """Comprehensive user profile for running coach AI"""

    # Basic Information
    age: int = Field(..., description="User's age in years", ge=13, le=100)
    weight_kg: float = Field(..., description="Weight in kilograms", gt=0, le=300)
    height_cm: float = Field(..., description="Height in centimeters", gt=0, le=250)

    # Running Experience
    running_start_date: Optional[date] = Field(
        None, description="When the user started running"
    )
    years_experience: Optional[float] = Field(
        None, description="Years of running experience", ge=0
    )
    personal_bests: List[PersonalBest] = Field(
        default_factory=list, description="Personal best times at various distances"
    )

    # Health Information
    injuries: List[RunningInjury] = Field(
        default_factory=list, description="History of running injuries"
    )

    # Lifestyle Information
    sleep_hours_per_night: float = Field(
        ..., description="Average hours of sleep per night", ge=3, le=12
    )
    job_type: JobType = Field(..., description="Type of job/occupation")
    has_gym_access: bool = Field(..., description="Whether user has access to a gym")
    training_time_per_week_hours: float = Field(
        ..., description="Hours available for training per week", ge=0, le=40
    )

    # Goals
    main_running_goal: RunningGoal = Field(..., description="Primary running goal")
    additional_goals: List[str] = Field(
        default_factory=list, description="Additional running goals or notes"
    )

    # Optional Additional Information
    current_fitness_level: Optional[str] = Field(
        None, description="Self-assessed fitness level"
    )
    preferred_training_times: Optional[List[str]] = Field(
        None, description="Preferred times to train (e.g., 'morning', 'evening')"
    )
    training_preferences: Optional[str] = Field(
        None, description="Any specific training preferences or constraints"
    )

    @validator("years_experience", always=True)
    def calculate_experience(cls, v, values):
        """Calculate years of experience if not provided but start date is"""
        if (
            v is None
            and "running_start_date" in values
            and values["running_start_date"]
        ):
            from datetime import date

            today = date.today()
            start_date = values["running_start_date"]
            years = (today - start_date).days / 365.25
            return round(years, 1)
        return v

    @validator("personal_bests")
    def validate_personal_bests(cls, v):
        """Ensure personal bests are in ascending order by distance"""
        if v:
            distances = [pb.distance_km for pb in v]
            if distances != sorted(distances):
                raise ValueError(
                    "Personal bests should be ordered by distance (ascending)"
                )
        return v

    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index"""
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m**2), 1)

    @property
    def bmi_category(self) -> str:
        """Get BMI category"""
        bmi = self.bmi
        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "overweight"
        else:
            return "obese"

    class Config:
        """Pydantic configuration"""

        use_enum_values = True
        validate_assignment = True
        extra = "forbid"
        json_encoders = {date: lambda v: v.isoformat()}
