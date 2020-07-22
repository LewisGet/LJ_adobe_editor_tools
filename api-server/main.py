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

    if None is not request.args.get("audio_file_path"):
        # todo: adobe 點音效 clips 時，取得 clips 的 start point 跟 end point 與 path
        # todo: 再透過 python 取 path 拿到音效檔，依照 start end point 截斷 array 在執行 vc, vc2
        pass

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
