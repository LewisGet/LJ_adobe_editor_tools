var active_sequence = app.project.activeSequence;
var tracks = app.project.activeSequence.videoTracks;
var total_tracks = tracks.numTracks;
var total_tracks_for_array = tracks.numTracks - 1;

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

    var org_track_clips = pre_clone_clip(insert_track);

    insert_track.overwriteClip(clone_item, insert_time_object);

    var now_track_clips = post_clone_clip(insert_track);

    var new_clips = now_track_clips.filter(function(obj) { return org_track_clips.indexOf(obj) == -1; });

    for (var i = 0; i < new_clips.length; i++)
    {
        new_clips[i].setSelected(true);
    }
}

function pre_clone_clip(execute_track)
{
    var pre_execute = [];

    for (var i = 0; i < execute_track.clips.numItems; i++)
    {
        pre_execute.push(execute_track.clips[i]);
    }

    return pre_execute;
}

function post_clone_clip(execute_track)
{
    var post_execute = [];

    for (var i = 0; i < execute_track.clips.numItems; i++)
    {
        post_execute.push(execute_track.clips[i]);
    }

    return post_execute;
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
