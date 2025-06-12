package com.presca.modul5.presentation.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.bumptech.glide.integration.compose.ExperimentalGlideComposeApi
import com.bumptech.glide.integration.compose.GlideImage
import com.presca.modul5.domain.model.CountryInfo
import com.presca.modul5.presentation.viewmodel.CountryViewModel

@OptIn(ExperimentalGlideComposeApi::class, ExperimentalMaterial3Api::class)
@Composable
fun CountryListScreen(
    state: CountryViewModel.CountryState,
    onRefresh: () -> Unit,
    onClickDetail: (CountryInfo) -> Unit,
    onClickInfo: (String) -> Unit,
    onToggleTheme: () -> Unit,
    isDarkTheme: Boolean
) {
    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Negara di Dunia") },
                navigationIcon = {
                    IconButton(onClick = { /* TODO */ }) {
                        Icon(Icons.Filled.Public, contentDescription = null)
                    }
                },
                actions = {
                    IconButton(onClick = onToggleTheme) {
                        Icon(
                            imageVector = if (isDarkTheme) Icons.Filled.LightMode else Icons.Filled.DarkMode,
                            contentDescription = "Toggle Theme"
                        )
                    }
                }
            )
        }
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding)) {
            when (state) {
                is CountryViewModel.CountryState.Loading -> LoadingView()
                is CountryViewModel.CountryState.Error -> ErrorView(state.message, onRefresh)
                is CountryViewModel.CountryState.Success ->
                    CountryListView(
                        countries = state.countries,
                        onClickDetail = onClickDetail,
                        onClickInfo = onClickInfo
                    )
            }
        }
    }
}

@Composable
fun LoadingView() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}

@Composable
fun ErrorView(message: String, onRefresh: () -> Unit) {
    Column(
        modifier = Modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(message)
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onRefresh) {
            Text("Coba Lagi")
        }
    }
}

@OptIn(ExperimentalGlideComposeApi::class)
@Composable
fun CountryListView(
    countries: List<CountryInfo>,
    onClickDetail: (CountryInfo) -> Unit,
    onClickInfo: (String) -> Unit
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(8.dp)
    ) {
        items(countries) { country ->
            CountryCard(
                country = country,
                onClickDetail = { onClickDetail(country) },
                onClickInfo = { onClickInfo(country.externalUrl) }
            )
        }
    }
}

@OptIn(ExperimentalGlideComposeApi::class)
@Composable
fun CountryCard(
    country: CountryInfo,
    onClickDetail: () -> Unit,
    onClickInfo: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                GlideImage(
                    model = country.flagUrl,
                    contentDescription = country.name,
                    modifier = Modifier
                        .size(80.dp)
                        .clip(RoundedCornerShape(8.dp))
                )
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text(country.name, fontSize = 18.sp)
                    Text(
                        text = "Lokasi: ${country.region}",
                        fontSize = 14.sp
                    )
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Button(
                    onClick = onClickInfo,
                    modifier = Modifier.weight(1f)
                ) {
                    Text("Info")
                }
                Button(
                    onClick = onClickDetail,
                    modifier = Modifier.weight(1f)
                ) {
                    Text("Detail")
                }
            }
        }
    }
}