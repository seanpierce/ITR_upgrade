import glob
import os
from django.conf import settings
from xml.etree.ElementTree import XML

from .models import Show


def initiate_ezstream(show: Show):
    # This function would contain the logic to start ezstream with the given show details.
    # The implementation would depend on how you have set up ezstream and how you want to pass the show details to it.

    if show.pre_recorded_show.field.blank or show.pre_recorded_show is None:
        message = 'Show for this time slot %s - %s does not have pre-recorded audio' %(show.start_date_time, show.end_date_time)
        return message
    
    audio = show.pre_recorded_show.path

    try:
        delete_existing_config()
    except Exception as ex:
        return str(ex)

    try:
        create_ezstream_config(audio)
    except Exception as ex:
        return str(ex)

    try:
        start_ezstream()
    except Exception as ex:
        return str(ex)

    return True


def delete_existing_config():
    """
    Deletes any existing pid or config files.
    """

    config_list = glob.glob('%s/scheduler.xml' %os.path.dirname(os.path.abspath(__file__)))
    pid_list = glob.glob('%s/pid.txt' %os.path.dirname(os.path.abspath(__file__)))

    # there should only be one, but just in case
    for config in config_list:
        os.remove(config)

    #  again, there should only be one...
    for pid_file in pid_list:
        # read pid from file
        with open("%s/pid.txt" %os.path.dirname(os.path.abspath(__file__))) as file:
            pid = file.readline().strip()
            # kill process (if exists)
            # note: ezstream process will always be 1 more than the pid on file
            os.system("kill -9 %s" %(int(pid) + 1))

        # delete file
        os.remove(pid_file)


def create_ezstream_config(filename):
    """
    Creates ezstream xml config file.
    """

    upload_dir = settings.SCHEDULER_UPLOAD_DIR
    host = settings.EZSTREAM_HOST
    port = settings.EZSTREAM_PORT
    password = settings.EZSTREAM_PASSWORD
    mountpoint = settings.EZSTREAM_MOUNTPOINT
    stream_format = settings.EZSTREAM_FORMAT

    # create the file structure
    ezstream = XML.Element('ezstream')
    servers = XML.SubElement(ezstream, 'servers')
    server = XML.SubElement(servers, 'server')
    hostname = XML.SubElement(server, 'hostname')
    port = XML.SubElement(server, 'port')
    password = XML.SubElement(server, 'password')
    streams = XML.SubElement(ezstream, 'streams')
    stream = XML.SubElement(streams, 'stream')
    mountpoint = XML.SubElement(stream, 'mountpoint')
    format_element = XML.SubElement(stream, 'format')
    intakes = XML.SubElement(ezstream, 'intakes')
    intake = XML.SubElement(intakes, 'intake')
    filename_element = XML.SubElement(intake, 'filename')
    shuffle = XML.SubElement(intake, 'shuffle')
    stream_once = XML.SubElement(intake, 'stream_once')

    # populate element values
    hostname.text = host
    port.text = port
    password.text = password
    mountpoint.text = mountpoint
    format_element.text = stream_format
    filename_element.text = '%s/%s' %(upload_dir, filename.rsplit('/', 1)[1])
    shuffle.text = '0'
    stream_once.text = '1'

    # write file
    ezstream_config = XML.tostring(ezstream)
    path = "%s/scheduler.xml" %os.path.dirname(os.path.abspath(__file__))
    ezstream_config_file = open(path, "wb")
    ezstream_config_file.write(ezstream_config)


def start_ezstream():
    """
    Compiles a command to execute an ezstream process.
    Saves the process id (pid) to a file for furure reference when
    replacing the current ezstream config.
    """

    path_to_config = "%s/scheduler.xml" %os.path.dirname(os.path.abspath(__file__))
    path_to_pid = "%s/pid.txt" %os.path.dirname(os.path.abspath(__file__))
    command = 'echo $$ > %s; ezstream -c %s' %(path_to_pid, path_to_config)
    os.system(command)

# def run():
#     now = datetime.datetime.now()
#     date = now.strftime('%Y-%m-%d')
#     time = now.strftime('%H:%M:%S')
#     hour = int(now.strftime('%H'))

#     show = repo.get_show_by_date_and_hour(date, hour)

#     if show is None:
#         message = 'No show for this time slot %s - %s' %(date, time)
#         return message

#     audio = show['pre_recorded_show']

#     if not audio:
#         message = 'Show for this time slot %s - %s does not have pre-recorded audio' %(date, time)
#         return message

#     try:
#         delete_existing_config()
#     except Exception as ex:
#         return str(ex)

#     try:
#         create_ezstream_config(audio)
#     except Exception as ex:
#         return str(ex)

#     try:
#         start_ezstream()
#     except Exception as ex:
#         return str(ex)

#     return True