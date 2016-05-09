import salt.config
import salt.client

class AzureClient(object):
    '''
    A client class for handling Azure.

    This should be replaced by CloudClient by Salt, however it was impossible
    to get working so we're using LocalClient instead and calling things directly
    to Salt.
    '''

    def __init__(self, username, password):
        '''
        Get the configuration of the Salt master and create a local client
        Username and password should be for a user allowed to use external auth
        in Salt master config
        '''
        self._opts = salt.config.master_config('/etc/salt/master')
        self._client = salt.client.LocalClient()
        self._username = username
        self._password = password


    def _async(self, fun, arg=[]):
        '''
        Helper method for asynchronous Salt calls
        '''
        self._client.cmd_async(tgt='master', fun=fun,
                               arg=arg, username=self._username,
                               password=self._password, eauth='pam')


    def _sync(self, fun, arg=[]):
        '''
        Helper method for synchronous Salt calls
        '''
        return self._client.cmd(tgt='master', fun=fun,
                                arg=arg, username=self._username,
                                password=self._password, eauth='pam')


    def create_machines(self, hostnames, profile):
        '''
        Creates a number of virtual machines from a list of hostnames.
        '''
        # Go through hostnames and create async jobs for each of them
        for host in hostnames:
            self._async(fun='cloud.profile', arg=[profile, host])


    def create_machines_with_options(self, hostnames, options):
        '''
        Creates a number of virtual machines from a list of hostnames.
        Similar to regular create_machine method, however here you need to
        specifiy all your own options.
        '''
        # Go through hostnames and create async jobs for each of them
        for host in hostnames:
            self._async(fun='cloud.profile', arg=[profile, host])


    def destroy_machines(self, hostnames):
        '''
        Destroys a number of virtual machines from a list of hostnames.
        '''
        for host in hostnames:
            self._async(fun='cloud.destroy', arg=[host])


    def list_machines(self):
        '''
        List information about all active machines
        '''
        return self._sync(fun='cloud.query')


    def _action(self, action, host):
        '''
        Helper method for sending cloud actions
        '''
        # Allowed actions
        actions = ['start', 'stop', 'reboot']
        if action not in actions:
            pass

        self._async(fun='cloud.action', arg=[action, 'instance=%s' % host])


    def start_machines(self, hostnames):
        '''
        Start virtual machines from a list of hostnames as strings
        '''
        for host in hostnames:
            self._action('start', host)


    def stop_machines(self, hostnames):
        '''
        Stop virtual machines from a list of hostnames as strings
        '''
        for host in hostnames:
            self._action('stop', host)


    def reboot_machines(self, hostnames):
        '''
        Reboot virtual machines from a list of hostnames as strings
        '''
        for host in hostnames:
            self._action('reboot', host)
