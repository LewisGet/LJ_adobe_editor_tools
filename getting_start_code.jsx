var console = {
        log: function (value) {
                $.writeln(value);
            }
    };

var lj = $;

//console.log(app.project.activeSequence.videoTracks.numTracks);
//console.log(options);

var now_sence = app.project.activeSequence;

// 所有影片編輯圖層
var tracks = app.project.activeSequence.videoTracks;

// 第一個編輯影片曾
var trackOne = tracks[0];

// 第一個影片層的第一個影片截斷
var firstClip = trackOne.clips[0];

var clipToProjectItem = firstClip.projectItem;

var clip_markers = clipToProjectItem.getMarkers();

var clipComponents = clipToProjectItem.videoComponents;

var now_markers = now_sence.markers;

// 在該影片截斷 10秒加入標記
//clipComponents.createMarker (10);

// 標記在現在瀏覽的時間軸上的 11秒處
now_markers.createMarker (11);


// 所有影片截斷
for (var i = 0; i < trackOne.clips.numItems; i++)
{
    var clip = trackOne.clips[i];
    
    // 設定選擇
    clip.setSelected ((Math.random() > 0.5), true);
    
    // 這影片片段是否被選擇
    //console.log(clip.isSelected());
    
    //console.log(clip.getLinkedItems());
}

// 現在啟用介面的 介面操作者選取位置
var now = app.project.activeSequence.getPlayerPosition();

// 時間軸的秒數
//console.log(now.seconds);

//console.log(track.setSelected(1, true));

//console.log(app.project.rootItem.getXMPMetadata());
console.log(clipToProjectItem.videoComponents);
//console.log(firstClip.mediaType);

// 開啟媒體管理氣 (另個應用程式)
//app.encoder.launchEncoder();