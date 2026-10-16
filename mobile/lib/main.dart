import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'package:flutter/material.dart';
import 'services/api_service.dart';


final FirebaseAnalytics analytics = FirebaseAnalytics.instance;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const EzyHelpersApp());
}

class EzyHelpersApp extends StatelessWidget {
  const EzyHelpersApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'EzyHelpers',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF176B55),
        ),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  bool _loading = false;
  bool _obscurePassword = true;
  String? _errorMessage;

  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _loading = true;
      _errorMessage = null;
    });

    try {
      await ApiService.login(
        _usernameController.text.trim(),
        _passwordController.text,
      );
      await analytics.logEvent(
          name: 'login_success'
      );

      if (!mounted) return;

      Navigator.of(context).pushReplacement(
        MaterialPageRoute(
          builder: (_) => const JobsScreen(),
        ),
      );
    } catch (error) {
      if (!mounted) return;

      setState(() {
        _errorMessage = error.toString().replaceFirst('Exception: ', '');
      });
    } finally {
      if (mounted) {
        setState(() => _loading = false);
      }
    }
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7F6),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 420),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Icon(
                      Icons.handyman_rounded,
                      size: 72,
                      color: Color(0xFF176B55),
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'EzyHelpers',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF176B55),
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Sign in to manage your assigned jobs',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.black54),
                    ),
                    const SizedBox(height: 36),
                    TextFormField(
                      controller: _usernameController,
                      textInputAction: TextInputAction.next,
                      decoration: const InputDecoration(
                        labelText: 'Username',
                        prefixIcon: Icon(Icons.person_outline),
                        border: OutlineInputBorder(),
                        filled: true,
                        fillColor: Colors.white,
                      ),
                      validator: (value) {
                        if (value == null || value.trim().isEmpty) {
                          return 'Enter your username';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 18),
                    TextFormField(
                      controller: _passwordController,
                      obscureText: _obscurePassword,
                      onFieldSubmitted: (_) => _login(),
                      decoration: InputDecoration(
                        labelText: 'Password',
                        prefixIcon: const Icon(Icons.lock_outline),
                        border: const OutlineInputBorder(),
                        filled: true,
                        fillColor: Colors.white,
                        suffixIcon: IconButton(
                          onPressed: () {
                            setState(() {
                              _obscurePassword = !_obscurePassword;
                            });
                          },
                          icon: Icon(
                            _obscurePassword
                                ? Icons.visibility_outlined
                                : Icons.visibility_off_outlined,
                          ),
                        ),
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Enter your password';
                        }
                        return null;
                      },
                    ),
                    if (_errorMessage != null) ...[
                      const SizedBox(height: 16),
                      Text(
                        _errorMessage!,
                        style: const TextStyle(color: Colors.red),
                      ),
                    ],
                    const SizedBox(height: 24),
                    SizedBox(
                      height: 52,
                      child: FilledButton(
                        onPressed: _loading ? null : _login,
                        child: _loading
                            ? const SizedBox(
                          height: 22,
                          width: 22,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                            : const Text(
                          'Sign In',
                          style: TextStyle(fontSize: 16),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class JobsScreen extends StatefulWidget {
  const JobsScreen({super.key});

  @override
  State<JobsScreen> createState() => _JobsScreenState();
}

class _JobsScreenState extends State<JobsScreen> {
  late Future<List<dynamic>> _jobsFuture;

  @override
  void initState() {
    super.initState();
    _loadJobs();
  }

  void _loadJobs() {
    _jobsFuture = ApiService.getJobs();
  }

  Future<void> _logout() async {
    await ApiService.logout();

    if (!mounted) return;

    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const LoginScreen()),
          (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Assigned Jobs'),
        backgroundColor: const Color(0xFF176B55),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            onPressed: _logout,
            tooltip: 'Sign out',
            icon: const Icon(Icons.logout),
          ),
        ],
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _jobsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text('Unable to load jobs.'),
                    const SizedBox(height: 12),
                    FilledButton(
                      onPressed: () {
                        setState(_loadJobs);
                      },
                      child: const Text('Try again'),
                    ),
                  ],
                ),
              ),
            );
          }

          final jobs = snapshot.data ?? [];

          if (jobs.isEmpty) {
            return const Center(child: Text('No jobs assigned to you.'));
          }

          return RefreshIndicator(
            onRefresh: () async {
              setState(_loadJobs);
              await _jobsFuture;
            },
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: jobs.length,
              itemBuilder: (context, index) {
                final job = jobs[index] as Map<String, dynamic>;
                final status = job['status']?.toString() ?? 'UNKNOWN';

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: const CircleAvatar(
                      backgroundColor: Color(0xFFE0F2E9),
                      child: Icon(
                        Icons.work_outline,
                        color: Color(0xFF176B55),
                      ),
                    ),
                    title: Text(
                      job['title']?.toString() ?? 'Untitled job',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Padding(
                      padding: const EdgeInsets.only(top: 8),
                      child: Text('Status: ${status.replaceAll('_', ' ')}'),
                    ),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () async {
                      await analytics.logEvent(
                        name: 'job_viewed',
                        parameters: {
                          'job_id': job['id'].toString(),
                        },
                      );

                      if (!context.mounted) return;

                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => JobDetailScreen(
                            jobId: job['id'] as int,
                          ),
                        ),
                      );
                      },
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class JobDetailScreen extends StatefulWidget {
  final int jobId;

  const JobDetailScreen({super.key, required this.jobId});

  @override
  State<JobDetailScreen> createState() => _JobDetailScreenState();
}

class _JobDetailScreenState extends State<JobDetailScreen> {
  late Future<Map<String, dynamic>> _jobFuture;
  bool _updating = false;

  @override
  void initState() {
    super.initState();
    _jobFuture = ApiService.getJob(widget.jobId);
  }

  Future<void> _updateStatus(String status) async {
    setState(() => _updating = true);

    try {
      await ApiService.updateJobStatus(widget.jobId, status);
      await analytics.logEvent(
        name: 'job_status_updated',
        parameters: {
          'job_id': widget.jobId.toString(),
          'new_status': status,
        },
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Job status updated to ${status.replaceAll('_', ' ')}')),
      );

      setState(() {
        _jobFuture = ApiService.getJob(widget.jobId);
      });
    } catch (error) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            error.toString().replaceFirst('Exception: ', ''),
          ),
        ),
      );
    } finally {
      if (mounted) {
        setState(() => _updating = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Job Details')),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _jobFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError || !snapshot.hasData) {
            return const Center(child: Text('Unable to load job details.'));
          }

          final job = snapshot.data!;
          final status = job['status']?.toString() ?? 'UNKNOWN';
          final description = job['description']?.toString() ?? '';

          return ListView(
            padding: const EdgeInsets.all(20),
            children: [
              Text(
                job['title']?.toString() ?? 'Job',
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              const SizedBox(height: 16),
              Chip(label: Text(status.replaceAll('_', ' '))),
              const SizedBox(height: 24),
              const Text(
                'Description',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
              const SizedBox(height: 8),
              Text(description.isEmpty ? 'No description provided.' : description),
              const SizedBox(height: 32),
              if (status == 'ASSIGNED')
                FilledButton.icon(
                  onPressed: _updating
                      ? null
                      : () => _updateStatus('IN_PROGRESS'),
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Start Job'),
                ),
              if (status == 'IN_PROGRESS')
                FilledButton.icon(
                  onPressed: _updating
                      ? null
                      : () => _updateStatus('COMPLETED'),
                  icon: const Icon(Icons.check_circle_outline),
                  label: const Text('Complete Job'),
                ),
              if (status == 'COMPLETED')
                const ListTile(
                  leading: Icon(Icons.check_circle, color: Colors.green),
                  title: Text('This job is completed'),
                ),
              if (_updating)
                const Padding(
                  padding: EdgeInsets.all(16),
                  child: Center(child: CircularProgressIndicator()),
                ),
            ],
          );
        },
      ),
    );
  }
}
