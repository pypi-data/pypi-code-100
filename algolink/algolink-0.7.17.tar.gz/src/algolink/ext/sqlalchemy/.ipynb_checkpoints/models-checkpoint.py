from abc import abstractmethod
from typing import Any, Dict, Iterable, List, Optional, Type, TypeVar

from pyjackson import dumps, loads
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from algolink.core.objects import DatasetType
from algolink.core.objects.artifacts import ArtifactCollection
from algolink.core.objects.core import (Buildable, EvaluationResults, EvaluationSet, Image, Model, Pipeline,
                                        PipelineStep, Project, RuntimeEnvironment, RuntimeInstance, Task, 
                                        Experiment, ModelMetric, ModelParam, BestResult)
from algolink.core.objects.dataset_source import DatasetSource
from algolink.core.objects.metric import Metric
from algolink.core.objects.requirements import Requirements

SQL_OBJECT_FIELD = '_sqlalchemy_object'


def json_column():
    return Column(Text)


def safe_loads(payload, as_class):
    return loads(payload, Optional[as_class])


def sqlobject(obj):
    return getattr(obj, SQL_OBJECT_FIELD, None)


def update_attrs(obj, **attrs):
    for name, value in attrs.items():
        setattr(obj, name, value)


T = TypeVar('T')
S = TypeVar('S', bound='Attaching')


class Attaching:
    id = ...
    name = ...

    def attach(self, obj):
        setattr(obj, SQL_OBJECT_FIELD, self)
        return obj

    @classmethod
    def from_obj(cls: Type[S], obj: T, new=False) -> S:
        kwargs = cls.get_kwargs(obj)
        existing = sqlobject(obj)
        if not new and existing is not None:
            update_attrs(existing, **kwargs)
            return existing
        return cls(**kwargs)

    @classmethod
    @abstractmethod
    def get_kwargs(cls, obj: T) -> dict:
        pass  # pragma: no cover

    @abstractmethod
    def to_obj(self) -> T:
        pass  # pragma: no cover


Base = declarative_base()


class SProject(Base, Attaching):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)

    tasks: Iterable['STask'] = relationship("STask", back_populates="project")

    def to_obj(self) -> Project:
        p = Project(self.name, id=self.id, author=self.author, creation_date=self.creation_date)
        for task in self.tasks:
            p._tasks.add(task.to_obj())
        return self.attach(p)

    @classmethod
    def get_kwargs(cls, project: Project) -> dict:
        return dict(id=project.id,
                    name=project.name,
                    author=project.author,
                    creation_date=project.creation_date,
                    tasks=[STask.from_obj(t) for t in project.tasks.values()])


class STask(Base, Attaching):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship("SProject", back_populates="tasks")
    models: Iterable['SModel'] = relationship("SModel", back_populates="task")
    pipelines: Iterable['SPipeline'] = relationship("SPipeline", back_populates='task')
    images: Iterable['SImage'] = relationship("SImage", back_populates='task')
    
    experiments: Iterable['TExperiment'] = relationship("TExperiment", back_populates='task')

    datasets = Column(Text)
    metrics = Column(Text)
    evaluation_sets = Column(Text)

    __table_args__ = (UniqueConstraint('name', 'project_id', name='tasks_name_and_ref'),)

    def to_obj(self) -> Task:
        task = Task(id=self.id,
                    name=self.name,
                    author=self.author,
                    creation_date=self.creation_date,
                    project_id=self.project_id,
                    datasets=safe_loads(self.datasets, Dict[str, DatasetSource]),
                    metrics=safe_loads(self.metrics, Dict[str, Metric]),
                    evaluation_sets=safe_loads(self.evaluation_sets, Dict[str, EvaluationSet]))
        for model in self.models:
            task._models.add(model.to_obj())

        for pipeline in self.pipelines:
            task._pipelines.add(pipeline.to_obj())

        for image in self.images:
            task._images.add(image.to_obj())

        for experiment in self.experiments:
            task._experiments.add(experiment.to_obj())
        return self.attach(task)

    @classmethod
    def get_kwargs(cls, task: Task) -> dict:
        return dict(id=task.id,
                    name=task.name,
                    author=task.author,
                    creation_date=task.creation_date,
                    project_id=task.project_id,
                    models=[SModel.from_obj(m) for m in task.models.values()],
                    images=[SImage.from_obj(i) for i in task.images.values()],
                    pipelines=[SPipeline.from_obj(p) for p in task.pipelines.values()],
                    datasets=dumps(task.datasets),
                    metrics=dumps(task.metrics),
                    evaluation_sets=dumps(task.evaluation_sets))


class SModel(Base, Attaching):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)
    wrapper = Column(Text)

    artifact = Column(Text)
    requirements = Column(Text)
    description = Column(Text)
    params = Column(Text)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship("STask", back_populates="models")

    evaluations = Column(Text)
    __table_args__ = (UniqueConstraint('name', 'task_id', name='models_name_and_ref'),)

    def to_obj(self) -> Model:
        model = Model(name=self.name,
                      wrapper_meta=safe_loads(self.wrapper, dict),
                      author=self.author,
                      creation_date=self.creation_date,
                      artifact=safe_loads(self.artifact, ArtifactCollection),
                      requirements=safe_loads(self.requirements, Requirements),
                      description=self.description,
                      params=safe_loads(self.params, Dict[str, Any]),
                      id=self.id,
                      task_id=self.task_id,
                      evaluations=safe_loads(self.evaluations, Dict[str, EvaluationResults]))
        return self.attach(model)

    @classmethod
    def get_kwargs(cls, model: Model) -> dict:
        return dict(id=model.id,
                    name=model.name,
                    author=model.author,
                    creation_date=model.creation_date,
                    wrapper=dumps(model.wrapper_meta),
                    artifact=dumps(model.artifact),
                    requirements=dumps(model.requirements),
                    description=model.description,
                    params=dumps(model.params),
                    task_id=model.task_id,
                    evaluations=dumps(model.evaluations))


class SPipeline(Base, Attaching):
    __tablename__ = 'pipelines'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)
    steps = Column(Text)

    input_data = Column(Text)
    output_data = Column(Text)

    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship("STask", back_populates="pipelines")

    evaluations = Column(Text)
    __table_args__ = (UniqueConstraint('name', 'task_id', name='pipelines_name_and_ref'),)

    def to_obj(self) -> Pipeline:
        pipeline = Pipeline(name=self.name,
                            steps=safe_loads(self.steps, List[PipelineStep]),
                            input_data=safe_loads(self.input_data, DatasetType),
                            output_data=safe_loads(self.output_data, DatasetType),
                            author=self.author,
                            creation_date=self.creation_date,
                            id=self.id,
                            task_id=self.task_id,
                            evaluations=safe_loads(self.evaluations, EvaluationResults))
        return self.attach(pipeline)

    @classmethod
    def get_kwargs(cls, pipeline: Pipeline) -> dict:
        return dict(id=pipeline.id,
                    name=pipeline.name,
                    author=pipeline.author,
                    creation_date=pipeline.creation_date,
                    steps=dumps(pipeline.steps),
                    input_data=dumps(pipeline.input_data),
                    output_data=dumps(pipeline.output_data),
                    task_id=pipeline.task_id,
                    evaluations=dumps(pipeline.evaluations))


class SImage(Base, Attaching):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)

    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship("STask", back_populates="images")

    environment_id = Column(Integer, ForeignKey('environments.id'), nullable=False)

    params = Column(Text)
    source = Column(Text)

    __table_args__ = (UniqueConstraint('name', 'task_id', name='image_name_and_ref'),)

    def to_obj(self) -> Image:
        image = Image(name=self.name,
                      author=self.author,
                      creation_date=self.creation_date,
                      id=self.id,
                      task_id=self.task_id,
                      params=safe_loads(self.params, Image.Params),
                      source=safe_loads(self.source, Buildable),
                      environment_id=self.environment_id)
        return self.attach(image)

    @classmethod
    def get_kwargs(cls, image: Image) -> dict:
        return dict(id=image.id,
                    name=image.name,
                    author=image.author,
                    creation_date=image.creation_date,
                    task_id=image.task_id,
                    params=dumps(image.params),
                    source=dumps(image.source),
                    environment_id=image.environment_id)


class SRuntimeEnvironment(Base, Attaching):
    __tablename__ = 'environments'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, unique=True, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)

    params = Column(Text)

    def to_obj(self) -> RuntimeEnvironment:
        environment = RuntimeEnvironment(
            name=self.name,
            author=self.author,
            creation_date=self.creation_date,
            id=self.id,
            params=safe_loads(self.params, RuntimeEnvironment.Params))
        return self.attach(environment)

    @classmethod
    def get_kwargs(cls, environment: RuntimeEnvironment) -> dict:
        return dict(id=environment.id,
                    name=environment.name,
                    author=environment.author,
                    creation_date=environment.creation_date,
                    params=dumps(environment.params))


class SRuntimeInstance(Base, Attaching):
    __tablename__ = 'instances'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    creation_date = Column(DateTime, unique=False, nullable=False)

    image_id = Column(Integer, ForeignKey('images.id'), nullable=False)
    environment_id = Column(Integer, ForeignKey('environments.id'), nullable=False)

    params = Column(Text)

    __table_args__ = (UniqueConstraint('name', 'image_id', 'environment_id', name='instance_name_and_ref'),)

    def to_obj(self) -> RuntimeInstance:
        instance = RuntimeInstance(
            name=self.name,
            author=self.author,
            creation_date=self.creation_date,
            id=self.id,
            image_id=self.image_id,
            environment_id=self.environment_id,
            params=safe_loads(self.params, RuntimeInstance.Params))
        return self.attach(instance)

    @classmethod
    def get_kwargs(cls, instance: RuntimeInstance) -> dict:
        return dict(id=instance.id,
                    name=instance.name,
                    author=instance.author,
                    creation_date=instance.creation_date,
                    image_id=instance.image_id,
                    environment_id=instance.environment_id,
                    params=dumps(instance.params))


class TExperiment(Base, Attaching):
    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    experiment_remark = Column(String, unique=False, nullable=False)
    experiment_sequence = Column(Integer, nullable=False)
    del_flag = Column(Integer, default = 0)

    creation_date = Column(DateTime, unique=False, nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)

    task = relationship("STask", back_populates="experiments")
    modelmetrics: Iterable['TModelmetric'] = relationship("TModelmetric", back_populates="experiment")
    modelparams: Iterable['TModelparam'] = relationship("TModelparam", back_populates="experiment")
    bestresult: Iterable['TBestresult'] = relationship("TBestresult", back_populates="experiment")


    __table_args__ = (UniqueConstraint('name', 'task_id', name='experiment_name_and_ref'),)

    def to_obj(self) -> Experiment:
        experiment = Experiment(
                        id=self.id,
                        name=self.name,
                        author=self.author,
                        creation_date=self.creation_date,
                        task_id=self.task_id,
                        experiment_remark=self.experiment_remark,
                        experiment_sequence=self.experiment_sequence)
        #for model_metric in self.modelmetrics:
        #    experiment._modelmetrics.add(model_metric.to_obj())

        #for model_param in self.modelparams:
        #    experiment._modelparams.add(model_param.to_obj())

        #for best_result in self.bestresult:
        #    experiment._bestresult.add(best_result.to_obj())
        return self.attach(experiment)

    @classmethod
    def get_kwargs(cls, experiment: Experiment) -> dict:
        return dict(id=experiment.id,
                    name=experiment.name,
                    author=experiment.author,
                    creation_date=experiment.creation_date,
                    task_id=experiment.task_id,
                    experiment_remark=experiment.experiment_remark,
                    experiment_sequence=experiment.experiment_sequence,
                    del_flag=experiment.del_flag)

class TModelmetric(Base, Attaching):
    __tablename__ = 'model_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    metric_type = Column(String, unique=False, nullable=False)
    metric_value = Column(Float, nullable=False)
    epoch = Column(Integer, nullable=False)

    creation_date = Column(DateTime, unique=False, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)

    experiment = relationship("TExperiment", back_populates="modelmetrics")

    def to_obj(self) -> ModelMetric:
        modelmetric = ModelMetric(id=self.id,
                        name=self.name,
                        author=self.author,
                        creation_date=self.creation_date,
                        metric_type=self.metric_type,
                        metric_value=self.metric_value,
                        epoch=self.epoch,
                        experiment_id=self.experiment_id)
        return self.attach(modelmetric)

    @classmethod
    def get_kwargs(cls, model_metric: ModelMetric) -> dict:
        return dict(id=model_metric.id,
                    name=model_metric.name,
                    author=model_metric.author,
                    creation_date=model_metric.creation_date,
                    experiment_id=model_metric.experiment_id,
                    metric_type = model_metric.metric_type,
                    metric_value = model_metric.metric_value,
                    epoch = model_metric.epoch)
    
class TModelparam(Base, Attaching):
    __tablename__ = 'model_params'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    param_type = Column(String, unique=False, nullable=False)
    param_value = Column(String, nullable=False)

    creation_date = Column(DateTime, unique=False, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)

    experiment = relationship("TExperiment", back_populates="modelparams")

    def to_obj(self) -> ModelParam:
        model_param = ModelParam(id=self.id,
                    name=self.name,
                    author=self.author,
                    creation_date=self.creation_date,
                    experiment_id=self.experiment_id,
                    param_type=self.param_type,
                    param_value=self.param_value)
        return self.attach(model_param)

    @classmethod
    def get_kwargs(cls, model_param: ModelParam) -> dict:
        return dict(id=model_param.id,
                    name=model_param.name,
                    author=model_param.author,
                    creation_date=model_param.creation_date,
                    experiment_id=model_param.experiment_id,
                    param_type = model_param.param_type,
                    param_value = model_param.param_value)
    
class TBestresult(Base, Attaching):
    __tablename__ = 'best_result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    author = Column(String, unique=False, nullable=False)
    best_value = Column(Float, nullable=False)
    best_epoch = Column(Integer, nullable=False)

    creation_date = Column(DateTime, unique=False, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'), nullable=False)

    experiment = relationship("TExperiment", back_populates="bestresult")

    def to_obj(self) -> BestResult:
        best_result = BestResult(id=self.id,
                    name=self.name,
                    author=self.author,
                    creation_date=self.creation_date,
                    best_value=self.best_value,
                    best_epoch=self.best_epoch,
                    experiment_id=self.experiment_id)

        return self.attach(best_result)

    @classmethod
    def get_kwargs(cls, best_result: BestResult) -> dict:
        return dict(id=best_result.id,
                    name=best_result.name,
                    author=best_result.author,
                    creation_date=best_result.creation_date,
                    best_value=best_result.best_value,
                    best_epoch = best_result.best_epoch,
                    experiment_id = best_result.experiment_id)