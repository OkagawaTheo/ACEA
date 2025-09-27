import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/user_provider.dart';
import '../providers/auth_provider.dart';
import '../widgets/register_user_form.dart';

class AdminDashboard extends StatelessWidget {
  const AdminDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    final userProvider = Provider.of<UserProvider>(context);
    final authProvider = Provider.of<AuthProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Painel do Administrador'),
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
            Text(
              'Cadastrar Professores e Presidentes',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 10),
            const Text('Cadastrar Professor'),
            const RegisterUserForm(role: 'teacher'),
            const SizedBox(height: 20),
            const Text('Cadastrar Presidente'),
            const RegisterUserForm(role: 'president'),
            const SizedBox(height: 20),
            const Text('Usuários Cadastrados:'),
            Expanded(
              child: ListView.builder(
                itemCount: userProvider.users.length,
                itemBuilder: (context, index) {
                  final user = userProvider.users[index];
                  return ListTile(
                    title: Text(user.name),
                    subtitle: Text(
                      user.role == 'teacher'
                          ? 'Email: ${user.email}\nCPF: ${user.cpf}, Telefone: ${user.phone}, Especialidade: ${user.specialty}'
                          : user.role == 'president'
                              ? 'Email: ${user.email}\nCPF: ${user.cpf}, Telefone: ${user.phone}'
                              : 'Email: ${user.email}\nTelefone: ${user.phone}\nData de Nascimento: ${user.birthDate}\nEndereço: ${user.address}',
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
