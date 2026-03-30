# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features Implemented

### Core Scheduling Algorithms

- **Chronological Sorting**: Tasks are sorted by date/time to display upcoming events in order
- **Priority-Based Sorting**: `organize_tasks_by_priority()` sorts tasks by priority (high → low) with chronological ordering as tiebreaker
- **Time Window Filtering**: `get_upcoming_tasks()` retrieves tasks within a specified timeframe (default: next 24 hours)
- **Per-Pet Scheduling**: `get_pet_schedule()` generates daily schedules for individual pets

### Conflict Detection

- **Overlap Detection**: Identifies when two tasks scheduled for the same pet have overlapping time windows
- **Duration-Aware Conflicts**: Calculates each task's end time using duration and checks for collisions
- **Per-Pet Isolation**: Conflicts are detected per-pet only, allowing cross-pet task overlap (realistic for multi-pet households)

### Recurrence & Task Management

- **Daily Recurrence**: Recurring tasks automatically generate new instances for the following day upon completion
- **Frequency Support**: Tasks support ONCE, DAILY, WEEKLY, and MONTHLY recurrence patterns
- **Auto-Rescheduling**: `mark_task_completed()` automatically creates next occurrence while setting current task status to COMPLETED
- **Overdue Tracking**: Identifies pending tasks past their scheduled time

### Task Organization

- **Multi-Pet Support**: Owner manages multiple pets, each with independent task lists
- **Status Filtering**: Tasks tracked with PENDING, COMPLETED, and OVERDUE statuses
- **Dynamic Filtering**: Retrieve tasks by pet, by date, by status, or within time windows
- **Task Rescheduling**: Modify task timing without removing the task

### Reporting

- **Daily Summary Generation**: `generate_daily_summary()` creates formatted reports of all tasks per pet with visual indicators
- **Conflict Warnings**: Schedule generation alerts when overlapping tasks are detected
- **Overdue Alerts**: Displays pending tasks that have passed their scheduled time

### Smarter Scheduling

I added conflict detection into my scheduling algorithm. Conflict detection is per-pet only, not cross-pet as we may want to overlap pet tasks across other pets (pet care scenario).


### Testing PawPal+
My Tests focus on:

Sorting Correctness: Verify tasks are returned in chronological order.
Recurrence Logic: Confirm that marking a daily task complete creates a new task for the following day.
Conflict Detection: Verify that the Scheduler flags duplicate times.

Confidence Level: 3 stars. This testing code seems to be working correctly, but I can't tell if my implementation/design is 

### 📸 Demo

<a href="/ai110-module2show-pawpal-starter/demo.png" target="_blank"><img src='/ai110-module2show-pawpal-starter/demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

