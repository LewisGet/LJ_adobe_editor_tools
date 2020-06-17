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
    var insert_time = active_sequence.getPlayerPosition().seconds;

    var clip_name = name + "_" + (parseInt(insert_time)).toString();
    var clone_item = clip.projectItem.createSubClip(clip_name, 0, 5, 1, 1, 1, 1);

    var insert_track = tracks[insert_track_index];

    insert_track.insertClip(clone_item, insert_time);
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
