import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/allermind_provider.dart';
import 'result_screen.dart';

class LoadingScreen extends StatefulWidget {
  const LoadingScreen({super.key});

  @override
  State<LoadingScreen> createState() => _LoadingScreenState();
}

class _LoadingScreenState extends State<LoadingScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);

    _scaleAnimation = Tween<double>(
      begin: 0.8,
      end: 1.2,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));

    // Otomatik olarak tahmin sürecini başlat
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _startPredictionProcess();
    });
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _startPredictionProcess() async {
    final provider = Provider.of<AllerMindProvider>(context, listen: false);

    try {
      // 1. Konum al
      final position = await provider.getCurrentLocation();
      if (position == null) {
        _showErrorAndReturn('Konum alınamadı');
        return;
      }

      // Kısa bir bekleme (UX için)
      await Future.delayed(const Duration(seconds: 1));

      // 2. Tahmin al
      final success = await provider.getPrediction();
      if (!success) {
        _showErrorAndReturn('Tahmin alınamadı');
        return;
      }

      // 3. Sonuç sayfasına git
      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (context) => const ResultScreen(),
          ),
        );
      }
    } catch (e) {
      _showErrorAndReturn('Bir hata oluştu: $e');
    }
  }

  void _showErrorAndReturn(String error) {
    if (mounted) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Hata'),
          content: Text(error),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(); // Dialog'u kapat
                Navigator.of(context).pop(); // Loading screen'i kapat
              },
              child: const Text('Tamam'),
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.teal.shade50,
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            // Animasyonlu logo/ikon
            AnimatedBuilder(
              animation: _scaleAnimation,
              builder: (context, child) {
                return Transform.scale(
                  scale: _scaleAnimation.value,
                  child: Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      color: Colors.teal,
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.teal.withOpacity(0.3),
                          blurRadius: 20,
                          spreadRadius: 5,
                        ),
                      ],
                    ),
                    child: const Icon(
                      Icons.air,
                      size: 60,
                      color: Colors.white,
                    ),
                  ),
                );
              },
            ),
            
            const SizedBox(height: 40),
            
            // Başlık
            const Text(
              'Allerji Riski Hesaplanıyor',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
            
            const SizedBox(height: 16),
            
            // Alt başlık
            const Text(
              'Konumunuz alınıyor ve çevresel veriler analiz ediliyor...',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey,
              ),
            ),
            
            const SizedBox(height: 40),
            
            // Loading indicator
            const CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Colors.teal),
              strokeWidth: 3,
            ),
            
            const SizedBox(height: 40),
            
            // Süreç adımları
            Consumer<AllerMindProvider>(
              builder: (context, provider, child) {
                return Column(
                  children: [
                    _buildProcessStep(
                      'Konum Alınıyor',
                      provider.currentPosition != null,
                      provider.isLoading,
                    ),
                    _buildProcessStep(
                      'Çevresel Veriler Toplanıyor',
                      provider.currentPosition != null,
                      provider.isLoading && provider.currentPosition != null,
                    ),
                    _buildProcessStep(
                      'Allerji Riski Hesaplanıyor',
                      provider.currentResponse != null,
                      provider.isLoading && provider.currentPosition != null,
                    ),
                  ],
                );
              },
            ),
            
            const Spacer(),
            
            // İptal butonu
            Padding(
              padding: const EdgeInsets.all(24.0),
              child: TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: const Text(
                  'İptal Et',
                  style: TextStyle(
                    color: Colors.grey,
                    fontSize: 16,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProcessStep(String title, bool isCompleted, bool isActive) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            isCompleted ? Icons.check_circle : (isActive ? Icons.radio_button_unchecked : Icons.circle_outlined),
            color: isCompleted ? Colors.green : (isActive ? Colors.teal : Colors.grey),
            size: 20,
          ),
          const SizedBox(width: 12),
          Text(
            title,
            style: TextStyle(
              color: isCompleted ? Colors.green : (isActive ? Colors.teal : Colors.grey),
              fontWeight: isActive ? FontWeight.w500 : FontWeight.normal,
            ),
          ),
        ],
      ),
    );
  }
}