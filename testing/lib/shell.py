#!/usr/bin/env python
#

from sys                                import stdout
from subprocess                         import Popen, PIPE, STDOUT
from threading                          import Thread
from time                               import sleep
from logging                            import debug, info

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

# ShellTimeoutError
#
class ShellTimeoutError(Exception):
    """
    """
    def __init__(self, cmd, timeout):
        self.__cmd = cmd
        self.__timeout = timeout

    @property
    def cmd(self):
        '''
        The shell command that was being executed when the timeout occured.
        '''
        return self.__cmd

    @property
    def timeout(self):
        '''
        The timeout period that expired.
        '''
        return self.__timeout

# ShellError
#
class ShellError(Exception):
    """
    """
    def __init__(self, cmd, returncode, output):
        self.__cmd = cmd
        self.__output = output
        self.__returncode = returncode

    @property
    def cmd(self):
        '''
        The shell command that was executed and returned a non-zero exit status.
        '''
        return self.__cmd

    @property
    def returncode(self):
        '''
        The exit status value for the command that was executed.
        '''
        return self.__returncode

    @property
    def output(self):
        return self.__output

# enqueue_output
#
def enqueue_output(out, queue, quiet=False):
    for line in iter(out.readline, b''):
        queue.put(line)
        if not quiet:
            stdout.write(line)
            stdout.flush()
    out.close()

# sh
#
def sh(cmd, timeout=None, ignore_result=False, quiet=False):
    debug('                       cmd : \'%s\'' % cmd)
    debug('                     quiet : %s' % quiet)
    debug('             ignore_result : %s' % ignore_result)
    out = []
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, shell=True)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q, quiet))
    t.daemon = True # thread dies with the program
    t.start()

    if timeout is not None:
        t.join(timeout)
        if t.is_alive():
            p.terminate()
            raise ShellTimeoutError(cmd, timeout)

    while p.poll() is None:
        # read line without blocking
        try:
            line = q.get_nowait()
        except Empty:
            pass
        else: # got line
            out.append(line)
        sleep(1)

    while True:
        try:
            line = q.get_nowait()
        except Empty:
            break
        else: # got line
            out.append(line)

    if not ignore_result:
        if p.returncode != 0:
            raise ShellError(cmd, p.returncode, out)

    return p.returncode, out

# ssh
#
def ssh(target, cmd, additional_ssh_options='', user=None, quiet=False, ignore_result=False):
    result, output = Shell.ssh(target, cmd, additional_ssh_options=additional_ssh_options, user=user, quiet=quiet, ignore_result=ignore_result)
    return result, output

class Shell():
    _dry_run = False
    ssh_options = '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=quiet'

    def __init__(self):
        Shell._dry_run = False

    # ssh
    #
    @classmethod
    def ssh(cls, target, cmd, user, additional_ssh_options='', quiet=False, ignore_result=False):
        debug("Enter Shell::ssh")
        debug('                    target : \'%s\'' % target)
        debug('                       cmd : \'%s\'' % cmd)
        debug('                      user : \'%s\'' % user)
        debug('    additional_ssh_options : \'%s\'' % additional_ssh_options)
        debug('                     quiet : %s' % quiet)
        debug('             ignore_result : %s' % ignore_result)
        ssh_options = cls.ssh_options + ' ' + additional_ssh_options
        if user:
            ssh_cmd = 'ssh %s %s@%s -- %s' % (ssh_options, user, target, cmd)
        else:
            ssh_cmd = 'ssh %s %s -- %s' % (ssh_options, target, cmd)
        result = 0
        output = ''
        debug("                  ssh_cmd : '%s'" % ssh_cmd)
        if cls._dry_run:
            debug('[dry-run] %s' % (ssh_cmd))
        else:
            try:
                result, output = sh(ssh_cmd, quiet=quiet, ignore_result=ignore_result)
                debug("+++ Completed")
                debug(output)

            except ShellError as e:
                debug("+++ ShellError")
                debug(output)
                if result != 0 and not ignore_result:
                    # Wait for just a few seconds and try it again.
                    #
                    #print(" **")
                    #print(" ** retrying the last command")
                    #print(" **")
                    result, output = sh(ssh_cmd, quiet=quiet, ignore_result=ignore_result)
                    if result != 0 and not ignore_result:
                        sleep(15)
                        raise ShellError(ssh_cmd, result, output)
            except:
                debug("+++ Some other exception")

        debug("Leave Shell::ssh")
        return result, output

# vi:set ts=4 sw=4 expandtab syntax=python:
