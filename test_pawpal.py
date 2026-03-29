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


class TestTaskStatusFiltering:
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
