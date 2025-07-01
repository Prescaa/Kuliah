package com.presca.foodfacts.data.local

import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import android.content.Context
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase
import com.presca.foodfacts.data.local.dao.FoodProductDao
import com.presca.foodfacts.data.local.dao.UserDao
import com.presca.foodfacts.data.local.entity.ProductEntity
import com.presca.foodfacts.data.local.entity.UserEntity

@Database(
    entities = [ProductEntity::class, UserEntity::class],
    version = 6,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun foodProductDao(): FoodProductDao
    abstract fun userDao(): UserDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        val MIGRATION_4_6 = object : Migration(4, 6) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL("ALTER TABLE users ADD COLUMN dateOfBirth TEXT")
            }
        }

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "food_database"
                )
                    .addMigrations(MIGRATION_4_6)
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}