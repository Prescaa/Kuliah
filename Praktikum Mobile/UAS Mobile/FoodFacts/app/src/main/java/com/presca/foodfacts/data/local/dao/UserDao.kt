package com.presca.foodfacts.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.presca.foodfacts.data.local.entity.UserEntity

@Dao
interface UserDao {
    @Insert(onConflict = OnConflictStrategy.ABORT)
    suspend fun insertUser(user: UserEntity): Long

    @Query("SELECT * FROM users WHERE email = :email LIMIT 1")
    suspend fun getUserByEmail(email: String): UserEntity?

    @Query("SELECT COUNT(*) FROM users")
    suspend fun getUserCount(): Int

    @Query("DELETE FROM users")
    suspend fun clearUsers()

    @Query("UPDATE users SET email = :newEmail WHERE email = :oldEmail")
    suspend fun updateEmail(oldEmail: String, newEmail: String): Int

    @Query("UPDATE users SET passwordHash = :newPasswordHash WHERE email = :email")
    suspend fun updatePasswordHash(email: String, newPasswordHash: String): Int

    @Update
    suspend fun updateUser(user: UserEntity): Int
}