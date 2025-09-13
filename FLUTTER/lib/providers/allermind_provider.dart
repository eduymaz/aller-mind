import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import '../models/allermind_response.dart';
import '../models/user_settings.dart';
import '../services/allermind_api_service.dart';

class AllerMindProvider extends ChangeNotifier {
  AllerMindResponse? _currentResponse;
  UserSettings? _userSettings;
  Position? _currentPosition;
  bool _isLoading = false;
  String? _errorMessage;

  // Getters
  AllerMindResponse? get currentResponse => _currentResponse;
  UserSettings? get userSettings => _userSettings;
  Position? get currentPosition => _currentPosition;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  /// Konum iznini kontrol et ve al
  Future<bool> requestLocationPermission() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      _errorMessage = 'Konum servisleri aktif değil';
      notifyListeners();
      return false;
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        _errorMessage = 'Konum izni reddedildi';
        notifyListeners();
        return false;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      _errorMessage = 'Konum izni kalıcı olarak reddedildi. Ayarlardan izin veriniz.';
      notifyListeners();
      return false;
    }

    return true;
  }

  /// Mevcut konumu al
  Future<Position?> getCurrentLocation() async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      bool hasPermission = await requestLocationPermission();
      if (!hasPermission) {
        _isLoading = false;
        notifyListeners();
        return null;
      }

      _currentPosition = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      
      _isLoading = false;
      notifyListeners();
      return _currentPosition;
    } catch (e) {
      _errorMessage = 'Konum alınırken hata oluştu: $e';
      _isLoading = false;
      notifyListeners();
      return null;
    }
  }

  /// Kullanıcı ayarlarını güncelle
  void updateUserSettings(UserSettings settings) {
    _userSettings = settings;
    notifyListeners();
  }

  /// Tahmin isteği gönder
  Future<bool> getPrediction() async {
    if (_currentPosition == null || _userSettings == null) {
      _errorMessage = 'Konum veya kullanıcı ayarları eksik';
      notifyListeners();
      return false;
    }

    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      _currentResponse = await AllerMindApiService.getPrediction(
        lat: _currentPosition!.latitude.toString(),
        lon: _currentPosition!.longitude.toString(),
        userSettings: _userSettings!,
      );

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _errorMessage = 'Tahmin alınırken hata oluştu: $e';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Hata mesajını temizle
  void clearError() {
    _errorMessage = null;
    notifyListeners();
  }

  /// Tüm verileri sıfırla
  void reset() {
    _currentResponse = null;
    _userSettings = null;
    _currentPosition = null;
    _isLoading = false;
    _errorMessage = null;
    notifyListeners();
  }
}