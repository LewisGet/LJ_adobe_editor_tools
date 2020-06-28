from werkzeug.wrappers import Request, Response
import json, os, sys
import input_audio
import threading
import config


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
        server_audio_recorder.record_stop = True

    from ast import literal_eval

    data = literal_eval(data)

    return Response(json.dumps(data), mimetype='text/json')

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple(config.host_ip, config.http_port, application)
