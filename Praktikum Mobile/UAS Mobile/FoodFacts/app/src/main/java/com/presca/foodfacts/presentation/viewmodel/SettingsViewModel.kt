package com.presca.foodfacts.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.presca.foodfacts.data.auth.AuthRepository
import com.presca.foodfacts.data.local.UserPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class SettingsViewModel(
    private val userPreferences: UserPreferences,
    private val authRepository: AuthRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(SettingsUiState())
    val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

    // State untuk pesan kesalahan/sukses yang akan ditampilkan di UI
    private val _message = MutableStateFlow<String?>(null)
    val message: StateFlow<String?> = _message.asStateFlow()

    init {
        loadUserProfile()
    }

    fun loadUserProfile() {
        viewModelScope.launch {
            val userProfileData = userPreferences.getFullUserProfile()
            _uiState.update {
                it.copy(
                    darkModeEnabled = userPreferences.getDarkMode(),
                    userProfile = UserProfile(
                        name = userProfileData.name,
                        email = userProfileData.email,
                        profileImage = userProfileData.imageUri,
                        dateOfBirth = userProfileData.dateOfBirth
                    )
                )
            }
        }
    }

    fun toggleDarkMode(enabled: Boolean) {
        viewModelScope.launch {
            userPreferences.setDarkMode(enabled)
            _uiState.update { it.copy(darkModeEnabled = enabled) }
        }
    }

    /**
     * Memperbarui profil pengguna (nama, email, tanggal lahir).
     * Memberikan umpan balik melalui callback onResult.
     *
     * @param newName Nama baru pengguna.
     * @param newEmail Email baru pengguna.
     * @param imageUri URI gambar profil (bisa null).
     * @param newDateOfBirth Tanggal lahir baru (bisa null atau string kosong).
     * @param onResult Callback yang dipanggil setelah operasi selesai: (Boolean, String) -> Unit
     * Boolean: true jika berhasil, false jika gagal.
     * String: Pesan status/kesalahan.
     */
    fun updateProfile(newName: String, newEmail: String, imageUri: String?, newDateOfBirth: String?, onResult: (Boolean, String) -> Unit) {
        viewModelScope.launch {
            val oldProfile = userPreferences.getFullUserProfile()

            var success = true
            var message = "Profil berhasil diperbarui!"

            // 1. Update nama dan gambar profil secara lokal di preferences dan state UI
            // Ini dilakukan terlebih dahulu karena tidak memerlukan panggilan API
            userPreferences.saveUserProfile(newName, oldProfile.email, imageUri, oldProfile.dateOfBirth)
            _uiState.update { it.copy(userProfile = it.userProfile.copy(name = newName, profileImage = imageUri)) }


            // 2. Perbarui Email jika ada perubahan
            if (oldProfile.email != newEmail) {
                authRepository.updateEmail(oldProfile.email, newEmail)
                    .onSuccess {
                        // Email berhasil diperbarui di database, simpan ke preferences
                        userPreferences.saveUserProfile(newName, newEmail, imageUri, oldProfile.dateOfBirth)
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(email = newEmail)) }
                    }
                    .onFailure { e ->
                        // Jika update email gagal, kembalikan email lama ke preferences dan state UI
                        userPreferences.saveUserProfile(newName, oldProfile.email, imageUri, oldProfile.dateOfBirth) // Kembalikan email lama
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(email = oldProfile.email)) }
                        success = false
                        message = "Gagal memperbarui email: ${e.message ?: "Terjadi kesalahan"}"
                        _message.value = message // Set pesan untuk ditampilkan di UI
                        onResult(success, message) // Beri tahu UI dan keluar dari coroutine
                        return@launch // Hentikan eksekusi coroutine lebih lanjut
                    }
            }

            // 3. Perbarui Tanggal Lahir jika ada perubahan (hanya jika email update berhasil atau tidak ada update email)
            if (success && oldProfile.dateOfBirth != newDateOfBirth) {
                // Gunakan newEmail yang mungkin sudah diupdate dari langkah sebelumnya
                authRepository.updateDateOfBirth(newEmail, newDateOfBirth)
                    .onSuccess {
                        // Tanggal lahir berhasil diperbarui di database, simpan ke preferences
                        userPreferences.saveUserProfile(newName, newEmail, imageUri, newDateOfBirth)
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(dateOfBirth = newDateOfBirth)) }
                    }
                    .onFailure { e ->
                        // Jika update tanggal lahir gagal, kembalikan tanggal lahir lama ke preferences dan state UI
                        userPreferences.saveUserProfile(newName, newEmail, imageUri, oldProfile.dateOfBirth) // Kembalikan tanggal lahir lama
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(dateOfBirth = oldProfile.dateOfBirth)) }
                        success = false
                        message = "Gagal memperbarui tanggal lahir: ${e.message ?: "Terjadi kesalahan"}"
                        _message.value = message // Set pesan untuk ditampilkan di UI
                        // Tidak return@launch di sini, karena update email (jika ada) mungkin sudah berhasil
                    }
            }

            // Beri tahu UI hasil akhir dari semua operasi
            _message.value = message // Set pesan untuk ditampilkan di UI
            onResult(success, message)
        }
    }

    fun updatePassword(oldPassword: String, newPassword: String, onResult: (Boolean) -> Unit) {
        viewModelScope.launch {
            authRepository.updatePassword(oldPassword, newPassword)
                .onSuccess {
                    _message.value = "Kata sandi berhasil diperbarui!"
                    onResult(true)
                }
                .onFailure { e ->
                    _message.value = "Gagal memperbarui kata sandi: ${e.message ?: "Terjadi kesalahan"}"
                    onResult(false)
                }
        }
    }

    // Fungsi untuk mengkonsumsi pesan setelah ditampilkan di UI
    fun consumeMessage() {
        _message.value = null
    }
}

data class SettingsUiState(
    val darkModeEnabled: Boolean = false,
    val userProfile: UserProfile = UserProfile()
)

data class UserProfile(
    val name: String = "",
    val email: String = "",
    val profileImage: String? = null,
    val dateOfBirth: String? = null
)