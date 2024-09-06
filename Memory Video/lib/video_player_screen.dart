import 'dart:io';

import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class VideoView extends StatefulWidget {
  @override
  _VideoViewState createState() => _VideoViewState();
}

class _VideoViewState extends State<VideoView> {
  late VideoPlayerController
      _controller; // Late initialization for the controller

  @override
  void initState() {
    super.initState();

    // Initialize the VideoPlayerController with a network video URL
    _controller = VideoPlayerController.file(
        File("C:\\Users\\SAHAN\\Desktop\\test_\\UI\\combined_video.mp4"));

    // Initialize the controller and update the state once initialized
    _controller.initialize().then((_) {
      setState(() {}); // Refresh the UI once video is initialized
      _controller.play(); // Start playing the video
    });
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: _controller.value.isInitialized
          ? AspectRatio(
              aspectRatio: _controller
                  .value.aspectRatio, // Maintain the aspect ratio of the video
              child: VideoPlayer(_controller),
            )
          : CircularProgressIndicator(), // Show loading indicator while video initializes
    );
  }

  @override
  void dispose() {
    _controller
        .dispose(); // Dispose of the VideoPlayerController to free resources
    super.dispose();
  }
}
