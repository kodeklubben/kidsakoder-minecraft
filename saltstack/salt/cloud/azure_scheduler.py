import salt.config
import salt.client

class AzureScheduler(object):
    '''
    A scheduler class for scheduling Azure jobs in Salt.
    '''

    def __init__(self):
        '''
        Get the configuration of the Salt master and create a local client
        '''
        self._opts = salt.config.master_config('/etc/salt/master')
        self._client = salt.client.LocalClient()


    def add_job(self, name, args, when):
        '''
        Adds a job to the Salt scheduler.
        Returns a dict with results.
        '''
        #'job_args': ['date >> /tmp/date.log'],
        #'when': '2016-05-05 23:00:00'
        kwarg = {
            'function': 'cmd.run',
            'job_args': [args],
            'when': when
        }
        return self._client.cmd(tgt='master', fun='schedule.add', arg=[name], kwarg=kwarg)
