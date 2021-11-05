from abc import abstractmethod
from functools import wraps
from typing import List, Optional, Sequence, TypeVar, Union

from pyjackson.decorators import type_field

from algolink.client.expose import ExposedMethod
from algolink.core import errors
from algolink.core.objects import core

Project = 'core.Project'
Task = 'core.Task'
Model = 'core.Model'
Image = 'core.Image'
Pipeline = 'core.Pipeline'
RuntimeEnvironment = 'core.RuntimeEnvironment'

## ML tracking
Experiment = 'core.Experiment'
ModelMetric = 'core.ModelMetric'
ModelParam ='core.ModelParam'
BestResult = 'core.BestResult'

T = TypeVar('T')
NameOrIdOrObject = Union[int, str, T]
ProjectVar = NameOrIdOrObject[Project]
TaskVar = NameOrIdOrObject[Task]
ModelVar = NameOrIdOrObject[Model]
PipelineVar = NameOrIdOrObject[Pipeline]
EnvironmentVar = NameOrIdOrObject[RuntimeEnvironment]

ExperimentVar = NameOrIdOrObject[Experiment]
ModelMetricVar = NameOrIdOrObject[ModelMetric]
ModelParamVar = NameOrIdOrObject[ModelParam]
BestResultVar = NameOrIdOrObject[BestResult]

class ExposedMetadataMethod(ExposedMethod):
    def __init__(self, bind=True, name: str = None):
        super().__init__(name)
        self.bind = bind
        self.method = None

    def generate_code(self):
        fields = self.get_signature().args
        declaration = self.get_declaration().replace('core.', '')
        result = f'''self.meta_repo.{self.original_name}({', '.join(f.name for f in fields)})'''
        if self.bind:
            result = f'''self._bind({result})'''
        return f'''    {declaration}
        """{self.method.__doc__}"""
        return {result}'''


def bind_to_self(method):
    """
    Decorator for methods which binds method result to metadata repository contained in `self` reference.

    :param method: method to decorate
    :return: decorated method
    """

    @wraps(method)
    def inner(self, *args, **kwargs):
        res = method(self, *args, **kwargs)
        if isinstance(res, core.AlgoLinkObject):
            res.bind_meta_repo(self)
        elif isinstance(res, Sequence):
            for o in res:
                o.bind_meta_repo(self)
        return res

    return inner


@type_field('type')
class MetadataRepository:
    """
    Abstract base class for persistent repositories of metadata (:class:`.core.Project`, :class:`.core.Task`, etc)
    """

    type = None

    @abstractmethod
    @ExposedMetadataMethod()
    def get_projects(self) -> List['core.Project']:
        """
        Gets all projects in the repository

        :return: all projects in the repository
        """

    @abstractmethod
    @ExposedMetadataMethod(name='get_project')
    def get_project_by_name(self, name: str) -> Optional['core.Project']:
        """
        Finds project in the repository by name

        :param name: name of the project to return
        :return: found project if exists or `None`
        """
    
    @abstractmethod
    def get_project_by_id(self, id: int) -> Optional['core.Project']:
        """
        Finds project in the repository by identifier

        :param id: project id
        :return: found project if exists or `None`
        """

    @abstractmethod
    def create_project(self, project: Project) -> Project:
        """
        Creates the project and all its tasks.

        :param project: project to create
        :return: created project
        :exception: :exc:`.errors.ExistingProjectError` if given project has the same name as existing one.
        """
    @abstractmethod
    def update_project(self, project: Project) -> Project:
        """
        Updates the project and all its tasks.

        :param project: project to update
        :return: updated project
        :exception: :exc:`.errors.NonExistingProjectError` if given project doesn't exist in the repository
        """

    @abstractmethod
    def delete_project(self, project: Project):
        """
        Deletes the project and all tasks.

        :param project: project to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingProjectError` if given project doesn't exist in the repository
        """

    def save_project(self, project: Project) -> Project:
        """
        Saves project into the repository

        :param project: project to save
        :return: saved project
        :exception: :exc:`.errors.ExistingProjectError` if given project has the same name as existing one.
        """
        existing_project = self.get_project_by_name(project.name)
        if project.id is None and existing_project is None:
            return self.create_project(project)
        elif existing_project is not None:
            if project.id is None or existing_project.id != project.id:
                raise errors.ExistingProjectError(existing_project)
        return self.update_project(project)

    @ExposedMetadataMethod()
    def get_or_create_project(self, name: str) -> Project:
        """
        Creates a project if not exists or gets existing project otherwise.

        :param name: project name
        :return: project
        """
        project = self.get_project_by_name(name)
        if project is None:
            project = core.Project(name)
            project = self.create_project(project)
        return project     
    
    @abstractmethod
    @ExposedMetadataMethod()
    def get_tasks(self, project: ProjectVar) -> List['core.Task']:
        """
        Gets a list of tasks for given project

        :param project: project to search for tasks in
        :return: project tasks
        """

    @abstractmethod
    @ExposedMetadataMethod(name='get_task')
    def get_task_by_name(self, project: ProjectVar, task_name: str) -> Optional['core.Task']:
        """
        Finds task with given name in given project

        :param project: project to search for task in
        :param task_name: expected name of task
        :return: task if exists or `None`
        """

    @abstractmethod
    def get_task_by_id(self, id: int) -> Optional['core.Task']:
        """
        Finds task with given id

        :param id: id of task to search for
        :return: task if exists or `None`
        """

    @ExposedMetadataMethod()
    def get_or_create_task(self, project: str, task_name: str) -> Task:
        """
        Creates a task if not exists or gets existing task otherwise.

        :param project: project to search/create task in
        :param task_name: expected name of task
        :return: created/found task
        """

        project = self.get_or_create_project(project)
        task = self.get_task_by_name(project, task_name)
        if task is None:
            task = core.Task(task_name, project_id=project.id)
            task = self.create_task(task)
        return task

    @abstractmethod
    def create_task(self, task: Task) -> Task:
        """
        Creates task in a repository

        :param task: task to create
        :return: created task
        :exception: :class:`.errors.ExistingTaskError` if given task has the same name and project as existing one
        """

    @abstractmethod
    def update_task(self, task: Task) -> Task:
        """
        Updates task in a repository.

        :param task: task to update
        :return: updated task
        :exception: :exc:`.errors.NonExistingTaskError` if given tasks doesn't exist in the repository
        """

    @abstractmethod
    def delete_task(self, task: Task):
        """
        Deletes the task and all its models.

        :param task: task to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingTaskError` if given tasks doesn't exist in the repository
        """

    def save_task(self, task: Task) -> Task:
        """
        Saves task into repository

        :param task: task
        :return: saved task
        :exception: :class:`.errors.ExistingTaskError` if given task has the same name and project as existing one
        """

        if task.project_id is None:
            raise ValueError("A project is not assigned to the task {}".format(task))

        existing_task = self.get_task_by_name(task.project_id, task.name)
        if task.id is None and existing_task is None:
            return self.create_task(task)
        elif existing_task is not None:
            if task.id is None or existing_task.id != task.id:
                raise errors.ExistingTaskError(existing_task)
        return self.update_task(task)

    @abstractmethod
    @ExposedMetadataMethod()
    def get_models(self, task: TaskVar, project: ProjectVar = None) -> List['core.Model']:
        """
        Gets a list of models in given project and task

        :param task: task to search for models in
        :param project: project to search for models in
        :return: found models
        """

    @abstractmethod
    def get_model_by_name(self, model_name: str, task: TaskVar, project: ProjectVar = None) -> Optional['core.Model']:
        """
        Finds model by name in given task and project.

        :param model_name: expected model name
        :param task: task to search for model in
        :param project: project to search for model in
        :return: found model if exists or `None`
        """

    @abstractmethod
    def get_model_by_id(self, id: int) -> Optional['core.Model']:
        """
        Finds model by identifier.

        :param id: expected model id
        :return: found model if exists or `None`
        """

    @abstractmethod
    def create_model(self, model: Model) -> Model:
        """
        Creates model in the repository

        :param model: model to create
        :return: created model
        :exception: :exc:`.errors.ExistingModelError` if given model has the same name and task as existing one
        """

    @abstractmethod
    def update_model(self, model: Model) -> Model:
        """
        Updates model in the repository

        :param model: model to update
        :return: updated model
        :exception: :exc:`.errors.NonExistingModelError` if given model doesn't exist in the repository
        """

    @abstractmethod
    def delete_model(self, model: Model):
        """
        Deletes model from the repository

        :param model: model to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingModelError` if given model doesn't exist in the repository
        """

    def save_model(self, model: Model) -> Model:
        """
        Saves model in the repository

        :param model: model to save
        :return: saved model
        :exception: :exc:`.errors.ExistingModelError` if given model has the same name and task as existing one
        """

        if model.task_id is None:
            raise ValueError("A task is not assigned to the model {}".format(model))

        existing_model = self.get_model_by_name(model.name, model.task_id)

        if model.id is None and existing_model is None:
            return self.create_model(model)
        elif existing_model is not None:
            if model.id is None or existing_model.id != model.id:
                raise errors.ExistingModelError(model)
        return self.update_model(model)

    # ___________________

    @abstractmethod
    @ExposedMetadataMethod()
    def get_pipelines(self, task: TaskVar, project: ProjectVar = None) -> List['core.Pipeline']:
        """
        Gets a list of pipelines in given project and task

        :param task: task to search for models in
        :param project: project to search for models in
        :return: found pipelines
        """

    @abstractmethod
    @ExposedMetadataMethod(name='get_pipeline')
    def get_pipeline_by_name(self, pipeline_name: str, task: TaskVar,
                             project: ProjectVar = None) -> Optional['core.Pipeline']:
        """
        Finds model by name in given task and project.

        :param pipeline_name: expected pipeline name
        :param task: task to search for pipeline in
        :param project: project to search for pipeline in
        :return: found pipeline if exists or `None`
        """

    @abstractmethod
    def get_pipeline_by_id(self, id: int) -> Optional['core.Pipeline']:
        """
        Finds model by identifier.

        :param id: expected model id
        :return: found model if exists or `None`
        """

    @abstractmethod
    def create_pipeline(self, pipeline: Pipeline) -> Pipeline:
        """
        Creates model in the repository

        :param pipeline: pipeline to create
        :return: created pipeline
        :exception: :exc:`.errors.ExistingPipelineError` if given model has the same name and task as existing one
        """

    @abstractmethod
    def update_pipeline(self, pipeline: Pipeline) -> Pipeline:
        """
        Updates model in the repository

        :param pipeline: pipeline to update
        :return: updated model
        :exception: :exc:`.errors.NonExistingPipelineError` if given pipeline doesn't exist in the repository
        """

    @abstractmethod
    def delete_pipeline(self, pipeline: Pipeline):
        """
        Deletes model from the repository

        :param pipeline: pipeline to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingPipelineError` if given pipeline doesn't exist in the repository
        """

    def save_pipeline(self, pipeline: Pipeline) -> Pipeline:
        """
        Saves pipeline in the repository

        :param pipeline: model to save
        :return: saved pipeline
        :exception: :exc:`.errors.ExistingPipelineError` if given pipeline has the same name and task as existing one
        """

        if pipeline.task_id is None:
            raise ValueError("A task is not assigned to the pipeline {}".format(pipeline))

        existing_pipeline = self.get_pipeline_by_name(pipeline.name, pipeline.task_id)

        if pipeline.id is None and existing_pipeline is None:
            return self.create_pipeline(pipeline)
        elif existing_pipeline is not None:
            if pipeline.id is None or existing_pipeline.id != pipeline.id:
                raise errors.ExistingPipelineError(pipeline)
        return self.update_pipeline(pipeline)

    # _______________
    @abstractmethod
    @ExposedMetadataMethod()
    def get_images(self, task: TaskVar, project: ProjectVar = None) -> List['core.Image']:
        """
        Gets a list of images in given model, task and project

        :param task: task to search for images in
        :param project: project to search for images in
        :return: found images
        """

    @abstractmethod
    @ExposedMetadataMethod(name='get_image')
    def get_image_by_name(self, image_name: str, task: TaskVar, project: ProjectVar = None) -> Optional['core.Image']:
        """
        Finds image by name in given model, task and project.

        :param image_name: expected image name
        :param task: task to search for image in
        :param project: project to search for image in
        :return: found image if exists or `None`
        """

    @abstractmethod
    def get_image_by_id(self, id: int) -> Optional['core.Image']:
        """
        Finds image by identifier.

        :param id: expected image id
        :return: found image if exists or `None`
        """

    @abstractmethod
    def create_image(self, image: Image) -> Image:
        """
        Creates image in the repository

        :param image: image to create
        :return: created image
        :exception: :exc:`.errors.ExistingImageError` if given image has the same name and model as existing one
        """

    @abstractmethod
    def update_image(self, image: Image) -> Image:
        """
        Updates image in the repository

        :param image: image to update
        :return: updated image
        :exception: :exc:`.errors.NonExistingImageError` if given image doesn't exist in the repository
        """

    @abstractmethod
    def delete_image(self, image: Image):
        """
        Deletes image from the repository

        :param image: image to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingImageError` if given image doesn't exist in the repository
        """

    def save_image(self, image: Image) -> Image:
        """
        Saves image in the repository

        :param image: image to save
        :return: saved image
        :exception: :exc:`.errors.ExistingImageError` if given image has the same name and model as existing one
        """
        self._validate_image(image)

        existing_image = self.get_image_by_name(image.name, image.task_id)

        if image.id is None and existing_image is None:
            return self.create_image(image)
        elif existing_image is not None:
            if image.id is None or existing_image.id != image.id:
                raise errors.ExistingImageError(image)
        return self.update_image(image)

    @abstractmethod
    @ExposedMetadataMethod()
    def get_environments(self) -> List[RuntimeEnvironment]:
        """
        Gets a list of runtime environments

        :return: found runtime environments
        """

    @abstractmethod
    @ExposedMetadataMethod(name='get_environment')
    def get_environment_by_name(self, name: str) -> Optional[RuntimeEnvironment]:
        """
        Finds runtime environment by name.

        :param name: expected runtime environment name
        :return: found runtime environment if exists or `None`
        """

    @abstractmethod
    def get_environment_by_id(self, id: int) -> Optional[RuntimeEnvironment]:
        """
        Finds runtime environment by identifier.

        :param id: expected runtime environment id
        :return: found runtime environment if exists or `None`
        """

    @abstractmethod
    @ExposedMetadataMethod(name='push_environment')
    def create_environment(self, environment: 'core.RuntimeEnvironment') -> RuntimeEnvironment:
        """
        Creates runtime environment in the repository

        :param environment: runtime environment to create
        :return: created runtime environment
        :exception: :exc:`.errors.ExistingEnvironmentError` if given runtime environment has the same name as existing
        """

    @abstractmethod
    def update_environment(self, environment: 'core.RuntimeEnvironment') -> RuntimeEnvironment:
        """
        Updates runtime environment in the repository

        :param environment: runtime environment to update
        :return: updated runtime environment
        :exception: :exc:`.errors.NonExistingEnvironmentError` if given runtime environment doesn't exist in the
        repository
        """

    @abstractmethod
    def delete_environment(self, environment: 'core.RuntimeEnvironment'):
        """
        Deletes runtime environment from the repository

        :param environment: runtime environment to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingEnvironmentError` if given runtime environment doesn't exist in the
        repository
        """

    def save_environment(self, environment: 'core.RuntimeEnvironment') -> RuntimeEnvironment:
        """
        Saves runtime environment in the repository

        :param environment: runtime environment to save
        :return: saved runtime environment
        :exception: :exc:`.errors.ExistingEnvironmentError` if given runtime environment has the same name as existing
        """
        self._validate_environment(environment)

        existing_environment = self.get_environment_by_name(environment.name)

        if environment.id is None and existing_environment is None:
            return self.create_environment(environment)
        elif existing_environment is not None:
            if environment.id is None or existing_environment.id != environment.id:
                raise errors.ExistingEnvironmentError(environment)
        return self.update_environment(environment)

    @abstractmethod
    @ExposedMetadataMethod()
    def get_instances(self, image: Union[int, 'core.Image'] = None,
                      environment: Union[int, 'core.RuntimeEnvironment'] = None) -> List['core.RuntimeInstance']:
        """
        Gets a list of instances in given image or environment

        :param image: image (or id) to search for instances in
        :param environment: environment (or id) to search for instances in
        :return: found instances
        """

    @abstractmethod
    @ExposedMetadataMethod(name='get_instance')
    def get_instance_by_name(self, instance_name: str, image: Union[int, 'core.Image'],
                             environment: Union[int, 'core.RuntimeEnvironment']) -> Optional['core.RuntimeInstance']:
        """
        Finds instance by name in given image and environment.

        :param instance_name: expected instance name
        :param image: image (or id) to search for instance in
        :param environment: environment (or id) to search for instance in
        :return: found instance if exists or `None`
        """

    @abstractmethod
    def get_instance_by_id(self, id: int) -> Optional['core.RuntimeInstance']:
        """
        Finds instance by identifier.

        :param id: expected instance id
        :return: found instance if exists or `None`
        """

    @abstractmethod
    def create_instance(self, instance: 'core.RuntimeInstance') -> 'core.RuntimeInstance':
        """
        Creates instance in the repository

        :param instance: instance to create
        :return: created instance
        :exception: :exc:`.errors.ExistingInstanceError` if given instance has the same name, image and environment
            as existing one
        """

    @abstractmethod
    def update_instance(self, instance: 'core.RuntimeInstance') -> 'core.RuntimeInstance':
        """
        Updates instance in the repository

        :param instance: instance to update
        :return: updated instance
        :exception: :exc:`.errors.NonExistingInstanceError` if given instance doesn't exist in the repository
        """

    @abstractmethod
    def delete_instance(self, instance: 'core.RuntimeInstance'):
        """
        Deletes instance from the repository

        :param instance: instance to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingInstanceError` if given instance doesn't exist in the repository
        """

    def save_instance(self, instance: 'core.RuntimeInstance') -> 'core.RuntimeInstance':
        """
        Saves instance in the repository

        :param instance: instance to save
        :return: saved instance
        :exception: :exc:`.errors.ExistingInstanceError` if given image has the same name, image and environment
            as existing one
        """
        self._validate_instance(instance)

        existing_instance = self.get_instance_by_name(instance.name, instance.image_id, instance.environment_id)

        if instance.id is None and existing_instance is None:
            return self.create_instance(instance)
        elif existing_instance is not None:
            if instance.id is None or existing_instance.id != instance.id:
                raise errors.ExistingInstanceError(instance)
        return self.update_instance(instance)

    def _resolve_project(self, project: ProjectVar) -> Optional['core.Project']:
        if isinstance(project, core.Project):
            project = project.id if project.id is not None else project.name
        if isinstance(project, int):
            return self.get_project_by_id(project)
        return self.get_project_by_name(project)

    def _resolve_task(self, task: TaskVar, project: ProjectVar = None) -> Optional['core.Task']:
        if isinstance(task, core.Task):
            task = task.id if task.id is not None else task.name
        if isinstance(task, int):
            return self.get_task_by_id(task)
        if project is None:
            raise ValueError('Cannot resolve task without project')
        return self.get_task_by_name(project, task)

    def _resolve_model(self, model: ModelVar, task: TaskVar = None, project: ProjectVar = None):
        if isinstance(model, core.Model):
            model = model.id if model.id is not None else model.name
        if isinstance(model, int):
            return self.get_model_by_id(model)
        if task is None:
            raise ValueError('Cannot resolve model without task')
        return self.get_model_by_name(model, task, project)

    def _resolve_environment(self, environment: EnvironmentVar) -> Optional[RuntimeEnvironment]:
        if isinstance(environment, core.RuntimeEnvironment):
            environment = environment.id if environment.id is not None else environment.name
        if isinstance(environment, int):
            return self.get_environment_by_id(environment)
        return self.get_environment_by_name(environment)

    def _validate_project(self, project: Project):
        pass

    def _validate_task(self, task: Task):
        if task.project_id is None:
            raise errors.TaskNotInProjectError(task)

    def _validate_experiment(self, experiment: Experiment):
        if experiment.task_id is None:
            raise errors.ExperimentNotInTaskError(experiment)

    def _validate_model(self, model: Model):
        if model.task_id is None:
            raise errors.ModelNotInTaskError(model)

    def _validate_pipeline(self, pipeline: Pipeline):
        if pipeline.task_id is None:
            raise errors.PipelineNotInTaskError(pipeline)

    def _validate_image(self, image: Image):
        if image.task_id is None:
            raise errors.ImageNotInTaskError(image)

    def _validate_environment(self, environment: 'core.RuntimeEnvironment'):
        pass

    def _validate_instance(self, instance: 'core.RuntimeInstance'):
        if instance.image_id is None:
            raise errors.InstanceNotInImageError(instance)
        if instance.environment_id is None:
            raise errors.InstanceNotInEnvironmentError(instance)

    @abstractmethod
    @ExposedMetadataMethod()
    def get_experiments(self, task: TaskVar) -> List['core.Experiment']:
        """
        Gets a list of experiments for given task

        :param task: task to search for experiments in
        :return: task experiments
        """
    @abstractmethod
    @ExposedMetadataMethod(name='get_experiment')
    def get_experiment_by_name(self, task: TaskVar, experiment_name: str) -> Optional['core.Experiment']:
        """
        Finds experiment with given name in given task

        :param task: task to search for experiment in
        :param experiment_name: expected name of experiment
        :return: experiment if exists or `None`
        """
    @abstractmethod
    @ExposedMetadataMethod(name='get_experiment_sequence')
    def get_experiment_sequence(self,task_id: str)-> Optional['core.Experiment']:
        """
        Finds experiment count with given name in given task

        :param task: task to search for experiment count in
        :param task_id: expected id of task
        :return: experiment count if exists or `None`
        """
    @abstractmethod
    def get_experiment_by_id(self, id: int) -> Optional['core.Experiment']:
        """
        Finds experiment with given id

        :param id: id of experiment to search for
        :return: experiment if exists or `None`
        """

    @ExposedMetadataMethod()
    def get_or_create_experiment(self,project: str, task: str, experiment_name: str) -> Experiment:
        """
        Creates a experiment if not exists or gets existing experiment otherwise.

        :param task: task to search/create experiment in
        :param experiment_name: expected name of experiment
        :return: created/found experiment
        """

        task = self.get_or_create_task(project,task)
        experiment = self.get_experiment_by_name(task, experiment_name)
        #print(task,experiment,task.id,"experiment")
        if experiment is None:
            experiment_sequence = self.get_experiment_sequence(task.id)
            experiment = core.Experiment(experiment_name, experiment_sequence= experiment_sequence+1, task_id=task.id)
            experiment = self.create_experiment(experiment)
            
        return experiment

    @abstractmethod
    def create_experiment(self, experiment: Experiment) -> Experiment:
        """
        Creates experiment in a repository

        :param experiment: experiment to create
        :return: created experiment
        :exception: :class:`.errors.ExistingExperimentError` if given experiment has the same name and task as existing one
        """

    @abstractmethod
    def update_experiment(self, experiment: Experiment) -> Experiment:
        """
        Updates experiment in a repository.

        :param experiment: experiment to update
        :return: updated experiment
        :exception: :exc:`.errors.NonExistingExperimentError` if given experiments doesn't exist in the repository
        """

    @abstractmethod
    def delete_experiment(self, experiment: Experiment):
        """
        Deletes the experiment and all its models.

        :param experiment: experiment to delete
        :return: nothing
        :exception: :exc:`.errors.NonExistingExperimentError` if given experiments doesn't exist in the repository
        """

    def save_experiment(self, experiment: Experiment) -> Experiment:
        """
        Saves experiment into repository

        :param experiment: experiment
        :return: saved experiment
        :exception: :class:`.errors.ExistingExperimentError` if given experiment has the same name and experiment as existing one
        """

        if experiment.task_id is None:
            raise ValueError("A task is not assigned to the experiment {}".format(experiment))

        existing_experiment = self.get_experiment_by_name(experiment.task_id, experiment.name)
        if experiment.id is None and existing_experiment is None:
            return self.create_experiment(experiment)
        elif existing_experiment is not None:
            if experiment.id is None or existing_experiment.id != experiment.id:
                raise errors.ExistingExperimentError(existing_experiment)
        return self.update_experiment(experiment)
    
    
    
    def save_metric(self, metric: ModelMetric) -> ModelMetric:
        """
        Saves model metric into repository

        :param metric: metric
        :return: saved metric
        :exception: :class:`.errors.ExistingModelMetricError` if given metric has the same name and metric as existing one
        """

        if metric.experiment_id is None:
            raise ValueError("A experiment is not assigned to the metric {}".format(metric))
        existing_epoch = self.get_metric_by_name_epoch(metric.experiment_id, metric.name, metric.epoch)
        #print(existing_epoch,"existing_epoch,",metric.experiment_id, metric.name, metric.epoch)
        if existing_epoch is not None:
            return
            #raise errors.ExistingModelMetricError("epoch {}".format(existing_epoch))
        return self.create_metric(metric)
        #existing_metric = self.get_metric_by_name(metric.experiment_id, metric.name)
        #if metric.id is None and existing_metric is None:
        #    return self.create_metric(metric)
        #elif existing_metric is not None:
        #    if metric.id is None or existing_metric.id != metric.id:
        #        raise errors.ExistingModelMetricError(existing_metric)
        #return self.update_metric(metric)

    @abstractmethod
    @ExposedMetadataMethod(name='get_metric')
    def get_metric_by_name(self, experiment: ExperimentVar, metric_name: str) -> Optional['core.ModelMetric']:
        """
        Finds metric with given name in given experiment

        :param experiment: experiment to search for metric in
        :param metric_name: expected name of metric
        :return: metric if exists or `None`
        """
        
    @abstractmethod
    def create_metric(self, metric: ModelMetric) -> ModelMetric:
        """
        Creates metric in a repository

        :param metric: metric to create
        :return: created metric
        :exception: :class:`.errors.ExistingMetricError` if given metric has the same name and experiment as existing one
        """

    @abstractmethod
    def update_metric(self, metric: ModelMetric) -> ModelMetric:
        """
        Updates metric in a repository.

        :param metric: metric to update
        :return: updated metric
        :exception: :exc:`.errors.NonExistingMetricError` if given metrics doesn't exist in the repository
        """
        
    def save_param(self, param: ModelParam) -> ModelParam:
        """
        Saves model param into repository

        :param param: param
        :return: saved param
        :exception: :class:`.errors.ExistingModelParamError` if given metric has the same name and metric as existing one
        """

        if param.experiment_id is None:
            raise ValueError("A experiment is not assigned to the metric {}".format(param))

        return self.create_param(param)  

    def save_best_result(self,best_result: BestResult) -> BestResult:
        """
        Saves best result into repository

        :param param: best_result
        :return: saved best result
        :exception: :class:`.errors.ExistingBestResultError` if given best result has the same name and best result as existing one
        """

        if best_result.experiment_id is None:
            raise ValueError("A experiment is not assigned to the best result {}".format(best_result))

        return self.create_best_result(best_result)          

    @abstractmethod
    def create_param(self, param: ModelParam) -> ModelParam:
        """
        Creates param in a repository

        :param param: param to create
        :return: created param
        :exception: :class:`.errors.ExistingModelMetricError` if given param has the same name and experiment as existing one
        """

    @abstractmethod
    def create_best_result(self, best_result: BestResult) -> BestResult:
        """
        Creates best result in a repository

        :param param: best_result to create
        :return: created best_result
        :exception: :class:`.errors.ExistingBestResultError` if given best result has the same name and best result as existing one
        """