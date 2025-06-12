package com.presca.modul5.presentation.theme

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "theme_preferences")

class ThemeViewModel(private val applicationContext: Context) : ViewModel() {

    private val IS_DARK_THEME_KEY = booleanPreferencesKey("is_dark_theme")

    private val _isDarkTheme = MutableStateFlow(false)
    val isDarkTheme: StateFlow<Boolean> = _isDarkTheme.asStateFlow()

    init {
        viewModelScope.launch {
            applicationContext.dataStore.data
                .map { preferences ->
                    preferences[IS_DARK_THEME_KEY] ?: false
                }
                .collect { isDark ->
                    _isDarkTheme.value = isDark
                }
        }
    }

    fun toggleTheme() {
        viewModelScope.launch {
            val currentTheme = _isDarkTheme.value
            applicationContext.dataStore.edit { preferences ->
                preferences[IS_DARK_THEME_KEY] = !currentTheme
            }
        }
    }
}