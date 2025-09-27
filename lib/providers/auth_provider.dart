import 'package:flutter/material.dart';

class AuthProvider with ChangeNotifier {
  String? _userRole; // 'admin', 'teacher', 'president'
  bool _isAuthenticated = false;

  bool get isAuthenticated => _isAuthenticated;
  String? get userRole => _userRole;

  void login(String username, String password) {
    // Login simulado
    if (username == 'admin' && password == 'admin') {
      _userRole = 'admin';
      _isAuthenticated = true;
    } else if (username == 'teacher' && password == 'teacher') {
      _userRole = 'teacher';
      _isAuthenticated = true;
    } else if (username == 'president' && password == 'president') {
      _userRole = 'president';
      _isAuthenticated = true;
    } else {
      _userRole = null;
      _isAuthenticated = false;
    }
    notifyListeners();
  }

  void logout() {
    _userRole = null;
    _isAuthenticated = false;
    notifyListeners();
  }
}
