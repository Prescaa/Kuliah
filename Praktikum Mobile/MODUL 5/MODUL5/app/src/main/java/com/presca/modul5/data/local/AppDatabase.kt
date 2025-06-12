package com.presca.modul5.data.local

import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import android.content.Context
import com.presca.modul5.data.local.dao.CountryDao
import com.presca.modul5.data.local.entity.CountryEntity

@Database(
    entities = [CountryEntity::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun countryDao(): CountryDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "country_database"
                ).build()
                INSTANCE = instance
                instance
            }
        }
    }
}