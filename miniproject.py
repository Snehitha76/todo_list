import json
from datetime import datetime, timedelta

# File to save tasks
TASK_FILE = 'tasks.json'

# Load tasks from a file
def load_tasks():
    try:
        with open(TASK_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to a file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Check if a task is due soon (within 3 days)
def is_due_soon(task):
    if task['due_date']:
        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
        return due_date <= datetime.now() + timedelta(days=3)
    return False

# Add a new task with priority level
def add_task(tasks):
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD) or leave empty: ")
    priority = input("Enter priority (low/medium/high) or leave empty: ").lower()
    due_date = due_date if due_date else None
    priority = priority if priority in ['low', 'medium', 'high'] else 'medium'  # default to medium

    task = {
        'description': description,
        'due_date': due_date,
        'status': 'Pending',
        'priority': priority
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added with priority:", priority)

# View tasks with optional filters and display priority
def view_tasks(tasks, filter_by=None):
    if filter_by == 'completed':
        filtered_tasks = [task for task in tasks if task['status'] == 'Completed']
    elif filter_by == 'pending':
        filtered_tasks = [task for task in tasks if task['status'] == 'Pending']
    elif filter_by == 'due_soon':
        filtered_tasks = [task for task in tasks if is_due_soon(task)]
    else:
        filtered_tasks = tasks

    if not filtered_tasks:
        print("No tasks to display.")
    else:
        for idx, task in enumerate(filtered_tasks, 1):
            due_info = f"(Due: {task['due_date']})" if task['due_date'] else "(No due date)"
            print(f"{idx}. {task['description']} {due_info} - {task['status']} - Priority: {task['priority'].capitalize()}")

# Mark a task as completed
def complete_task(tasks):
    view_tasks(tasks, filter_by='pending')
    index = int(input("Enter task number to mark as completed: ")) - 1
    tasks[index]['status'] = 'Completed'
    save_tasks(tasks)
    print("Task marked as completed!")

# Edit a task's description or due date
def edit_task(tasks):
    view_tasks(tasks)
    index = int(input("Enter task number to edit: ")) - 1
    new_description = input("Enter new task description or press Enter to skip: ")
    new_due_date = input("Enter new due date (YYYY-MM-DD) or press Enter to skip: ")
    if new_description:
        tasks[index]['description'] = new_description
    if new_due_date:
        tasks[index]['due_date'] = new_due_date
    save_tasks(tasks)
    print("Task updated!")

# Delete a task
def delete_task(tasks):
    view_tasks(tasks)
    index = int(input("Enter task number to delete: ")) - 1
    tasks.pop(index)
    save_tasks(tasks)
    print("Task deleted!")

# Check and remind about tasks due soon
def check_reminders(tasks):
    print("\n--- Task Reminders ---")
    due_soon_tasks = [task for task in tasks if task['status'] == 'Pending' and is_due_soon(task)]

    if due_soon_tasks:
        print("Reminder: You have tasks due soon!")
        for task in due_soon_tasks:
            print(f"- {task['description']} (Due: {task['due_date']}) - Priority: {task['priority'].capitalize()}")
    else:
        print("No tasks are due soon.")
    print("-----------------------\n")

# User-friendly menu
def show_menu():
    print("\nTo-Do List Manager")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("4. Edit Task")
    print("5. Delete Task")
    print("6. Exit")

# Main function
def main():
    tasks = load_tasks()
    check_reminders(tasks)  # Notify user of tasks due soon

    while True:
        show_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_filter = input("View [all/completed/pending/due_soon]: ").strip().lower()
            view_tasks(tasks, filter_by=view_filter)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            edit_task(tasks)
        elif choice == '5':
            delete_task(tasks)
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
