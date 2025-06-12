package com.presca.modul5.data.remote.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class Country(
    val name: Name,
    val flags: Flags,
    val region: String? = null,
    val subregion: String? = null,
    val capital: List<String>? = null,
    val population: Long? = null,
    val languages: Map<String, String>? = null,
    val timezones: List<String>? = null
)

@Serializable
data class Name(
    val common: String,
    val official: String? = null,
    @SerialName("nativeName")
    val nativeNames: Map<String, NativeName>? = null
)

@Serializable
data class NativeName(
    val official: String? = null,
    val common: String? = null
)

@Serializable
data class Flags(
    val png: String,
    val svg: String? = null,
    val alt: String? = null
)