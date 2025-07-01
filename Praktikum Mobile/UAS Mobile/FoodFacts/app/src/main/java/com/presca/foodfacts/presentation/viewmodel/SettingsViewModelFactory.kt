package com.presca.foodfacts.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.presca.foodfacts.data.local.UserPreferences
import com.presca.foodfacts.data.auth.AuthRepository

class SettingsViewModelFactory(
    private val userPreferences: UserPreferences,
    private val authRepository: AuthRepository
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(SettingsViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return SettingsViewModel(userPreferences, authRepository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}