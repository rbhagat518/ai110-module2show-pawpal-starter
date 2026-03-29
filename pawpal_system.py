from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum


class Frequency(Enum):
    """Task frequency options."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ONCE = "once"


class CompletionStatus(Enum):
    """Task completion status."""
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"


@dataclass
class Task:
    """Represents a single activity for a pet."""
    description: str
    time: datetime
    frequency: Frequency = Frequency.ONCE
    completion_status: CompletionStatus = CompletionStatus.PENDING
    duration: int = 30  # in minutes
    priority: int = 0

    def get_description(self) -> str:
        """Return the task description."""
        return self.description

    def get_time(self) -> datetime:
        """Return the task time."""
        return self.time

    def get_duration(self) -> int:
        """Return the task duration in minutes."""
        return self.duration

    def set_time(self, time: datetime) -> None:
        """Set a new time for the task."""
        self.time = time

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completion_status = CompletionStatus.COMPLETED

    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        return self.time < datetime.now() and self.completion_status == CompletionStatus.PENDING

    def get_next_occurrence(self) -> Optional[datetime]:
        """Get the next occurrence based on frequency."""
        if self.frequency == Frequency.ONCE:
            return None
        elif self.frequency == Frequency.DAILY:
            return self.time + timedelta(days=1)
        elif self.frequency == Frequency.WEEKLY:
            return self.time + timedelta(weeks=1)
        elif self.frequency == Frequency.MONTHLY:
            # Approximate monthly as 30 days
            return self.time + timedelta(days=30)
        return None


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    name: str
    species: str = ""
    age: Optional[int] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return only pending tasks."""
        return [task for task in self.tasks if task.completion_status == CompletionStatus.PENDING]

    def get_completed_tasks(self) -> List[Task]:
        """Return only completed tasks."""
        return [task for task in self.tasks if task.completion_status == CompletionStatus.COMPLETED]

    def get_overdue_tasks(self) -> List[Task]:
        """Return only overdue tasks."""
        return [task for task in self.tasks if task.is_overdue()]

    def get_name(self) -> str:
        """Return the pet's name."""
        return self.name


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's collection."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pets(self) -> List[Pet]:
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all pending tasks across all pets."""
        all_pending = []
        for pet in self.pets:
            all_pending.extend(pet.get_pending_tasks())
        return all_pending

    def get_all_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks across all pets."""
        all_overdue = []
        for pet in self.pets:
            all_overdue.extend(pet.get_overdue_tasks())
        return all_overdue

    def get_tasks_by_pet(self, pet_name: str) -> List[Task]:
        """Get all tasks for a specific pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_upcoming_tasks(self, hours_ahead: int = 24) -> List[Task]:
        """Get all tasks scheduled within the next specified hours."""
        now = datetime.now()
        cutoff = now + timedelta(hours=hours_ahead)
        upcoming = []

        for task in self.owner.get_all_tasks():
            if task.time >= now and task.time <= cutoff and task.completion_status == CompletionStatus.PENDING:
                upcoming.append(task)

        return sorted(upcoming, key=lambda t: t.time)

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks across all pets."""
        return self.owner.get_all_overdue_tasks()

    def organize_tasks_by_priority(self) -> List[Task]:
        """Organize all pending tasks by priority (highest first)."""
        pending_tasks = self.owner.get_all_pending_tasks()
        return sorted(pending_tasks, key=lambda t: (-t.priority, t.time))

    def schedule_task(self, pet: Pet, task: Task) -> None:
        """Schedule a new task for a specific pet."""
        pet.add_task(task)

    def mark_task_completed(self, task: Task) -> None:
        """Mark a task as completed."""
        task.mark_completed()

    def reschedule_task(self, task: Task, new_time: datetime) -> None:
        """Reschedule a task to a new time."""
        task.set_time(new_time)

    def get_pet_schedule(self, pet: Pet, date: Optional[datetime] = None) -> List[Task]:
        """Get all tasks for a specific pet on a given date."""
        if date is None:
            date = datetime.now()

        # Get tasks for the specific date
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        pet_tasks = []
        for task in pet.get_tasks():
            if start_of_day <= task.time < end_of_day and task.completion_status == CompletionStatus.PENDING:
                pet_tasks.append(task)

        return sorted(pet_tasks, key=lambda t: t.time)

    def check_conflicts(self, pet: Pet, date: Optional[datetime] = None) -> List[str]:
        """Check for time conflicts in a pet's schedule for a given date."""
        tasks = self.get_pet_schedule(pet, date)
        conflicts = []

        for i, task1 in enumerate(tasks):
            task1_end = task1.time + timedelta(minutes=task1.duration)
            for task2 in tasks[i+1:]:
                if task2.time < task1_end:
                    conflicts.append(f"Conflict between '{task1.description}' and '{task2.description}'")

        return conflicts

    def generate_daily_summary(self, date: Optional[datetime] = None) -> str:
        """Generate a daily summary of all tasks."""
        if date is None:
            date = datetime.now()

        summary = f"Daily Summary for {date.strftime('%Y-%m-%d')}\n"
        summary += "=" * 40 + "\n\n"

        for pet in self.owner.get_pets():
            pet_tasks = self.get_pet_schedule(pet, date)
            if pet_tasks:
                summary += f"{pet.name} ({pet.species}):\n"
                for task in pet_tasks:
                    status_icon = "✓" if task.completion_status == CompletionStatus.COMPLETED else "○"
                    summary += f"  {status_icon} {task.time.strftime('%H:%M')} - {task.description}\n"
                summary += "\n"

        overdue = self.get_overdue_tasks()
        if overdue:
            summary += "Overdue Tasks:\n"
            for task in overdue:
                summary += f"  ⚠️  {task.description} (was due {task.time.strftime('%Y-%m-%d %H:%M')})\n"

        return summary
