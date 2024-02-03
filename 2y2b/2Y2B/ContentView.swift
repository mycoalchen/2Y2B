//
//  ContentView.swift
//  2Y2B
//
//  Created by Michael Chen on 2/2/24.
//

import SwiftUI

let backgroundColor : Color = Color(red:30/255, green:11/255, blue:4/255)
let offWhite1 : Color = Color(red:246/255, green:241/255, blue:237/255)
let offWhite2 : Color = Color(red: 196/255, green: 186/255, blue: 182/255)

struct ContentView: View {
    @State private var name: String = ""
    @State private var nameWidth: CGFloat = 0
    @State private var signedIn = false
    @State private var audioLoaded = false
    @State private var audioPlaying = true
    @FocusState private var nameFocused: Bool
    
    private var firebaseHelper: FirebaseHelper = FirebaseHelper()
    
    var body: some View {
        VStack(spacing: 0.0) {
            Text("2Y2B")
                .foregroundStyle(offWhite1)
                .font(.custom("EBGaramond-Regular", size: 46))
            HStack(spacing: 0) {
                if signedIn {
                    Text("your blend.")
                        .foregroundStyle(offWhite2)
                        .font(.custom("EBGaramond-Regular", size: 18))
                } else {
                    Text("[")
                        .foregroundColor(offWhite2)
                        .font(.custom("EBGaramond-Regular", size: 18))
                    TextField("", text: $name, prompt: Text("your name").foregroundColor(offWhite2), axis: .horizontal)
                        .autocorrectionDisabled()
                        .accentColor(offWhite2)
                        .foregroundColor(offWhite2)
                        .font(.custom("EBGaramond-Regular", size: 18))
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 0)
                        .fixedSize()
                        .frame(idealWidth: 0)
                        .focused($nameFocused)
                        .onSubmit {
                            print("Name submitted: " + name)
                            checkName()
                        }
                    Text("]")
                        .foregroundColor(offWhite2)
                        .font(.custom("EBGaramond-Regular", size: 18))
                }
            }
            .frame(minWidth: 20)
            if audioLoaded {
                HStack(spacing: 0) {
                    Button(action: {
                        if audioPlaying {
                            print("Set to pause")
                            firebaseHelper.pausePlayer()
                        } else {
                            print("Set to play")
                            firebaseHelper.playPlayer()
                        }
                        audioPlaying = !audioPlaying
                    }) {
                        if audioPlaying {
                            Image ("Pause")
                        } else {
                            Image("Play")
                        }
                    }
                    .frame(width: 30, height: 30)
                    .background(Color.clear)
                }
                .padding(.vertical, 15)
            }
        }
        .padding(0.0)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(backgroundColor)
    }
    
    func checkName() {
        firebaseHelper.playAudioFromName(filename: "Tunak Tunak tun.mp3")
        signedIn = true
        audioLoaded = true
    }
}

#Preview {
    ContentView()
}
