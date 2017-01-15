from multiprocessing import cpu_count

bind = '0.0.0.0:8000'
reload = True

worker_class = 'eventlet'
workers = 2 * cpu_count() + 1
threads = 2 * cpu_count()
timeout = 180
