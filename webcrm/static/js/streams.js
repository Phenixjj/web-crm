// Description: This file contains the configuration for the streams.

const APP_ID = '56f0277797a9410a96f336a003598711';
const CHANNEL = 'main'
const AGORA_TOKEN = '007eJxTYNBQ0924e/acK3fEnO5tW+G0U2nygsQjEz/8E6icWiTx79NrBQZTszQDI3Nzc0vzREsTQ4NES7M0Y2OzRAMDY1NLC3NDw4Wqb1IbAhkZTpfuY2CEQhCfhSE3MTOPgQEAwrgg/A==';
let UID;
console.log("stream.js connected!");

// Create a client
var client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'});

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    client.on('user-published', handleUserPublished);
    client.on('user-unpublished', handleUserLeft);
    UID = await client.join(APP_ID, CHANNEL, AGORA_TOKEN, null)
    console.warn("User ID: ", UID);

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    console.warn('======> Local audio track:', localTracks[0]);
    console.warn('======> Local video track:', localTracks[1]);

    let player = `<div class="video-container" id="user-container-${UID}"><div class="username-wrapper"><span class="user-name">Me</span></div><div class="video-player" id="user-${UID}"></div></div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)
    await client.publish(localTracks[0], localTracks[1])
}

let handleUserPublished = async (user, mediaType) => {

    remoteUsers[user.uid] = user
    console.warn("User ID: ", user.uid);
    console.warn("subscribe success");
    console.warn("'======> User mediaType : ", mediaType);
    remoteTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    let remoteAudioTrack = remoteTracks[0]
    let remoteVideoTrack = remoteTracks[1]
    // Subscribe to the user
    await client.subscribe(user, mediaType);
    console.warn('======> User remote published video track:', remoteVideoTrack);
    console.warn('======> User remote published audio track:', remoteAudioTrack);


    if(remoteVideoTrack) {
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null) {
            player.remove()
        }
        player = `<div class="video-container" id="user-container-${user.uid}"><div class="username-wrapper"><span class="user-name">User ${user.uid}</span></div><div class="video-player" id="user-${user.uid}"></div></div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        remoteVideoTrack.play(`user-${user.uid}`)
    }
    if (remoteAudioTrack) {
        remoteAudioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    let player = document.getElementById(`user-container-${user.uid}`);
    if (player) {
        player.remove();
    }
}
joinAndDisplayLocalStream()