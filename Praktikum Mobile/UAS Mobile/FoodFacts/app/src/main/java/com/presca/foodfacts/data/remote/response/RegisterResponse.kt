package com.presca.foodfacts.data.remote.response

import kotlinx.serialization.Serializable

@Serializable
data class RegisterResponse(val message: String, val userId: String)