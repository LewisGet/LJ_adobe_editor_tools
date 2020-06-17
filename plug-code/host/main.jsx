var active_sequence = app.project.activeSequence;
var tracks = app.project.activeSequence.videoTracks;
var total_tracks = tracks.numTracks;
var total_tracks_for_array = tracks.numTracks - 1;

function get_clip(track_sort, clip_sort)
{
    return (tracks[track_sort]).clips[clip_sort];
}


function clone_lewis()
{
    // 從最後列數回來
    var add_in = 0;
    var insert_track_index = total_tracks_for_array - add_in;
    var org_track_index = insert_track_index - 3;

    var clip = get_clip(org_track_index, 0);
    var insert_time = active_sequence.getPlayerPosition().seconds;

    var clip_name = "lewis_" + (parseInt(insert_time)).toString();
    var clone_item = clip.projectItem.createSubClip(clip_name, 0, 5, 1, 1, 1, 1);

    var insert_track = tracks[insert_track_index];

    insert_track.insertClip(clone_item, insert_time);
}
