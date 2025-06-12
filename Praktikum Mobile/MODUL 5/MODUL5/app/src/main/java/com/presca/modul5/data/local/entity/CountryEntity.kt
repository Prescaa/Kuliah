package com.presca.modul5.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "countries")
data class CountryEntity(
    @PrimaryKey val id: Long,
    val name: String,
    val officialName: String,
    val flagUrl: String,
    val region: String,
    val capital: String,
    val description: String,
    val externalUrl: String,
    val lastUpdated: Long = System.currentTimeMillis()
)