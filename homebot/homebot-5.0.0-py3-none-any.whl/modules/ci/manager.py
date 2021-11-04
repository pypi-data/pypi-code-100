from homebot.core.error_handler import format_exception
from homebot.core.logging import LOGE, LOGI
from importlib import import_module
from queue import Queue
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from threading import Thread

class CIManager(Queue):
	def __init__(self):
		"""Initialize the QueueManager class."""
		super().__init__()
		self.current_workflow = None
		self.thread = Thread(target=self.daemon, name="CI daemon", daemon=True)
		self.thread.start()

	def daemon(self):
		while True:
			self.current_workflow = self.get()
			LOGI(f"CI workflow started, project: {self.current_workflow.name}")
			try:
				self.current_workflow.build()
			except Exception as e:
				LOGE("Unhandled exception from CI workflow:\n"
					 f"{format_exception(e)}")
			LOGI(f"CI workflow finished, project: {self.current_workflow.name}")
			self.current_workflow = None

	def add(self, name: str, update: Update, context: CallbackContext, args: list):
		try:
			project = import_module(f"homebot.modules.ci.projects.{name}", package="Project").Project
		except (ModuleNotFoundError, AttributeError):
			return "Error: Project script not found"
		except Exception as e:
			return ("Error: Error while importing project:\n"
					f"{format_exception(e)}")

		try:
			workflow = project(update, context, args)
		except Exception as e:
			return ("Error: Project class initialization failed:\n"
					f"{format_exception(e)}")

		self.put(workflow)

	def get_list(self):
		with self.mutex:
			return list(self.queue)

	def get_formatted_workflow(self, workflow):
		return (
			f"{workflow.name}\n"
			f"Arguments: {' '.join(workflow.args)}\n"
			f"Started by: {workflow.update.effective_user.name}\n"
		)

	def get_formatted_list(self):
		qsize = self.qsize()
		workflows_info = [f"{i}) " + self.get_formatted_workflow(workflow)
						  for i, workflow in enumerate(self.get_list(), 1)]
		running = self.current_workflow is not None
		text = f"CI status: Running: {str(running)}\n\n"
		if running:
			text += f"Running workflow: {self.get_formatted_workflow(self.current_workflow)}\n"
		text += f"Queued workflows: {qsize}\n\n"
		text += "\n".join(workflows_info)
		return text

manager = CIManager()
