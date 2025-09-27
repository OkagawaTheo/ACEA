// lib/main.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';
import 'providers/user_provider.dart';
import 'screens/login_screen.dart';
import 'screens/admin_dashboard.dart';
import 'screens/teacher_dashboard.dart';
import 'screens/president_dashboard.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => UserProvider()),
      ],
      child: MaterialApp(
        title: 'NGO Management App',
        theme: ThemeData(primarySwatch: Colors.blue),
        home: const LoginScreen(),
        routes: {
          '/admin': (context) => const AdminDashboard(),
          '/teacher': (context) => const TeacherDashboard(),
          '/president': (context) => const PresidentDashboard(),
        },
      ),
    );
  }
}
