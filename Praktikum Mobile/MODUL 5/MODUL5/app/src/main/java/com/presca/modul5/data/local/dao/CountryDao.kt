package com.presca.modul5.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.presca.modul5.data.local.entity.CountryEntity

@Dao
interface CountryDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(countries: List<CountryEntity>)

    @Query("SELECT * FROM countries")
    suspend fun getAllCountries(): List<CountryEntity>

    @Query("DELETE FROM countries")
    suspend fun clearAll()

    @Query("SELECT COUNT(*) FROM countries")
    suspend fun count(): Int
}