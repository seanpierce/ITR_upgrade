import glob
import os
import xml.etree.ElementTree as XML

from django.conf import settings
from .models import Show

upload_dir = os.path.join(settings.BASE_DIR, settings.SCHEDULER_UPLOAD_DIR)

def initiate_ezstream(show: Show):
    # This function would contain the logic to start ezstream with the given show details.
    # The implementation would depend on how you have set up ezstream and how you want to pass the show details to it.

    if show.pre_recorded_show is None:
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

    config_list = glob.glob(f'{upload_dir}/scheduler.xml')
    pid_list = glob.glob(f'{upload_dir}/pid.txt')

    # there should only be one, but just in case
    for config in config_list:
        os.remove(config)

    #  again, there should only be one...
    for pid_file in pid_list:
        # read pid from file
        
        with open(f"{upload_dir}/pid.txt") as file:
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
    
    host = settings.EZSTREAM_HOST
    port = settings.EZSTREAM_PORT
    password = settings.EZSTREAM_PASSWORD
    mountpoint = settings.EZSTREAM_MOUNTPOINT
    stream_format = settings.EZSTREAM_FORMAT

    # create the file structure
    ezstream_elem = XML.Element('ezstream')
    servers_elem = XML.SubElement(ezstream_elem, 'servers')
    server_elem = XML.SubElement(servers_elem, 'server')
    hostname_elem = XML.SubElement(server_elem, 'hostname')
    port_elem = XML.SubElement(server_elem, 'port')
    password_elem = XML.SubElement(server_elem, 'password')
    streams_elem = XML.SubElement(ezstream_elem, 'streams')
    stream_elem = XML.SubElement(streams_elem, 'stream')
    mountpoint_elem = XML.SubElement(stream_elem, 'mountpoint')
    format_elem = XML.SubElement(stream_elem, 'format')
    intakes_elem = XML.SubElement(ezstream_elem, 'intakes')
    intake_elem = XML.SubElement(intakes_elem, 'intake')
    filename_elem = XML.SubElement(intake_elem, 'filename')
    shuffle_elem = XML.SubElement(intake_elem, 'shuffle')
    stream_once_elem = XML.SubElement(intake_elem, 'stream_once')

    # populate element values
    hostname_elem.text = host
    port_elem.text = port
    password_elem.text = password
    mountpoint_elem.text = mountpoint
    format_elem.text = stream_format
    filename_elem.text = f"{upload_dir}{filename}"
    shuffle_elem.text = '0'
    stream_once_elem.text = '1'

    # write file
    ezstream_config = XML.tostring(ezstream_elem, encoding='utf-8', method='xml')
    path = f"{upload_dir}scheduler.xml"
    ezstream_config_file = open(path, "wb")
    ezstream_config_file.write(ezstream_config)
    ezstream_config_file.close()

def start_ezstream():
    """
    Compiles a command to execute an ezstream process.
    Saves the process id (pid) to a file for furure reference when
    replacing the current ezstream config.
    """

    upload_dir = os.path.join(settings.BASE_DIR, settings.SCHEDULER_UPLOAD_DIR)
    path_to_config = f"{upload_dir}scheduler.xml"
    path_to_pid = f"{upload_dir}pid.txt"
    command = f'echo $$ > {path_to_pid}; ezstream -c {path_to_config}'
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