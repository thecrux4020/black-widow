import gc2

gcat = gc2.Gcat()

gcat.checkCommands()

print gcat.pending_tasks

for task in gcat.pending_tasks:
	gcat.sendEmail('daskjdajhdagdjhsagdsahdsgajdgashdfaghdasfdhas', task['task_id'])
	gcat.delete_pending_task(task['task_id'])
