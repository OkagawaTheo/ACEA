import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';

class PresidentDashboard extends StatelessWidget {
  const PresidentDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    final authProvider = Provider.of<AuthProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard Presidente'),
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
            Text('Acesso a Pagamentos e Documentos',
                style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 10),
            const Text(
                'Funcionalidades de cadastro não disponíveis para Presidente.'),
          ],
        ),
      ),
    );
  }
}
