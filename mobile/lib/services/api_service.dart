
import 'dart:convert';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://192.168.1.7:8000/api';

  static const FlutterSecureStorage _storage =
  FlutterSecureStorage();

  static Future<String> login(
      String username,
      String password,
      ) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Login failed. Check your credentials.');
    }

    final data = jsonDecode(response.body);
    final token = data['token'] as String;

    await _storage.write(
      key: 'auth_token',
      value: token,
    );

    return token;
  }

  static Future<Map<String, String>> _headers() async {
    final token = await _storage.read(key: 'auth_token');

    if (token == null) {
      throw Exception('Please log in first.');
    }

    return {
      'Authorization': 'Token $token',
      'Content-Type': 'application/json',
    };
  }

  static Future<List<dynamic>> getJobs() async {
    final response = await http.get(
      Uri.parse('$baseUrl/jobs/'),
      headers: await _headers(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load jobs.');
    }

    return jsonDecode(response.body) as List<dynamic>;
  }

  static Future<Map<String, dynamic>> getJob(int id) async {
    final response = await http.get(
      Uri.parse('$baseUrl/jobs/$id/'),
      headers: await _headers(),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to load job details.');
    }

    return jsonDecode(response.body)
    as Map<String, dynamic>;
  }

  static Future<Map<String, dynamic>> updateJobStatus(
      int id,
      String newStatus,
      ) async {
    final response = await http.patch(
      Uri.parse('$baseUrl/jobs/$id/status/'),
      headers: await _headers(),
      body: jsonEncode({'status': newStatus}),
    );

    if (response.statusCode != 200) {
      throw Exception('Status update failed: ${response.body}');
    }

    return jsonDecode(response.body)
    as Map<String, dynamic>;
  }

  static Future<void> logout() async {
    await _storage.delete(key: 'auth_token');
  }
}
