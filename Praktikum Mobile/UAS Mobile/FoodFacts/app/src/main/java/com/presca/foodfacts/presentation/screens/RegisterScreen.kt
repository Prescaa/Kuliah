package com.presca.foodfacts.presentation.screens

import android.app.DatePickerDialog
import android.widget.DatePicker
import android.widget.Toast
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.CalendarMonth
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.presca.foodfacts.navigateToLogin
import com.presca.foodfacts.presentation.viewmodel.AuthViewModel
import java.util.Calendar
import java.util.Locale
import java.text.SimpleDateFormat

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RegisterScreen(
    authViewModel: AuthViewModel,
    navController: NavController
) {
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var dateOfBirth by remember { mutableStateOf("") }
    val context = LocalContext.current

    val registerState by authViewModel.registerState.collectAsState()

    val calendar = Calendar.getInstance()
    val year = calendar.get(Calendar.YEAR)
    val month = calendar.get(Calendar.MONTH)
    val day = calendar.get(Calendar.DAY_OF_MONTH)

    val datePickerDialog = DatePickerDialog(
        context,
        { _: DatePicker, selectedYear: Int, selectedMonth: Int, selectedDayOfMonth: Int ->
            val selectedDate = Calendar.getInstance()
            selectedDate.set(selectedYear, selectedMonth, selectedDayOfMonth)
            val sdf = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault())
            dateOfBirth = sdf.format(selectedDate.time)
        }, year, month, day
    )

    var passwordVisibility by remember { mutableStateOf(false) }
    var confirmPasswordVisibility by remember { mutableStateOf(false) }

    LaunchedEffect(registerState) {
        when (registerState) {
            is AuthViewModel.AuthResult.Success -> {
                Toast.makeText(context, (registerState as AuthViewModel.AuthResult.Success).message, Toast.LENGTH_SHORT).show()
                navController.navigateToLogin()
            }
            is AuthViewModel.AuthResult.Error -> {
                Toast.makeText(context, (registerState as AuthViewModel.AuthResult.Error).message, Toast.LENGTH_LONG).show()
            }
            else -> {}
        }
    }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Daftar") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Kembali")
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            OutlinedTextField(
                value = username,
                onValueChange = { username = it },
                label = { Text("Nama Pengguna") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))
            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Kata Sandi") },
                visualTransformation = if (passwordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                trailingIcon = {
                    val image = if (passwordVisibility)
                        Icons.Filled.Visibility
                    else Icons.Filled.VisibilityOff

                    val description = if (passwordVisibility) "Sembunyikan kata sandi" else "Tampilkan kata sandi"

                    IconButton(onClick = { passwordVisibility = !passwordVisibility }) {
                        Icon(imageVector = image, description)
                    }
                },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))
            OutlinedTextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it },
                label = { Text("Konfirmasi Kata Sandi") },
                visualTransformation = if (confirmPasswordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                trailingIcon = {
                    val image = if (confirmPasswordVisibility)
                        Icons.Filled.Visibility
                    else Icons.Filled.VisibilityOff

                    val description = if (confirmPasswordVisibility) "Sembunyikan kata sandi" else "Tampilkan kata sandi"

                    IconButton(onClick = { confirmPasswordVisibility = !confirmPasswordVisibility }) {
                        Icon(imageVector = image, description)
                    }
                },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(8.dp))

            OutlinedTextField(
                value = dateOfBirth,
                onValueChange = { },
                label = { Text("Tanggal Lahir (DD/MM/YYYY)") },
                readOnly = true,
                trailingIcon = {
                    IconButton(onClick = { datePickerDialog.show() }) {
                        Icon(Icons.Default.CalendarMonth, contentDescription = "Pilih Tanggal")
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .clickable { datePickerDialog.show() }
            )
            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = {
                    if (password != confirmPassword) {
                        Toast.makeText(context, "Kata sandi tidak cocok!", Toast.LENGTH_SHORT).show()
                    } else {
                        authViewModel.register(username, email, password, dateOfBirth.ifEmpty { null })
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Daftar")
            }
            Spacer(modifier = Modifier.height(8.dp))
            TextButton(onClick = { navController.navigateToLogin() }) {
                Text("Sudah punya akun? Masuk")
            }
        }
    }
}