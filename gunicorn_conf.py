from multiprocessing import cpu_count

bind = '0.0.0.0:8000'
reload = True

workers = 2 * cpu_count() + 1
worker_class = 'eventlet'
