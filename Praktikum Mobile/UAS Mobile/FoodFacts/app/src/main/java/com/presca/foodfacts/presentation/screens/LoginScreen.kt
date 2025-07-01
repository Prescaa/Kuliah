package com.presca.foodfacts.presentation.screens

import android.widget.Toast
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.presca.foodfacts.presentation.viewmodel.AuthViewModel
import com.presca.foodfacts.navigateToDashboard

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoginScreen(
    authViewModel: AuthViewModel,
    navController: NavController,
    onLoginSuccess: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val loginState by authViewModel.loginState.collectAsState()
    val context = LocalContext.current

    var passwordVisibility by remember { mutableStateOf(false) }

    LaunchedEffect(loginState) {
        when (loginState) {
            is AuthViewModel.AuthResult.Success -> {
                Toast.makeText(context, (loginState as AuthViewModel.AuthResult.Success).message, Toast.LENGTH_SHORT).show()
                onLoginSuccess()
            }
            is AuthViewModel.AuthResult.Error -> {
                Toast.makeText(context, (loginState as AuthViewModel.AuthResult.Error).message, Toast.LENGTH_LONG).show()
            }
            else -> {}
        }
    }

    Scaffold { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(text = "Masuk", style = MaterialTheme.typography.headlineLarge)
            Spacer(modifier = Modifier.height(32.dp))

            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Kata Sandi") },
                visualTransformation = if (passwordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
                trailingIcon = {
                    val image = if (passwordVisibility)
                        Icons.Filled.Visibility
                    else Icons.Filled.VisibilityOff

                    val description = if (passwordVisibility) "Sembunyikan kata sandi" else "Tampilkan kata sandi"

                    IconButton(onClick = { passwordVisibility = !passwordVisibility }) {
                        Icon(imageVector = image, contentDescription = description)
                    }
                },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = { authViewModel.login(email, password) },
                enabled = loginState !is AuthViewModel.AuthResult.Loading,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (loginState is AuthViewModel.AuthResult.Loading) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                } else {
                    Text("Masuk")
                }
            }
            Spacer(modifier = Modifier.height(8.dp))

            TextButton(
                onClick = { navController.navigate("register") },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Belum punya akun? Daftar di sini")
            }
        }
    }
}