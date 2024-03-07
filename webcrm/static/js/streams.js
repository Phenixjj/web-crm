// Description: This file contains the configuration for the streams.

const APP_ID = '56f0277797a9410a96f336a003598711';
const CHANNEL = 'main'
const AGORA_TOKEN = '007eJxTYAg2/HS4bpPKTZuY5Akymz5LeH9bLGpbJDRRY6V33iOhefMUGEzN0gyMzM3NLc0TLU0MDRItzdKMjc0SDQyMTS0tzA0NLWe/TG0IZGQ4VdfBxMgAgSA+C0NuYmYeAwMA4YYd0Q==';
let UID;
console.log("stream.js connected!");

// Create a client
var client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'});

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
        UID = await client.join(APP_ID, CHANNEL, AGORA_TOKEN, null)
        console.log("User ID: ", UID);

        localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

        let player = `<div class="video-container" id="user-container-${UID}"><div class="username-wrapper"><span class="user-name">Me</span></div><div class="video-player" id="user-${UID}"></div></div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

        localTracks[1].play(`user-${UID}`)
        await client.publish(localTracks[0], localTracks[1])
}

joinAndDisplayLocalStream();