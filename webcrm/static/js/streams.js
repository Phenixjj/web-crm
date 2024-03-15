/**
 * This file contains the configuration for the streams.
 * @file streams.js
 */

// The APP_ID for the Agora application
const APP_ID = '56f0277797a9410a96f336a003598711';

// The channel name for the Agora application
const CHANNEL = 'main'

// The token for the Agora application
const AGORA_TOKEN = '007eJxTYHj5q4zDWNnBYd1f9VlnQtjWK0iUiuT7flg/4Vl5OEPp/X0KDKZmaQZG5ubmluaJliaGBomWZmnGxmaJBgbGppYW5oaGKS8/pjYEMjLM/3qNhZEBAkF8FobcxMw8BgYA+rIfCQ==';

// The user ID for the current session, to be assigned later
let UID;

console.log("stream.js connected!");

/**
 * Create a client using AgoraRTC
 * @type {AgoraRTC.Client}
 */
var client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'});

// Tracks for the local user
let localTracks = []

// Object to store remote users
let remoteUsers = {}

/**
 * Function to join the Agora channel and display the local stream
 * @async
 */
let joinAndDisplayLocalStream = async () => {
    // Set up event listeners for user-published and user-unpublished events
    client.on('user-published', handleUserPublished);
    client.on('user-unpublished', handleUserLeft);

    // Join the Agora channel and get the user ID
    UID = await client.join(APP_ID, CHANNEL, AGORA_TOKEN, null)
    console.warn("User ID: ", UID);

    // Create audio and video tracks for the local user
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    // Add the local user's video to the DOM
    let player = `<div class="video-container" id="user-container-${UID}"><div class="username-wrapper"><span class="user-name">Me</span></div><div class="video-player" id="user-${UID}"></div></div>`
    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    // Play the local user's video and publish the local tracks
    localTracks[1].play(`user-${UID}`)
    await client.publish(localTracks[0], localTracks[1])
}

/**
 * Function to handle when a user publishes their stream
 * @async
 * @param {AgoraRTC.User} user - The user who published their stream
 * @param {string} mediaType - The type of media that was published
 */
let handleUserPublished = async (user, mediaType) => {

    // Add the user to the remoteUsers object
    remoteUsers[user.uid] = user

    // Create audio and video tracks for the remote user
    let remoteTracks = await AgoraRTC.createMicrophoneAndCameraTracks()
    let remoteAudioTrack = remoteTracks[0]
    let remoteVideoTrack = remoteTracks[1]

    // Subscribe to the user's stream
    await client.subscribe(user, mediaType);

    // If the user published a video track, add it to the DOM and play it
    if(remoteVideoTrack) {
        let player = document.getElementById(`user-container-${user.uid}`)
        if(player != null) {
            player.remove()
        }
        player = `<div class="video-container" id="user-container-${user.uid}"><div class="username-wrapper"><span class="user-name">User ${user.uid}</span></div><div class="video-player" id="user-${user.uid}"></div></div>`
        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        remoteVideoTrack.play(`user-${user.uid}`)
    }

    // If the user published an audio track, play it
    if (remoteAudioTrack) {
        remoteAudioTrack.play()
    }
}

/**
 * Function to handle when a user leaves the channel
 * @async
 * @param {AgoraRTC.User} user - The user who left the channel
 */
let handleUserLeft = async (user) => {
    // Remove the user from the remoteUsers object
    delete remoteUsers[user.uid]

    // Remove the user's video from the DOM
    let player = document.getElementById(`user-container-${user.uid}`);
    if (player) {
        player.remove();
    }
}

// Join the channel and display the local stream when the script is loaded
joinAndDisplayLocalStream()