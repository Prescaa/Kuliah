package com.presca.foodfacts.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.presca.foodfacts.data.auth.AuthRepository
import com.presca.foodfacts.data.local.UserPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class AuthViewModel(
    private val authRepository: AuthRepository,
    private val userPreferences: UserPreferences
) : ViewModel() {

    private val _loginState = MutableStateFlow<AuthResult>(AuthResult.Idle)
    val loginState: StateFlow<AuthResult> = _loginState.asStateFlow()

    private val _registerState = MutableStateFlow<AuthResult>(AuthResult.Idle)
    val registerState: StateFlow<AuthResult> = _registerState.asStateFlow()

    fun login(email: String, password: String) {
        _loginState.value = AuthResult.Loading
        viewModelScope.launch {
            authRepository.login(email, password)
                .onSuccess {
                    _loginState.value = AuthResult.Success("Login berhasil!")
                }
                .onFailure { e ->
                    _loginState.value = AuthResult.Error(e.message ?: "Login gagal")
                }
        }
    }

    fun register(username: String, email: String, password: String, dateOfBirth: String?) {
        _registerState.value = AuthResult.Loading
        viewModelScope.launch {
            authRepository.register(username, email, password, dateOfBirth)
                .onSuccess {
                    _registerState.value = AuthResult.Success("Pendaftaran berhasil!")
                }
                .onFailure { e ->
                    _registerState.value = AuthResult.Error(e.message ?: "Pendaftaran gagal")
                }
        }
    }

    suspend fun isLoggedIn(): Boolean {
        return userPreferences.isLoggedIn()
    }

    fun logout() {
        viewModelScope.launch {
            authRepository.logout()
        }
        _loginState.value = AuthResult.Idle
        _registerState.value = AuthResult.Idle
    }

    sealed class AuthResult {
        object Idle : AuthResult()
        object Loading : AuthResult()
        data class Success(val message: String) : AuthResult()
        data class Error(val message: String) : AuthResult()
    }
}