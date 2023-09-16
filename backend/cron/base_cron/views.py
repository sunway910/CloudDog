from abc import abstractmethod
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJob
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from handler import APIResponse
from cron.serializers import DjangoJobSerializer
from config import settings

import logging

logger = logging.getLogger('cpm')

scheduler = BackgroundScheduler(
    job_defaults=settings.JOB_DEFAULTS,
    executors=settings.EXECUTORS,
    timezone=settings.JOB_TIMEZONE)
scheduler.add_jobstore(DjangoJobStore(), "job_store")


class DjangoJobBaseViewSet(ModelViewSet):
    @abstractmethod
    def custom_job(self):
        pass

    permission_classes = ['IsAdminUserOrReadOnly']
    authentication_classes = ['JWTAuthentication']
    queryset = DjangoJob.objects.all()
    serializer_class = DjangoJobSerializer

    def create(self, request, *args, **kwargs):
        try:
            trigger_type = request.data.get('trigger_type')
            if trigger_type == "date":
                run_time = request.data.get('run_time')
                job = scheduler.add_job(func=self.custom_job,
                                        trigger=trigger_type,
                                        next_run_time=run_time,
                                        replace_existing=True,
                                        coalesce=False)
                logger.info("Add one-time task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == 'interval':
                seconds = int(request.data.get('interval_time'))
                if seconds <= 0:
                    raise TypeError('interval_time must great than 0')
                job = scheduler.add_job(func=self.custom_job,
                                        trigger=trigger_type,
                                        seconds=seconds,
                                        replace_existing=True,
                                        coalesce=False)
                logger.info("Add interval task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == "cron":
                day_of_week = eval(request.data.get("run_time"))["day_of_week"]
                hour = eval(request.data.get("run_time"))["hour"]
                minute = eval(request.data.get("run_time"))["minute"]
                second = eval(request.data.get("run_time"))["second"]
                job = scheduler.add_job(func=self.custom_job, trigger=trigger_type, day_of_week=day_of_week,
                                        hour=hour, minute=minute,
                                        second=second, replace_existing=True)
                logger.info("Add cron task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            return APIResponse(code=0, msg='success', data="Add task successfully")
        except Exception as e:
            logger.info("Add task failed: {}".format(e))
            return APIResponse(code=1, msg='fail', data="Add task failed")

    @action(methods=['POST'], detail=True)
    def pause(self, request, *args, **kwargs):
        try:
            job_id = request.data.get['id']
            scheduler.pause_job(job_id)
            return APIResponse(code=0, msg='success', data="Pause task successfully")
        except Exception as e:
            logger.info("Pause task failed: {}".format(e))
            return APIResponse(code=1, msg='fail', data="Pause task failed")

    @action(methods=['POST'], detail=True)
    def resume(self, request):
        try:
            job_id = request.data.get['id']
            scheduler.resume_job(job_id)
            return APIResponse(code=0, msg='success', data="Resume task successfully")
        except Exception as e:
            logger.info("Resume task failed: {}".format(e))
            return APIResponse(code=1, msg='fail', data="Resume task failed")

    def update(self, request, *args, **kwargs):
        job_id = request.get('id')
        try:
            trigger_type = request.data.get('trigger_type')
            if trigger_type == "date":
                run_time = request.data.get('run_time')
                job = scheduler.modify_job(job_id,
                                           func=self.custom_job,
                                           trigger=trigger_type,
                                           next_run_time=run_time,
                                           replace_existing=True,
                                           coalesce=False)
                logger.info("Update one-time task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == 'interval':
                seconds = int(request.data.get('interval_time'))
                print('seconds value is', seconds)
                if seconds <= 0:
                    raise TypeError('interval_time must great than 0')
                job = scheduler.modify_job(job_id, func=self.custom_job,
                                           trigger=trigger_type,
                                           seconds=seconds,
                                           replace_existing=True,
                                           coalesce=False)
                logger.info("Update interval task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            elif trigger_type == "cron":
                day_of_week = eval(request.data.get("run_time"))["day_of_week"]
                hour = eval(request.data.get("run_time"))["hour"]
                minute = eval(request.data.get("run_time"))["minute"]
                second = eval(request.data.get("run_time"))["second"]
                temp_dict = dict(day_of_week=day_of_week,
                                 hour=hour, minute=minute,
                                 second=second)
                job = scheduler.reschedule_job(job_id, trigger='cron', **temp_dict)
                logger.info("Update cron task successfully, Job: {}, Job ID: {}".format(job, job.__getstate__().get('id')))
            return APIResponse(code=0, msg='success', data="Update task successfully")
        except Exception as e:
            logger.info("Update task failed: {}".format(e))
            return APIResponse(code=1, msg='fail', data="Update task failed")


scheduler.start()
