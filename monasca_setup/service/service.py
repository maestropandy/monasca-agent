# (C) Copyright 2015 Hewlett Packard Enterprise Development Company LP
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Code to handle various service managers used on different OS

"""
from monasca_agent.common.psutil_wrapper import psutil


class Service(object):
    """Abstract base class implementing the interface for various service types.

    """

    def __init__(self, prefix_dir, config_dir, log_dir, template_dir,
                 name='monasca-agent', username='monasca-agent'):
        self.prefix_dir = prefix_dir
        self.config_dir = config_dir
        self.log_dir = log_dir
        self.template_dir = template_dir
        self.name = name
        self.username = username

    def enable(self):
        """Sets monasca-agent to start on boot.

            Generally this requires running as super user
        """
        raise NotImplementedError

    def start(self, restart=True):
        """Starts monasca-agent.

            If the agent is running and restart is True, restart
        """
        raise NotImplementedError

    def stop(self):
        """Stops monasca-agent.

        """
        raise NotImplementedError

    def is_enabled(self):
        """Returns True if monasca-agent is setup to start on boot, false otherwise.

        """
        raise NotImplementedError

    def is_running(self):
        """Returns True if monasca-agent is running, false otherwise.

        """
        # Looking for the supervisor process not the individual components
        for process in psutil.process_iter():
            if ('{0}/supervisor.conf'.format(self.config_dir)
                    in process.as_dict(['cmdline'])['cmdline']):
                return True

        return False
