package com.presca.modul5.domain.model

data class CountryInfo(
    val id: Long,
    val name: String,
    val officialName: String,
    val flagUrl: String,
    val region: String,
    val capital: String,
    val description: String,
    val externalUrl: String
)