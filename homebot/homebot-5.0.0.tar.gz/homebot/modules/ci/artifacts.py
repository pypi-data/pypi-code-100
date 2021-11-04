from pathlib import Path

(
	STATUS_ON_QUEUE,
	STATUS_UPLOADING,
	STATUS_SUCCESS,
	STATUS_ERROR,
) = range(4)

STATUS_MESSAGE = {
	STATUS_ON_QUEUE: "On queue",
	STATUS_UPLOADING: "Uploading",
	STATUS_SUCCESS: "Uploaded",
	STATUS_ERROR: "Error while uploading",
}

class Artifacts(dict):
	def __init__(self, path: Path, patterns: str):
		"""Find the artifacts."""
		super().__init__()
		self.path = path
		self.patterns = patterns

	def update(self):
		self.clear()
		files = [list(self.path.glob(pattern)) for pattern in self.patterns]
		for artifact in [artifact for sublist in files for artifact in sublist]:
			self[artifact] = STATUS_ON_QUEUE

	def get_artifacts_on_status(self, status: int):
		return [k for k, v in self.items() if v == status]

	def get_readable_artifacts_list(self):
		artifact_total = len(self)
		artifact_uploaded = len(self.get_artifacts_on_status(STATUS_SUCCESS))

		text = f"Uploaded {artifact_uploaded} out of {artifact_total} artifact(s)\n"
		for i, artifact in enumerate(self.keys(), 1):
			text += f"{i}) {artifact.name}: {STATUS_MESSAGE[self[artifact]]}\n"
		return text
