var active_sequence = app.project.activeSequence;
var tracks = app.project.activeSequence.videoTracks;
var total_tracks = tracks.numTracks;
var total_tracks_for_array = tracks.numTracks - 1;

var audio_tracks = app.project.activeSequence.audioTracks;
var audio_total_tracks = audio_tracks.numTracks;
var audio_total_tracks_for_array = audio_tracks.numTracks - 1;

function get_clip(track_sort, clip_sort)
{
    return (tracks[track_sort]).clips[clip_sort];
}


function clone_clip(name, start_at)
{
    // start_at 是從最後列數回來的 track index

    var insert_track_index = total_tracks_for_array - start_at;
    var org_track_index = insert_track_index - 3;

    var clip = get_clip(org_track_index, 0);
    var insert_time_object = active_sequence.getPlayerPosition();
    var insert_time = insert_time_object.seconds;

    var clip_name = name + "_" + (parseInt(insert_time)).toString();
    var clone_item = clip.projectItem.createSubClip(clip_name, 0, 5, 1, 1, 1, 1);

    var insert_track = tracks[insert_track_index];

    insert_track.overwriteClip(clone_item, insert_time_object);

    for (var i = 0; i < insert_track.clips.numItems; i++)
    {
        var this_clip = insert_track.clips[i];

        if (this_clip.projectItem.nodeId == clone_item.nodeId)
        {
            this_clip.setSelected(true);
        }
        else
        {
            this_clip.setSelected(false);
        }
    }
}

function clone_lewis()
{
    clone_clip("lewis", 0);
}

function clone_kevin()
{
    clone_clip("kevin", 1);
}

function clone_gold()
{
    clone_clip("gold", 2);
}

/**
 * path string
 */
function load_file(path)
{
    app.project.importFiles([path], 1, app.project.rootItem, 0);

    return app.project.rootItem.findItemsMatchingMediaPath(path)[0];
}

function input_to_now(path, start_at)
{
    var input_item = load_file(path);

    var insert_time_object = active_sequence.getPlayerPosition();
    var insert_track = audio_tracks[audio_total_tracks_for_array - start_at];

    insert_track.overwriteClip(input_item, insert_time_object);

    for (var i = 0; i < insert_track.clips.numItems; i++)
    {
        var this_clip = insert_track.clips[i];

        if (this_clip.projectItem.nodeId == input_item.nodeId)
        {
            this_clip.setSelected(true);
        }
        else
        {
            this_clip.setSelected(false);
        }
    }
}

function get_selected_clips(type)
{
    var loop_track = function (tracks, indexs) {
        var return_value = [];

        for (var i = 0; i < indexs; i++)
        {
            var this_track = tracks[i];

            for (var ii = 0; ii < this_track.clips.numItems; ii++)
            {
                var this_clip = this_track.clips[ii];

                if (this_clip.isSelected())
                {
                    return_value.push(this_clip);
                }
            }
        }

        return return_value;
    };

    if (type == "audio")
    {
        return loop_track(audio_tracks, audio_total_tracks);
    }

    return loop_track(tracks, total_tracks);
}

function get_clip_info(clip)
{
    var start = clip.inPoint.seconds;
    var end = clip.outPoint.seconds;
    var file_path = clip.projectItem.getMediaPath();

    return [start, end, file_path];
}

function get_selected_clips_info(type)
{
    var return_value = [];
    var selected_clips = get_selected_clips(type);

    for (var i = 0; i < selected_clips.length; i++)
    {
        var this_clip = selected_clips[i];

        return_value.push(get_clip_info(this_clip));
    }

    return return_value;
}

/**
 * server to client return will only pass string.
 */
function pass_to_client(v)
{
    return JSON.stringify(v);
}

function _client_get_selected_clips_info(type)
{
    return pass_to_client(get_selected_clips_info(type));
}

function server_debug(code)
{
    return eval(code);
}
