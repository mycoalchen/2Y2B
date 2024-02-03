//
//  AudioLoader.swift
//  2Y2B
//
//  Created by Michael Chen on 2/2/24.
//

import Foundation
import FirebaseCore
import FirebaseFirestore
import FirebaseStorage
import AVFoundation

class FirebaseHelper {
    private var db: Firestore
    private var audioRef: StorageReference
    private var audioPlayer: AVAudioPlayer
    
    init() {
        FirebaseApp.configure()
        db = Firestore.firestore()
        let storage = Storage.storage()
        let storageRef = storage.reference()
        audioRef = storageRef.child("audio")
        print("AudioLoader initialized")
        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Failed to set audio session category: \(error)")
        }
        audioPlayer = AVAudioPlayer()
    }
    
    public func playAudioFromName(filename: String) {
        let firebaseURL = audioRef.child(filename)
        let tempDirectoryURL = FileManager.default.temporaryDirectory
        let localURL = tempDirectoryURL.appendingPathComponent(filename)
        _ = firebaseURL.write(toFile: localURL) {
            url, error in
            if let error = error {
                print("Error downloading audio file: \(error)")
            } else {
                print("Audio file downloaded to \(localURL)")
                do {
                    print("Playing audio file")
                    self.audioPlayer = try AVAudioPlayer(contentsOf: localURL)
                    self.audioPlayer.play()
                } catch {
                    print("Failed to initialize/play audio: \(error)")
                }
            }
        }
    }
    public func playPlayer() {
        self.audioPlayer.play()
    }
    public func pausePlayer() {
        self.audioPlayer.pause()
    }
    var currentTime: TimeInterval {
        return audioPlayer.currentTime
    }
    var duration: TimeInterval {
        return audioPlayer.duration
    }
    func seek(to time: TimeInterval) {
        audioPlayer.currentTime = time
    }
}

/*
 db.collection("users").document(name).getDocument { (document, error) in
     if let document = document {
         print("found user \(name)")
         print(document.get("audio"))
         
     } else {
         print("didn't find mycoal")
     }
 }
 */
