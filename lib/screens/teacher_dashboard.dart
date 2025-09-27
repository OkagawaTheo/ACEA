import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/user_provider.dart';
import '../providers/auth_provider.dart';
import '../widgets/register_user_form.dart';

class TeacherDashboard extends StatelessWidget {
  const TeacherDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    final authProvider = Provider.of<AuthProvider>(context);

    final students =
        userProvider.users.where((u) => u.role == 'student').toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Painel do Professor'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              authProvider.logout();
              Navigator.pushReplacementNamed(context, '/');
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Cadastrar Alunos',
                style: Theme.of(context).textTheme.headlineSmall),
            const RegisterUserForm(role: 'student'),
            const SizedBox(height: 20),
            const Text('Alunos Cadastrados:'),
            Expanded(
              child: ListView.builder(
                itemCount: students.length,
                itemBuilder: (context, index) {
                  final student = students[index];
                  return ListTile(
                    title: Text(student.name),
                    subtitle: Text(
                      'Email: ${student.email}\nTelefone: ${student.phone}\nData de Nascimento: ${student.birthDate}\nEndereço: ${student.address}',
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
