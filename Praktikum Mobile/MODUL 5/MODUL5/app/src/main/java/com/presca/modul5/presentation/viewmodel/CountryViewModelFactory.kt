package com.presca.modul5.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.presca.modul5.domain.repository.CountryRepository // Add this import

class CountryViewModelFactory(
    private val repository: CountryRepository
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(CountryViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return CountryViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}