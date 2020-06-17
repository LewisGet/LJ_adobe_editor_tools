#target PremierePro

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

/**
    projectItem.createSubClip
    1. clone item name.
    2. start time ( in clip )
    3. end time ( in clip )
    4. time extends to the end of the video
    5. session counter???  in don't know that it is.
    6. clone video
    7. clone audio
 */
var item2 = track_2_clip_1_item_1.createSubClip("hello", 0, 5, 1, 1, 1, 1);

track_2.insertClip(item2, 5);
track_2.insertClip(item2, 6);
track_2.insertClip(item2, 7);

/**
    app.project.importFiles
    1. array file paths
    2. suppress warnings
    3. input to where
    4. import as numbered stills
 */
app.project.importFiles(["D:\\code\\LJ_adobe_editor_tools\\test_video2.mp4"], 1, app.project.rootItem, 0);

var logs = item2.getXMPMetadata();

/**
    now active player time bar
   */
var active_time_point = active_sequence.getPlayerPosition();