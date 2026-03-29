import streamlit as st
from datetime import datetime

from pawpal_system import Owner, Pet, Task, Scheduler, Frequency, CompletionStatus

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

# session-stored owner to survive reruns
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
else:
    if st.session_state.owner.name != owner_name:
        st.session_state.owner.name = owner_name

st.markdown("### Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner = st.session_state.owner
    existing_pet = next((p for p in owner.get_pets() if p.name.lower() == pet_name.strip().lower()), None)
    if existing_pet:
        st.info(f"Pet '{pet_name}' already added")
        st.session_state.current_pet = existing_pet
    else:
        new_pet = Pet(name=pet_name.strip(), species=species)
        owner.add_pet(new_pet)
        st.success(f"Added pet '{pet_name}'")
        st.session_state.current_pet = new_pet

if "current_pet" in st.session_state:
    st.write("Current pet:", f"{st.session_state.current_pet.name} ({st.session_state.current_pet.species})")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

task_time = st.datetime_input("Task date/time", value=datetime.now())

if st.button("Schedule task"):
    if "current_pet" not in st.session_state:
        st.error("Select or add a pet before scheduling tasks.")
    else:
        pet = st.session_state.current_pet
        priority_map = {"low": 1, "medium": 2, "high": 3}
        task = Task(
            description=task_title,
            time=task_time,
            duration=int(duration),
            priority=priority_map.get(priority, 1),
        )
        scheduler = Scheduler(st.session_state.owner)
        scheduler.schedule_task(pet, task)

        st.session_state.tasks.append(
            {
                "pet": pet.name,
                "description": task_title,
                "time": task_time.strftime("%Y-%m-%d %H:%M"),
                "duration_minutes": int(duration),
                "priority": priority,
            }
        )

        st.success(f"Scheduled task '{task_title}' for {pet.name}")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button now calls your scheduler logic from pawpal_system.")

if st.button("Generate schedule"):
    owner = st.session_state.owner
    scheduler = Scheduler(owner)

    upcoming = scheduler.get_upcoming_tasks(hours_ahead=24)
    if not upcoming:
        st.info("No upcoming tasks in the next 24 hours.")
    else:
        st.write("Upcoming tasks in next 24h:")
        schedule_rows = [
            {
                "pet": next((pet.name for pet in owner.get_pets() if task in pet.tasks), "N/A"),
                "task": task.description,
                "time": task.time.strftime("%Y-%m-%d %H:%M"),
                "priority": task.priority,
                "status": task.completion_status.value,
            }
            for task in upcoming
        ]
        st.table(schedule_rows)

    overdue = scheduler.get_overdue_tasks()
    if overdue:
        st.warning("Overdue tasks detected:")
        overdue_rows = [
            {
                "pet": next((pet.name for pet in owner.get_pets() if task in pet.tasks), "N/A"),
                "task": task.description,
                "time": task.time.strftime("%Y-%m-%d %H:%M"),
                "status": task.completion_status.value,
            }
            for task in overdue
        ]
        st.table(overdue_rows)
