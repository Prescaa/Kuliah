package com.presca.modul5.data.repository

import com.presca.modul5.data.local.AppDatabase
import com.presca.modul5.data.mapper.CountryMapper
import com.presca.modul5.data.remote.CountryApiService
import com.presca.modul5.domain.model.CountryInfo
import com.presca.modul5.domain.repository.CountryRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.withContext

class CountryRepositoryImpl constructor(
    private val api: CountryApiService,
    private val db: AppDatabase
) : CountryRepository {

    override fun fetchCountries(): Flow<List<CountryInfo>> = flow {
        try {
            val cachedCountries = withContext(Dispatchers.IO) {
                db.countryDao().getAllCountries()
            }

            if (cachedCountries.isNotEmpty()) {
                emit(cachedCountries.map { CountryMapper.mapEntityToDomain(it) })
            }

            val countries = api.getAllCountries()
            val entities = countries.mapIndexed { index, country ->
                CountryMapper.mapResponseToEntity(country, index.toLong())
            }

            withContext(Dispatchers.IO) {
                db.countryDao().clearAll()
                db.countryDao().insertAll(entities)
            }

            emit(entities.map { CountryMapper.mapEntityToDomain(it) })
        } catch (e: Exception) {
            val cachedCountries = withContext(Dispatchers.IO) {
                db.countryDao().getAllCountries()
            }
            if (cachedCountries.isNotEmpty()) {
                emit(cachedCountries.map { CountryMapper.mapEntityToDomain(it) })
            } else {
                throw e
            }
        }
    }.flowOn(Dispatchers.IO)

    override suspend fun refreshCountries() {
        try {
            val countries = api.getAllCountries()
            val entities = countries.mapIndexed { index, country ->
                CountryMapper.mapResponseToEntity(country, index.toLong())
            }
            db.countryDao().clearAll()
            db.countryDao().insertAll(entities)
        } catch (e: Exception) {
            throw e
        }
    }
}