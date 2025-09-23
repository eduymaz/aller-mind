import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/user_settings.dart';
import '../providers/allermind_provider.dart';
import '../services/allermind_api_service.dart';

class UserProfileScreen extends StatefulWidget {
  const UserProfileScreen({super.key});

  @override
  State<UserProfileScreen> createState() => _UserProfileScreenState();
}

class _UserProfileScreenState extends State<UserProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  
  // Form kontrolleri
  final _ageController = TextEditingController();
  String _selectedGender = 'male';
  bool _hasChronicDisease = false;
  bool _hasAsthma = false;
  bool _hasEczema = false;
  bool _hasRhinitis = false;
  bool _hasConjunctivitis = false;
  bool _hasFoodAllergy = false;
  
  // Alerjik geçmiş
  final List<String> _allergyHistory = [];
  final List<String> _medicationUsage = [];
  
  // Alerji türleri
  final Map<String, bool> _allergyTypes = {
    'Polen Alerjisi': false,
    'Ev Tozu Akarı': false,
    'Hayvan Tüyü': false,
    'Küf': false,
    'Gıda Alerjisi': false,
    'İlaç Alerjisi': false,
    'Böcek Sokması': false,
  };
  
  // İlaç kullanımları
  final Map<String, bool> _medications = {
    'Antihistaminik': false,
    'Nazal Kortikosteroid': false,
    'Bronkodilatör': false,
    'İmmünoterapie': false,
    'Epinefrin (EpiPen)': false,
  };

  bool _isLoading = false;
  UserGroup? _determinedGroup;

  @override
  void dispose() {
    _ageController.dispose();
    super.dispose();
  }

  Future<void> _classifyUser() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
    });

    try {
      // Kullanıcı özelliklerini hazırla
      final userCharacteristics = {
        'age': int.tryParse(_ageController.text) ?? 30,
        'gender': _selectedGender,
        'hasChronicDisease': _hasChronicDisease,
        'hasAsthma': _hasAsthma,
        'hasEczema': _hasEczema,
        'hasRhinitis': _hasRhinitis,
        'hasConjunctivitis': _hasConjunctivitis,
        'hasFoodAllergy': _hasFoodAllergy,
        'allergyHistory': _allergyHistory,
        'medicationUsage': _medicationUsage,
        'allergyTypes': _allergyTypes.entries
            .where((entry) => entry.value)
            .map((entry) => entry.key)
            .toList(),
        'medications': _medications.entries
            .where((entry) => entry.value)
            .map((entry) => entry.key)
            .toList(),
      };

      // API'ye gönder ve grubu belirle
      final group = await AllerMindApiService.classifyUser(userCharacteristics);
      
      setState(() {
        _determinedGroup = group;
      });

      // Provider'a kaydet
      final userSettings = UserSettings(
        userId: 'user_${DateTime.now().millisecondsSinceEpoch}',
        userGroup: group,
        userCharacteristics: userCharacteristics,
      );

      if (mounted) {
        context.read<AllerMindProvider>().updateUserSettings(userSettings);
        
        // Başarı mesajı göster
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Profil oluşturuldu: ${group.groupName}'),
            backgroundColor: Colors.green,
          ),
        );
      }

    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Hata: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _updateAllergyHistory() {
    _allergyHistory.clear();
    _allergyTypes.forEach((key, value) {
      if (value) _allergyHistory.add(key);
    });
  }

  void _updateMedicationUsage() {
    _medicationUsage.clear();
    _medications.forEach((key, value) {
      if (value) _medicationUsage.add(key);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Kullanıcı Profili'),
        elevation: 0,
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Başlık
              Text(
                'Kişisel Bilgiler',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  color: Colors.teal,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),

              // Yaş
              TextFormField(
                controller: _ageController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Yaş',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.calendar_today),
                ),
                validator: (value) {
                  if (value == null || value.isEmpty) {
                    return 'Yaşınızı giriniz';
                  }
                  final age = int.tryParse(value);
                  if (age == null || age < 1 || age > 120) {
                    return 'Geçerli bir yaş giriniz (1-120)';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Cinsiyet
              Text('Cinsiyet', style: Theme.of(context).textTheme.titleMedium),
              Row(
                children: [
                  Expanded(
                    child: RadioListTile<String>(
                      title: const Text('Erkek'),
                      value: 'male',
                      groupValue: _selectedGender,
                      onChanged: (value) {
                        setState(() {
                          _selectedGender = value!;
                        });
                      },
                    ),
                  ),
                  Expanded(
                    child: RadioListTile<String>(
                      title: const Text('Kadın'),
                      value: 'female',
                      groupValue: _selectedGender,
                      onChanged: (value) {
                        setState(() {
                          _selectedGender = value!;
                        });
                      },
                    ),
                  ),
                ],
              ),

              const Divider(height: 32),

              // Sağlık Durumu
              Text(
                'Sağlık Durumu',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  color: Colors.teal,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),

              CheckboxListTile(
                title: const Text('Kronik Hastalığım Var'),
                subtitle: const Text('Diyabet, kalp hastalığı, vb.'),
                value: _hasChronicDisease,
                onChanged: (value) {
                  setState(() {
                    _hasChronicDisease = value ?? false;
                  });
                },
              ),

              CheckboxListTile(
                title: const Text('Astım'),
                value: _hasAsthma,
                onChanged: (value) {
                  setState(() {
                    _hasAsthma = value ?? false;
                  });
                },
              ),

              CheckboxListTile(
                title: const Text('Egzama'),
                value: _hasEczema,
                onChanged: (value) {
                  setState(() {
                    _hasEczema = value ?? false;
                  });
                },
              ),

              CheckboxListTile(
                title: const Text('Alerjik Rinit'),
                value: _hasRhinitis,
                onChanged: (value) {
                  setState(() {
                    _hasRhinitis = value ?? false;
                  });
                },
              ),

              CheckboxListTile(
                title: const Text('Allejik Konjunktivit'),
                value: _hasConjunctivitis,
                onChanged: (value) {
                  setState(() {
                    _hasConjunctivitis = value ?? false;
                  });
                },
              ),

              CheckboxListTile(
                title: const Text('Gıda Alerjim Var'),
                value: _hasFoodAllergy,
                onChanged: (value) {
                  setState(() {
                    _hasFoodAllergy = value ?? false;
                  });
                },
              ),

              const Divider(height: 32),

              // Alerji Türleri
              Text(
                'Alerji Türleri',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  color: Colors.teal,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),

              ..._allergyTypes.entries.map((entry) {
                return CheckboxListTile(
                  title: Text(entry.key),
                  value: entry.value,
                  onChanged: (value) {
                    setState(() {
                      _allergyTypes[entry.key] = value ?? false;
                      _updateAllergyHistory();
                    });
                  },
                );
              }).toList(),

              const Divider(height: 32),

              // İlaç Kullanımı
              Text(
                'Kullandığım İlaçlar',
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  color: Colors.teal,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),

              ..._medications.entries.map((entry) {
                return CheckboxListTile(
                  title: Text(entry.key),
                  value: entry.value,
                  onChanged: (value) {
                    setState(() {
                      _medications[entry.key] = value ?? false;
                      _updateMedicationUsage();
                    });
                  },
                );
              }).toList(),

              const SizedBox(height: 32),

              // Belirlenen Grup
              if (_determinedGroup != null) ...[
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.teal.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.teal.shade200),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Belirlenen Alerji Grubunuz:',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          color: Colors.teal.shade700,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        _determinedGroup!.groupName,
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          color: Colors.teal.shade900,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        _determinedGroup!.description,
                        style: TextStyle(color: Colors.teal.shade600),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
              ],

              // Profil Oluştur Butonu
              SizedBox(
                width: double.infinity,
                height: 56,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _classifyUser,
                  child: _isLoading
                      ? const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            ),
                            SizedBox(width: 8),
                            Text('İşleniyor...'),
                          ],
                        )
                      : Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(_determinedGroup == null 
                                ? Icons.person_add 
                                : Icons.update),
                            const SizedBox(width: 8),
                            Text(_determinedGroup == null 
                                ? 'Profil Oluştur' 
                                : 'Profili Güncelle'),
                          ],
                        ),
                ),
              ),

              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }
}