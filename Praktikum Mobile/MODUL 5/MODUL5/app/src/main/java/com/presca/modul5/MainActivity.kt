package com.presca.modul5

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.presca.modul5.data.local.AppDatabase
import com.presca.modul5.data.remote.RetrofitInstance
import com.presca.modul5.data.repository.CountryRepositoryImpl
import com.presca.modul5.presentation.screens.CountryDetailScreen
import com.presca.modul5.presentation.screens.CountryListScreen
import com.presca.modul5.ui.theme.Modul5Theme
import com.presca.modul5.presentation.theme.ThemeViewModel
import com.presca.modul5.presentation.viewmodel.CountryViewModel
import com.presca.modul5.presentation.viewmodel.CountryViewModelFactory

class MainActivity : ComponentActivity() {
    private val db by lazy {
        AppDatabase.getDatabase(this)
    }
    private val repository by lazy {
        CountryRepositoryImpl(RetrofitInstance.api, db)
    }
    private val countryViewModel: CountryViewModel by viewModels {
        CountryViewModelFactory(repository)
    }
    private val themeViewModel: ThemeViewModel by viewModels {
        object : ViewModelProvider.Factory {
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                if (modelClass.isAssignableFrom(ThemeViewModel::class.java)) {
                    @Suppress("UNCHECKED_CAST")
                    return ThemeViewModel(applicationContext) as T
                }
                throw IllegalArgumentException("Unknown ViewModel class")
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val isDarkTheme by themeViewModel.isDarkTheme.collectAsState()

            Modul5Theme(darkTheme = isDarkTheme) {
                AppNavigation(
                    viewModel = countryViewModel,
                    themeViewModel = themeViewModel
                )
            }
        }
    }
}

@Composable
fun AppNavigation(
    viewModel: CountryViewModel,
    themeViewModel: ThemeViewModel
) {
    val navController = rememberNavController()
    val context = LocalContext.current
    val state by viewModel.state.collectAsState()
    val isDarkTheme by themeViewModel.isDarkTheme.collectAsState()

    NavHost(
        navController = navController,
        startDestination = "country_list"
    ) {
        composable("country_list") {
            CountryListScreen(
                state = state,
                onRefresh = { viewModel.refreshCountries() },
                onClickDetail = { country ->
                    navController.navigate("detail/${country.id}")
                },
                onClickInfo = { url ->
                    try {
                        context.startActivity(
                            Intent(Intent.ACTION_VIEW, Uri.parse(url))
                        )
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                },
                onToggleTheme = { themeViewModel.toggleTheme() },
                isDarkTheme = isDarkTheme
            )
        }
        composable("detail/{id}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id")?.toLongOrNull()

            when (val currentState = state) {
                is CountryViewModel.CountryState.Success -> {
                    currentState.countries.find { it.id == id }?.let { country ->
                        CountryDetailScreen(
                            country = country,
                            navController = navController,
                            onClickInfo = {
                                context.startActivity(
                                    Intent(
                                        Intent.ACTION_VIEW,
                                        Uri.parse(country.externalUrl)
                                    )
                                )
                            }
                        )
                    } ?: run {
                        println("Error: Country with ID $id not found in current state.")
                    }
                }
                else -> {
                    println("Error: Cannot display detail screen in state: $currentState")
                }
            }
        }
    }
}