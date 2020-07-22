from werkzeug.wrappers import Request, Response
import json, os, sys
import cycle_gan_2_input as vc2
import input_audio
import threading
import config
import time

server_audio_recorder = input_audio.basic_recorder(input_device_index=config.input_device_index)

@Request.application
def application(request):
    data = {"hello": "this is not working now."}

    if None is not request.args.get("audio_file_path") and \
       None is not request.args.get("start") and \
       None is not request.args.get("end"):
        path = request.args.get("audio_file_path")
        org_name, _ = os.path.splitext(os.path.basename(path))
        filename = str(time.time()) + "-" + org_name + ".wav"

        start = float(request.args.get("start"))
        end = float(request.args.get("end"))

        #todo: cute audio
        x = vc2.file_to_input(path, backup=True, start=start, end=end, backup_rename = filename)
        vc2.conversion_with_config(x, filename)

        data = {
            "message": "clip " + filename,
            "org_path": path,
            "pre_path": os.path.sep.join([os.getcwd(), config.pre_vc_2_audio_save_path, filename]),
            "vc2_path": os.path.sep.join([os.getcwd(), config.vc_2_audio_save_path, filename])
        }

    if None is not request.args.get("start_record"):
        background = threading.Thread(name='background', target=server_audio_recorder.start)
        background.start()

        data = {"message": "start record"}

    if None is not request.args.get("stop_record"):
        server_audio_recorder.end()

        filename = str(time.time()) + ".wav"
        org_file_path = os.path.sep.join([config.org_audio_save_path, filename])

        server_audio_recorder.save(org_file_path)
        x = vc2.file_to_input(org_file_path, True)
        vc2.conversion_with_config(x, filename)

        data = {
            "message": "stop record",
            "org_path": os.path.sep.join([os.getcwd(), org_file_path]),
            "vc2_path": os.path.sep.join([os.getcwd(), config.vc_2_audio_save_path, filename])
        }

    return Response(json.dumps(data), mimetype='text/json')

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple(config.host_ip, config.http_port, application)
