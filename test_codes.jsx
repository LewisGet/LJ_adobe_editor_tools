var console = {
        log: function (value) {
                $.writeln(value);
            }
    };

var lj = $;

app.enableQE();

var active_sequence = app.project.activeSequence;

var tracks = app.project.activeSequence.videoTracks;

var track_2 = tracks[1];

var track_2_clips = track_2.clips;

var track_2_clip_1 = track_2.clips[0];

track_2_clips[0].setSelected(true);

var track_2_clip_1_component_1 = track_2_clip_1.components[0];
var track_2_clip_1_component_2 = track_2_clip_1.components[1];

console.log(track_2_clip_1.getLinkedItems());

for (var i = 0; i < track_2_clip_1_component_2.properties.numItems; i++)
{
    var property = {};
    
    property[i.toString()] = track_2_clip_1_component_2.properties[i];
}

var track_2_clip_1_item_1 = track_2_clip_1.projectItem;

for (var i = 0; i < track_2_clip_1_item_1.videoComponents.numItems; i++)
{
    var video_components = {};
    
    video_components[i.toString()] = track_2_clip_1_item_1.videoComponents[i];
}

var item2 = track_2_clip_1_item_1.createSubClip("hello", 0, 5, 1, 1, 1, 1);

track_2.insertClip(item2, 5);
track_2.insertClip(item2, 6);
track_2.insertClip(item2, 7);