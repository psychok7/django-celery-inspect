# django-celery-inspect

Django reusable-app that uses Celery Inspect command to monitor workers via the [Django REST Framework](https://github.com/tomchristie/django-rest-framework).

The main idea is to be able to monitor celery workers from another external service or server via a REST API and figure out if they are running or not by using celery's own [Inspect API]
(http://docs.celeryproject.org/en/latest/userguide/workers.html#inspecting-workers).

## Quick start

1. Install:

		pip install django-celery-inspect

2. Add "celery_inspect" to your INSTALLED_APPS setting like this:

		INSTALLED_APPS = [
    
          ...
          'celery_inspect',
        ]

3. Add the following to your urls.py:

		url(r'^api/v1/celery-inspect/', include('celery_inspect.urls', namespace='celery_inspect')),
    
4. If you Desire to use DRF's Authentication to protect these endpoints (Optional).

		REST_FRAMEWORK = {
		    'DEFAULT_AUTHENTICATION_CLASSES': (
			'rest_framework.authentication.TokenAuthentication',
		    ),
		    'DEFAULT_PERMISSION_CLASSES': (
			'rest_framework.permissions.IsAuthenticated',
		    ),
		}

## Usage:

1. http://localhost:8000/api/v1/celery-inspect/ping/

		{
			"worker2@localhost:8000": {
			    "ok": "pong"
			},
			"worker1@localhost:8000": {
			    "ok": "pong"
			}
        	}
        
2. http://localhost:8000/api/v1/celery-inspect/active/

        {
            "worker2@localhost:8000": [],
            "worker1@localhost:8000": []
        }
        
3. http://localhost:8000/api/v1/celery-inspect/registered/

        {
            "worker2@localhost:8000": [
                "core.tasks.db_backup",
                "core.tasks.send_queued_emails",
                "yy.tasks.assign_to_mongo",
                "xx.tasks.check_for_new_registered",
                "xx.tasks.create_and_associate_manager",
                "qq.celery.debug_task"
            ],
            "worker1@localhost:8000": [
                "core.tasks.db_backup",
                "core.tasks.send_queued_emails",
                "yy.tasks.assign_to_mongo",
                "xx.tasks.check_for_new_registered",
                "xx.tasks.create_and_associate_manager",
                "qq.celery.debug_task"
            ]
        }
        
4. http://localhost:8000/api/v1/celery-inspect/scheduled/

        {
            "worker2@localhost:8000": [],
            "worker1@localhost:8000": []
        }



### If for some reason you can only deal with status codes (This feature will only work if you have django-celery installed)

1. http://localhost:8000/api/v1/celery-inspect/active-status/

    - Returns 200 if all workers in WorkerState are up.
    - Returns 404 if workers are down (WorkerState != then inspect()).
    - Returns 501 if djcelery a.k.a django-celery is not installed.