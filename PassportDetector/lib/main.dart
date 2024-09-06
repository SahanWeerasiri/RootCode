import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Passport Detection',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PassportDetectionScreen(),
    );
  }
}

class PassportDetectionScreen extends StatefulWidget {
  @override
  _PassportDetectionScreenState createState() =>
      _PassportDetectionScreenState();
}

class _PassportDetectionScreenState extends State<PassportDetectionScreen> {
  File? _image;
  Map<String, dynamic>? _passportData;
  String? _extractedFacePath;

  final ImagePicker _picker = ImagePicker();

  Future<void> _pickImage() async {
    final XFile? pickedFile =
        await _picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
      _sendImageToServer(_image!.path);
    }
  }

  Future<void> _sendImageToServer(String imagePath) async {
    final url = Uri.parse(
        'http://127.0.0.1:5000/detect-passport'); // Update with your server address if different
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'image': imagePath}),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> responseData = jsonDecode(response.body);
        setState(() {
          _passportData = responseData['passport_info'];
          _extractedFacePath = responseData['face_image'];
        });
      } else {
        print('Server error: ${response.body}');
      }
    } catch (e) {
      print('Error: $e');
    }
  }

  Widget _buildPassportDataView() {
    if (_passportData == null) return Container();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: _passportData!.entries.map((entry) {
        return Text('${entry.key}: ${entry.value}');
      }).toList(),
    );
  }

  Widget _buildExtractedFaceView() {
    if (_extractedFacePath == null) return Container();

    return Column(
      children: [
        Image.file(File(_extractedFacePath!)),
        SizedBox(height: 10),
        Text('Extracted Face'),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Passport Detection'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _pickImage,
              child: Text('Select Passport Image'),
            ),
            SizedBox(height: 20),
            _buildPassportDataView(),
            SizedBox(height: 20),
            _buildExtractedFaceView(),
          ],
        ),
      ),
    );
  }
}
