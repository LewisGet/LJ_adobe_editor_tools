from werkzeug.wrappers import Request, Response
import json, os, sys
import input_audio
import threading
import config
import time

server_audio_recorder = input_audio.basic_recorder(input_device_index=config.input_device_index)

@Request.application
def application(request):
    data = '{"hello": "this is not working now."}'

    if None is not request.args.get("audio_file_path"):
        # todo: all
        pass

    if None is not request.args.get("start_record"):
        background = threading.Thread(name='background', target=server_audio_recorder.start)
        background.start()

    if None is not request.args.get("stop_record"):
        server_audio_recorder.end()

        filename = str(time.time()) + ".wav"
        org_file_path = os.path.sep.join([config.org_audio_save_path, filename])

        server_audio_recorder.save(org_file_path)
        x = input_audio.file_to_input(org_file_path)
        input_audio.conversion_with_config(x, filename)


    from ast import literal_eval

    data = literal_eval(data)

    return Response(json.dumps(data), mimetype='text/json')

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple(config.host_ip, config.http_port, application)
