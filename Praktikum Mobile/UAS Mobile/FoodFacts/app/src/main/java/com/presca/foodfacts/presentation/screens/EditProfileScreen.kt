package com.presca.foodfacts.presentation.screens

import android.app.DatePickerDialog
import android.util.Log
import android.widget.DatePicker
import android.widget.Toast
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.CalendarMonth
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
import com.presca.foodfacts.presentation.viewmodel.SettingsViewModel
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EditProfileScreen(
    settingsViewModel: SettingsViewModel,
    navController: NavController
) {
    val uiState by settingsViewModel.uiState.collectAsState()
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var dateOfBirth by remember { mutableStateOf("") }
    var showPasswordDialog by remember { mutableStateOf(false) }
    var oldPassword by remember { mutableStateOf("") }
    var newPassword by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var passwordError by remember { mutableStateOf<String?>(null) }
    val context = LocalContext.current

    val settingsMessage by settingsViewModel.message.collectAsState()

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

    var oldPasswordVisibility by remember { mutableStateOf(false) }
    var newPasswordVisibility by remember { mutableStateOf(false) }
    var confirmPasswordVisibility by remember { mutableStateOf(false) }

    // Load user profile when the screen is first composed
    LaunchedEffect(Unit) {
        settingsViewModel.loadUserProfile()
    }

    // Update local state variables when ViewModel's userProfile changes
    LaunchedEffect(uiState.userProfile) {
        name = uiState.userProfile.name
        email = uiState.userProfile.email
        dateOfBirth = uiState.userProfile.dateOfBirth ?: ""
    }

    // Display Toast message when settingsMessage changes
    LaunchedEffect(settingsMessage) {
        settingsMessage?.let { message ->
            Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
            settingsViewModel.consumeMessage() // Consume the message to avoid showing it again
        }
    }


    if (showPasswordDialog) {
        AlertDialog(
            onDismissRequest = { showPasswordDialog = false },
            title = { Text("Ubah Kata Sandi") },
            text = {
                Column {
                    OutlinedTextField(
                        value = oldPassword,
                        onValueChange = { oldPassword = it },
                        label = { Text("Kata Sandi Saat Ini") },
                        visualTransformation = if (oldPasswordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
                        trailingIcon = {
                            val image = if (oldPasswordVisibility) Icons.Filled.Visibility else Icons.Filled.VisibilityOff
                            val description = if (oldPasswordVisibility) "Sembunyikan kata sandi" else "Tampilkan kata sandi"
                            IconButton(onClick = { oldPasswordVisibility = !oldPasswordVisibility }) {
                                Icon(imageVector = image, description)
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = newPassword,
                        onValueChange = { newPassword = it },
                        label = { Text("Kata Sandi Baru") },
                        visualTransformation = if (newPasswordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
                        trailingIcon = {
                            val image = if (newPasswordVisibility) Icons.Filled.Visibility else Icons.Filled.VisibilityOff
                            val description = if (newPasswordVisibility) "Sembunyikan kata sandi" else "Tampilkan kata sandi"
                            IconButton(onClick = { newPasswordVisibility = !newPasswordVisibility }) {
                                Icon(imageVector = image, description)
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    OutlinedTextField(
                        value = confirmPassword,
                        onValueChange = { confirmPassword = it },
                        label = { Text("Konfirmasi Kata Sandi Baru") },
                        visualTransformation = if (confirmPasswordVisibility) VisualTransformation.None else PasswordVisualTransformation(),
                        trailingIcon = {
                            val image = if (confirmPasswordVisibility) Icons.Filled.Visibility else Icons.Filled.VisibilityOff
                            val description = if (confirmPasswordVisibility) "Sembunyikan kata sandi" else "Tampilkan kata sandi"
                            IconButton(onClick = { confirmPasswordVisibility = !confirmPasswordVisibility }) {
                                Icon(imageVector = image, description)
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    )
                    passwordError?.let {
                        Text(
                            text = it,
                            color = MaterialTheme.colorScheme.error,
                            modifier = Modifier.padding(top = 8.dp)
                        )
                    }
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        when {
                            oldPassword.isEmpty() -> passwordError = "Kata sandi saat ini diperlukan"
                            newPassword.isEmpty() -> passwordError = "Kata sandi baru diperlukan"
                            newPassword.length < 6 -> passwordError = "Kata sandi harus minimal 6 karakter"
                            newPassword != confirmPassword -> passwordError = "Kata sandi tidak cocok"
                            else -> {
                                settingsViewModel.updatePassword(
                                    oldPassword = oldPassword,
                                    newPassword = newPassword,
                                    onResult = { success ->
                                        if (success) {
                                            showPasswordDialog = false
                                            oldPassword = ""
                                            newPassword = ""
                                            confirmPassword = ""
                                            passwordError = null
                                        } else {
                                            passwordError = "Kata sandi saat ini salah atau pembaruan gagal"
                                        }
                                    }
                                )
                            }
                        }
                    }
                ) {
                    Text("Simpan")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = {
                        showPasswordDialog = false
                        passwordError = null
                        oldPassword = ""
                        newPassword = ""
                        confirmPassword = ""
                    }
                ) {
                    Text("Batal")
                }
            }
        )
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Edit Profil") },
                navigationIcon = {
                    IconButton(onClick = { navController.popBackStack() }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Kembali")
                    }
                },
                actions = {
                    TextButton(
                        onClick = {
                            Log.d("EditProfileScreen", "Tombol Simpan diklik!")
                            settingsViewModel.updateProfile(
                                name,
                                email,
                                null,
                                dateOfBirth.ifEmpty { null }
                            ) { success, msg ->
                                if (success) {
                                    navController.popBackStack()
                                }
                            }
                        }
                    ) {
                        Text("Simpan", color = MaterialTheme.colorScheme.onPrimary)
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary,
                    actionIconContentColor = MaterialTheme.colorScheme.onPrimary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .padding(padding)
                .fillMaxWidth()
        ) {
            OutlinedTextField(
                value = name,
                onValueChange = { name = it },
                label = { Text("Nama") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            )

            OutlinedTextField(
                value = email,
                onValueChange = { email = it },
                label = { Text("Email") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            )

            OutlinedTextField(
                value = dateOfBirth,
                onValueChange = { /* Read-only, handled by DatePickerDialog */ },
                label = { Text("Tanggal Lahir (DD/MM/YYYY)") },
                readOnly = true,
                trailingIcon = {
                    IconButton(onClick = { datePickerDialog.show() }) {
                        Icon(Icons.Default.CalendarMonth, contentDescription = "Pilih Tanggal")
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
                    .clickable { datePickerDialog.show() }
            )
            Spacer(modifier = Modifier.height(8.dp))

            Button(
                onClick = { showPasswordDialog = true },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                Text("Ubah Kata Sandi")
            }
        }
    }
}