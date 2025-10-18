import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import '../models/allergy_profile_request.dart';
import '../services/allergy_classification_service.dart';
import '../services/user_storage_service.dart';
import 'allergy_classification_result_screen.dart';

class DetailedProfileFormScreen extends StatefulWidget {
  final AllergyProfileRequest? existingRequest;
  final bool isEditing;
  
  const DetailedProfileFormScreen({
    Key? key, 
    this.existingRequest,
    this.isEditing = false,
  }) : super(key: key);

  @override
  State<DetailedProfileFormScreen> createState() => _DetailedProfileFormScreenState();
}

class _DetailedProfileFormScreenState extends State<DetailedProfileFormScreen> {
  final _formKey = GlobalKey<FormState>();
  
  // Form controllers and values
  final _ageController = TextEditingController();
  
  String _selectedGender = '';
  String _selectedClinicalDiagnosis = '';
  bool _familyAllergyHistory = false;
  List<String> _selectedMedications = [];
  
  // Location data
  double? _latitude;
  double? _longitude;

  
  // Environmental triggers
  bool _airPollution = false;
  bool _dustMites = false;
  bool _petDander = false;
  bool _smoke = false;
  bool _mold = false;
  
  // Food allergies
  bool _appleAllergy = false;
  bool _shellfishAllergy = false;
  bool _nutsAllergy = false;
  
  // Tree pollen allergies
  bool _pineAllergy = false;
  bool _oliveAllergy = false;
  bool _birchAllergy = false;
  
  // Grass pollen allergies
  bool _graminalesAllergy = false;
  
  // Weed pollen allergies
  bool _mugwortAllergy = false;
  bool _ragweedAllergy = false;
  
  // Previous allergic reactions
  bool _severeAsthma = false;
  bool _hospitalization = false;
  bool _anaphylaxis = false;
  
  bool _isLoading = false;


  @override
  void initState() {
    super.initState();
    if (widget.isEditing && widget.existingRequest != null) {
      _populateExistingData();
    } else {
      // Automatically get location when form loads
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _getCurrentLocation();
      });
    }
  }

  void _populateExistingData() {
    final request = widget.existingRequest!;
    
    _ageController.text = request.age.toString();
    _latitude = request.latitude;
    _longitude = request.longitude;

    
    _selectedGender = request.gender;
    _selectedClinicalDiagnosis = request.clinicalDiagnosis;
    _familyAllergyHistory = request.familyAllergyHistory;
    _selectedMedications = List.from(request.currentMedications);
    
    // Environmental triggers
    _airPollution = request.environmentalTriggers.airPollution;
    _dustMites = request.environmentalTriggers.dustMites;
    _petDander = request.environmentalTriggers.petDander;
    _smoke = request.environmentalTriggers.smoke;
    _mold = request.environmentalTriggers.mold;
    
    // Food allergies
    _appleAllergy = request.foodAllergies.apple;
    _shellfishAllergy = request.foodAllergies.shellfish;
    _nutsAllergy = request.foodAllergies.nuts;
    
    // Tree pollen allergies
    _pineAllergy = request.treePollenAllergies.pine;
    _oliveAllergy = request.treePollenAllergies.olive;
    _birchAllergy = request.treePollenAllergies.birch;
    
    // Grass pollen allergies
    _graminalesAllergy = request.grassPollenAllergies.graminales;
    
    // Weed pollen allergies
    _mugwortAllergy = request.weedPollenAllergies.mugwort;
    _ragweedAllergy = request.weedPollenAllergies.ragweed;
    
    // Previous allergic reactions
    _severeAsthma = request.previousAllergicReactions.severeAsthma;
    _hospitalization = request.previousAllergicReactions.hospitalization;
    _anaphylaxis = request.previousAllergicReactions.anaphylaxis;
  }

  @override
  void dispose() {
    _ageController.dispose();
    super.dispose();
  }

  Future<void> _getCurrentLocation() async {
    try {
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          throw Exception('Konum izni reddedildi. Lütfen ayarlardan konum iznini açın.');
        }
      }

      if (permission == LocationPermission.deniedForever) {
        throw Exception('Konum izni kalıcı olarak reddedildi. Lütfen ayarlardan konum iznini açın.');
      }

      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );

      setState(() {
        _latitude = position.latitude;
        _longitude = position.longitude;
      });
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Konum başarıyla alındı!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Konum alınamadı: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }



  Future<void> _submitForm() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    if (_selectedGender.isEmpty) {
      _showErrorDialog('Lütfen cinsiyet seçin');
      return;
    }

    if (_selectedClinicalDiagnosis.isEmpty) {
      _showErrorDialog('Lütfen klinik durum seçin');
      return;
    }

    if (_latitude == null || _longitude == null) {
      _showErrorDialog('Konum bilgisi alınamadı. Lütfen konum iznini verin veya tekrar deneyin.');
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final request = AllergyProfileRequest(
        age: int.parse(_ageController.text),
        clinicalDiagnosis: _selectedClinicalDiagnosis,
        currentMedications: _selectedMedications,
        environmentalTriggers: EnvironmentalTriggers(
          airPollution: _airPollution,
          dustMites: _dustMites,
          petDander: _petDander,
          smoke: _smoke,
          mold: _mold,
        ),
        familyAllergyHistory: _familyAllergyHistory,
        foodAllergies: FoodAllergies(
          apple: _appleAllergy,
          shellfish: _shellfishAllergy,
          nuts: _nutsAllergy,
        ),
        gender: _selectedGender,
        grassPollenAllergies: GrassPollenAllergies(
          graminales: _graminalesAllergy,
        ),
        latitude: _latitude!,
        longitude: _longitude!,
        previousAllergicReactions: PreviousAllergicReactions(
          severeAsthma: _severeAsthma,
          hospitalization: _hospitalization,
          anaphylaxis: _anaphylaxis,
        ),
        treePollenAllergies: TreePollenAllergies(
          pine: _pineAllergy,
          olive: _oliveAllergy,
          birch: _birchAllergy,
        ),
        weedPollenAllergies: WeedPollenAllergies(
          mugwort: _mugwortAllergy,
          ragweed: _ragweedAllergy,
        ),
      );

      if (!AllergyClassificationService.validateRequest(request)) {
        _showErrorDialog('Form verilerinde hata var. Lütfen tüm alanları kontrol edin.');
        return;
      }

      final response = await AllergyClassificationService.classifyAllergyProfile(request);
      
      // Save user data to local storage
      if (response.userPreferenceId.isNotEmpty) {
        await UserStorageService.saveUserPreferenceId(response.userPreferenceId);
        await UserStorageService.saveUserRequest(request);
        await UserStorageService.saveLastClassification(response);
      }
      
      if (mounted) {
        if (widget.isEditing) {
          // Show success message for profile update
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Klinik profil başarıyla güncellendi!'),
              backgroundColor: Colors.green,
              duration: Duration(seconds: 2),
            ),
          );
        }
        
        // Her durumda da stack'i temizleyip sonuç sayfası
        // Böylece sonuç sayfasından geri dönüş her zaman user selection sayfasına olacak
        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(
            builder: (context) => AllergyClassificationResultScreen(
              response: response,
              request: request,
            ),
          ),
          (route) => route.settings.name == '/' || route.isFirst,
        );
      }
      
    } catch (e) {
      if (mounted) {
        _showErrorDialog('Hata: $e');
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Hata'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Tamam'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.isEditing ? 'Klinik Profil Güncelle' : 'Klinik Profil Oluştur',
          style: const TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.w600,
          ),
        ),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        elevation: 2,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Form(
              key: _formKey,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildBasicInfoSection(),
                    const SizedBox(height: 24),
                    _buildLocationSection(),
                    const SizedBox(height: 24),
                    _buildClinicalSection(),
                    const SizedBox(height: 24),
                    _buildPollenAllergiesSection(),
                    const SizedBox(height: 24),
                    _buildFoodAllergiesSection(),
                    const SizedBox(height: 24),
                    _buildEnvironmentalTriggersSection(),
                    const SizedBox(height: 24),
                    _buildPreviousReactionsSection(),
                    const SizedBox(height: 24),
                    _buildMedicationsSection(),
                    const SizedBox(height: 32),
                    _buildSubmitButton(),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildBasicInfoSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Temel Bilgiler',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    controller: _ageController,
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Yaş',
                      border: OutlineInputBorder(),
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Lütfen yaşınızı girin';
                      }
                      final age = int.tryParse(value);
                      if (age == null || age <= 0 || age > 150) {
                        return 'Geçerli bir yaş girin (1-150)';
                      }
                      return null;
                    },
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: DropdownButtonFormField<String>(
                    value: _selectedGender.isEmpty ? null : _selectedGender,
                    decoration: const InputDecoration(
                      labelText: 'Cinsiyet',
                      border: OutlineInputBorder(),
                    ),
                    items: AllergyFormOptions.genders.map((gender) {
                      return DropdownMenuItem(
                        value: gender,
                        child: Text(AllergyFormOptions.genderLabels[gender] ?? gender),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() {
                        _selectedGender = value ?? '';
                      });
                    },
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Lütfen cinsiyet seçin';
                      }
                      return null;
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLocationSection() {
    // Konum bilgileri kullanıcıya gösterilmiyor, arka planda otomatik alınıyor -sunumda aktarılmalı 
    return const SizedBox.shrink();
  }



  Widget _buildClinicalSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Klinik Bilgiler',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _selectedClinicalDiagnosis.isEmpty ? null : _selectedClinicalDiagnosis,
              decoration: const InputDecoration(
                labelText: 'Klinik Durum',
                border: OutlineInputBorder(),
              ),
              items: AllergyFormOptions.clinicalDiagnoses.map((diagnosis) {
                return DropdownMenuItem(
                  value: diagnosis,
                  child: Text(AllergyFormOptions.clinicalDiagnosisLabels[diagnosis] ?? diagnosis),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _selectedClinicalDiagnosis = value ?? '';
                });
              },
              validator: (value) {
                if (value == null || value.isEmpty) {
                  return 'Lütfen klinik durum seçin';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            SwitchListTile(
              title: const Text('Ailede Alerji Öyküsü Mevcut'), // standart tıbbi kayıt dili olarak kullanıldı 
              value: _familyAllergyHistory,
              onChanged: (value) {
                setState(() {
                  _familyAllergyHistory = value;
                });
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPollenAllergiesSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Polen Alerjileri',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            Text(
              'Ağaç Poleni',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            CheckboxListTile(
              title: const Text('Huş ağacı'),
              value: _birchAllergy,
              onChanged: (value) {
                setState(() {
                  _birchAllergy = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Zeytin'),
              value: _oliveAllergy,
              onChanged: (value) {
                setState(() {
                  _oliveAllergy = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Çam'),
              value: _pineAllergy,
              onChanged: (value) {
                setState(() {
                  _pineAllergy = value ?? false;
                });
              },
            ),
            const Divider(),
            Text(
              'Çim Poleni',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            CheckboxListTile(
              title: const Text('Çim poleni (Graminales)'),
              value: _graminalesAllergy,
              onChanged: (value) {
                setState(() {
                  _graminalesAllergy = value ?? false;
                });
              },
            ),
            const Divider(),
            Text(
              'Yabani Ot Poleni',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            CheckboxListTile(
              title: const Text('Karaot (Ragweed)'),
              value: _ragweedAllergy,
              onChanged: (value) {
                setState(() {
                  _ragweedAllergy = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Pelin (Mugwort)'),
              value: _mugwortAllergy,
              onChanged: (value) {
                setState(() {
                  _mugwortAllergy = value ?? false;
                });
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFoodAllergiesSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Besin Alerjileri',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            CheckboxListTile(
              title: const Text('Elma'),
              value: _appleAllergy,
              onChanged: (value) {
                setState(() {
                  _appleAllergy = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Fındık/Fıstık'),
              value: _nutsAllergy,
              onChanged: (value) {
                setState(() {
                  _nutsAllergy = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Kabuklu deniz ürünleri'),
              value: _shellfishAllergy,
              onChanged: (value) {
                setState(() {
                  _shellfishAllergy = value ?? false;
                });
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEnvironmentalTriggersSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Çevresel Tetikleyiciler',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            CheckboxListTile(
              title: const Text('Ev tozu akarı'),
              value: _dustMites,
              onChanged: (value) {
                setState(() {
                  _dustMites = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Hayvan tüyü'),
              value: _petDander,
              onChanged: (value) {
                setState(() {
                  _petDander = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Küf'),
              value: _mold,
              onChanged: (value) {
                setState(() {
                  _mold = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Hava kirliliği'),
              value: _airPollution,
              onChanged: (value) {
                setState(() {
                  _airPollution = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Duman'),
              value: _smoke,
              onChanged: (value) {
                setState(() {
                  _smoke = value ?? false;
                });
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPreviousReactionsSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Önceki Alerjik Reaksiyonlar',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            CheckboxListTile(
              title: const Text('Şiddetli astım atağı'),
              value: _severeAsthma,
              onChanged: (value) {
                setState(() {
                  _severeAsthma = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Hastaneye yatış'),
              value: _hospitalization,
              onChanged: (value) {
                setState(() {
                  _hospitalization = value ?? false;
                });
              },
            ),
            CheckboxListTile(
              title: const Text('Anafilaksi'),
              value: _anaphylaxis,
              onChanged: (value) {
                setState(() {
                  _anaphylaxis = value ?? false;
                });
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMedicationsSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Mevcut İlaçlar',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            Text(
              'Kullandığınız ilaçları seçin:',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8.0,
              children: AllergyFormOptions.availableMedications.map((medication) {
                final isSelected = _selectedMedications.contains(medication);
                return FilterChip(
                  label: Text(AllergyFormOptions.medicationLabels[medication] ?? medication),
                  selected: isSelected,
                  onSelected: (selected) {
                    setState(() {
                      if (selected) {
                        _selectedMedications.add(medication);
                      } else {
                        _selectedMedications.remove(medication);
                      }
                    });
                  },
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSubmitButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        onPressed: _isLoading ? null : _submitForm,
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(vertical: 16.0),
        ),
        child: _isLoading
            ? const CircularProgressIndicator()
            : Text(
                widget.isEditing ? 'Klinik Profil Kaydet' : 'Klinik Analiz Başlat',
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                ),
              ),
      ),
    );
  }
}