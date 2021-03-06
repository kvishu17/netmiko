from __future__ import unicode_literals
import time
from netmiko.cisco_base_connection import CiscoSSHConnection
from netmiko import log


class AristaSSH(CiscoSSHConnection):
    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self._test_channel_read(pattern=r'[>#]')
        self.set_base_prompt()
        self.disable_paging()
        self.set_terminal_width(command='terminal width 511')
        # Clear the read buffer
        time.sleep(.3 * self.global_delay_factor)
        self.clear_buffer()

    def check_config_mode(self, check_string=')#', pattern=''):
        """
        Checks if the device is in configuration mode or not.

        Arista, unfortunately, does this:
        loc1-core01(s1)#

        Can also be (s2)
        """
        log.debug("pattern: {0}".format(pattern))
        self.write_channel(self.RETURN)
        output = self.read_until_pattern(pattern=pattern)
        log.debug("check_config_mode: {0}".format(repr(output)))
        output = output.replace("(s1)", "")
        output = output.replace("(s2)", "")
        log.debug("check_config_mode: {0}".format(repr(output)))
        return check_string in output
