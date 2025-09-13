class UserSettings {
  final String userId;
  final UserGroup userGroup;

  UserSettings({
    required this.userId,
    required this.userGroup,
  });

  Map<String, dynamic> toJson() {
    return {
      'userId': userId,
      'userGroup': userGroup.toJson(),
    };
  }

  factory UserSettings.fromJson(Map<String, dynamic> json) {
    return UserSettings(
      userId: json['userId'] ?? '',
      userGroup: UserGroup.fromJson(json['userGroup'] ?? {}),
    );
  }
}

class UserGroup {
  final int groupId;
  final String groupName;
  final String description;

  UserGroup({
    required this.groupId,
    required this.groupName,
    required this.description,
  });

  Map<String, dynamic> toJson() {
    return {
      'groupId': groupId,
      'groupName': groupName,
      'description': description,
    };
  }

  factory UserGroup.fromJson(Map<String, dynamic> json) {
    return UserGroup(
      groupId: json['groupId'] ?? 0,
      groupName: json['groupName'] ?? '',
      description: json['description'] ?? '',
    );
  }

  static List<UserGroup> getAllGroups() {
    return [
      UserGroup(groupId: 1, groupName: "Şiddetli Alerjik Grup", description: "Ciddi alerjik reaksiyonları olan kişiler"),
      UserGroup(groupId: 2, groupName: "Hafif-Orta Grup", description: "Hafif ve orta düzeyde alerjisi olan kişiler"),
      UserGroup(groupId: 3, groupName: "Olası Alerjik/Genetik", description: "Genetik yatkınlığı olan kişiler"),
      UserGroup(groupId: 4, groupName: "Teşhis Almamış", description: "Henüz alerjik teşhis almamış kişiler"),
      UserGroup(groupId: 5, groupName: "Hassas Grup (Çocuk/Yaşlı/Kronik)", description: "Çocuk, yaşlı veya kronik hastalığı olan kişiler"),
    ];
  }
}