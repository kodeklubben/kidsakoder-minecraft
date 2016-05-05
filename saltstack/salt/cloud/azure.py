import salt.config
import salt.client

class AzureClient(object):
    '''
    A client class for handling Azure.

    This should be replaced by CloudClient by Salt, however it was impossible
    to get working so we're using LocalClient instead and calling things directly
    to Salt.
    '''

    def __init__(self):
        '''
        Get the configuration of the Salt master and create a local client
        '''
        self._opts = salt.config.master_config('/etc/salt/master')
        self._client = salt.client.LocalClient()


    def _async(self, fun, arg=[]):
        '''
        Helper method for asynchronous Salt calls
        '''
        self._client.cmd_async(tgt='master', fun=fun, arg=arg)


    def _sync(self, fun, arg=[]):
        '''
        Helper method for synchronous Salt calls
        '''
        return self._client.cmd(tgt='master', fun=fun, arg=arg)


    def create_machines(self, hostnames, size):
        '''
        Creates a number of virtual machines from a list of hostnames.
        Note: This uses asynchronous Salt commands.
        '''
        # TODO Switch just size to profiles
        profile = size

        # Go through hostnames and create async jobs for each of them
        for host in hostnames:
            self._async(fun='cloud.profile', arg=[profile, host])


    def destroy_machines(self, hostnames):
        '''
        Destroys a number of virtual machines from a list of hostnames.
        Note: This uses asynchronous Salt commands.
        '''
        for host in hostnames:
            self._async(fun='cloud.destroy', arg=[host])


    def list_machines(self):
        '''
        List information about all active machines
        '''
        return self._sync(fun='cloud.query')


    def start_machines(self, hostnames):
        '''
        Start virtual machines from a list of hostnames
        '''
        for host in hostnames:
            self._async(fun='cloud.action', arg=['start', 'instance=%s' % host])


    def stop_machines(self, hostnames):
        '''
        Stop virtual machines from a list of hostnames
        '''
        for host in hostnames:
            self._async(fun='cloud.action', arg=['stop', 'instance=%s' % host])


class AzureScheduler(object):


    def __init__(self):
        '''
        Get the configuration of the Salt master and create a local client
        '''
        self._opts = salt.config.master_config('/etc/salt/master')
        self._client = salt.client.LocalClient()


    def add_job(self, name, args, when):
        #'job_args': ['date >> /tmp/date.log'],
        #'when': '2016-05-05 23:00:00'
        kwarg = {
            'function': 'cmd.run',
            'job_args': [args],
            'when': when
        }
        return self._client.cmd(tgt='master', fun='schedule.add', arg=[name], kwarg=kwarg)
