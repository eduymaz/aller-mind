/// Application configuration
/// Supports both production (Docker/Cloud) and local development modes
class AppConfig {
  // Singleton pattern
  static final AppConfig _instance = AppConfig._internal();
  factory AppConfig() => _instance;
  AppConfig._internal();

  // Service URLs with fallback to production (empty string for Docker/nginx proxy)
  late final String modelServiceUrl;
  late final String userPreferenceServiceUrl;

  /// Initialize configuration from environment variables or dart-define
  /// 
  /// For production (Docker): URLs default to empty string (nginx proxy handles routing)
  /// For local development: Pass URLs via --dart-define
  /// 
  /// Example local development:
  /// ```
  /// flutter run --dart-define=MODEL_SERVICE_URL=http://localhost:8484 \
  ///             --dart-define=USER_PREFERENCE_SERVICE_URL=http://localhost:9191
  /// ```
  void initialize() {
    // Read from --dart-define or default to production values (empty for nginx proxy)
    modelServiceUrl = const String.fromEnvironment(
      'MODEL_SERVICE_URL',
      defaultValue: '', // Production: nginx proxy handles this
    );
    
    userPreferenceServiceUrl = const String.fromEnvironment(
      'USER_PREFERENCE_SERVICE_URL',
      defaultValue: '', // Production: nginx proxy handles this
    );

    // Debug logging
    print('🔧 AppConfig initialized:');
    print('   Model Service URL: ${modelServiceUrl.isEmpty ? "[NGINX PROXY]" : modelServiceUrl}');
    print('   User Preference Service URL: ${userPreferenceServiceUrl.isEmpty ? "[NGINX PROXY]" : userPreferenceServiceUrl}');
  }

  /// Check if running in local development mode
  bool get isLocalDevelopment => modelServiceUrl.isNotEmpty || userPreferenceServiceUrl.isNotEmpty;

  /// Check if running in production mode (Docker/Cloud)
  bool get isProduction => !isLocalDevelopment;

  /// Get the mode as a string for debugging
  String get mode => isProduction ? 'PRODUCTION (Docker/Cloud)' : 'LOCAL DEVELOPMENT';
}
