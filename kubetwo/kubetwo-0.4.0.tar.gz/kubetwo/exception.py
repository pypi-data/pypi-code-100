class ProcessException(Exception):
    pass

class CheckDeniedException(Exception):
    pass

class AnsibleException(ProcessException):
    pass

class AnsibleKubesprayException(AnsibleException):
    pass

class AnsibleSetupException(AnsibleException):
    pass

class AnsibleDeploySampleException(AnsibleException):
    pass

class AnsibleFetchAdminConfException(AnsibleException):
    pass

class TerraformException(ProcessException):
    pass

class TerraformInitException(TerraformException):
    pass

class TerraformPlanException(TerraformException):
    pass

class TerraformApplyException(TerraformException):
    pass

class TerraformDestroyException(TerraformException):
    pass

class TerraformStateNotFound(Exception):
    pass
