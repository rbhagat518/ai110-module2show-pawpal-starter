# PawPal+ Project Reflection

## 1. System Design

three core actions a user should be able to perform:
add pets
add tasks for a pet
allocate time slots for each task
info needs to hold:
Classes: Pet, Task, Schedule, Scheduler
Pet object has attributes such as task objects, name. it has methods such as add task
Task Objects have attributes such as time, name.
Schedule class which interacts with Pet Objects and Tasks to generate schedules


**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

There are 4 critical classes to the UML design: Schedule, Scheduler, Pet and Task.
Each Pet has an associated Schedule to them. Each Pet has Tasks associated with them
The Scheduler class holds multitudes of Schedules and Pets.
More specifically, the Scheduler tracks the Pets and manages Schedules.
The Pets have tasks and own Schedules.
Schedules contain Tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, during implementation I opted to use a Task, Owner, Pet and Scheduler format. This reformatting was partially due to Copilot's suggestions and seemed like a simpler way to display the relationships.
## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler consider constraints on priority and preference. I decided this for organization and simplicity purposes.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff the scheduler makes is checking for conflicts only within a single pet's schedule, not across multiple pets. For example, in the `check_conflicts` method in `pawpal_system.py`, it iterates through tasks for one pet and compares their times and durations, but does not consider tasks from other pets. 
In a pet care scenario we may want overlap, but at the same time each pet's routine is typically independent, and cross-pet conflicts are less common or can be managed manually by the owner, keeping the system simple and focused on per-pet reliability rather than complex multi-pet optimization.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

Designing UML, Evaluating UML, Analyzing Core Functionality, Analyzing test cases, Implementing Core Functionality, Implementing Tests, Rewriting Explainations
Explaining, Implementing, Analyzing functionality was most helpful.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

UML diagram seemed too complicated initally.
I went a lot slower and understood the tests very carefully when taking AI suggestions.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I added conflict detection into my scheduling algorithm. Conflict detection is per-pet only, not cross-pet as we may want to overlap pet tasks across other pets (pet care scenario).

My Tests focus on:

Sorting Correctness: Verify tasks are returned in chronological order.
Recurrence Logic: Confirm that marking a daily task complete creates a new task for the following day.
Conflict Detection: Verify that the Scheduler flags duplicate times.


**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

Confidence Level: 3 stars. This testing code seems to be working correctly, but I can't tell if my implementation/design is 


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm satisfied with the end to end development of this project.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

Add more complexity to the scheduling.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Its so easy to get a bunch of code thrown at you and get so lost.

