import logging
from abc import abstractmethod

import rest_framework.request
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpRequest
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from config import settings
from cron.serializers import DjangoJobSerializer, DjangoJobExecutionSerializer
from handler import APIResponse
from paginator import CustomPaginator

logger = logging.getLogger('clouddog')
JOB_SERIALIZER_FIELDS = ['id', 'next_run_time']

scheduler = BackgroundScheduler(
    job_defaults=settings.JOB_DEFAULTS, executors=settings.EXECUTORS, timezone=settings.JOB_TIMEZONE
)
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()


class DjangoJobViewSet(ModelViewSet):
    @abstractmethod
    def custom_job(self):
        pass

    permission_classes = []
    authentication_classes = []
    queryset = DjangoJob.objects.all()
    serializer_class = DjangoJobSerializer

    def list(self, request, *args, **kwargs):
        logger.info("{} call job list api".format(request.user.username))
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            job = None
            trigger_type = request.data.get('trigger_type')
            if trigger_type == "date":
                run_time = request.data.get('run_time')
                job = scheduler.add_job(
                    func=self.custom_job, trigger=trigger_type, next_run_time=run_time, replace_existing=True, coalesce=False
                )
                logger.info("Add one-time task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == 'interval':
                seconds = int(request.data.get('interval_time'))
                if seconds <= 0:
                    raise TypeError('interval_time must great than 0')
                job = scheduler.add_job(
                    func=self.custom_job, trigger=trigger_type, seconds=seconds, replace_existing=True, coalesce=False
                )
                logger.info("Add interval task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == "cron":
                run_time = request.data.get('run_time')
                day_of_week = eval(run_time)["day_of_week"]
                hour = eval(run_time)["hour"]
                minute = eval(run_time)["minute"]
                second = eval(run_time)["second"]
                job = scheduler.add_job(
                    func=self.custom_job, trigger=trigger_type, day_of_week=day_of_week, hour=hour, minute=minute, second=second, replace_existing=True
                )
                logger.info("Add cron task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            serializer = DjangoJobSerializer(job, fields=JOB_SERIALIZER_FIELDS)
            return APIResponse(code=0, msg='success', data=serializer.data)
        except Exception as e:
            logger.info("Add task failed: {}".format(e))
            return APIResponse(code=1, msg='fail')

    @action(methods=['POST'], detail=True)
    def pause(self, request, *args, **kwargs):
        try:
            job_id = request.data.get['id']
            scheduler.pause_job(job_id)
            return APIResponse(code=0, msg='success')
        except Exception as e:
            logger.info("Pause task failed: {}".format(e))
            return APIResponse(code=1, msg='fail')

    @action(methods=['POST'], detail=True)
    def resume(self, request):
        try:
            job_id = request.data.get['id']
            scheduler.resume_job(job_id)
            return APIResponse(code=0, msg='success')
        except Exception as e:
            logger.info("Resume task failed: {}".format(e))
            return APIResponse(code=1, msg='fail')

    def update(self, request, *args, **kwargs):
        job_id = request.get('id')
        try:
            job = None
            trigger_type = request.data.get('trigger_type')
            if trigger_type == "date":
                run_time = request.data.get('run_time')
                job = scheduler.modify_job(
                    job_id, func=self.custom_job, trigger=trigger_type, next_run_time=run_time, replace_existing=True, coalesce=False
                )
                logger.info("Update one-time task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == 'interval':
                seconds = int(request.data.get('interval_time'))
                if seconds <= 0:
                    raise TypeError('interval_time must great than 0')
                job = scheduler.modify_job(
                    job_id, func=self.custom_job, trigger=trigger_type, seconds=seconds, replace_existing=True, coalesce=False
                )
                logger.info("Update interval task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == "cron":
                day_of_week = eval(request.data.get("run_time"))["day_of_week"]
                hour = eval(request.data.get("run_time"))["hour"]
                minute = eval(request.data.get("run_time"))["minute"]
                second = eval(request.data.get("run_time"))["second"]
                temp_dict = dict(
                    day_of_week=day_of_week, hour=hour, minute=minute, second=second
                )
                job = scheduler.reschedule_job(job_id, trigger='cron', **temp_dict)
                logger.info("Update cron task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            serializer = DjangoJobSerializer(job, fields=JOB_SERIALIZER_FIELDS)
            return APIResponse(code=0, msg='success', data=serializer.data)
        except Exception as e:
            logger.info("Update task failed: {}".format(e))
            return APIResponse(code=1, msg='fail')


class DjangoJobExecutionViewSet(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = DjangoJobExecution.objects.all()
    serializer_class = DjangoJobExecutionSerializer

    def list(self, request, *args, **kwargs):
        logger.info("{} call job exec list api".format(request.user.username))
        return super().list(request, *args, **kwargs)
