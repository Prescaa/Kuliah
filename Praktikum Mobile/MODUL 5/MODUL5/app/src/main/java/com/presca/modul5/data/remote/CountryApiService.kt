package com.presca.modul5.data.remote

import com.presca.modul5.data.remote.response.Country
import retrofit2.http.GET

interface CountryApiService {
    @GET("v3.1/all?fields=name,flags,region,subregion,capital,population,languages,timezones")
    suspend fun getAllCountries(): List<Country>
}