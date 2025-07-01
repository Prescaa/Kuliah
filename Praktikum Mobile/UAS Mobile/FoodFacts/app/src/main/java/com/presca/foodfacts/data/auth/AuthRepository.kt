package com.presca.foodfacts.data.auth

import com.presca.foodfacts.data.local.UserPreferences
import com.presca.foodfacts.data.remote.response.LoginResponse
import com.presca.foodfacts.data.remote.response.RegisterResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import com.presca.foodfacts.data.local.dao.UserDao
import com.presca.foodfacts.data.local.entity.UserEntity
import java.security.MessageDigest

interface AuthRepository {
    suspend fun login(email: String, password: String): Result<LoginResponse>
    suspend fun register(username: String, email: String, password: String, dateOfBirth: String?): Result<RegisterResponse>
    suspend fun isLoggedIn(): Boolean
    suspend fun logout(): Result<Unit>
    suspend fun updateEmail(oldEmail: String, newEmail: String): Result<Unit>
    suspend fun updatePassword(oldPassword: String, newPassword: String): Result<Unit>
    suspend fun updateDateOfBirth(email: String, newDateOfBirth: String?): Result<Unit>
}

class AuthRepositoryImpl(
    private val userPreferences: UserPreferences,
    private val userDao: UserDao
) : AuthRepository {

    private fun hashPassword(password: String): String {
        return try {
            val bytes = MessageDigest.getInstance("SHA-256").digest(password.toByteArray())
            bytes.joinToString("") { "%02x".format(it) }
        } catch (e: Exception) {
            password
        }
    }

    override suspend fun login(email: String, password: String): Result<LoginResponse> {
        return withContext(Dispatchers.IO) {
            try {
                val user = userDao.getUserByEmail(email)
                if (user == null) {
                    return@withContext Result.failure(Exception("Email tidak terdaftar."))
                }

                val hashedPassword = hashPassword(password)
                if (user.passwordHash == hashedPassword) {
                    val token = "simulated_token_${System.currentTimeMillis()}"
                    userPreferences.saveAuthToken(token)
                    userPreferences.saveUserProfile(user.username, user.email, user.dateOfBirth, null)
                    Result.success(LoginResponse(token = token, userId = "user_$email"))
                } else {
                    return@withContext Result.failure(Exception("Email atau kata sandi tidak valid."))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Login gagal: ${e.message}"))
            }
        }
    }

    override suspend fun register(
        username: String,
        email: String,
        password: String,
        dateOfBirth: String?
    ): Result<RegisterResponse> {
        return withContext(Dispatchers.IO) {
            try {
                if (username.isBlank()) return@withContext Result.failure(Exception("Nama pengguna tidak boleh kosong."))
                if (email.isBlank()) return@withContext Result.failure(Exception("Email tidak boleh kosong."))
                if (!email.contains("@")) return@withContext Result.failure(Exception("Format email tidak valid."))
                if (password.length < 6) return@withContext Result.failure(Exception("Kata sandi harus minimal 6 karakter."))

                val existingUserWithEmail = userDao.getUserByEmail(email)
                if (existingUserWithEmail != null) {
                    return@withContext Result.failure(Exception("Email sudah terdaftar. Silakan login."))
                }

                val hashedPassword = hashPassword(password)
                val userEntity = UserEntity(
                    username = username,
                    email = email,
                    passwordHash = hashedPassword,
                    dateOfBirth = dateOfBirth
                )

                val insertedId = userDao.insertUser(userEntity)
                if (insertedId == -1L) {
                    return@withContext Result.failure(Exception("Gagal mendaftar pengguna. Email mungkin sudah ada."))
                }

                userPreferences.saveUserProfile(username, email, null, dateOfBirth)

                Result.success(
                    RegisterResponse(
                        message = "Pendaftaran berhasil.",
                        userId = "user_$email"
                    )
                )
            } catch (e: Exception) {
                Result.failure(Exception("Pendaftaran gagal: ${e.message}"))
            }
        }
    }

    override suspend fun isLoggedIn(): Boolean = userPreferences.isLoggedIn()

    override suspend fun logout(): Result<Unit> {
        return withContext(Dispatchers.IO) {
            try {
                userPreferences.clearAuthToken()
                Result.success(Unit)
            } catch (e: Exception) {
                Result.failure(Exception("Gagal logout: ${e.message}"))
            }
        }
    }

    override suspend fun updateEmail(oldEmail: String, newEmail: String): Result<Unit> {
        return withContext(Dispatchers.IO) {
            try {
                val currentLoggedInEmail = userPreferences.getFullUserProfile().email

                if (currentLoggedInEmail != oldEmail) {
                    return@withContext Result.failure(Exception("Email lama tidak cocok dengan email pengguna yang sedang login."))
                }
                if (newEmail.isBlank() || !newEmail.contains("@")) {
                    return@withContext Result.failure(Exception("Format email baru tidak valid."))
                }

                val existingUserWithNewEmail = userDao.getUserByEmail(newEmail)
                if (existingUserWithNewEmail != null && existingUserWithNewEmail.email != oldEmail) {
                    return@withContext Result.failure(Exception("Email baru sudah digunakan oleh pengguna lain."))
                }

                val updatedRows = userDao.updateEmail(oldEmail, newEmail)
                if (updatedRows > 0) {
                    val (currentName, _, currentImage, currentDateOfBirth) = userPreferences.getFullUserProfile()
                    userPreferences.saveUserProfile(currentName, newEmail, currentImage, currentDateOfBirth)
                    Result.success(Unit)
                } else {
                    Result.failure(Exception("Gagal memperbarui email di database. Pengguna mungkin tidak ada."))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Gagal memperbarui email: ${e.message}"))
            }
        }
    }

    override suspend fun updatePassword(oldPassword: String, newPassword: String): Result<Unit> {
        return withContext(Dispatchers.IO) {
            try {
                val currentLoggedInEmail = userPreferences.getFullUserProfile().email
                val currentUser = userDao.getUserByEmail(currentLoggedInEmail)

                if (currentUser == null) {
                    return@withContext Result.failure(Exception("Data pengguna tidak ditemukan untuk email yang sedang login."))
                }

                val hashedOldPassword = hashPassword(oldPassword)
                if (hashedOldPassword != currentUser.passwordHash) {
                    return@withContext Result.failure(Exception("Kata sandi saat ini salah."))
                }

                if (newPassword.isBlank() || newPassword.length < 6) {
                    return@withContext Result.failure(Exception("Kata sandi baru harus minimal 6 karakter."))
                }

                val hashedNewPassword = hashPassword(newPassword)
                val updatedRows = userDao.updatePasswordHash(currentUser.email, hashedNewPassword)
                if (updatedRows > 0) {
                    Result.success(Unit)
                } else {
                    Result.failure(Exception("Gagal memperbarui kata sandi di database."))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Gagal memperbarui kata sandi: ${e.message}"))
            }
        }
    }

    override suspend fun updateDateOfBirth(email: String, newDateOfBirth: String?): Result<Unit> {
        return withContext(Dispatchers.IO) {
            try {
                val currentUser = userDao.getUserByEmail(email)
                if (currentUser == null) {
                    return@withContext Result.failure(Exception("Pengguna tidak ditemukan."))
                }

                val updatedUser = currentUser.copy(dateOfBirth = newDateOfBirth)
                val updatedRows = userDao.updateUser(updatedUser)
                if (updatedRows > 0) {
                    val (name, _, imageUri, _) = userPreferences.getFullUserProfile()
                    userPreferences.saveUserProfile(name, email, imageUri, newDateOfBirth)
                    Result.success(Unit)
                } else {
                    Result.failure(Exception("Gagal memperbarui tanggal lahir."))
                }
            } catch (e: Exception) {
                Result.failure(Exception("Gagal memperbarui tanggal lahir: ${e.message}"))
            }
        }
    }
}