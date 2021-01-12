from werkzeug.wrappers import Request, Response
import json, os, sys
import input_audio
import threading
import config
import time
import unit

server_audio_recorder = input_audio.basic_recorder(input_device_index=config.input_device_index)

@Request.application
def application(request):
    data = {"hello": "this is not working now."}

    if None is not request.args.get("path") and \
       None is not request.args.get("start") and \
       None is not request.args.get("end") and \
       None is not request.args.get("type"):

        path = request.args.get("path")
        start = float(request.args.get("start"))
        end = float(request.args.get("end"))
        clip_type = request.args.get("type")

        # debug print
        print (path, start, end, clip_type)

        p1, p2 = unit.save_clip_research(path, start, end, clip_type)

        data = {
            "message": "org: " + p1 + " 16k: " + p2,
            "org_path": p1,
            "min_path": p2
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
