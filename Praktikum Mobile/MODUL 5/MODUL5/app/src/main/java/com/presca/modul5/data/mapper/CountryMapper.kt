package com.presca.modul5.data.mapper

import com.presca.modul5.data.local.entity.CountryEntity
import com.presca.modul5.data.remote.response.Country
import com.presca.modul5.domain.model.CountryInfo
import java.text.DecimalFormat

object CountryMapper {
    fun mapResponseToEntity(country: Country, index: Long): CountryEntity {
        return CountryEntity(
            id = index,
            name = country.name.common,
            officialName = country.name.official ?: country.name.common,
            flagUrl = country.flags.png,
            region = country.region ?: "Unknown",
            capital = country.capital?.firstOrNull() ?: "Unknown",
            description = buildCountryDescription(country),
            externalUrl = generateWikipediaUrl(country.name.common)
        )
    }

    fun mapEntityToDomain(entity: CountryEntity): CountryInfo {
        return CountryInfo(
            id = entity.id,
            name = entity.name,
            officialName = entity.officialName,
            flagUrl = entity.flagUrl,
            region = entity.region,
            capital = entity.capital,
            description = entity.description,
            externalUrl = entity.externalUrl
        )
    }

    private fun buildCountryDescription(country: Country): String {
        return """
            |Nama Resmi: ${country.name.official ?: country.name.common}
            |Ibukota: ${country.capital?.firstOrNull() ?: "Unknown"}
            |Region: ${country.region ?: "Unknown"}
            |Subregion: ${country.subregion ?: "Unknown"}
            |Populasi: ${country.population?.formatWithCommas() ?: "Unknown"} jiwa
            |Bahasa Resmi: ${country.languages?.values?.joinToString(", ") ?: "Unknown"}
        """.trimMargin()
    }

    private fun Long.formatWithCommas(): String {
        return DecimalFormat("#,###").format(this)
    }

    private fun generateWikipediaUrl(countryName: String): String {
        return "https://en.wikipedia.org/wiki/${countryName.replace(" ", "_")}"
    }
}