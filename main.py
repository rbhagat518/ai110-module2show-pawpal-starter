#!/usr/bin/env python3
"""
PawPal+ Pet Care Scheduler - Main Application
Demonstrates the core functionality of the pet care scheduling system.
"""

from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, Frequency, CompletionStatus


def main():
    """Main application entry point."""
    print("🐾 PawPal+ Pet Care Scheduler")
    print("=" * 40)

    # Create an owner
    owner = Owner(name="Alex Johnson")

    # Create pets
    max_pet = Pet(name="Max", species="Dog", age=3)
    luna_pet = Pet(name="Luna", species="Cat", age=2)

    # Add pets to owner
    owner.add_pet(max_pet)
    owner.add_pet(luna_pet)

    # Create tasks for today (set to future times)
    now = datetime.now()
    today_base = now.replace(hour=14, minute=0, second=0, microsecond=0)  # Start at 2 PM

    # Tasks for Max (Dog)
    max_walk = Task(
        description="Afternoon walk",
        time=today_base,
        frequency=Frequency.DAILY,
        duration=30,
        priority=3
    )

    max_feed = Task(
        description="Evening feeding",
        time=today_base + timedelta(hours=2),
        frequency=Frequency.DAILY,
        duration=10,
        priority=2
    )

    # Add a conflict task at the same exact time to verify warning behavior
    max_conflict = Task(
        description="Quick grooming",
        time=today_base + timedelta(hours=2),
        frequency=Frequency.ONCE,
        duration=15,
        priority=4
    )

    max_play = Task(
        description="Evening playtime",
        time=today_base + timedelta(hours=4),
        frequency=Frequency.DAILY,
        duration=45,
        priority=1
    )

    # Tasks for Luna (Cat)
    luna_feed = Task(
        description="Evening feeding",
        time=today_base + timedelta(hours=2, minutes=30),
        frequency=Frequency.DAILY,
        duration=5,
        priority=2
    )

    luna_litter = Task(
        description="Evening litter box cleaning",
        time=today_base + timedelta(hours=3, minutes=30),
        frequency=Frequency.DAILY,
        duration=15,
        priority=2
    )

    # Add tasks out of chronological order to test sorting behavior
    # (max_play is late, max_walk is early, max_feed is in-between)
    max_pet.add_task(max_play)
    max_pet.add_task(max_walk)
    max_pet.add_task(max_feed)
    max_pet.add_task(max_conflict)

    # (luna_litter is later than luna_feed)
    luna_pet.add_task(luna_litter)
    luna_pet.add_task(luna_feed)

    # Create scheduler and display today's schedule
    scheduler = Scheduler(owner)

    print(f"\nToday's Schedule for {owner.name}")
    print("-" * 40)

    # Generate and print the daily summary
    daily_summary = scheduler.generate_daily_summary()
    print(daily_summary)

    # Show upcoming tasks for the next 6 hours
    print("\n📋 Upcoming Tasks (Next 6 Hours)")
    print("-" * 35)
    upcoming = scheduler.get_upcoming_tasks(hours_ahead=6)
    if upcoming:
        for task in upcoming:
            pet_name = ""
            for pet in owner.get_pets():
                if task in pet.get_tasks():
                    pet_name = f"({pet.name})"
                    break
            print(f"• {task.time.strftime('%H:%M')} - {task.description} {pet_name}")
    else:
        print("No upcoming tasks in the next 6 hours.")

    # Check for conflicts
    print("\n⚠️  Schedule Conflicts")
    print("-" * 20)
    conflicts_found = False
    for pet in owner.get_pets():
        pet_conflicts = scheduler.check_conflicts(pet)
        if pet_conflicts:
            conflicts_found = True
            print(f"{pet.name}:")
            for conflict in pet_conflicts:
                print(f"  • {conflict}")

    if not conflicts_found:
        print("No conflicts detected! ✅")

    # Demonstrate sorting/filtering methods
    print("\n🧪 Validation: sorting and filtering checks")
    print("-" * 35)
    all_tasks = owner.get_all_tasks()
    print("All tasks (in insertion order):")
    for task in all_tasks:
        print(f"  • {task.time.strftime('%H:%M')} - {task.description} ({task.frequency.value})")

    print("\nAll tasks sorted by time:")
    sorted_by_time = sorted(all_tasks, key=lambda t: t.time)
    for task in sorted_by_time:
        print(f"  • {task.time.strftime('%H:%M')} - {task.description}")

    print("\nUpcoming pending tasks (next 6h via scheduler.get_upcoming_tasks):")
    upcoming_sorted = scheduler.get_upcoming_tasks(hours_ahead=6)
    for task in upcoming_sorted:
        print(f"  • {task.time.strftime('%H:%M')} - {task.description}")

    print("\nTasks for Max (by pet filter):")
    max_tasks = owner.get_tasks_by_pet('Max')
    for task in max_tasks:
        print(f"  • {task.time.strftime('%H:%M')} - {task.description} [{task.completion_status.value}]")

    # Mark one task completed and filter by status
    if max_tasks:
        max_tasks[0].mark_completed()

    pending_max = [t for t in max_tasks if t.completion_status == CompletionStatus.PENDING]
    print("\nPending tasks for Max:")
    for task in pending_max:
        print(f"  • {task.time.strftime('%H:%M')} - {task.description}")

    print("\n🎯 Priority Tasks")
    print("-" * 15)
    priority_tasks = scheduler.organize_tasks_by_priority()
    for i, task in enumerate(priority_tasks[:5], 1):  # Show top 5
        pet_name = ""
        for pet in owner.get_pets():
            if task in pet.get_tasks():
                pet_name = f"({pet.name})"
                break
        priority_icon = "🔴" if task.priority >= 3 else "🟡" if task.priority >= 2 else "🟢"
        print(f"{i}. {priority_icon} {task.description} {pet_name}")


if __name__ == "__main__":
    main()
