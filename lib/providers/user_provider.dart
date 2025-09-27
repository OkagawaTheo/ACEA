import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class User {
  final String id;
  final String name;
  final String cpf;
  final String phone;
  final String email;
  final String specialty; // Apenas professores
  final String birthDate; // Apenas alunos
  final String address; // Apenas alunos
  final String role; // 'teacher', 'president', 'student'
  final List<int> cursos; // IDs dos cursos
  final List<int> atividades; // IDs das atividades

  User({
    required this.id,
    required this.name,
    required this.cpf,
    required this.phone,
    required this.email,
    required this.specialty,
    required this.birthDate,
    required this.address,
    required this.role,
    required this.cursos,
    required this.atividades,
  });

  factory User.fromJson(Map<String, dynamic> json, String role) {
    List<int> parseIds(dynamic value) {
      if (value == null) return [];
      if (value is List) {
        return value.map<int>((e) => e as int).toList();
      }
      return [];
    }

    return User(
      id: json['id'].toString(),
      name: json['nome'] ?? '',
      cpf: json['cpf'] ?? '',
      phone: json['telefone'] ?? '',
      email: json['email'] ?? '',
      specialty: json['especialidade'] ?? '',
      birthDate: json['data_nascimento'] ?? '',
      address: json['endereco'] ?? '',
      role: role,
      cursos: parseIds(json['cursos']),
      atividades: parseIds(json['atividades']),
    );
  }
}

class UserProvider with ChangeNotifier {
  final List<User> _users = [];
  final String baseUrl = 'http://127.0.0.1:8000/api'; // Altere se necessário

  List<User> get users => _users;

  Future<void> fetchUsers() async {
    _users.clear();

    // Alunos
    var response = await http.get(Uri.parse('$baseUrl/alunos/'));
    if (response.statusCode == 200) {
      List data = jsonDecode(response.body);
      for (var item in data) {
        _users.add(User.fromJson(item, 'student'));
      }
    }

    // Professores
    response = await http.get(Uri.parse('$baseUrl/professores/'));
    if (response.statusCode == 200) {
      List data = jsonDecode(response.body);
      for (var item in data) {
        _users.add(User.fromJson(item, 'teacher'));
      }
    }

    // Presidentes
    response = await http.get(Uri.parse('$baseUrl/presidentes/'));
    if (response.statusCode == 200) {
      List data = jsonDecode(response.body);
      for (var item in data) {
        _users.add(User.fromJson(item, 'president'));
      }
    }

    notifyListeners();
  }

  Future<void> createUser({
    required String name,
    required String cpf,
    required String phone,
    required String email,
    required String specialty,
    required String birthDate,
    required String address,
    required String role,
    List<int>? cursos,
    List<int>? atividades,
  }) async {
    String url;
    Map<String, dynamic> payload = {'nome': name, 'email': email};

    switch (role) {
      case 'teacher':
        url = '$baseUrl/professores/';
        payload.addAll({
          'cpf': cpf,
          'telefone': phone,
          'especialidade': specialty,
          'cursos_ministrados': [],
          'atividades_ministradas': [],
        });
        break;
      case 'president':
        url = '$baseUrl/presidentes/';
        payload.addAll({'cpf': cpf, 'telefone': phone});
        break;
      case 'student':
        url = '$baseUrl/alunos/';
        payload.addAll({
          'telefone': phone,
          'data_nascimento': birthDate,
          'endereco': address,
          'cursos': cursos ?? [],
          'atividades': atividades ?? [],
        });
        break;
      default:
        throw Exception('Role inválida');
    }

    final response = await http.post(
      Uri.parse(url),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201) {
      await fetchUsers(); // Atualiza lista
    } else {
      throw Exception(
          'Erro ao criar usuário: ${response.statusCode} ${response.body}');
    }
  }
}
