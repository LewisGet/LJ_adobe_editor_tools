from werkzeug.wrappers import Request, Response
import json, os, sys
import config


@Request.application
def application(request):
    data = '{"hello": "this is not working now."}'

    if None is not request.args.get("audio_file_path"):
        # todo: all
        pass

    from ast import literal_eval

    data = literal_eval(data)

    return Response(json.dumps(data), mimetype='text/json')

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple(config.host_ip, config.http_port, application)
