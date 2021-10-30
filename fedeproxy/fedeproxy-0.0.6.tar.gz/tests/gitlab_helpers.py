class GitLabHelpers(object):
    def __init__(self, g):
        self.g = g

    def hooks_relax_restrictions(self):
        settings = self.g.settings.get()
        settings.allow_local_requests_from_system_hooks = True
        settings.allow_local_requests_from_web_hooks_and_services = True
        settings.save()
