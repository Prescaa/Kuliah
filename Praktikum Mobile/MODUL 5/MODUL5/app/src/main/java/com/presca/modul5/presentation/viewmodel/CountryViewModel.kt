package com.presca.modul5.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.presca.modul5.domain.model.CountryInfo
import com.presca.modul5.domain.repository.CountryRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class CountryViewModel(private val repository: CountryRepository) : ViewModel() {
    sealed class CountryState {
        object Loading : CountryState()
        data class Success(val countries: List<CountryInfo>) : CountryState()
        data class Error(val message: String) : CountryState()
    }

    private val _state = MutableStateFlow<CountryState>(CountryState.Loading)
    val state: StateFlow<CountryState> = _state.asStateFlow()

    init {
        fetchCountries()
    }

    fun fetchCountries() {
        viewModelScope.launch {
            _state.value = CountryState.Loading
            try {
                repository.fetchCountries().collect { countries ->
                    _state.value = if (countries.isEmpty()) {
                        CountryState.Error("Tidak ada data negara yang ditemukan")
                    } else {
                        CountryState.Success(countries)
                    }
                }
            } catch (e: Exception) {
                _state.value = CountryState.Error(
                    "Gagal memuat data: ${e.message ?: "Terjadi kesalahan"}"
                )
            }
        }
    }

    fun refreshCountries() {
        viewModelScope.launch {
            _state.value = CountryState.Loading
            try {
                repository.refreshCountries()
                fetchCountries()
            } catch (e: Exception) {
                _state.value = CountryState.Error(
                    "Gagal menyegarkan data: ${e.message ?: "Terjadi kesalahan"}"
                )
            }
        }
    }
}