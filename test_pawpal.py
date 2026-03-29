#!/usr/bin/env python3
"""
Unit tests for PawPal+ Pet Care Scheduler
Tests core functionality of Task and Pet classes.
"""

import pytest
from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler, Frequency, CompletionStatus


class TestTaskCompletion:
    """Test task completion functionality."""

    def test_mark_completed_changes_status(self):
        """Verify that calling mark_completed() changes the task's status from PENDING to COMPLETED."""
        # Create a task with PENDING status
        task = Task(
            description="Test task",
            time=datetime.now() + timedelta(hours=1),
            frequency=Frequency.ONCE,
            completion_status=CompletionStatus.PENDING
        )

        # Verify initial status is PENDING
        assert task.completion_status == CompletionStatus.PENDING

        # Mark task as completed
        task.mark_completed()

        # Verify status changed to COMPLETED
        assert task.completion_status == CompletionStatus.COMPLETED

    def test_mark_completed_multiple_calls(self):
        """Verify that calling mark_completed() multiple times keeps status as COMPLETED."""
        task = Task(
            description="Test task",
            time=datetime.now() + timedelta(hours=1),
            frequency=Frequency.ONCE,
            completion_status=CompletionStatus.PENDING
        )

        # Mark completed once
        task.mark_completed()
        assert task.completion_status == CompletionStatus.COMPLETED

        # Mark completed again
        task.mark_completed()
        assert task.completion_status == CompletionStatus.COMPLETED


class TestTaskAddition:
    """Test task addition functionality."""

    def test_add_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Create a pet with no tasks
        pet = Pet(name="TestPet", species="Dog")

        # Verify initial task count is 0
        assert len(pet.tasks) == 0
        assert len(pet.get_tasks()) == 0

        # Create and add a task
        task = Task(
            description="Test task",
            time=datetime.now() + timedelta(hours=1),
            frequency=Frequency.ONCE
        )
        pet.add_task(task)

        # Verify task count increased to 1
        assert len(pet.tasks) == 1
        assert len(pet.get_tasks()) == 1
        assert pet.get_tasks()[0] == task

    def test_add_multiple_tasks_increases_count(self):
        """Verify that adding multiple tasks increases the pet's task count accordingly."""
        pet = Pet(name="TestPet", species="Cat")

        # Verify initial count
        assert len(pet.get_tasks()) == 0

        # Add first task
        task1 = Task(description="Task 1", time=datetime.now() + timedelta(hours=1))
        pet.add_task(task1)
        assert len(pet.get_tasks()) == 1

        # Add second task
        task2 = Task(description="Task 2", time=datetime.now() + timedelta(hours=2))
        pet.add_task(task2)
        assert len(pet.get_tasks()) == 2

        # Add third task
        task3 = Task(description="Task 3", time=datetime.now() + timedelta(hours=3))
        pet.add_task(task3)
        assert len(pet.get_tasks()) == 3

        # Verify all tasks are present
        tasks = pet.get_tasks()
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks

    def test_add_task_to_different_pets(self):
        """Verify that adding tasks to different pets maintains separate task lists."""
        pet1 = Pet(name="Max", species="Dog")
        pet2 = Pet(name="Luna", species="Cat")

        # Create tasks
        task1 = Task(description="Walk Max", time=datetime.now() + timedelta(hours=1))
        task2 = Task(description="Feed Luna", time=datetime.now() + timedelta(hours=2))

        # Add task to pet1
        pet1.add_task(task1)
        assert len(pet1.get_tasks()) == 1
        assert len(pet2.get_tasks()) == 0
        assert task1 in pet1.get_tasks()
        assert task1 not in pet2.get_tasks()

        # Add task to pet2
        pet2.add_task(task2)
        assert len(pet1.get_tasks()) == 1
        assert len(pet2.get_tasks()) == 1
        assert task2 in pet2.get_tasks()
        assert task2 not in pet1.get_tasks()


class TestSchedulerAndTaskCoreFeatures:
    """Test additional core behaviors for tasks, pets, and scheduler."""

    def test_task_next_occurrence_frequency(self):
        now = datetime.now()
        task_once = Task(description="Once", time=now, frequency=Frequency.ONCE)
        task_daily = Task(description="Daily", time=now, frequency=Frequency.DAILY)
        task_weekly = Task(description="Weekly", time=now, frequency=Frequency.WEEKLY)
        task_monthly = Task(description="Monthly", time=now, frequency=Frequency.MONTHLY)

        assert task_once.get_next_occurrence() is None
        assert task_daily.get_next_occurrence() == now + timedelta(days=1)
        assert task_weekly.get_next_occurrence() == now + timedelta(weeks=1)
        assert task_monthly.get_next_occurrence() == now + timedelta(days=30)

    def test_task_is_overdue_flag(self):
        overdue_time = datetime.now() - timedelta(days=1)
        overdue_task = Task(description="Overdue", time=overdue_time, completion_status=CompletionStatus.PENDING)
        completed_task = Task(description="Done", time=overdue_time, completion_status=CompletionStatus.COMPLETED)

        assert overdue_task.is_overdue() is True
        assert completed_task.is_overdue() is False

    def test_pet_overdue_tasks_reporting(self):
        pet = Pet(name="TestPet", species="Dog")
        overdue_task = Task(description="Overdue", time=datetime.now() - timedelta(days=1), completion_status=CompletionStatus.PENDING)
        pending_task = Task(description="Pending", time=datetime.now() + timedelta(hours=1), completion_status=CompletionStatus.PENDING)

        pet.add_task(overdue_task)
        pet.add_task(pending_task)

        overdue_tasks = pet.get_overdue_tasks()
        assert len(overdue_tasks) == 1
        assert overdue_task in overdue_tasks

    def test_scheduler_organize_tasks_by_priority(self):
        owner = Owner(name="Owner")
        pet = Pet(name="Buddy", species="Dog")
        owner.add_pet(pet)

        low = Task(description="Low", time=datetime.now() + timedelta(hours=1), priority=1)
        high = Task(description="High", time=datetime.now() + timedelta(hours=2), priority=5)
        mid = Task(description="Mid", time=datetime.now() + timedelta(hours=3), priority=3)

        pet.add_task(low)
        pet.add_task(high)
        pet.add_task(mid)

        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.organize_tasks_by_priority()

        assert sorted_tasks == [high, mid, low]

    def test_scheduler_conflict_detection(self):
        owner = Owner(name="Owner")
        pet = Pet(name="Buddy", species="Dog")
        owner.add_pet(pet)

        t0 = datetime.now().replace(second=0, microsecond=0)
        task1 = Task(description="Task 1", time=t0 + timedelta(hours=1), duration=60)
        task2 = Task(description="Task 2", time=t0 + timedelta(hours=1, minutes=30), duration=30)
        task3 = Task(description="Task 3", time=t0 + timedelta(hours=3), duration=30)

        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        scheduler = Scheduler(owner)
        conflicts = scheduler.check_conflicts(pet)

        assert len(conflicts) == 1
        assert "Task 1" in conflicts[0] and "Task 2" in conflicts[0]

    def test_scheduler_flags_duplicate_times_as_conflict(self):
        owner = Owner(name="Owner")
        pet = Pet(name="Buddy", species="Dog")
        owner.add_pet(pet)

        when = datetime.now().replace(second=0, microsecond=0) + timedelta(hours=1)
        task_a = Task(description="Task A", time=when, duration=30)
        task_b = Task(description="Task B", time=when, duration=30)

        pet.add_task(task_a)
        pet.add_task(task_b)

        scheduler = Scheduler(owner)
        conflicts = scheduler.check_conflicts(pet)

        assert len(conflicts) == 1
        assert "Task A" in conflicts[0] and "Task B" in conflicts[0]

    def test_scheduler_get_upcoming_tasks_chronological_order(self):
        owner = Owner(name="Owner")
        pet = Pet(name="Buddy", species="Dog")
        owner.add_pet(pet)

        now = datetime.now().replace(second=0, microsecond=0)
        earliest = Task(description="Earliest", time=now + timedelta(hours=1))
        middle = Task(description="Middle", time=now + timedelta(hours=2))
        latest = Task(description="Latest", time=now + timedelta(hours=3))

        pet.add_task(middle)
        pet.add_task(latest)
        pet.add_task(earliest)

        scheduler = Scheduler(owner)
        upcoming = scheduler.get_upcoming_tasks(hours_ahead=4)

        assert upcoming == [earliest, middle, latest]

    def test_recurring_daily_task_completion_creates_next_task(self):
        owner = Owner(name="Owner")
        pet = Pet(name="Buddy", species="Dog")
        owner.add_pet(pet)

        now = datetime.now().replace(second=0, microsecond=0)
        daily_task = Task(description="Daily Walk", time=now, frequency=Frequency.DAILY)
        pet.add_task(daily_task)

        scheduler = Scheduler(owner)
        next_task = scheduler.mark_task_completed(daily_task, pet=pet)

        assert daily_task.completion_status == CompletionStatus.COMPLETED
        assert next_task is not None
        assert next_task.frequency == Frequency.DAILY
        assert next_task.time == now + timedelta(days=1)
        assert next_task.completion_status == CompletionStatus.PENDING

        all_tasks = pet.get_tasks()
        assert len(all_tasks) == 2
        assert next_task in all_tasks

    """Test task status filtering methods."""

    def test_get_pending_tasks(self):
        """Verify get_pending_tasks returns only pending tasks."""
        pet = Pet(name="TestPet", species="Dog")

        # Create tasks with different statuses
        pending_task = Task(
            description="Pending task",
            time=datetime.now() + timedelta(hours=1),
            completion_status=CompletionStatus.PENDING
        )
        completed_task = Task(
            description="Completed task",
            time=datetime.now() + timedelta(hours=2),
            completion_status=CompletionStatus.COMPLETED
        )

        pet.add_task(pending_task)
        pet.add_task(completed_task)

        # Verify pending tasks
        pending_tasks = pet.get_pending_tasks()
        assert len(pending_tasks) == 1
        assert pending_task in pending_tasks
        assert completed_task not in pending_tasks

    def test_get_completed_tasks(self):
        """Verify get_completed_tasks returns only completed tasks."""
        pet = Pet(name="TestPet", species="Dog")

        # Create tasks with different statuses
        pending_task = Task(
            description="Pending task",
            time=datetime.now() + timedelta(hours=1),
            completion_status=CompletionStatus.PENDING
        )
        completed_task = Task(
            description="Completed task",
            time=datetime.now() + timedelta(hours=2),
            completion_status=CompletionStatus.COMPLETED
        )

        pet.add_task(pending_task)
        pet.add_task(completed_task)

        # Verify completed tasks
        completed_tasks = pet.get_completed_tasks()
        assert len(completed_tasks) == 1
        assert completed_task in completed_tasks
        assert pending_task not in completed_tasks


if __name__ == "__main__":
    pytest.main([__file__])
