package com.presca.modul5.domain.repository

import com.presca.modul5.domain.model.CountryInfo
import kotlinx.coroutines.flow.Flow

interface CountryRepository {
    fun fetchCountries(): Flow<List<CountryInfo>>
    suspend fun refreshCountries()
}