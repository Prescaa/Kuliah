package com.presca.foodfacts

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.presca.foodfacts.data.auth.AuthRepositoryImpl
import com.presca.foodfacts.data.local.AppDatabase
import com.presca.foodfacts.data.local.UserPreferences
import com.presca.foodfacts.data.remote.FoodApiService
import com.presca.foodfacts.data.remote.RetrofitInstance
import com.presca.foodfacts.data.repository.FoodProductRepositoryImpl
import com.presca.foodfacts.presentation.screens.DashboardScreen
import com.presca.foodfacts.presentation.screens.EditProfileScreen
import com.presca.foodfacts.presentation.screens.LoginScreen
import com.presca.foodfacts.presentation.screens.ProductDetailScreen
import com.presca.foodfacts.presentation.screens.ProductListScreen
import com.presca.foodfacts.presentation.screens.RegisterScreen
import com.presca.foodfacts.presentation.screens.SettingsScreen
import com.presca.foodfacts.presentation.viewmodel.AuthViewModel
import com.presca.foodfacts.presentation.viewmodel.AuthViewModelFactory
import com.presca.foodfacts.presentation.viewmodel.ProductViewModel
import com.presca.foodfacts.presentation.viewmodel.ProductViewModelFactory
import com.presca.foodfacts.presentation.viewmodel.SettingsViewModel
import com.presca.foodfacts.presentation.viewmodel.SettingsViewModelFactory
import com.presca.foodfacts.ui.theme.FoodFactsTheme
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.material3.Text
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.runtime.collectAsState

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val userPreferences = UserPreferences(applicationContext)
            val authRepository = AuthRepositoryImpl(userPreferences, AppDatabase.getDatabase(applicationContext).userDao())
            val authViewModel: AuthViewModel = viewModel(factory = AuthViewModelFactory(authRepository, userPreferences))
            val settingsViewModel: SettingsViewModel = viewModel(factory = SettingsViewModelFactory(userPreferences, authRepository))
            val foodApiService: FoodApiService = RetrofitInstance.api
            val foodProductDao = AppDatabase.getDatabase(applicationContext).foodProductDao()
            val foodProductRepository = FoodProductRepositoryImpl(foodApiService, AppDatabase.getDatabase(applicationContext))
            val productViewModel: ProductViewModel = viewModel(factory = ProductViewModelFactory(foodProductRepository))

            var startDestination by remember { mutableStateOf("splash") }

            FoodFactsTheme(darkTheme = settingsViewModel.uiState.collectAsState().value.darkModeEnabled) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()

                    NavHost(navController = navController, startDestination = "splash") {
                        composable("splash") {
                            SplashScreen(navController = navController, authViewModel = authViewModel)
                        }
                        composable("login") {
                            LoginScreen(
                                authViewModel = authViewModel,
                                navController = navController,
                                onLoginSuccess = { navController.navigateToDashboard() }
                            )
                        }
                        composable("register") {
                            RegisterScreen(authViewModel = authViewModel, navController = navController)
                        }
                        composable("dashboard") {
                            DashboardScreen(navController = navController, authViewModel = authViewModel, settingsViewModel = settingsViewModel)
                        }
                        composable("product_list") {
                            val productState by productViewModel.state.collectAsState()
                            ProductListScreen(
                                state = productState,
                                onRefresh = { productViewModel.refreshProducts() },
                                onClickProduct = { product ->
                                    navController.navigate("product_detail/${product.code}")
                                },
                                navController = navController,
                                settingsViewModel = settingsViewModel
                            )
                        }
                        composable("product_detail/{productCode}") { backStackEntry ->
                            val productCode = backStackEntry.arguments?.getString("productCode")
                            val productState by productViewModel.state.collectAsState()

                            val productInfo = remember(productCode, productState) {
                                (productState as? ProductViewModel.ProductState.Success)?.products?.find { it.code == productCode }
                            }

                            if (productInfo != null) {
                                ProductDetailScreen(product = productInfo, navController = navController)
                            } else {
                                Text("Memuat detail produk...", modifier = Modifier.fillMaxSize(), textAlign = TextAlign.Center)
                                LaunchedEffect(productCode) {
                                    if (productCode != null && productInfo == null) {
                                        productViewModel.refreshProducts()
                                    }
                                }
                            }
                        }
                        composable("settings") {
                            SettingsScreen(settingsViewModel = settingsViewModel, navController = navController)
                        }
                        composable("edit_profile") {
                            EditProfileScreen(settingsViewModel = settingsViewModel, navController = navController)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun SplashScreen(navController: NavController, authViewModel: AuthViewModel) {
    val scope = rememberCoroutineScope()
    LaunchedEffect(Unit) {
        delay(2000)
        scope.launch {
            if (authViewModel.isLoggedIn()) {
                navController.navigate("dashboard") {
                    popUpTo("splash") { inclusive = true }
                }
            } else {
                navController.navigate("login") {
                    popUpTo("splash") { inclusive = true }
                }
            }
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.primary),
        contentAlignment = Alignment.Center
    ) {
        Image(
            painter = painterResource(id = R.drawable.logo_foodfacts),
            contentDescription = "FoodFacts Logo",
            modifier = Modifier.size(200.dp)
        )
    }
}

fun NavController.navigateToLogin() {
    navigate("login") {
        popUpTo(graph.id) {
            inclusive = true
        }
    }
}

fun NavController.navigateToDashboard() {
    navigate("dashboard") {
        popUpTo(graph.id) {
            inclusive = true
        }
    }
}


@Preview(showBackground = true)
@Composable
fun DefaultPreview() {
    FoodFactsTheme {
        // You would typically not preview the whole MainActivity like this.
        // Instead, preview individual composables.
    }
}
