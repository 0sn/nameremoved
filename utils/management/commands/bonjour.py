"""
This is autodiscovered by Django and added to the manage.py commands::

python manage.py bonjour

starts the development server on the current computer, listening on all
interfaces, on port 8000.

It also runs the dns-sd discovery program simultaneously, thus the title.
"""

from django.core.management.base import NoArgsCommand
import sys, os, atexit
import subprocess

DNS_SD_PID = None

def _start_bonjour():
    global DNS_SD_PID
    if DNS_SD_PID:
        return
    
    from django.conf import settings
    name = "Django: " + settings.SETTINGS_MODULE
    command = ["/usr/bin/dns-sd", "-R", name, "_http._tcp", ".", "8000", "path=/"]
    if os.path.exists("/usr/bin/dns-sd"):
        # stdout can go hang. no-one wants to hear about your stupid registry!!
        DNS_SD_PID = subprocess.Popen(command, stdout=subprocess.PIPE).pid
        atexit.register(_stop_bonjour)

def _stop_bonjour():
    global DNS_SD_PID
    if not DNS_SD_PID:
        return
    try:
        os.kill(DNS_SD_PID, 15)
    except OSError:
        pass

class Command(NoArgsCommand):
    help = "Starts a lightweight Web server for development, registered on Bonjour."
    
    def handle_noargs(self, **options):
        # This is mostly just swiped from the django source... but check out
        # 1. no way ability to change the default settings
        # 2. _start and _stop_bonjour, swiped from turbogears
        import django
        from django.core.servers.basehttp import run, AdminMediaHandler, WSGIServerException
        from django.core.handlers.wsgi import WSGIHandler
        
        def inner_run():
            from django.conf import settings
            from django.utils import translation
            print "Validating models..."
            self.validate(display_num_errors=True)
            print "\nDjango version %s, using settings %r" % (django.get_version(), settings.SETTINGS_MODULE)
            print "Development server is running at http://0.0.0.0:8000"
            print "Quit the server with CONTROL-C."
            
            translation.activate(settings.LANGUAGE_CODE)
            
            try:
                path = django.__path__[0] + '/contrib/admin/media'
                handler = AdminMediaHandler(WSGIHandler(), path)
                run("0.0.0.0", 8000, handler)
            except WSGIServerException, e:
                ERRORS = {
                    13: "You don't have permission to access that port.",
                    98: "That port is already in use.",
                    99: "That IP address can't be assigned-to.",
                }
                try:
                    error_text = ERRORS[e.args[0].args[0]]
                except (AttributeError, KeyError):
                    error_text = str(e)
                sys.stderr.write(self.style.ERROR("Error: %s" % error_text) + '\n')
                _stop_bonjour()
                os._exit(1)
            except KeyboardInterrupt:
                _stop_bonjour()
                sys.exit(0)
        
        _start_bonjour()
        from django.utils import autoreload
        autoreload.main(inner_run)