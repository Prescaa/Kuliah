package com.presca.foodfacts.data.local

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

val Context.dataStore by preferencesDataStore(name = "user_prefs")

class UserPreferences(private val context: Context) {

    companion object {
        private val AUTH_TOKEN_KEY = stringPreferencesKey("auth_token")
        private val DARK_MODE_KEY = booleanPreferencesKey("dark_mode")
        private val USER_NAME_KEY = stringPreferencesKey("user_name")
        private val USER_EMAIL_KEY = stringPreferencesKey("user_email")
        private val USER_IMAGE_KEY = stringPreferencesKey("user_image")
        private val USER_DATE_OF_BIRTH_KEY = stringPreferencesKey("user_date_of_birth")
    }

    suspend fun saveAuthToken(token: String) {
        context.dataStore.edit { preferences ->
            preferences[AUTH_TOKEN_KEY] = token
        }
    }

    fun getAuthToken(): Flow<String?> {
        return context.dataStore.data.map { preferences ->
            preferences[AUTH_TOKEN_KEY]
        }
    }

    suspend fun clearAuthToken() {
        context.dataStore.edit { preferences ->
            preferences.remove(AUTH_TOKEN_KEY)
            preferences.remove(USER_NAME_KEY)
            preferences.remove(USER_EMAIL_KEY)
            preferences.remove(USER_IMAGE_KEY)
            preferences.remove(USER_DATE_OF_BIRTH_KEY)
        }
    }

    suspend fun isLoggedIn(): Boolean {
        return try {
            val token = getAuthToken().first()
            !token.isNullOrEmpty()
        } catch (e: Exception) {
            false
        }
    }

    suspend fun setDarkMode(enabled: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[DARK_MODE_KEY] = enabled
        }
    }

    suspend fun getDarkMode(): Boolean {
        return try {
            context.dataStore.data.map { preferences ->
                preferences[DARK_MODE_KEY] ?: false
            }.first()
        } catch (e: Exception) {
            false
        }
    }

    suspend fun saveUserProfile(name: String, email: String, imageUri: String?, dateOfBirth: String?) {
        context.dataStore.edit { preferences ->
            preferences[USER_NAME_KEY] = name
            preferences[USER_EMAIL_KEY] = email
            if (imageUri != null) {
                preferences[USER_IMAGE_KEY] = imageUri
            } else {
                preferences.remove(USER_IMAGE_KEY)
            }
            if (dateOfBirth != null) {
                preferences[USER_DATE_OF_BIRTH_KEY] = dateOfBirth
            } else {
                preferences.remove(USER_DATE_OF_BIRTH_KEY)
            }
        }
    }

    suspend fun getUserProfile(): Triple<String, String, String?> {
        val userProfileData = getFullUserProfile()
        return Triple(userProfileData.name, userProfileData.email, userProfileData.imageUri)
    }

    suspend fun getFullUserProfile(): UserProfileData {
        return context.dataStore.data.map { preferences ->
            val name = preferences[USER_NAME_KEY] ?: ""
            val email = preferences[USER_EMAIL_KEY] ?: ""
            val imageUri = preferences[USER_IMAGE_KEY]
            val dateOfBirth = preferences[USER_DATE_OF_BIRTH_KEY]
            UserProfileData(name, email, imageUri, dateOfBirth)
        }.first()
    }
}

data class UserProfileData(
    val name: String,
    val email: String,
    val imageUri: String?,
    val dateOfBirth: String?
)