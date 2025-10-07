import 'package:flutter/material.dart';

class AppColors {
  // Ana renk paleti
  static const Color white = Color(0xFFFFFFFF);
  static const Color cream = Color(0xFFF5F5DC);
  static const Color lightGreen = Color(0xFF1F3905);
  static const Color mediumGreen = Color(0xFF364D1C);
  static const Color darkGreen = Color(0xFF4C642C);
  static const Color darkerGreen = Color(0xFF2B4B04);
  static const Color deepGreen = Color(0xFF142701);
  
  // Gradient kombinasyonları
  static const List<Color> primaryGradient = [lightGreen, mediumGreen];
  static const List<Color> secondaryGradient = [mediumGreen, darkGreen];
  static const List<Color> darkGradient = [darkerGreen, deepGreen];
  static const List<Color> lightGradient = [cream, white];
  
  // Metin renkleri
  static const Color primaryText = deepGreen;
  static const Color secondaryText = darkerGreen;
  static const Color lightText = white;
  static const Color mutedText = Color(0xFF6B7A5A);
  
  // Notification ve bilgilendirme renkleri
  static const Color successBg = Color(0xFFE8F5E8);
  static const Color successText = Color(0xFF2E7D32);
  static const Color successBorder = Color(0xFF4CAF50);
  
  static const Color errorBg = Color(0xFFFFEBEE);
  static const Color errorText = Color(0xFFC62828);
  static const Color errorBorder = Color(0xFFE57373);
  
  static const Color warningBg = Color(0xFFFFF3E0);
  static const Color warningText = Color(0xFFE65100);
  static const Color warningBorder = Color(0xFFFFB74D);
  
  static const Color infoBg = Color(0xFFE3F2FD);
  static const Color infoText = Color(0xFF1976D2);
  static const Color infoBorder = Color(0xFF64B5F6);
  
  // Buton renkleri
  static const Color primaryButton = darkGreen;
  static const Color secondaryButton = cream;
  static const Color buttonText = white;
  static const Color buttonTextDark = deepGreen;
  
  // Card ve surface renkleri
  static const Color cardBackground = white;
  static const Color surfaceLight = cream;
  static const Color surfaceDark = lightGreen;
  
  // Border ve divider renkleri
  static const Color borderLight = Color(0xFFE0E0E0);
  static const Color borderMedium = Color(0xFF9E9E9E);
  static const Color borderDark = mediumGreen;
  
  // Shadow renkleri
  static Color shadowLight = deepGreen.withOpacity(0.1);
  static Color shadowMedium = deepGreen.withOpacity(0.2);
  static Color shadowDark = deepGreen.withOpacity(0.3);
}