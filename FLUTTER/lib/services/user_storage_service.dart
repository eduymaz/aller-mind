import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_profile_response.dart';
import '../models/allergy_profile_request.dart';
import '../models/allergy_classification_response.dart';

class UserStorageService {
  static const String _userPreferenceIdKey = 'user_preference_id';
  static const String _userProfileKey = 'user_profile';
  static const String _userRequestKey = 'user_request';
  static const String _lastClassificationKey = 'last_classification';

  /// Save user preference ID
  static Future<void> saveUserPreferenceId(String userPreferenceId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userPreferenceIdKey, userPreferenceId);
  }

  /// Get user preference ID
  static Future<String?> getUserPreferenceId() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_userPreferenceIdKey);
  }

  /// Save user profile response
  static Future<void> saveUserProfile(UserProfileResponse profile) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userProfileKey, jsonEncode(profile.toJson()));
  }

  /// Get user profile response
  static Future<UserProfileResponse?> getUserProfile() async {
    final prefs = await SharedPreferences.getInstance();
    final profileString = prefs.getString(_userProfileKey);
    if (profileString != null) {
      try {
        final profileMap = jsonDecode(profileString) as Map<String, dynamic>;
        return UserProfileResponse.fromJson(profileMap);
      } catch (e) {
        // If parsing fails, return null
        return null;
      }
    }
    return null;
  }

  /// Save user request data
  static Future<void> saveUserRequest(AllergyProfileRequest request) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userRequestKey, jsonEncode(request.toJson()));
  }

  /// Get user request data
  static Future<AllergyProfileRequest?> getUserRequest() async {
    final prefs = await SharedPreferences.getInstance();
    final requestString = prefs.getString(_userRequestKey);
    if (requestString != null) {
      try {
        final requestMap = jsonDecode(requestString) as Map<String, dynamic>;
        return AllergyProfileRequest.fromJson(requestMap);
      } catch (e) {
        // If parsing fails, return null
        return null;
      }
    }
    return null;
  }

  /// Save last classification response
  static Future<void> saveLastClassification(AllergyClassificationResponse classification) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_lastClassificationKey, jsonEncode(classification.toJson()));
  }

  /// Get last classification response
  static Future<AllergyClassificationResponse?> getLastClassification() async {
    final prefs = await SharedPreferences.getInstance();
    final classificationString = prefs.getString(_lastClassificationKey);
    if (classificationString != null) {
      try {
        final classificationMap = jsonDecode(classificationString) as Map<String, dynamic>;
        return AllergyClassificationResponse.fromJson(classificationMap);
      } catch (e) {
        // If parsing fails, return null
        return null;
      }
    }
    return null;
  }

  /// Check if user has an existing profile
  static Future<bool> hasUserProfile() async {
    final userPreferenceId = await getUserPreferenceId();
    return userPreferenceId != null && userPreferenceId.isNotEmpty;
  }

  /// Clear all user data
  static Future<void> clearUserData() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_userPreferenceIdKey);
    await prefs.remove(_userProfileKey);
    await prefs.remove(_userRequestKey);
    await prefs.remove(_lastClassificationKey);
  }

  /// Save complete user session (profile + request + classification)
  static Future<void> saveUserSession({
    required String userPreferenceId,
    required UserProfileResponse profile,
    required AllergyProfileRequest request,
    required AllergyClassificationResponse classification,
  }) async {
    await Future.wait([
      saveUserPreferenceId(userPreferenceId),
      saveUserProfile(profile),
      saveUserRequest(request),
      saveLastClassification(classification),
    ]);
  }
}