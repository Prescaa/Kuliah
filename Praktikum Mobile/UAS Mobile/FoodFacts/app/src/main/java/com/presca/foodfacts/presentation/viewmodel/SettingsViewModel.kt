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
    
    fun updateProfile(newName: String, newEmail: String, imageUri: String?, newDateOfBirth: String?, onResult: (Boolean, String) -> Unit) {
        viewModelScope.launch {
            val oldProfile = userPreferences.getFullUserProfile()

            var success = true
            var message = "Profil berhasil diperbarui!"

            userPreferences.saveUserProfile(newName, oldProfile.email, imageUri, oldProfile.dateOfBirth)
            _uiState.update { it.copy(userProfile = it.userProfile.copy(name = newName, profileImage = imageUri)) }


            if (oldProfile.email != newEmail) {
                authRepository.updateEmail(oldProfile.email, newEmail)
                    .onSuccess {
                        userPreferences.saveUserProfile(newName, newEmail, imageUri, oldProfile.dateOfBirth)
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(email = newEmail)) }
                    }
                    .onFailure { e ->
                        userPreferences.saveUserProfile(newName, oldProfile.email, imageUri, oldProfile.dateOfBirth)
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(email = oldProfile.email)) }
                        success = false
                        message = "Gagal memperbarui email: ${e.message ?: "Terjadi kesalahan"}"
                        _message.value = message
                        onResult(success, message)
                        return@launch
                    }
            }

            if (success && oldProfile.dateOfBirth != newDateOfBirth) {
                authRepository.updateDateOfBirth(newEmail, newDateOfBirth)
                    .onSuccess {
                        userPreferences.saveUserProfile(newName, newEmail, imageUri, newDateOfBirth)
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(dateOfBirth = newDateOfBirth)) }
                    }
                    .onFailure { e ->
                        userPreferences.saveUserProfile(newName, newEmail, imageUri, oldProfile.dateOfBirth)
                        _uiState.update { it.copy(userProfile = it.userProfile.copy(dateOfBirth = oldProfile.dateOfBirth)) }
                        success = false
                        message = "Gagal memperbarui tanggal lahir: ${e.message ?: "Terjadi kesalahan"}"
                        _message.value = message
                    }
            }

            _message.value = message
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
