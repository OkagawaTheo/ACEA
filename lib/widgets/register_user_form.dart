import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../providers/user_provider.dart';

class RegisterUserForm extends StatefulWidget {
  final String role;

  const RegisterUserForm({super.key, required this.role});

  @override
  _RegisterUserFormState createState() => _RegisterUserFormState();
}

class _RegisterUserFormState extends State<RegisterUserForm> {
  final _nameController = TextEditingController();
  final _cpfController = TextEditingController();
  final _phoneController = TextEditingController();
  final _emailController = TextEditingController();
  final _specialtyController = TextEditingController();
  final _birthDateController = TextEditingController();
  final _addressController = TextEditingController();

  final _birthDateFormatter =
      TextInputFormatter.withFunction((oldValue, newValue) {
    // Apenas garante que só números e "/" serão digitados
    String filtered = newValue.text.replaceAll(RegExp(r'[^0-9/]'), '');
    return TextEditingValue(text: filtered, selection: newValue.selection);
  });

  void _register() async {
    final userProvider = Provider.of<UserProvider>(context, listen: false);

    String birthDateFormatted = '';
    if (widget.role == 'student') {
      try {
        DateTime parsedDate =
            DateFormat('dd/MM/yyyy').parse(_birthDateController.text);
        birthDateFormatted = DateFormat('yyyy-MM-dd').format(parsedDate);
      } catch (_) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Data inválida. Use DD/MM/YYYY')),
        );
        return;
      }
    }

    try {
      await userProvider.createUser(
        name: _nameController.text,
        cpf: _cpfController.text,
        phone: _phoneController.text,
        email: _emailController.text,
        specialty: _specialtyController.text,
        birthDate: birthDateFormatted,
        address: _addressController.text,
        role: widget.role,
      );

      _nameController.clear();
      _cpfController.clear();
      _phoneController.clear();
      _emailController.clear();
      _specialtyController.clear();
      _birthDateController.clear();
      _addressController.clear();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
              content:
                  Text('${widget.role.capitalize()} cadastrado com sucesso!')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context)
            .showSnackBar(SnackBar(content: Text(e.toString())));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(
          controller: _nameController,
          decoration: const InputDecoration(labelText: 'Nome'),
        ),
        if (widget.role == 'teacher' || widget.role == 'president')
          TextField(
            controller: _cpfController,
            decoration: const InputDecoration(labelText: 'CPF'),
            keyboardType: TextInputType.number,
          ),
        if (widget.role == 'teacher' ||
            widget.role == 'president' ||
            widget.role == 'student')
          TextField(
            controller: _phoneController,
            decoration: const InputDecoration(labelText: 'Telefone'),
            keyboardType: TextInputType.number,
            inputFormatters: [FilteringTextInputFormatter.digitsOnly],
          ),
        TextField(
          controller: _emailController,
          decoration: const InputDecoration(labelText: 'Email'),
          keyboardType: TextInputType.emailAddress,
        ),
        if (widget.role == 'teacher')
          TextField(
            controller: _specialtyController,
            decoration: const InputDecoration(labelText: 'Especialidade'),
          ),
        if (widget.role == 'student') ...[
          TextField(
            controller: _birthDateController,
            decoration: const InputDecoration(
                labelText: 'Data de Nascimento (DD/MM/YYYY)'),
            keyboardType: TextInputType.datetime,
            inputFormatters: [_birthDateFormatter],
          ),
          TextField(
            controller: _addressController,
            decoration: const InputDecoration(labelText: 'Endereço'),
          ),
        ],
        const SizedBox(height: 10),
        ElevatedButton(
          onPressed: _register,
          child: Text('Cadastrar ${widget.role.capitalize()}'),
        ),
      ],
    );
  }
}

extension StringExtension on String {
  String capitalize() => "${this[0].toUpperCase()}${substring(1)}";
}
